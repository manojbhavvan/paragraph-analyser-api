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
