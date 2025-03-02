# language_skill_enhancer.py

import random

class LanguageSkillEnhancer:
    def __init__(self):
        self.languages = ["English", "Spanish", "French", "German", "Italian"]
        self.difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        self.vocabulary = {
            "English": {
                "Beginner": ["apple", "banana", "cat", "dog", "elephant"],
                "Intermediate": ["accommodate", "acknowledge", "analyze", "anticipate", "assess"],
                "Advanced": ["abstruse", "acumen", "alacrity", "amalgamate", "anachronism"]
            },
            "Spanish": {
                "Beginner": ["manzana", "perro", "gato", "elefante", "casa"],
                "Intermediate": ["acceso", "análisis", "aplicación", "asistencia", "asunto"],
                "Advanced": ["abstruso", "acuidad", "alacridad", "amalgama", "anacronismo"]
            },
            "French": {
                "Beginner": ["pomme", "chien", "chat", "éléphant", "maison"],
                "Intermediate": ["accès", "analyse", "application", "assistance", "affaire"],
                "Advanced": ["abstrus", "acuité", "alacrité", "amalgame", "anachronisme"]
            },
            "German": {
                "Beginner": ["Apfel", "Hund", "Katze", "Elefant", "Haus"],
                "Intermediate": ["Zugang", "Analyse", "Anwendung", "Unterstützung", "Angelegenheit"],
                "Advanced": ["abstrus", "Scharfsinn", "Lebhaftigkeit", "Amalgam", "Anachronismus"]
            },
            "Italian": {
                "Beginner": ["mela", "cane", "gatto", "elefante", "casa"],
                "Intermediate": ["accesso", "analisi", "applicazione", "assistenza", "affare"],
                "Advanced": ["abstruso", "acutezza", "alacrità", "amalgama", "anacronismo"]
            }
        }
        self.grammar = {
            "English": {
                "Beginner": ["What is your name?", "How are you?", "What is your favorite color?"],
                "Intermediate": ["What do you like to do in your free time?", "What is your favorite hobby?", "What do you like to eat for breakfast?"],
                "Advanced": ["What is the difference between 'affect' and 'effect'?", "What is the correct usage of 'who' and 'whom'?", "What is the difference between 'its' and 'it's'?" ]
            },
            "Spanish": {
                "Beginner": ["¿Cómo te llamas?", "¿Cómo estás?", "¿Cuál es tu color favorito?"],
                "Intermediate": ["¿Qué te gusta hacer en tu tiempo libre?", "¿Cuál es tu pasatiempo favorito?", "¿Qué te gusta comer para desayunar?"],
                "Advanced": ["¿Cuál es la diferencia entre 'afectar' y 'efecto'?", "¿Cuál es el uso correcto de 'quién' y 'quién'?", "¿Cuál es la diferencia entre 'su' y 'su'?" ]
            },
            "French": {
                "Beginner": ["Comment t'appelles-tu?", "Comment vas-tu?", "Quel est ton couleur préférée?"],
                "Intermediate": ["Qu'est-ce que tu aimes faire dans ton temps libre?", "Quel est ton passe-temps préféré?", "Qu'est-ce que tu aimes manger pour déjeuner?"],
                "Advanced": ["Quelle est la différence entre 'affecter' et 'effet'?", "Quelle est l'utilisation correcte de 'qui' et 'qui'?", "Quelle est la différence entre 'son' et 'son'?" ]
            },
            "German": {
                "Beginner": ["Wie heißt du?", "Wie geht es dir?", "Was ist deine Lieblingsfarbe?"],
                "Intermediate": ["Was machst du gerne in deiner Freizeit?", "Was ist dein Lieblingshobby?", "Was isst du gerne zum Frühstück?"],
                "Advanced": ["Was ist der Unterschied zwischen 'beeinflussen' und 'Effekt'?", "Was ist die korrekte Verwendung von 'wer' und 'wen'?", "Was ist der Unterschied zwischen 'sein' und 'sein'?" ]
            },
            "Italian": {
                "Beginner": ["Come ti chiami?", "Come stai?", "Qual è il tuo colore preferito?"],
                "Intermediate": ["Cosa ti piace fare nel tuo tempo libero?", "Qual è il tuo hobby preferito?", "Cosa ti piace mangiare per colazione?"],
                "Advanced": ["Qual è la differenza tra 'influenzare' e 'effetto'?", "Qual è l'uso corretto di 'chi' e 'chi'?", "Qual è la differenza tra 'suo' e 'suo'?" ]
            }
        }
        self.comprehension = {
            "English": {
                "Beginner": ["The sun is shining.", "The cat is sleeping.", "The dog is barking."],
                "Intermediate": ["The weather is nice today.", "I am going to the store.", "I am reading a book."],
                "Advanced": ["The new policy has been implemented.", "The company is expanding its operations.", "The economy is growing rapidly."]
            },
            "Spanish": {
                "Beginner": ["El sol brilla.", "El gato duerme.", "El perro ladra."],
                "Intermediate": ["El clima es agradable hoy.", "Voy a la tienda.", "Estoy leyendo un libro."],
                "Advanced": ["La nueva política ha sido implementada.", "La empresa está expandiendo sus operaciones.", "La economía está creciendo rápidamente."]
            },
            "French": {
                "Beginner": ["Le soleil brille.", "Le chat dort.", "Le chien aboie."],
                "Intermediate": ["Le temps est agréable aujourd'hui.", "Je vais au magasin.", "Je lis un livre."],
                "Advanced": ["La nouvelle politique a été mise en œuvre.", "L'entreprise étend ses opérations.", "L'économie croît rapidement."]
            },
            "German": {
                "Beginner": ["Die Sonne scheint.", "Die Katze schläft.", "Der Hund bellt."],
                "Intermediate": ["Das Wetter ist schön heute.", "Ich gehe zum Laden.", "Ich lese ein Buch."],
                "Advanced": ["Die neue Politik wurde umgesetzt.", "Das Unternehmen erweitert seine Operationen.", "Die Wirtschaft wächst schnell."]
            },
            "Italian": {
                "Beginner": ["Il sole splende.", "Il gatto dorme.", "Il cane abbaia."],
                "Intermediate": ["Il clima è piacevole oggi.", "Vado al negozio.", "Sto leggendo un libro."],
                "Advanced": ["La nuova politica è stata implementata.", "L'azienda sta espandendo le sue operazioni.", "L'economia sta crescendo rapidamente."]
            }
        }

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
        print("Vocabulary Exercise:")
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
        print("Grammar Exercise:")
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
        print("Comprehension Exercise:")
        passages = self.comprehension[language][difficulty]
        score = 0
        for passage in passages:
            print(passage)
            answer = input("Enter a summary of the passage: ")
            if answer.lower() == passage.lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{passage}'.")
        print(f"Your score is {score}/{len(passages)}")

    def start_exercise(self):
        language = self.select_language()
        difficulty = self.select_difficulty()
        print(f"Welcome to the {language} {difficulty} exercise!")
        self.vocabulary_exercise(language, difficulty)
        self.grammar_exercise(language, difficulty)
        self.comprehension_exercise(language, difficulty)

def main():
    enhancer = LanguageSkillEnhancer()
    enhancer.start_exercise()

if __name__ == "__main__":
    main()