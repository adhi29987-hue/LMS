from django.contrib import admin
from .models import Book, Student, Issue, Attendance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'author', 'status')
    search_fields = ('book_id', 'title', 'author')
    list_filter = ('status',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'department')
    search_fields = ('student_id', 'name', 'department')
    list_filter = ('department',)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('book', 'student', 'issue_date', 'return_date', 'is_returned')
    search_fields = ('book__title', 'student__name')
    list_filter = ('is_returned', 'issue_date')
    list_editable = ('is_returned',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'time_in', 'status')
    search_fields = ('name', 'role')
    list_filter = ('status', 'role')
