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

def word_matches_feedback(word, feedback, current_guess):
    """
    Checks if a word matches the given feedback based on the current guess.

    Args:
    word (str): The word to check.
    feedback (str): A string of feedback ('G', 'Y', '-') for each letter of the guess.
    current_guess (str): The guessed word.

    Returns:
    bool: True if the word matches the feedback, False otherwise.
    """
    # Create a dictionary to keep track of letter counts in the word
    letter_counts = {letter: word.count(letter) for letter in set(word)}

    for i, letter_feedback in enumerate(feedback):
        if letter_feedback == 'G':
            # If feedback is 'G', the letter must be in the exact position
            if word[i] != current_guess[i]:
                return False
            # Reduce the count for the matched letter
            letter_counts[current_guess[i]] -= 1

    for i, letter_feedback in enumerate(feedback):
        if letter_feedback == 'Y':
            # If feedback is 'Y', the letter must be present but not in the same position
            if current_guess[i] not in word or word[i] == current_guess[i] or letter_counts[current_guess[i]] <= 0:
                return False
            # Reduce the count for the matched letter
            letter_counts[current_guess[i]] -= 1

    for i, letter_feedback in enumerate(feedback):
        if letter_feedback == '-':
            # If feedback is '-', the letter should not appear in the word
            # unless it's already matched as 'G' or 'Y'
            if current_guess[i] in word and letter_counts[current_guess[i]] > 0:
                return False

    return True
    
def get_next_best_guess(remaining_words):
    """
    Query the database for the next best guess given the current remaining words.
    
    Args:
    remaining_words (list): List of remaining words.

    Returns:
    str: The next best guess.
    """
    # Ensure the remaining words are in alphabetical order
    remaining_words.sort()
    remaining_words_str = ','.join(remaining_words)
    
    # Query the database
    try:
        next_best_guess_entry = NextBestGuess.objects.get(remaining_words=remaining_words_str)
        return next_best_guess_entry.next_best_word
    except NextBestGuess.DoesNotExist:
        return "crane" # Fallback or default guess if no entry is found

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