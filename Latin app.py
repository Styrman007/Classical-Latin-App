import random
from latin_1st_declension_a import words

def quiz_user(words):
    score = 0
    question_count = 0

    streaks = {w['English']: 0 for w in words}      # consecutive correct answers per word
    locked_words = {}                               # English word -> remaining questions to skip

    while True:
        # Decrement counters for locked words
        for w in list(locked_words):
            locked_words[w] -= 1
            if locked_words[w] <= 0:
                del locked_words[w]

        # Filter words to those NOT locked
        available_words = [w for w in words if w['English'] not in locked_words]
        if not available_words:
            print("No available words to quiz! Try again later.")
            break

        chosen_word = random.choice(available_words)
        correct_latin = chosen_word['Latin']

        # Get 3 random wrong answers
        wrong_options = [w['Latin'] for w in words if w['Latin'] != correct_latin]
        wrong_choices = random.sample(wrong_options, 3)

        options = wrong_choices + [correct_latin]
        random.shuffle(options)

        print(f"Mis on ladina keeles '{chosen_word['English']}'?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        user_input = input("Vali õige number (või 'q' väljumiseks): ").strip()
        if user_input.lower() == 'q':
            print(f"Lõpp! Sinu lõpp-punktid: {score}")
            break

        if not user_input.isdigit() or int(user_input) not in range(1, 5):
            print("Palun sisesta number 1 kuni 4.\n")
            continue

        user_choice = options[int(user_input) - 1]
        question_count += 1

        if user_choice.lower() == correct_latin.lower():
            print("Õige vastus!")
            score += 1
            # Increase streak for this word
            streaks[chosen_word['English']] += 1
            # Reset streak for others? (No, keep independent streaks)

            # If streak reaches 5, lock the word for 50 questions
            if streaks[chosen_word['English']] >= 3:
                locked_words[chosen_word['English']] = 50
                print(f"Võrratu! Sõna '{chosen_word['English']}' lukustatud järgmiste 50 küsimuse ajaks.\n")
                streaks[chosen_word['English']] = 0  # reset streak after locking

        else:
            print(f"Vale vastus. Õige on '{correct_latin}'.\n")
            # Reset streak for this word on mistake
            streaks[chosen_word['English']] = 0

        print(f"Sinu punktid: {score}\n")
        
def main():
    print("Welcome!")
    print("Press Enter to start or 'q' to quit.")
    start = input()
    if start.lower() == 'q':
        return
    quiz_user(words)  # Use words here

if __name__ == "__main__":
    main()