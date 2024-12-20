from . models import Book, Borrow, User
from . serializer import BookSerializer, BorrowSerializer
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny , IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ValidationError("Please enter a username and password")
        if User.objects.filter(username=username).exists():
            raise ValidationError("User already exists")
        user = User.objects.create_user(username = username, password = password)
        return Response({"message":"User created successfully"}, status = status.HTTP_201_CREATED)
    

class LoginAPIView(TokenObtainPairView):
    permission_classes = [AllowAny] 
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return Response(
            {
                "message": "Login successful",
                "tokens": response.data,
            },
            status=status.HTTP_200_OK,
        )

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author']

class BookCreateAPIView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class BookRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser] 

class BorrowBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        if book.available_copies < 1:
            return Response({"error": "No copies available for borrowing."}, status=status.HTTP_400_BAD_REQUEST)

        borrow = Borrow.objects.create(user=request.user, book=book)
        book.available_copies -= 1
        book.save()

        serializer = BorrowSerializer(borrow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReturnBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        borrow_id = request.data.get('borrow_id')
        try:
            borrow = Borrow.objects.get(id=borrow_id, user=request.user)
        except Borrow.DoesNotExist:
            return Response({"error": "Borrow entry not found."}, status=status.HTTP_404_NOT_FOUND)

        if borrow.returned_at is not None:
            return Response({"error": "Book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)

        borrow.returned_at = timezone.now()
        borrow.book.available_copies += 1
        borrow.book.save()
        borrow.save()

        serializer = BorrowSerializer(borrow)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyBorrowsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        borrows = Borrow.objects.filter(user=request.user).order_by('-borrowed_at')
        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data)
