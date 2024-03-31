# from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Paragraph, Word
from .serializers import ParagraphSerializer


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
