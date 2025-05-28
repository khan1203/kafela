from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    details = models.TextField()

    def __str__(self):
        return self.name

class BookRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('returned', 'Returned'),
        ('due', 'Due'),
        ('overdue', 'Overdue'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    borrow_duration = models.IntegerField()  # In days
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issued_date = models.DateTimeField(null=True, blank=True)
    issued_duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.name} - {self.user.username}"