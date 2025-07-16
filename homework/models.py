from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class Homework(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="homeworks")

    def __str__(self):
        return self.title

TASK_TYPE_CHOICES = (
    ('catatan', 'Catatan'),
    ('quiz', 'Quiz'),
)

class HomeworkTask(models.Model):
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='tasks')
    task_type = models.CharField(max_length=10, choices=TASK_TYPE_CHOICES)
    instruction = models.TextField()
    quiz_keyword = models.CharField(max_length=100, blank=True, null=True)  # hanya kalau tipe quiz
    deadline = models.DateField(null=True, blank=True)  # <<== Tambahan di sini
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task_type} - {self.instruction[:20]}"

class HomeworkSubmission(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(HomeworkTask, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='homework_uploads/', blank=True, null=True)
    quiz_completed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # True jika sudah di-ACC admin/guru

    def __str__(self):
        return f"{self.student.username} - {self.task.instruction[:20]}"
