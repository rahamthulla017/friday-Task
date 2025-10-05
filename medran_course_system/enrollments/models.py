from django.db import models
from users.models import User
from courses.models import Course

PROGRESS_CHOICES = [
    ('Not Started', 'Not Started'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
]

class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.CharField(max_length=20, choices=PROGRESS_CHOICES, default='Not Started')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"
