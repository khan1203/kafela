
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomUserCreationForm, BookRequestForm
from .models import Book, BookRequest
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

# Create your views here.

def is_admin(user):
    return user.is_superuser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_landing')
    else:
        form = CustomUserCreationForm()
    return render(request, 'library/register.html', {'form': form})

@login_required
def user_landing(request):
    books = Book.objects.all()
    user_requests = BookRequest.objects.filter(user=request.user, status='pending')
    accepted_requests = BookRequest.objects.filter(user=request.user, status='accepted')
    
    # Update status for accepted requests
    for req in accepted_requests:
        if req.issued_date:
            due_date = req.issued_date + timedelta(days=req.issued_duration)
            if timezone.now() > due_date:
                req.status = 'overdue'
            elif timezone.now() > due_date - timedelta(days=2):
                req.status = 'due'
            req.save()

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.user = request.user
            book_request.book = book
            book_request.save()
            messages.success(request, 'Book request submitted!')
            return redirect('user_landing')
    else:
        form = BookRequestForm()

    return render(request, 'library/user_landing.html', {
        'books': books,
        'user_requests': user_requests,
        'accepted_requests': accepted_requests,
        'form': form,
    })

@login_required
def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.user = request.user
            book_request.book_id = request.POST.get('book_id')
            book_request.save()
            return redirect('user_landing')
    else:
        form = BookRequestForm()
    return render(request, 'library/user_landing.html', {'form': form})

@login_required
def cancel_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id, user=request.user)
    if book_request.status == 'pending':
        book_request.delete()
        messages.success(request, 'Request canceled.')
    return redirect('user_landing')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    requests = BookRequest.objects.all()
    books = Book.objects.all()

    if query:
        requests = requests.filter(
            Q(user__username__icontains=query) |
            Q(book__name__icontains=query) |
            Q(user__student_id__icontains=query)
        )
    if status:
        requests = requests.filter(status=status)

    if request.method == 'POST' and 'accept_request' in request.POST:
        request_id = request.POST.get('request_id')
        book_request = get_object_or_404(BookRequest, id=request_id)
        book_request.status = 'accepted'
        book_request.issued_date = timezone.now()
        book_request.issued_duration = book_request.borrow_duration
        book_request.save()
        messages.success(request, 'Request accepted.')
        return redirect('admin_dashboard')

    return render(request, 'library/admin_dashboard.html', {
        'requests': requests,
        'books': books,
        'query': query,
        'status': status,
    })