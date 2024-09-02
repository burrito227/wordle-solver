import itertools
import Calculate_Entropy as parallel_entropy
import pandas as pd

# Load words from the text files into lists
# with open('accepted_words.txt', 'r') as file:
#     accepted_words = file.read().splitlines()

with open('possible_words.txt', 'r') as file:
    possible_words = file.read().splitlines()

def get_feedback(guess, actual):
    """
    Generates feedback for a given guess compared to the actual word.

    Args:
    guess (str): The guessed word.
    actual (str): The actual word to compare against.

    Returns:
    str: Feedback string using 'G' for green, 'Y' for yellow, and '-' for grey.
    """
    feedback = ['-' for _ in range(5)]
    actual_letters = list(actual)

    # First pass: Check for correct letters in the correct place ('G')
    for i in range(5):
        if guess[i] == actual[i]:
            feedback[i] = 'G'
            actual_letters[i] = None  # Mark this letter as used

    # Second pass: Check for correct letters in the wrong place ('Y')
    for i in range(5):
        if feedback[i] == '-':  # Only consider letters not already marked as 'G'
            if guess[i] in actual_letters:
                feedback[i] = 'Y'
                actual_letters[actual_letters.index(guess[i])] = None  # Mark this letter as used

    return ''.join(feedback)

def get_remaining_words(guess, feedback, words):
    """
    Filters the list of words based on feedback from the guess.

    Args:
    guess (str): The guessed word.
    feedback (str): A string of feedback ('G', 'Y', '-') for each letter of the guess.
    words (list): List of current possible words.

    Returns:
    list: Filtered list of remaining valid words.
    """
    remaining_words = []
    green_letters = [guess[i] if feedback[i] == 'G' else None for i in range(5)]
    yellow_letters = [guess[i] if feedback[i] == 'Y' else None for i in range(5)]
    grey_letters = set(guess[i] for i in range(5) if feedback[i] == '-')

    for word in words:
        is_valid = True

        # Check greens
        for i, letter in enumerate(green_letters):
            if letter and word[i] != letter:
                is_valid = False
                break

        # Check yellows
        for i, letter in enumerate(yellow_letters):
            if letter:
                if letter not in word or word[i] == letter:
                    is_valid = False
                    break

        # Check greys
        if any(letter in word for letter in grey_letters):
            is_valid = False

        if is_valid:
            remaining_words.append(word)

    return remaining_words

def split_words_to_dataframe(words):
    """
    Splits a list of 5-letter words into a DataFrame where each column represents a letter position.

    Args:
    words (list): List of words to split.

    Returns:
    pd.DataFrame: DataFrame with each letter of the word in separate columns.
    """
    # Convert list of words to a DataFrame, splitting each word into separate letters
    df = pd.DataFrame([list(word) for word in words], columns=['0', '1', '2', '3', '4'])
    return df

def concatWord(row) -> str:
    """
    Concatenates a 5-letter word from a DataFrame row.

    Args:
    row (pd.Series): A row from a DataFrame containing letters.

    Returns:
    str: The concatenated word.
    """
    return row['0'] + row['1'] + row['2'] + row['3'] + row['4']

def calculate_entropy(remaining_words):
    """
    Based on the remaining words, returns the word with the highest entropy.

    Args:
    remaining_words (list): List of remaining valid words.

    Returns:
    tuple: (entropy value, next best word)
    """
    # Convert the list of remaining words to a DataFrame with each letter in a separate column
    remaining_words_df = split_words_to_dataframe(remaining_words)

    # Initialize entropy calculation object
    entropy = parallel_entropy.wordleEntropy()

    # Calculate entropy for remaining words DataFrame
    entropy.parallelEntropy(remaining_words_df, numProcess=11)
    df = entropy.df

    # Get the word with the maximum entropy
    max_entropy_index = df['E'].idxmax()
    max_entropy_word = concatWord(df.loc[max_entropy_index])

    return df['E'].max(), max_entropy_word

def simulate_game(possible_words, output_sql_file):
    """
    Simulates all possible games starting with 'salet' and computes next best guesses.

    Args:
    possible_words (list): List of possible words that can be actual answers.
    output_sql_file (str): Path to the output .sql file.
    """
    # Open the file for writing
    with open(output_sql_file, 'w') as sql_file:
        # Write SQL to create the table (if needed)
        sql_file.write('''
            CREATE TABLE IF NOT EXISTS next_best_guess (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                remaining_words TEXT,
                next_best_word TEXT
            );
        ''')

        for actual_word in possible_words:
            current_guess = 'salet'
            remaining_words = possible_words.copy()

            while current_guess != actual_word:
                feedback = get_feedback(current_guess, actual_word)
                remaining_words = get_remaining_words(current_guess, feedback, remaining_words)
                
                if not remaining_words:  # No possible words remaining
                    break

                _, next_best_word = calculate_entropy(remaining_words)

                # Insert the current state into the SQL file
                insert_statement = f"INSERT INTO next_best_guess (remaining_words, next_best_word) VALUES ('{','.join(remaining_words)}', '{next_best_word}');\n"
                sql_file.write(insert_statement)

                current_guess = next_best_word

# Main execution
output_sql_file = 'next_best_guess.sql'
simulate_game(possible_words, output_sql_file)