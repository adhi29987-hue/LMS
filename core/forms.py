from django import forms
from .models import Book, Student, Issue, Attendance

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'author', 'status']
        widgets = {
            'book_id': forms.TextInput(attrs={'placeholder': 'e.g. B001'}),
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'department']
        widgets = {
            'student_id': forms.TextInput(attrs={'placeholder': 'e.g. S1001'}),
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'department': forms.TextInput(attrs={'placeholder': 'e.g. Computer Science'}),
        }

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['student', 'book', 'return_date']
        widgets = {
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(status='Available')

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['name', 'role', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full name'}),
            'role': forms.TextInput(attrs={'placeholder': 'e.g. Librarian'}),
        }
