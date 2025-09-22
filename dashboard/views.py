from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def student_dashboard(request):
    return render(request, 'dashboard/student_dashboard.html')

@login_required
def assessor_dashboard(request):
    return render(request, 'dashboard/assessor_dashboard.html')

# Add a health check endpoint
def health_check(request):
    return HttpResponse("Server is running", content_type="text/plain")
