# library/urls.py
from django.urls import path
from .views import AuthorListCreateView, BookListCreateView, BorrowerListCreateView

urlpatterns = [
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('borrowers/', BorrowerListCreateView.as_view(), name='borrower-list-create'),
]
