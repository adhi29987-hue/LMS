from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Book, Student, Issue, Attendance
from .forms import BookForm, StudentForm, IssueForm, AttendanceForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    total_books = Book.objects.count()
    issued_books = Book.objects.filter(status='Issued').count()
    available_books = Book.objects.filter(status='Available').count()
    total_students = Student.objects.count()
    today = timezone.now().date()
    overdue_books = Issue.objects.filter(return_date__lt=today, is_returned=False).count()
    issues = Issue.objects.select_related('student', 'book').order_by('-issue_date')[:10]
    context = {
        'total_books': total_books,
        'issued_books': issued_books,
        'available_books': available_books,
        'total_students': total_students,
        'overdue_books': overdue_books,
        'issues': issues,
        'today': today,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def books_list(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query) if query else Book.objects.all()
    return render(request, 'core/books.html', {'books': books, 'query': query})


@login_required
def book_add(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Book added successfully!')
        return redirect('books_list')
    return render(request, 'core/book_form.html', {'form': form, 'action': 'Add'})


@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        messages.success(request, 'Book updated successfully!')
        return redirect('books_list')
    return render(request, 'core/book_form.html', {'form': form, 'action': 'Edit'})


@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('books_list')
    return render(request, 'core/confirm_delete.html', {'object': book, 'type': 'Book'})


@login_required
def students_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.filter(name__icontains=query) | Student.objects.filter(department__icontains=query) if query else Student.objects.all()
    return render(request, 'core/students.html', {'students': students, 'query': query})


@login_required
def student_add(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student added successfully!')
        return redirect('students_list')
    return render(request, 'core/student_form.html', {'form': form, 'action': 'Add'})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('students_list')
    return render(request, 'core/student_form.html', {'form': form, 'action': 'Edit'})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('students_list')
    return render(request, 'core/confirm_delete.html', {'object': student, 'type': 'Student'})


@login_required
def issue_book(request):
    form = IssueForm(request.POST or None)
    if form.is_valid():
        issue = form.save(commit=False)
        issue.book.status = 'Issued'
        issue.book.save()
        issue.save()
        messages.success(request, f'"{issue.book.title}" issued to {issue.student.name} successfully!')
        return redirect('dashboard')
    return render(request, 'core/issue.html', {'form': form})


@login_required
def return_book(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    if request.method == 'POST':
        issue.is_returned = True
        issue.save()
        issue.book.status = 'Available'
        issue.book.save()
        messages.success(request, f'"{issue.book.title}" returned successfully!')
        return redirect('dashboard')
    return render(request, 'core/confirm_return.html', {'issue': issue})


@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().order_by('-id')
    return render(request, 'core/attendance.html', {'attendances': attendances})


@login_required
def attendance_add(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Attendance marked successfully!')
        return redirect('attendance_list')
    return render(request, 'core/attendance_form.html', {'form': form})


@login_required
def reports(request):
    today = timezone.now().date()
    total_books = Book.objects.count()
    total_students = Student.objects.count()
    total_issued = Issue.objects.filter(is_returned=False).count()
    total_returned = Issue.objects.filter(is_returned=True).count()
    overdue = Issue.objects.filter(return_date__lt=today, is_returned=False).count()
    return_rate = round((total_returned / (total_returned + total_issued) * 100), 1) if (total_returned + total_issued) > 0 else 0
    recent_issues = Issue.objects.select_related('student', 'book').order_by('-issue_date')[:5]
    context = {
        'total_books': total_books,
        'total_students': total_students,
        'total_issued': total_issued,
        'total_returned': total_returned,
        'overdue': overdue,
        'return_rate': return_rate,
        'recent_issues': recent_issues,
        'today': today,
    }
    return render(request, 'core/reports.html', context)


@login_required
def download_excel(request):
    from django.http import FileResponse, Http404
    import os
    from django.conf import settings
    file_path = os.path.join(settings.BASE_DIR, 'LMS_Data.xlsx')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="LMS_Data.xlsx"'
        return response
    else:
        messages.error(request, 'Excel file has not been generated yet. Please add some data first.')
        return redirect('dashboard')

