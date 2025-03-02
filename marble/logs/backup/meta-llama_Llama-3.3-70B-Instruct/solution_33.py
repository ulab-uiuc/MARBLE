# solution.py
import random

class LanguageSkillEnhancer:
    """
    A comprehensive language learning application that provides users with a variety of interactive activities.
    """

    def __init__(self):
        # Initialize the language and difficulty level
        self.languages = ["English", "Spanish", "French", "German", "Italian"]
        self.difficulty_levels = ["Beginner", "Intermediate", "Advanced"]
        self.vocabulary = {
            "English": {
                "Beginner": ["apple", "banana", "cherry"],
                "Intermediate": ["accommodate", "acknowledge", "acquire"],
                "Advanced": ["abstruse", "acumen", "allegory"]
            },
            "Spanish": {
                "Beginner": ["manzana", "plátano", "cereza"],
                "Intermediate": ["acomodar", "reconocer", "adquirir"],
                "Advanced": ["abstruso", "perspicacia", "alegoría"]
            },
            "French": {
                "Beginner": ["pomme", "banane", "cerise"],
                "Intermediate": ["accueillir", "reconnaître", "acquérir"],
                "Advanced": ["abstrus", "perspicacité", "allégorie"]
            },
            "German": {
                "Beginner": ["Apfel", "Banane", "Kirsche"],
                "Intermediate": ["unterbringen", "anerkennen", "erwerben"],
                "Advanced": ["abstrus", "Scharfsinn", "Allegorie"]
            },
            "Italian": {
                "Beginner": ["mela", "banana", "ciliegia"],
                "Intermediate": ["alloggiare", "riconoscere", "acquisire"],
                "Advanced": ["abstruso", "perspicacia", "allegoria"]
            }
        }
        self.grammar = {
self.vocabulary_answers = {
"English": {
"Beginner": {"apple": "a type of fruit", "banana": "a type of fruit", "cherry": "a type of fruit"},
"Intermediate": {"accommodate": "to provide something needed or wanted", "acknowledge": "to recognize or admit something", "acquire": "to get or obtain something"},
"Advanced": {"abstruse": "difficult to understand", "acumen": "the ability to make good judgments", "allegory": "a story or picture that can be interpreted to reveal a hidden meaning"}
},
"Spanish": {
"Beginner": {"manzana": "a type of fruit", "plátano": "a type of fruit", "cereza": "a type of fruit"},
"Intermediate": {"acomodar": "to provide something needed or wanted", "reconocer": "to recognize or admit something", "adquirir": "to get or obtain something"},
"Advanced": {"abstruso": "difficult to understand", "perspicacia": "the ability to make good judgments", "alegoría": "a story or picture that can be interpreted to reveal a hidden meaning"}
},
"French": {
"Beginner": {"pomme": "a type of fruit", "banane": "a type of fruit", "cerise": "a type of fruit"},
"Intermediate": {"accueillir": "to provide something needed or wanted", "reconnaître": "to recognize or admit something", "acquérir": "to get or obtain something"},
"Advanced": {"abstrus": "difficult to understand", "perspicacité": "the ability to make good judgments", "allégorie": "a story or picture that can be interpreted to reveal a hidden meaning"}
},
"German": {
"Beginner": {"Apfel": "a type of fruit", "Banane": "a type of fruit", "Kirsche": "a type of fruit"},
"Intermediate": {"unterbringen": "to provide something needed or wanted", "anerkennen": "to recognize or admit something", "erwerben": "to get or obtain something"},
"Advanced": {"abstrus": "difficult to understand", "Scharfsinn": "the ability to make good judgments", "Allegorie": "a story or picture that can be interpreted to reveal a hidden meaning"}
},
"Italian": {
"Beginner": {"mela": "a type of fruit", "banana": "a type of fruit", "ciliegia": "a type of fruit"},
"Intermediate": {"alloggiare": "to provide something needed or wanted", "riconoscere": "to recognize or admit something", "acquisire": "to get or obtain something"},
"Advanced": {"abstruso": "difficult to understand", "perspicacia": "the ability to make good judgments", "allegoria": "a story or picture that can be interpreted to reveal a hidden meaning"}
}
}

            "English": {
                "Beginner": ["What is your name?", "How old are you?", "Where are you from?"],
                "Intermediate": ["What do you like to do?", "What is your favorite food?", "What do you like to watch?"],
                "Advanced": ["What is the difference between...", "How do you think...", "What do you believe..."]
            },
            "Spanish": {
                "Beginner": ["¿Cómo te llamas?", "¿Cuántos años tienes?", "¿De dónde eres?"],
                "Intermediate": ["¿Qué te gusta hacer?", "¿Cuál es tu comida favorita?", "¿Qué te gusta ver?"],
                "Advanced": ["¿Cuál es la diferencia entre...", "¿Cómo crees que...", "¿Qué crees que..."]
            },
            "French": {
                "Beginner": ["Comment t'appelles-tu?", "Quel âge as-tu?", "D'où viens-tu?"],
                "Intermediate": ["Qu'est-ce que tu aimes faire?", "Quel est ton plat préféré?", "Qu'est-ce que tu aimes regarder?"],
                "Advanced": ["Quelle est la différence entre...", "Comment penses-tu que...", "Qu'est-ce que tu penses que..."]
            },
            "German": {
                "Beginner": ["Wie heißt du?", "Wie alt bist du?", "Woher kommst du?"],
                "Intermediate": ["Was gefällt dir?", "Was ist dein Lieblingsessen?", "Was gefällt dir ansehen?"],
                "Advanced": ["Was ist der Unterschied zwischen...", "Wie denkst du, dass...", "Was denkst du, dass..."]
            },
            "Italian": {
                "Beginner": ["Come ti chiami?", "Quanti anni hai?", "Di dove sei?"],
                "Intermediate": ["Cosa ti piace fare?", "Qual è il tuo cibo preferito?", "Cosa ti piace guardare?"],
                "Advanced": ["Qual è la differenza tra...", "Come pensi che...", "Cosa pensi che..."]
            }
        }
        self.comprehension = {
self.grammar_answers = {
"English": {
"Beginner": {"What is your name?": "My name is", "How old are you?": "I am", "Where are you from?": "I am from"},
"Intermediate": {"What do you like to do?": "I like to", "What is your favorite food?": "My favorite food is", "What do you like to watch?": "I like to watch"},
"Advanced": {"What is the difference between...": "The difference between", "How do you think...": "I think", "What do you believe...": "I believe"}
},
"Spanish": {
"Beginner": {"¿Cómo te llamas?": "Me llamo", "¿Cuántos años tienes?": "Tengo", "¿De dónde eres?": "Soy de"},
"Intermediate": {"¿Qué te gusta hacer?": "Me gusta", "¿Cuál es tu comida favorita?": "Mi comida favorita es", "¿Qué te gusta ver?": "Me gusta ver"},
"Advanced": {"¿Cuál es la diferencia entre...": "La diferencia entre", "¿Cómo crees que...": "Creo que", "¿Qué crees que...": "Creo que"}
},
"French": {
"Beginner": {"Comment t'appelles-tu?": "Je m'appelle", "Quel âge as-tu?": "J'ai", "D'où viens-tu?": "Je suis de"},
"Intermediate": {"Qu'est-ce que tu aimes faire?": "J'aime", "Quel est ton plat préféré?": "Mon plat préféré est", "Qu'est-ce que tu aimes regarder?": "J'aime regarder"},
"Advanced": {"Quelle est la différence entre...": "La différence entre", "Comment penses-tu que...": "Je pense que", "Qu'est-ce que tu penses que...": "Je pense que"}
},
"German": {
"Beginner": {"Wie heißt du?": "Ich heiße", "Wie alt bist du?": "Ich bin", "Woher kommst du?": "Ich komme aus"},
"Intermediate": {"Was gefällt dir?": "Mir gefällt", "Was ist dein Lieblingsessen?": "Mein Lieblingsessen ist", "Was gefällt dir ansehen?": "Mir gefällt ansehen"},
"Advanced": {"Was ist der Unterschied zwischen...": "Der Unterschied zwischen", "Wie denkst du, dass...": "Ich denke, dass", "Was denkst du, dass...": "Ich denke, dass"}
},
"Italian": {
"Beginner": {"Come ti chiami?": "Mi chiamo", "Quanti anni hai?": "Ho", "Di dove sei?": "Sono di"},
"Intermediate": {"Cosa ti piace fare?": "Mi piace", "Qual è il tuo cibo preferito?": "Il mio cibo preferito è", "Cosa ti piace guardare?": "Mi piace guardare"},
"Advanced": {"Qual è la differenza tra...": "La differenza tra", "Come pensi che...": "Penso che", "Cosa pensi che...": "Penso che"}
}
}

            "English": {
                "Beginner": ["The sun is shining.", "The cat is sleeping.", "The dog is barking."],
                "Intermediate": ["The weather is nice today.", "I like to read books.", "The movie was very interesting."],
                "Advanced": ["The concept of time is relative.", "The importance of education cannot be overstated.", "The impact of social media on society is significant."]
            },
            "Spanish": {
                "Beginner": ["El sol brilla.", "El gato duerme.", "El perro ladra."],
                "Intermediate": ["El clima es agradable hoy.", "Me gusta leer libros.", "La película fue muy interesante."],
                "Advanced": ["El concepto de tiempo es relativo.", "La importancia de la educación no puede ser exagerada.", "El impacto de las redes sociales en la sociedad es significativo."]
            },
            "French": {
                "Beginner": ["Le soleil brille.", "Le chat dort.", "Le chien aboie."],
                "Intermediate": ["Le temps est agréable aujourd'hui.", "J'aime lire des livres.", "Le film était très intéressant."],
                "Advanced": ["Le concept de temps est relatif.", "L'importance de l'éducation ne peut être exagérée.", "L'impact des réseaux sociaux sur la société est significatif."]
            },
            "German": {
                "Beginner": ["Die Sonne scheint.", "Die Katze schläft.", "Der Hund bellt."],
                "Intermediate": ["Das Wetter ist heute schön.", "Ich mag Bücher lesen.", "Der Film war sehr interessant."],
                "Advanced": ["Das Konzept der Zeit ist relativ.", "Die Bedeutung der Bildung kann nicht übertrieben werden.", "Die Auswirkungen der sozialen Medien auf die Gesellschaft sind signifikant."]
            },
            "Italian": {
                "Beginner": ["Il sole splende.", "Il gatto dorme.", "Il cane abbaia."],
                "Intermediate": ["Il tempo è bello oggi.", "Mi piace leggere libri.", "Il film è stato molto interessante."],
                "Advanced": ["Il concetto di tempo è relativo.", "L'importanza dell'istruzione non può essere esagerata.", "L'impatto dei social media sulla società è significativo."]
            }
        }
        self.progress = {}
self.comprehension_answers = {
"English": {
"Beginner": {"The sun is shining.": "The sun is shining", "The cat is sleeping.": "The cat is sleeping", "The dog is barking.": "The dog is barking"},
"Intermediate": {"The weather is nice today.": "The weather is nice", "I like to read books.": "I like to read", "The movie was very interesting.": "The movie was interesting"},
"Advanced": {"The concept of time is relative.": "Time is relative", "The importance of education cannot be overstated.": "Education is important", "The impact of social media on society is significant.": "Social media has an impact"}
},
"Spanish": {
"Beginner": {"El sol brilla.": "El sol brilla", "El gato duerme.": "El gato duerme", "El perro ladra.": "El perro ladra"},
"Intermediate": {"El clima es agradable hoy.": "El clima es agradable", "Me gusta leer libros.": "Me gusta leer", "La película fue muy interesante.": "La película fue interesante"},
"Advanced": {"El concepto de tiempo es relativo.": "El tiempo es relativo", "La importancia de la educación no puede ser exagerada.": "La educación es importante", "El impacto de las redes sociales en la sociedad es significativo.": "Las redes sociales tienen un impacto"}
},
"French": {
"Beginner": {"Le soleil brille.": "Le soleil brille", "Le chat dort.": "Le chat dort", "Le chien aboie.": "Le chien aboie"},
"Intermediate": {"Le temps est agréable aujourd'hui.": "Le temps est agréable", "J'aime lire des livres.": "J'aime lire", "Le film était très intéressant.": "Le film était intéressant"},
"Advanced": {"Le concept de temps est relatif.": "Le temps est relatif", "L'importance de l'éducation ne peut être exagérée.": "L'éducation est importante", "L'impact des réseaux sociaux sur la société est significatif.": "Les réseaux sociaux ont un impact"}
},
"German": {
"Beginner": {"Die Sonne scheint.": "Die Sonne scheint", "Die Katze schläft.": "Die Katze schläft", "Der Hund bellt.": "Der Hund bellt"},
"Intermediate": {"Das Wetter ist heute schön.": "Das Wetter ist schön", "Ich mag Bücher lesen.": "Ich mag lesen", "Der Film war sehr interessant.": "Der Film war interessant"},
"Advanced": {"Das Konzept der Zeit ist relativ.": "Die Zeit ist relativ", "Die Bedeutung der Bildung kann nicht übertrieben werden.": "Die Bildung ist wichtig", "Die Auswirkungen der sozialen Medien auf die Gesellschaft sind signifikant.": "Die sozialen Medien haben eine Auswirkung"}
},
"Italian": {
"Beginner": {"Il sole splende.": "Il sole splende", "Il gatto dorme.": "Il gatto dorme", "Il cane abbaia.": "Il cane abbaia"},
"Intermediate": {"Il tempo è bello oggi.": "Il tempo è bello", "Mi piace leggere libri.": "Mi piace leggere", "Il film è stato molto interessante.": "Il film è stato interessante"},
"Advanced": {"Il concetto di tempo è relativo.": "Il tempo è relativo", "L'importanza dell'istruzione non può essere esagerata.": "L'istruzione è importante", "L'impatto dei social media sulla società è significativo.": "I social media hanno un impatto"}
}
}


    def select_language(self):
        # Select the target language
        print("Select your target language:")
        for i, language in enumerate(self.languages):
            print(f"{i+1}. {language}")
        language_choice = int(input("Enter the number of your chosen language: "))
        return self.languages[language_choice - 1]

    def select_difficulty(self):
        # Select the difficulty level
        print("Select your difficulty level:")
        for i, difficulty in enumerate(self.difficulty_levels):
            print(f"{i+1}. {difficulty}")
        difficulty_choice = int(input("Enter the number of your chosen difficulty level: "))
        return self.difficulty_levels[difficulty_choice - 1]

    def vocabulary_exercise(self, language, difficulty):
        # Vocabulary exercise
        print("Vocabulary Exercise:")
        words = self.vocabulary[language][difficulty]
        random_word = random.choice(words)
        print(f"What is the meaning of '{random_word}'?")if answer.lower() in self.vocabulary_answers[language][difficulty][random_word].lower():print("Correct!")
        else:
            print(f"Sorry, the correct answer is '{random_word}'.")

    def grammar_exercise(self, language, difficulty):
        # Grammar exercise
        print("Grammar Exercise:")
        questions = self.grammar[language][difficulty]
        random_question = random.choice(questions)
        print(f"{random_question}")if answer.lower() in self.grammar_answers[language][difficulty][random_question].lower():print("Correct!")
        else:
            print(f"Sorry, the correct answer is '{random_question}'.")

    def comprehension_exercise(self, language, difficulty):
        # Comprehension exercise
        print("Comprehension Exercise:")
        passages = self.comprehension[language][difficulty]
        random_passage = random.choice(passages)
        print(f"Read the following passage: {random_passage}")if answer.lower() in self.comprehension_answers[language][difficulty][random_passage].lower():print("Correct!")
        else:
            print(f"Sorry, the correct answer is '{random_passage}'.")

    def track_progress(self, language, difficulty, exercise, score):
        # Track the user's progress
        if language not in self.progress:
            self.progress[language] = {}
        if difficulty not in self.progress[language]:
            self.progress[language][difficulty] = {}
        if exercise not in self.progress[language][difficulty]:
            self.progress[language][difficulty][exercise] = []
        self.progress[language][difficulty][exercise].append(score)

    def display_progress(self):
        # Display the user's progress
        print("Your Progress:")
        for language, difficulties in self.progress.items():
            print(f"Language: {language}")
            for difficulty, exercises in difficulties.items():
                print(f"Difficulty: {difficulty}")
                for exercise, scores in exercises.items():
                    print(f"Exercise: {exercise}")
                    print(f"Scores: {scores}")

def main():
    # Main function
    enhancer = LanguageSkillEnhancer()
    language = enhancer.select_language()
    difficulty = enhancer.select_difficulty()
    while True:
        print("Select an exercise:")
        print("1. Vocabulary Exercise")
        print("2. Grammar Exercise")
        print("3. Comprehension Exercise")
        print("4. Display Progress")
        print("5. Quit")
        choice = int(input("Enter the number of your chosen exercise: "))
        if choice == 1:
            enhancer.vocabulary_exercise(language, difficulty)score = 1 if answer.lower() in self.vocabulary_answers[language][difficulty][random_word].lower() else 0
enhancer.track_progress(language, difficulty, "Vocabulary", score)elif choice == 2:
            enhancer.grammar_exercise(language, difficulty)score = 1 if answer.lower() in self.grammar_answers[language][difficulty][random_question].lower() else 0
enhancer.track_progress(language, difficulty, "Grammar", score)elif choice == 3:
            enhancer.comprehension_exercise(language, difficulty)score = 1 if answer.lower() in self.comprehension_answers[language][difficulty][random_passage].lower() else 0
enhancer.track_progress(language, difficulty, "Comprehension", score)elif choice == 4:
            enhancer.display_progress()
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()