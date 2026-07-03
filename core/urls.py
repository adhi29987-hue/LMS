from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('books/', views.books_list, name='books_list'),
    path('books/add/', views.book_add, name='book_add'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('students/', views.students_list, name='students_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('issue/', views.issue_book, name='issue_book'),
    path('issue/<int:pk>/return/', views.return_book, name='return_book'),
    path('issued/', views.issued_books, name='issued_books'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/add/', views.attendance_add, name='attendance_add'),
    path('reports/', views.reports, name='reports'),
    path('download-excel/', views.download_excel, name='download_excel'),
]
