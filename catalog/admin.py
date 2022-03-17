from django.contrib import admin
from . models import Author, Book, BookInstance, Genre


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'date_of_birth', 'date_of_death')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')



class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )



admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Genre)








