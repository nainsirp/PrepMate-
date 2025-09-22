from django.db import models
from accounts.models import User

class AptitudeQuestion(models.Model):
    CATEGORIES = (
        ('logical', 'Logical Reasoning'),
        ('mathematical', 'Mathematical Ability'),
        ('programming', 'Programming Fundamentals'),
        ('domain', 'Domain Specific')
    )
    
    category = models.CharField(max_length=20, choices=CATEGORIES)
    question_text = models.TextField()
    option_1 = models.CharField(max_length=200)
    option_2 = models.CharField(max_length=200)
    option_3 = models.CharField(max_length=200)
    option_4 = models.CharField(max_length=200)
    correct_answer = models.IntegerField(choices=[(1,1), (2,2), (3,3), (4,4)])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_correct_option(self):
        if self.correct_answer == 1:
            return self.option_1
        elif self.correct_answer == 2:
            return self.option_2
        elif self.correct_answer == 3:
            return self.option_3
        else:
            return self.option_4

class QuizResult(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=AptitudeQuestion.CATEGORIES)
    score = models.IntegerField()
    max_score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def percentage(self):
        return (self.score / self.max_score) * 100 if self.max_score > 0 else 0
