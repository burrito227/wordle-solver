"""
Simple script to build the possibleword and acceptedword database static data
"""

# Load words from the text files into lists
with open('accepted_words.txt', 'r') as file:
    accepted_words = file.read().splitlines()

with open('possible_words.txt', 'r') as file:
    possible_words = file.read().splitlines()

with open("accepted_words.sql", 'w') as sql_file:
    for word in accepted_words:
        insert_statement = f"INSERT INTO [dbo].game_acceptedword (word) VALUES ('{word}');\n"
        sql_file.write(insert_statement)

with open("possible_words.sql", 'w') as sql_file:
    for word in possible_words:
        insert_statement = f"INSERT INTO [dbo].game_possibleword (word) VALUES ('{word}');\n"
        sql_file.write(insert_statement)