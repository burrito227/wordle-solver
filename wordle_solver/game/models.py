from django.db import models

# Create your models here.
class PossibleWord(models.Model):
    word = models.CharField(max_length=5, unique=True)

class AcceptedWord(models.Model):
    word = models.CharField(max_length=5, unique=True)

class NextBestGuess(models.Model):
    remaining_words = models.TextField()
    next_best_word = models.CharField(max_length=5)