# from django.shortcuts import render

# Create your views here.

from .models import Paragraph, Word, CustomUser
from .serializers import ParagraphSerializer, CustomUserSerializer
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password  # Import check_password function

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        if not (username and password and email):
            return Response(
                {"error": "Username, password, and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the user without authentication credentials
        user = User.objects.create_user(
            username=username, password=password, email=email
        )

        # Optionally, you can customize the response
        return Response(
            {"message": "User registered successfully.", "user_id": user.id},
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Query the database for the user based on email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and check_password(password, user.password):
            # Password matches, generate tokens and return success response
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        else:
            # User authentication failed, return error response
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class ParagraphCreateAPIView(APIView):
    def post(self, request, format=None):
        content = request.data.get("content", "")
        paragraphs = content.split(
            "\n\n"
        )  # Split content into paragraphs based on two newline characters

        for para in paragraphs:
            words = para.split()  # Tokenize words by splitting at whitespace
            words_lower = [word.lower() for word in words]  # Convert words to lowercase

            # Create a new paragraph object with content and save it
            paragraph = Paragraph(content=para)
            paragraph.save()

            # Index words against the paragraph they are from
            for word in words_lower:
                word_obj = Word(word=word, paragraph=paragraph)
                word_obj.save()

        return Response(
            {"message": "Paragraph created successfully", "paragraph_id": paragraph.id},
            status=status.HTTP_201_CREATED,
        )


class SearchParagraphsAPIView(generics.ListAPIView):
    serializer_class = ParagraphSerializer

    def get_queryset(self):
        word = self.request.query_params.get(
            "word", ""
        ).lower()  # Convert the search word to lowercase
        return Paragraph.objects.filter(content__icontains=word)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        word = self.request.query_params.get("word", "")

        if len(queryset) > 2:
            paragraphs = [f"Paragraph {idx + 1}" for idx, _ in enumerate(queryset)]
            output = ", ".join(paragraphs[:-1]) + f", and {paragraphs[-1]}"
        elif len(queryset) == 2:
            output = f"Paragraph {queryset[0].id} and {queryset[1].id}"
        elif len(queryset) == 1:
            output = f"Paragraph {queryset[0].id}"
        else:
            output = "No matching paragraphs"

        response_data = {"word": word, "output": output}
        return Response(response_data)
