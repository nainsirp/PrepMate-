from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AptitudeQuestion, QuizResult

@login_required
def test_list(request):
    if not request.user.is_student:
        return redirect('dashboard:home')
        
    results = QuizResult.objects.filter(student=request.user)
    categories = dict(AptitudeQuestion.CATEGORIES)
    
    context = {
        'categories': categories,
        'results': results
    }
    return render(request, 'aptitude/test_list.html', context)

@login_required
def take_test(request, category):
    if not request.user.is_student:
        return redirect('dashboard:home')
        
    if request.method == 'POST':
        questions = AptitudeQuestion.objects.filter(category=category)
        score = 0
        for q in questions:
            answered = request.POST.get(f'q{q.id}')
            if answered and int(answered) == q.correct_answer:
                score += 1
                
        QuizResult.objects.create(
            student=request.user,
            category=category,
            score=score,
            max_score=questions.count()
        )
        messages.success(request, 'Test completed successfully!')
        return redirect('aptitude:results')
    
    context = {
        'questions': AptitudeQuestion.objects.filter(category=category)
    }
    return render(request, 'aptitude/take_test.html', context)

@login_required
def manage_tests(request):
    if not request.user.is_assessor:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        category = request.POST.get('category')
        question = request.POST.get('question')
        options = [
            request.POST.get('option1'),
            request.POST.get('option2'),
            request.POST.get('option3'),
            request.POST.get('option4')
        ]
        correct = request.POST.get('correct')
        
        try:
            AptitudeQuestion.objects.create(
                category=category,
                question_text=question,
                option_1=options[0],
                option_2=options[1],
                option_3=options[2],
                option_4=options[3],
                correct_answer=correct,
                created_by=request.user
            )
            messages.success(request, 'Question added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding question: {str(e)}')
    
    context = {
        'questions': AptitudeQuestion.objects.all(),
        'categories': dict(AptitudeQuestion.CATEGORIES)
    }
    return render(request, 'aptitude/manage_tests.html', context)

@login_required
def test_results(request):
    if not request.user.is_student:
        return redirect('dashboard:home')
        
    results = QuizResult.objects.filter(student=request.user).order_by('-date_taken')
    
    context = {
        'results': results
    }
    return render(request, 'aptitude/test_results.html', context)

@login_required
def test_detail(request, result_id):
    if not request.user.is_student:
        return redirect('dashboard:home')
    
    result = get_object_or_404(QuizResult, id=result_id, student=request.user)
    
    # Get all questions from the category
    questions = AptitudeQuestion.objects.filter(category=result.category)
    
    context = {
        'result': result,
        'questions': questions,
        'category_name': dict(AptitudeQuestion.CATEGORIES).get(result.category)
    }
    return render(request, 'aptitude/test_detail.html', context)
