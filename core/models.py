from django.db import models
from django.utils import timezone

class Book(models.Model):
    book_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    STATUS_CHOICES = (
        ('Available', 'Available'),
        ('Issued', 'Issued'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.book_id} - {self.title}"

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.student_id} - {self.name}"

class Issue(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=timezone.now)
    return_date = models.DateField()
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} issued to {self.student.name}"

class Attendance(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100)
    time_in = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Present')

    def __str__(self):
        return f"{self.name} - {self.status}"
