from django.shortcuts import render, get_object_or_404
from .models import Homework, HomeworkSubmission
from django.contrib.auth.decorators import login_required
from courses.models import QuizResult, Course
from .forms import HomeworkUploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import HomeworkTask

@login_required
def homework_list(request):
    homeworks = Homework.objects.filter(assigned_to=request.user)  # type: ignore

    for hw in homeworks:
        task_list = []  # tampung task yang sudah diproses

        for task in hw.tasks.all():
            task = task  # penting agar bisa modifikasi task sendiri
            task.completed = False
            task.course_id = None

            if task.task_type == 'quiz' and task.quiz_keyword:
                course = Course.objects.filter(name__icontains=task.quiz_keyword).first()  # type: ignore
                task.course_id = course.id if course else None

                done = QuizResult.objects.filter(
                    user=request.user,
                    course__name__icontains=task.quiz_keyword,
                    percentage__gte=50
                ).exists()

                task.completed = done

                if done:
                    submission, created = HomeworkSubmission.objects.get_or_create(
                        student=request.user,
                        task=task,
                        defaults={'quiz_completed': True}
                    )
                    if not created and not submission.quiz_completed:
                        submission.quiz_completed = True
                        submission.save()

            # Ganti dari 'upload' ke 'catatan' agar konsisten
            elif task.task_type == 'catatan':
                submission = HomeworkSubmission.objects.filter(
                    student=request.user,
                    task=task
                ).first()

                if submission:
                    task.completed = bool(submission.image) and submission.is_approved
                    task.approved = submission.is_approved
                    task.waiting_approval = bool(submission.image) and not submission.is_approved
                    print(f"DEBUG: image={submission.image}, is_approved={submission.is_approved}, waiting_approval={task.waiting_approval}")
                else:
                    task.completed = False
                    task.approved = False
                    task.waiting_approval = False

                print(f"[CATATAN] {task.instruction[:30]} | uploaded={bool(submission and submission.image)} | approved={getattr(submission, 'is_approved', False)}")

            else:
                task.completed = False
                print(f"[LAINNYA] {task.instruction[:30]} | completed={task.completed}")

            task_list.append(task)

        # Tambahkan hasil task yang sudah diproses ke atribut custom
        hw.enriched_tasks = task_list

    return render(request, "homework/homework_list.html", {"homeworks": homeworks})

def homework_upload(request, task_id):
    task = get_object_or_404(HomeworkTask, id=task_id)
    # Pastikan hanya untuk tipe catatan/upload
    if task.task_type != 'catatan':
        return HttpResponseRedirect(reverse('homework_list'))

    submission, created = HomeworkSubmission.objects.get_or_create(
        student=request.user,
        task=task
    )

    if request.method == 'POST':
        form = HomeworkUploadForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('homework_list'))
    else:
        form = HomeworkUploadForm(instance=submission)

    return render(request, 'homework/upload_task.html', {
        'form': form,
        'task': task
    })
