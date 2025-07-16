from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth.views import LoginView
from django.contrib import messages

def lobby(request):
    return render(request, 'home.html') 

@login_required
def home(request):
    show_login_toast = request.session.pop('show_login_toast', False)
    if request.user.is_authenticated:
        return render(request, 'welcome.html', {'user': request.user, 'show_login_toast': show_login_toast})
    return render(request, 'welcome.html', {'show_login_toast': show_login_toast})

@login_required
def dashboard_redirect(request):
    role = getattr(request.user, 'role', None)

    if role == 'teacher':
        return redirect('teacher_dashboard')
    elif role == 'student':
        return redirect('student_dashboard')
    else:
        return HttpResponse("Akun ini belum punya role yang benar.")  # type: ignore

@login_required
def course_redirect(request):
    return redirect('course_list')  

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # ganti nama url sesuai punya kamu
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # supaya user tidak logout
            return redirect('profile')
    else:
        form = CustomPasswordChangeForm(user=request.user)

    return render(request, 'users/change_password.html', {'form': form})

class CustomLoginView(LoginView):
    def form_valid(self, form):
        self.request.session['show_login_toast'] = True
        return super().form_valid(form)