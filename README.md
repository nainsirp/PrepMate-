# PrepMate

## Overview

PrepMate is a comprehensive interview preparation platform designed to help job seekers and students excel in their interview processes. The platform provides tools for mock interviews, aptitude testing, and group discussions, all managed through an intuitive and interactive interface.

## Features

### For Students
- **Mock Interviews**: Schedule and participate in one-on-one mock interviews with assessors
- **Aptitude Tests**: Take various aptitude tests categorized by domain and difficulty level
- **Group Discussions**: Join moderated group discussions to improve communication skills
- **Performance Analytics**: Track progress and review test results
- **Personalized Dashboard**: Get an overview of upcoming interviews and completed activities

### For Assessors
- **Interview Management**: Create and schedule mock interviews
- **Test Creation**: Design custom aptitude tests with various question formats
- **Group Discussion Moderation**: Create and moderate group discussion sessions
- **Candidate Evaluation**: Provide feedback and ratings for interview performance
- **Analytics Dashboard**: Monitor student progress and performance metrics

## Technical Stack

- **Backend**: Django 5.2
- **Frontend**: HTML, TailwindCSS, JavaScript
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Real-time Communication**: WebRTC for video interviews and group discussions
- **Authentication**: Django's built-in auth system with custom User model

## Getting Started

### Prerequisites
- Python 3.10+
- pip
- Virtual environment (recommended)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/prepmate.git
   cd prepmate
   ```

2. Create and activate virtual environment
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations
   ```bash
   python manage.py migrate
   ```

5. Create a superuser
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server
   ```bash
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## 📂 Project Structure

```text
PrepMate
├── accounts/           # User authentication and profiles
├── aptitude/           # Aptitude tests functionality
├── dashboard/          # Main dashboards for users
├── groupdiscussion/    # Group discussion module
├── interviews/         # Interview scheduling and management
├── prepmate/           # Main project settings
├── static/             # Static files (CSS, JS, images)
├── templates/          # HTML templates
├── media/              # User-uploaded content
├── manage.py           # Django management script
└── requirements.txt    # Project dependencies
```
## Features in Detail

Interview Module:
    Schedule interviews with specific time slots
    Video conferencing for remote interviews
    Structured feedback and evaluation system

Aptitude Test Module:
    Multiple question types (MCQ, coding challenges)
    Automatic grading system
    Category-specific test creation

Group Discussion Module:
    Real-time video-based group discussions
    Moderation tools for assessors
    Participant management features
    
UI/UX Features:
    Responsive Design: Works on desktop, tablet, and mobile devices
    Dark Mode: Toggle between light and dark themes
    Interactive UI Elements: Smooth animations and
