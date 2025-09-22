from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
import uuid
from .models import GDTopic, GDSession, GDParticipant
from accounts.models import User
from django.conf import settings
from django.db.utils import OperationalError

@login_required
def gd_list(request):
    """View for students to see available GD sessions"""
    if not request.user.is_student:
        return redirect('dashboard:home')
        
    # Get all active and upcoming sessions
    active_sessions = GDSession.objects.filter(
        status__in=['scheduled', 'active'],
        date__gte=timezone.now().date()
    )
    
    # Get sessions the student is participating in
    my_sessions = GDSession.objects.filter(
        participants__student=request.user
    ).distinct()
    
    context = {
        'active_sessions': active_sessions,
        'my_sessions': my_sessions
    }
    return render(request, 'groupdiscussion/gd_list.html', context)

@login_required
def manage_gd(request):
    """View for assessors to manage GD sessions"""
    if not request.user.is_assessor:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        # Handle creating a new GD session
        topic_id = request.POST.get('topic')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        # If topic_id is 'new', create a new topic
        if topic_id == 'new':
            topic_text = request.POST.get('new_topic_text')
            description = request.POST.get('new_topic_description', '')
            
            if not topic_text:
                messages.error(request, 'Topic text is required')
                return redirect('groupdiscussion:manage')
                
            topic = GDTopic.objects.create(
                topic_text=topic_text,
                description=description,
                created_by=request.user
            )
        else:
            topic = get_object_or_404(GDTopic, id=topic_id)
        
        # Create the GD session
        try:
            GDSession.objects.create(
                topic=topic,
                assessor=request.user,
                date=date,
                time=time,
                room_id=f"gd-{uuid.uuid4().hex[:8]}"
            )
            messages.success(request, 'Group Discussion session created successfully!')
        except Exception as e:
            messages.error(request, f'Error creating session: {str(e)}')
    
    # Get all topics and sessions created by this assessor
    topics = GDTopic.objects.all().order_by('-created_at')
    sessions = GDSession.objects.filter(assessor=request.user).order_by('-date', '-time')
    
    context = {
        'topics': topics,
        'sessions': sessions
    }
    return render(request, 'groupdiscussion/manage_gd.html', context)

@login_required
def join_gd(request, session_id):
    """View for students to join or rejoin a GD session"""
    if not request.user.is_student:
        return redirect('dashboard:home')
        
    session = get_object_or_404(GDSession, id=session_id)
    
    # Check if session is available to join
    if session.status not in ['scheduled', 'active']:
        messages.error(request, 'This session is no longer available to join')
        return redirect('groupdiscussion:list')
    
    # Check if participant exists
    try:
        # Try with is_blocked field
        participant, created = GDParticipant.objects.get_or_create(
            session=session,
            student=request.user,
            defaults={'is_removed': False, 'is_blocked': False}
        )
        
        # If participant exists but left or was removed (but not blocked), allow them to rejoin
        if not created:
            if participant.is_blocked:
                messages.error(request, 'You have been blocked from this discussion by the moderator')
                return redirect('groupdiscussion:list')
            
            # Allow rejoining if previously left or removed
            if participant.is_removed or participant.left_at:
                participant.is_removed = False
                participant.left_at = None
                participant.joined_at = timezone.now()
                participant.save()
                messages.success(request, f'You have rejoined the discussion on "{session.topic.topic_text}"')
            else:
                messages.info(request, f'You are already a participant in this discussion')
    except OperationalError:
        # Fallback if is_blocked field doesn't exist yet
        participant, created = GDParticipant.objects.get_or_create(
            session=session,
            student=request.user,
            defaults={'is_removed': False}
        )
        
        # Allow rejoining if previously left or removed
        if not created and (participant.is_removed or participant.left_at):
            participant.is_removed = False
            participant.left_at = None
            participant.joined_at = timezone.now()
            participant.save()
            messages.success(request, f'You have rejoined the discussion on "{session.topic.topic_text}"')
        elif not created:
            messages.info(request, f'You are already a participant in this discussion')
    
    if created:
        # New participant
        messages.success(request, f'You have joined the discussion on "{session.topic.topic_text}"')
    
    return redirect('groupdiscussion:session', session_id=session.id)

@login_required
def gd_session(request, session_id):
    """View for the actual GD session interface"""
    session = get_object_or_404(GDSession, id=session_id)
    
    # Check if user is authorized to view this session
    is_participant = False
    if request.user.is_student:
        try:
            is_participant = GDParticipant.objects.filter(
                session=session, 
                student=request.user,
                is_removed=False
            ).exists()
        except OperationalError:
            # Fallback if is_blocked field doesn't exist yet
            is_participant = GDParticipant.objects.filter(
                session=session, 
                student=request.user,
                is_removed=False
            ).exists()
        
        if not is_participant:
            messages.error(request, 'You are not a participant in this discussion')
            return redirect('groupdiscussion:list')
    elif request.user.is_assessor:
        if request.user != session.assessor:
            messages.error(request, 'You are not the assessor for this discussion')
            return redirect('groupdiscussion:manage')
    else:
        return redirect('dashboard:home')
    
    # Mark session as active if it's scheduled and the time has come
    if session.status == 'scheduled' and timezone.now().date() >= session.date:
        session.status = 'active'
        session.save()
    
    # Update joined_at timestamp for participant if not already set
    if is_participant:
        participant = GDParticipant.objects.get(session=session, student=request.user)
        if not participant.joined_at:
            participant.joined_at = timezone.now()
            participant.save()
    
    # Get participant data for the session
    try:
        participants = GDParticipant.objects.filter(session=session, is_removed=False)
        blocked_participants = GDParticipant.objects.filter(session=session, is_blocked=True)
    except OperationalError:
        # Fallback if is_blocked field doesn't exist yet
        participants = GDParticipant.objects.filter(session=session, is_removed=False)
        blocked_participants = []
    
    context = {
        'session': session,
        'participants': participants,
        'blocked_participants': blocked_participants,  # Pass blocked participants to template
        'is_assessor': request.user.is_assessor,
        'webrtc_enabled': session.status == 'active',
        'ice_servers': settings.WEBRTC_ICE_SERVERS,
        'participant_data': [
            {
                'id': p.student.id, 
                'username': p.student.username
            } for p in participants
        ],
        'has_migration_error': False
    }
    
    try:
        # Check if any participant is blocked (will fail if column doesn't exist)
        has_blocked = GDParticipant.objects.filter(session=session, is_blocked=True).exists()
    except OperationalError:
        # Migration hasn't been applied yet
        context['has_migration_error'] = True
        messages.warning(request, "Database migration needed. Please run 'python manage.py migrate' to fully enable all features.")
    
    return render(request, 'groupdiscussion/gd_session.html', context)

@login_required
def end_gd(request, session_id):
    """View for assessors to end a GD session"""
    if not request.user.is_assessor:
        return redirect('dashboard:home')
        
    session = get_object_or_404(GDSession, id=session_id, assessor=request.user)
    
    if session.status in ['scheduled', 'active']:
        session.status = 'completed'
        session.save()
        messages.success(request, 'Group Discussion session has been marked as completed')
    
    return redirect('groupdiscussion:manage')

@login_required
def remove_participant(request, session_id, participant_id):
    """View for assessors to remove participants permanently"""
    if not request.user.is_assessor:
        return redirect('dashboard:home')
        
    session = get_object_or_404(GDSession, id=session_id, assessor=request.user)
    participant = get_object_or_404(GDParticipant, id=participant_id, session=session)
    
    participant.is_removed = True
    participant.left_at = timezone.now()
    participant.save()
    
    messages.success(request, f'{participant.student.username} has been removed from the discussion')
    return redirect('groupdiscussion:session', session_id=session.id)

@login_required
def block_participant(request, session_id, participant_id):
    """View for assessors to block participants"""
    if not request.user.is_assessor:
        return redirect('dashboard:home')
        
    session = get_object_or_404(GDSession, id=session_id, assessor=request.user)
    participant = get_object_or_404(GDParticipant, id=participant_id, session=session)
    
    participant.is_blocked = True
    participant.is_removed = True
    participant.left_at = timezone.now()
    participant.save()
    
    messages.success(request, f'{participant.student.username} has been blocked from the discussion')
    return redirect('groupdiscussion:session', session_id=session.id)

@login_required
def unblock_participant(request, session_id, participant_id):
    """View for assessors to unblock participants"""
    if not request.user.is_assessor:
        return redirect('dashboard:home')
        
    session = get_object_or_404(GDSession, id=session_id, assessor=request.user)
    participant = get_object_or_404(GDParticipant, id=participant_id, session=session)
    
    participant.is_blocked = False
    participant.is_removed = False
    participant.left_at = None
    participant.save()
    
    messages.success(request, f'{participant.student.username} has been unblocked and can now rejoin the discussion')
    return redirect('groupdiscussion:session', session_id=session.id)

@login_required
def leave_gd(request, session_id):
    """View for students to leave a GD session temporarily"""
    if not request.user.is_student:
        return redirect('dashboard:home')
        
    session = get_object_or_404(GDSession, id=session_id)
    
    try:
        participant = GDParticipant.objects.get(
            session=session,
            student=request.user
        )
        
        # Mark as left but don't remove completely
        participant.left_at = timezone.now()
        participant.save()
        
        messages.success(request, f'You have left the discussion on "{session.topic.topic_text}". You can rejoin later if needed.')
    except GDParticipant.DoesNotExist:
        messages.error(request, 'You are not a participant in this discussion')
    
    return redirect('groupdiscussion:list')
