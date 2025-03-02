# language_skill_enhancer.py

import random

class LanguageSkillEnhancer:
    def __init__(self):
        self.languages = ["English", "Spanish", "French", "German", "Italian"]
        self.difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        self.vocabulary = {
            "English": {
                "Beginner": ["apple", "banana", "cherry"],
                "Intermediate": ["accommodate", "acknowledge", "analyze"],
                "Advanced": ["abstruse", "callipygian", "defenestration"]
            },
            "Spanish": {
                "Beginner": ["manzana", "naranja", "plátano"],
                "Intermediate": ["acompañar", "admitir", "analizar"],
                "Advanced": ["abstruso", "callípigo", "defenestración"]
            },
            "French": {
                "Beginner": ["pomme", "banane", "cerise"],
                "Intermediate": ["accompagner", "admettre", "analyser"],
                "Advanced": ["abstrus", "callipyge", "défenestration"]
            },
            "German": {
                "Beginner": ["Apfel", "Banane", "Kirsche"],
                "Intermediate": ["begleiten", "anerkennen", "analysieren"],
                "Advanced": ["abstrus", "callipyg", "Fenstersturz"]
            },
            "Italian": {
                "Beginner": ["mela", "banana", "ciliegia"],
                "Intermediate": ["accompagnare", "ammettere", "analizzare"],
                "Advanced": ["abstruso", "callipigio", "defenestrazione"]
            }
        }
        self.grammar = {
            "English": {
                "Beginner": ["What is your name?", "How are you?", "What is your favorite color?"],
                "Intermediate": ["What do you like to do in your free time?", "What is your favorite hobby?", "What do you like to eat for breakfast?"],
                "Advanced": ["What is the difference between 'affect' and 'effect'?", "What is the correct usage of 'who' and 'whom'?", "What is the difference between 'its' and 'it's'?"]
            },
            "Spanish": {
                "Beginner": ["¿Cómo te llamas?", "¿Cómo estás?", "¿Cuál es tu color favorito?"],
                "Intermediate": ["¿Qué te gusta hacer en tu tiempo libre?", "¿Cuál es tu pasatiempo favorito?", "¿Qué te gusta comer para desayunar?"],
                "Advanced": ["¿Cuál es la diferencia entre 'afectar' y 'efecto'?", "¿Cuál es el uso correcto de 'quién' y 'quién'?", "¿Cuál es la diferencia entre 'su' y 'sus'?"]
            },
            "French": {
                "Beginner": ["Comment t'appelles-tu?", "Comment vas-tu?", "Quel est ton couleur préférée?"],
                "Intermediate": ["Qu'est-ce que tu aimes faire dans ton temps libre?", "Quel est ton passe-temps préféré?", "Qu'est-ce que tu aimes manger pour petit-déjeuner?"],
                "Advanced": ["Quelle est la différence entre 'affecter' et 'effet'?", "Quelle est l'utilisation correcte de 'qui' et 'qui'?", "Quelle est la différence entre 'son' et 'ses'?"]
            },
            "German": {
                "Beginner": ["Wie heißt du?", "Wie geht es dir?", "Was ist deine Lieblingsfarbe?"],
                "Intermediate": ["Was machst du gerne in deiner Freizeit?", "Was ist dein Lieblingshobby?", "Was isst du gerne zum Frühstück?"],
                "Advanced": ["Was ist der Unterschied zwischen 'beeinflussen' und 'Effekt'?", "Was ist die korrekte Verwendung von 'wer' und 'wen'?", "Was ist der Unterschied zwischen 'sein' und 'seine'?"]
            },
            "Italian": {
                "Beginner": ["Come ti chiami?", "Come stai?", "Qual è il tuo colore preferito?"],
                "Intermediate": ["Cosa ti piace fare nel tuo tempo libero?", "Qual è il tuo passatempo preferito?", "Cosa ti piace mangiare per colazione?"],
                "Advanced": ["Qual è la differenza tra 'influenzare' e 'effetto'?", "Qual è l'uso corretto di 'chi' e 'chi'?", "Qual è la differenza tra 'suo' e 'sua'?"]
            }
        }
        self.comprehension = {
            "English": {
                "Beginner": ["The sun is shining.", "The cat is sleeping.", "The dog is barking."],
                "Intermediate": ["The weather is nice today.", "I am going to the store.", "I am reading a book."],
                "Advanced": ["The impact of climate change is a pressing issue.", "The benefits of meditation are numerous.", "The history of the world is complex."]
            },
            "Spanish": {
                "Beginner": ["El sol brilla.", "El gato duerme.", "El perro ladra."],
                "Intermediate": ["El clima es agradable hoy.", "Voy a la tienda.", "Estoy leyendo un libro."],
                "Advanced": ["El impacto del cambio climático es un tema apremiante.", "Los beneficios de la meditación son numerosos.", "La historia del mundo es compleja."]
            },
            "French": {
                "Beginner": ["Le soleil brille.", "Le chat dort.", "Le chien aboie."],
                "Intermediate": ["Le temps est agréable aujourd'hui.", "Je vais au magasin.", "Je lis un livre."],
                "Advanced": ["L'impact du changement climatique est une question pressante.", "Les avantages de la méditation sont nombreux.", "L'histoire du monde est complexe."]
            },
            "German": {
                "Beginner": ["Die Sonne scheint.", "Die Katze schläft.", "Der Hund bellt."],
                "Intermediate": ["Das Wetter ist schön heute.", "Ich gehe zum Laden.", "Ich lese ein Buch."],
                "Advanced": ["Der Einfluss des Klimawandels ist ein dringendes Thema.", "Die Vorteile der Meditation sind zahlreich.", "Die Geschichte der Welt ist komplex."]
            },
            "Italian": {
                "Beginner": ["Il sole splende.", "Il gatto dorme.", "Il cane abbaia."],
                "Intermediate": ["Il clima è piacevole oggi.", "Vado al negozio.", "Sto leggendo un libro."],
                "Advanced": ["L'impatto del cambiamento climatico è un tema urgente.", "I benefici della meditazione sono numerosi.", "La storia del mondo è complessa."]
            }
        }
        self.progress = {}

    def select_language(self):
        print("Select a language:")
        for i, language in enumerate(self.languages):
            print(f"{i+1}. {language}")
        choice = input("Enter the number of your chosen language: ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.languages):
            return self.languages[int(choice) - 1]
        else:
            print("Invalid choice. Please try again.")
            return self.select_language()

    def select_difficulty(self):
        print("Select a difficulty level:")
        for i, difficulty in enumerate(self.difficulty_levels):
            print(f"{i+1}. {difficulty}")
        choice = input("Enter the number of your chosen difficulty level: ")
        if choice.isdigit() and 1 <= int(choice) <= len(self.difficulty_levels):
            return self.difficulty_levels[int(choice) - 1]
        else:
            print("Invalid choice. Please try again.")
            return self.select_difficulty()

    def vocabulary_exercise(self, language, difficulty):
        words = self.vocabulary[language][difficulty]
        score = 0
        for word in words:
            print(f"What is the meaning of '{word}'?")
            answer = input("Enter your answer: ")
            if answer.lower() == word.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{word}'.")
        print(f"Your score is {score}/{len(words)}")

    def grammar_exercise(self, language, difficulty):
        questions = self.grammar[language][difficulty]
        score = 0
        for question in questions:
            print(question)
            answer = input("Enter your answer: ")
            if answer.lower() == question.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{question}'.")
        print(f"Your score is {score}/{len(questions)}")

    def comprehension_exercise(self, language, difficulty):
        passages = self.comprehension[language][difficulty]
        score = 0
        for passage in passages:
            print(passage)
            answer = input("What is the main idea of this passage? ")
            if answer.lower() == passage.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{passage}'.")
        print(f"Your score is {score}/{len(passages)}")

    def track_progress(self, language, difficulty, score):
        if language not in self.progress:
            self.progress[language] = {}
        if difficulty not in self.progress[language]:
            self.progress[language][difficulty] = []
        self.progress[language][difficulty].append(score)

    def display_progress(self):
        for language, difficulties in self.progress.items():
            print(f"Progress in {language}:")
            for difficulty, scores in difficulties.items():
                print(f"{difficulty}: {sum(scores) / len(scores)}")

def main():
    enhancer = LanguageSkillEnhancer()
    language = enhancer.select_language()
    difficulty = enhancer.select_difficulty()
    print("Select an exercise:")
    print("1. Vocabulary")
    print("2. Grammar")
    print("3. Comprehension")
    choice = input("Enter the number of your chosen exercise: ")
    if choice == "1":
        enhancer.vocabulary_exercise(language, difficulty)
    elif choice == "2":
        enhancer.grammar_exercise(language, difficulty)
    elif choice == "3":
        enhancer.comprehension_exercise(language, difficulty)
    else:
        print("Invalid choice. Please try again.")
        return main()
    enhancer.track_progress(language, difficulty, 1)
    enhancer.display_progress()

if __name__ == "__main__":
    main()