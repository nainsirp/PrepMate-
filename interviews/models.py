from django.db import models
from accounts.models import User

class InterviewSession(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_interviews')
    assessor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessor_interviews')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

class InterviewQuestion(models.Model):
    QUESTION_TYPE = (
        ('hr', 'HR'),
        ('technical', 'Technical')
    )
    
    type = models.CharField(max_length=10, choices=QUESTION_TYPE)
    question_text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class InterviewFeedback(models.Model):
    session = models.OneToOneField(InterviewSession, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
