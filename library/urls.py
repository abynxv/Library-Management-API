from django.urls import path
from . views import BookRetrieveUpdateDeleteAPIView, BookCreateAPIView, BookListAPIView
from . views import BorrowBookAPIView, ReturnBookAPIView, MyBorrowsAPIView
from . views import RegisterAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),  
    path('logout/', LogoutAPIView.as_view(), name='logout'), 

    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDeleteAPIView.as_view(), name='book-detail'),    

    path('borrow/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('return/', ReturnBookAPIView.as_view(), name='return-book'),
    path('my-borrows/', MyBorrowsAPIView.as_view(), name='my-borrows'),
]
