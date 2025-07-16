from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, QuizResult
from homework.models import HomeworkTask, HomeworkSubmission  # ✅ Tambahan

import json
import re

# Google Gemini
from google import genai
client = genai.Client(api_key="AIzaSyDiEHMNpXl_5kTccPLBEIO0q7-FMkVlCH0")

@login_required
def course_list(request):
    courses = Course.objects.all()  # type: ignore
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def generate_quiz(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    questions = []
    error_message = None

    # Check for show_results query parameter
    if request.method == "GET" and request.GET.get('show_results') == 'true':
        # Try to get results from session
        quiz_results = request.session.get('quiz_last_answers')
        if quiz_results:
            score = sum(1 for i, q in enumerate(quiz_results['questions']) if quiz_results['user_answers'][i] == q['answer'])
            total = len(quiz_results['questions'])
            percentage = round((score / total) * 100) if total > 0 else 0
            return render(request, 'courses/quiz_result.html', {
                'course': course,
                'score': score,
                'total': total,
                'percentage': percentage
            })
        # Fallback to latest QuizResult from database
        latest_result = QuizResult.objects.filter(user=request.user, course=course).order_by('-created_at').first()  # type: ignore
        if latest_result:
            return render(request, 'courses/quiz_result.html', {
                'course': course,
                'score': latest_result.score,
                'total': latest_result.total_questions,
                'percentage': latest_result.percentage
            })
        # If no results found, redirect to quiz start
        return redirect('quiz_generate', course_id=course_id)

    # === POST: Menilai jawaban ===
    if request.method == "POST":
        try:
            questions = request.session.get("quiz_questions", [])
            if not questions:
                raise ValueError("❌ Soal tidak ditemukan di sesi.")

            score = 0
            total = len(questions)
            user_answers = []

            for i, q in enumerate(questions):
                user_answer = request.POST.get(f"q{i}")
                user_answers.append(user_answer)
                if user_answer == q["answer"]:
                    score += 1

            percentage = round((score / total) * 100) if total > 0 else 0

            QuizResult.objects.create(  # type: ignore
                user=request.user,
                course=course,
                score=score,
                total_questions=total,
                percentage=percentage
            )
            # ✅ Tandai tugas quiz selesai kalau ada
            related_tasks = HomeworkTask.objects.filter(  # type: ignore
                task_type='quiz',
                quiz_keyword__iexact=course.name
            )

            print("🧪 course.name:", course.name)
            print("🧪 related_tasks:", related_tasks)

            show_homework_toast = False
            for task in related_tasks:
                HomeworkSubmission.objects.get_or_create(  # type: ignore
                    student=request.user,
                    task=task,
                    defaults={'quiz_completed': True}
                )
                if percentage >= 50:
                    show_homework_toast = True

            request.session["quiz_last_answers"] = {
                "questions": questions,
                "user_answers": user_answers
            }

            del request.session["quiz_questions"]

            return render(request, 'courses/quiz_result.html', {
                'course': course,
                'score': score,
                'total': total,
                'percentage': percentage,
                'show_homework_toast': show_homework_toast
            })

        except Exception as e:
            print("❌ POST Error:", e)
            error_message = "Terjadi kesalahan saat memproses jawaban."
            return render(request, 'courses/quiz.html', {
                'course': course,
                'questions': questions if 'questions' in locals() else [],
                'error': error_message
            })

    # === GET: Minta soal dari Gemini ===
    else:
        prompt = f"""
        Buatkan 10 soal pilihan ganda tentang '{course.name}'.
        Format HARUS JSON valid seperti ini:
        [
            {{
                "question": "Apa itu simple present tense?",
                "options": {{
                    "A": "Untuk kebiasaan",
                    "B": "Untuk masa depan",
                    "C": "Untuk masa lalu"
                }},
                "answer": "A"
            }},
            ...
        ]
        Jangan beri penjelasan tambahan. Langsung dari tanda [ dan hanya JSON saja.
        """

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            # 🧹 Bersihin dari ```json ... ```
            response_text = response.text.strip()  # type: ignore
            if response_text.startswith("```"):
                response_text = re.sub(r"^```[a-z]*\n?", "", response_text)
                response_text = re.sub(r"\n?```$", "", response_text)

            questions = json.loads(response_text)

        except Exception as e:
            print("❌ Gagal ambil soal dari Gemini:", e)
            error_message = "Gagal memuat soal dari Gemini AI."

        # Simpan soal ke session
        if questions:
            request.session["quiz_questions"] = questions

        return render(request, 'courses/quiz.html', {
            'course': course,
            'questions': questions,
            'error': error_message
        })

@login_required
def quiz_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    review_data = request.session.get("quiz_last_answers")

    if not review_data:
        return redirect("course_list")

    user_answers = review_data["user_answers"]  # Sudah list, langsung pakai

    return render(request, "courses/quiz_review.html", {
        "course": course,
        "questions": review_data["questions"],
        "user_answers": user_answers,
    })