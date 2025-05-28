
from django.contrib import admin
from .models import Book, BookRequest

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'writer')
    search_fields = ('name', 'writer')

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'status', 'request_date')
    list_filter = ('status',)
    search_fields = ('book__name', 'user__username')