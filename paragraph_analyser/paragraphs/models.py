from django.db import models


# Create your models here.
class Paragraph(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[
            :50
        ]  # Display first 50 characters of content as the string representation


class Word(models.Model):
    word = models.CharField(max_length=255)
    paragraph = models.ForeignKey(
        Paragraph, related_name="words", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.word
