from django.db import models
from accounts.models import User

class GDTopic(models.Model):
    topic_text = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.topic_text

class GDSession(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    
    topic = models.ForeignKey(GDTopic, on_delete=models.CASCADE)
    assessor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gd_sessions_created')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    room_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"GD on {self.topic} - {self.date}"
    
class GDParticipant(models.Model):
    session = models.ForeignKey(GDSession, on_delete=models.CASCADE, related_name='participants')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    is_removed = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)  # New field for blocking participants
    
    def __str__(self):
        return f"{self.student.username} in {self.session}"
    
    class Meta:
        unique_together = ('session', 'student')
