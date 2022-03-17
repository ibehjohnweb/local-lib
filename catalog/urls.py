from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='author'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('fill-in-book/', views.bookentry, name='book_form'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('sign-up-form/', views.signup, name='signup'),

]

# path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
# path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
# re_path(r'^book/(?P<stub>[-\w]+)$', views.BookDetailView.as_view(), name='book_detail'),