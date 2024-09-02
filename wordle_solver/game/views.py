from django.shortcuts import render
from django.http import JsonResponse
from .models import PossibleWord, NextBestGuess

# Helper function to calculate remaining words based on feedback and guesses
def calculate_remaining_words(all_feedback, all_guesses):
    # Start with all possible words
    remaining_words = list(PossibleWord.objects.values_list('word', flat=True))

    # Apply each feedback to filter down remaining words
    for feedback, guess in zip(all_feedback, all_guesses):
        remaining_words = [word for word in remaining_words if word_matches_feedback(word, feedback, guess)]

    return remaining_words

# Function to determine if a word matches the feedback
def word_matches_feedback(word, feedback, current_guess):
    # Implement logic to check if the word matches the feedback given the current guess
    for i, letter in enumerate(feedback):
        if letter == 'G' and word[i] != current_guess[i]:
            return False
        if letter == 'Y' and (word[i] == current_guess[i] or current_guess[i] not in word):
            return False
        if letter == '-' and current_guess[i] in word:
            return False
    return True

# Function to get the next best guess based on remaining words
def get_next_best_guess(remaining_words):
    remaining_words_str = ','.join(remaining_words)
    try:
        next_best_guess_entry = NextBestGuess.objects.get(remaining_words=remaining_words_str)
        return next_best_guess_entry.next_best_word
    except NextBestGuess.DoesNotExist:
        return "crane"  # Fallback or default guess if no entry is found

def wordle_solver(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        # Get all feedback and guesses from the form submission
        all_feedback = request.POST.getlist('feedback[]')
        all_guesses = request.POST.getlist('guess[]')

        # Calculate remaining words based on all feedback and guesses
        remaining_words = calculate_remaining_words(all_feedback, all_guesses)

        # Determine the next best guess based on the updated remaining words
        next_best_guess = get_next_best_guess(remaining_words)

        # Return the next guess as a JSON response for AJAX to process
        return JsonResponse({'current_guess': next_best_guess})

    # For initial page load or other HTTP methods, render the HTML template
    return render(request, 'game/wordle_solver.html', {'current_guess': 'salet'})