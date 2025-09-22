from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import InterviewSession, InterviewQuestion, InterviewFeedback
from accounts.models import User

@login_required
def interview_list(request):
    if request.user.is_student:
        interviews = InterviewSession.objects.filter(student=request.user)
    else:
        return redirect('interviews:manage')
        
    context = {
        'interviews': interviews
    }
    return render(request, 'interviews/interview_list.html', context)

@login_required
def manage_interviews(request):
    if not request.user.is_assessor:
        messages.error(request, 'Permission denied')
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        student_id = request.POST.get('student')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        try:
            student = User.objects.get(id=student_id, role='student')
            InterviewSession.objects.create(
                student=student,
                assessor=request.user,
                date=date,
                time=time
            )
            messages.success(request, 'Interview scheduled successfully')
        except Exception as e:
            messages.error(request, f'Error scheduling interview: {str(e)}')
    
    context = {
        'interviews': InterviewSession.objects.filter(assessor=request.user),
        'students': User.objects.filter(role='student')
    }
    return render(request, 'interviews/manage_interviews.html', context)
