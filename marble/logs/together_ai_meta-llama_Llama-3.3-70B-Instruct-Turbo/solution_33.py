```python
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
        self.user_language = None
        self.user_difficulty = None
        self.user_progress = {"vocabulary": 0, "grammar": 0, "comprehension": 0}

    def select_language(self):
        # Allow the user to select their target language
        print("Select your target language:")
        for i, language in enumerate(self.languages):
            print(f"{i+1}. {language}")
        while True:
            choice = input("Enter the number of your chosen language: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.languages):
                self.user_language = self.languages[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")

    def select_difficulty(self):
        # Allow the user to select their difficulty level
        print("Select your difficulty level:")
        for i, difficulty in enumerate(self.difficulty_levels):
            print(f"{i+1}. {difficulty}")
        while True:
            choice = input("Enter the number of your chosen difficulty level: ")
            if choice.isdigit() and 1 <= int(choice) <= len(self.difficulty_levels):
                self.user_difficulty = self.difficulty_levels[int(choice) - 1]
                break
            else:
                print("Invalid choice. Please try again.")

    def vocabulary_module(self):
        # Vocabulary module with flashcards, multiple-choice questions, and fill-in-the-blank exercisesdef vocabulary_module(self):
    # Vocabulary module with flashcards, multiple-choice questions, and fill-in-the-blank exercises
    print("Vocabulary Module")
    vocabulary_exercises = {
        "flashcards": self.vocabulary_flashcards,
        "multiple-choice": self.vocabulary_multiple_choice,
        "fill-in-the-blank": self.vocabulary_fill_in_the_blank
    }
    while True:
        print("Select an exercise:")
        for i, exercise in enumerate(vocabulary_exercises.keys()):
            print(f"{i+1}. {exercise}")
        choice = input("Enter the number of your chosen exercise: ")
        if choice.lower() == 'quit' or (choice.isdigit() and 1 <= int(choice) <= len(vocabulary_exercises)):
            if choice.lower() == 'quit':
                print("Exercise quit. Returning to main menu.")
                break
            else:
                exercise = list(vocabulary_exercises.keys())[int(choice) - 1]
                vocabulary_exercises[exercise]()()
        else:
            print("Invalid choice. Please try again.")print("Vocabulary Module")
        vocabulary_exercises = {
            "flashcards": self.vocabulary_flashcards,
            "multiple-choice": self.vocabulary_multiple_choice,
            "fill-in-the-blank": self.vocabulary_fill_in_the_blank
        }
        while True:
            print("Select an exercise:")
            for i, exercise in enumerate(vocabulary_exercises.keys()):
                print(f"{i+1}. {exercise}")
            choice = input("Enter the number of your chosen exercise: ")if choice.lower() == 'quit' or (choice.isdigit() and 1 <= int(choice) <= len(vocabulary_exercises)):                exercise = list(vocabulary_exercises.keys())[int(choice) - 1]
                vocabulary_exercises[exercise]()
            print("Exercise quit. Returning to main menu.")
            break
                break
            else:
                print("Invalid choice. Please try again.")

    def vocabulary_flashcards(self):
        # Flashcards exercise
        print("Flashcards Exercise")
        vocabulary = {
            "English": {"hello": "hello", "goodbye": "goodbye"},
            "Spanish": {"hola": "hello", "adiós": "goodbye"},
            "French": {"bonjour": "hello", "au revoir": "goodbye"},
            "German": {"hallo": "hello", "auf wiedersehen": "goodbye"},
            "Italian": {"ciao": "hello", "arrivederci": "goodbye"}
        }
        words = list(vocabulary[self.user_language].keys())
            random.shuffle(words)
            score = 0
            for word in words:
                answer = input(f"What is the translation of '{word}' in {self.user_language}? ")
                if answer.lower() == vocabulary[self.user_language][word].lower():
                    print("Correct!")
                    score += 1
                else:
                    print(f"Sorry, the correct answer is '{vocabulary[self.user_language][word]}'")
            self.user_progress["vocabulary"] = score / len(words)
            print(f"Your score is {score / len(words) * 100}%")
        random.shuffle(words)
        score = 0
        for word in words:self.user_progress["vocabulary"] = score / len(words)print(f"Your score is {score / len(words) * 100}%")

    def grammar_module(self):
        # Grammar module with quizzes covering various aspects of grammar
        print("Grammar Module")
        grammar_exercises = {
            "verb tenses": self.grammar_verb_tenses,
            "sentence structure": self.grammar_sentence_structure,
            "parts of speech": self.grammar_parts_of_speech
        }
        while True:
            print("Select an exercise:")
            for i, exercise in enumerate(grammar_exercises.keys()):
                print(f"{i+1}. {exercise}")
            choice = input("Enter the number of your chosen exercise: ")
            if choice.isdigit() and 1 <= int(choice) <= len(grammar_exercises):
                exercise = list(grammar_exercises.keys())[int(choice) - 1]
                grammar_exercises[exercise]()
                break
            else:
                print("Invalid choice. Please try again.")

    def grammar_verb_tenses(self):
        # Verb tenses exercise
        print("Verb Tenses Exercise")
        verb_tenses = {
            "English": {"present": "I go to the store.", "past": "I went to the store.", "future": "I will go to the store."},
            "Spanish": {"present": "Voy a la tienda.", "past": "Fui a la tienda.", "future": "Iré a la tienda."},
            "French": {"present": "Je vais au magasin.", "past": "Je suis allé au magasin.", "future": "J'irai au magasin."},
            "German": {"present": "Ich gehe zum Laden.", "past": "Ich ging zum Laden.", "future": "Ich werde zum Laden gehen."},
            "Italian": {"present": "Vado al negozio.", "past": "Sono andato al negozio.", "future": "Andrò al negozio."}
        }
        tenses = list(verb_tenses[self.user_language].keys())
        random.shuffle(tenses)
        score = 0
        for tense in tenses:
            answer = input(f"What is the {tense} tense of the verb 'to go' in {self.user_language}? ")
            if answer.lower() == verb_tenses[self.user_language][tense].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{verb_tenses[self.user_language][tense]}'")
        self.user_progress["grammar"] = score / len(tenses)
        print(f"Your score is {score / len(tenses) * 100}%")

    def grammar_sentence_structure(self):
        # Sentence structure exercise
        print("Sentence Structure Exercise")
        sentence_structures = {
            "English": {"simple": "I like ice cream.", "compound": "I like ice cream, and my friend likes cake.", "complex": "I like ice cream because it is delicious."},
            "Spanish": {"simple": "Me gusta el helado.", "compound": "Me gusta el helado, y a mi amigo le gusta el pastel.", "complex": "Me gusta el helado porque es delicioso."},
            "French": {"simple": "J'aime la glace.", "compound": "J'aime la glace, et mon ami aime le gâteau.", "complex": "J'aime la glace parce qu'elle est délicieuse."},
            "German": {"simple": "Ich mag Eis.", "compound": "Ich mag Eis, und mein Freund mag Kuchen.", "complex": "Ich mag Eis, weil es lecker ist."},
            "Italian": {"simple": "Mi piace il gelato.", "compound": "Mi piace il gelato, e il mio amico piace la torta.", "complex": "Mi piace il gelato perché è delizioso."}
        }
        structures = list(sentence_structures[self.user_language].keys())
        random.shuffle(structures)
        score = 0
        for structure in structures:
            answer = input(f"What is an example of a {structure} sentence in {self.user_language}? ")
            if answer.lower() == sentence_structures[self.user_language][structure].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{sentence_structures[self.user_language][structure]}'")
        self.user_progress["grammar"] = score / len(structures)
        print(f"Your score is {score / len(structures) * 100}%")

    def grammar_parts_of_speech(self):
        # Parts of speech exercise
        print("Parts of Speech Exercise")
        parts_of_speech = {
            "English": {"noun": "dog", "verb": "run", "adjective": "happy", "adverb": "quickly"},
            "Spanish": {"noun": "perro", "verb": "correr", "adjective": "feliz", "adverb": "rápidamente"},
            "French": {"noun": "chien", "verb": "courir", "adjective": "heureux", "adverb": "rapidement"},
            "German": {"noun": "Hund", "verb": "laufen", "adjective": "glücklich", "adverb": "schnell"},
            "Italian": {"noun": "cane", "adjective": "felice", "verb": "correre", "adverb": "rapidamente"}
        }
        parts = list(parts_of_speech[self.user_language].keys())
        random.shuffle(parts)
        score = 0
        for part in parts:
            answer = input(f"What is an example of a {part} in {self.user_language}? ")
            if answer.lower() == parts_of_speech[self.user_language][part].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{parts_of_speech[self.user_language][part]}'")
        self.user_progress["grammar"] = score / len(parts)
        print(f"Your score is {score / len(parts) * 100}%")

    def comprehension_module(self):
        # Comprehension module with reading passages and questions
        print("Comprehension Module")
        comprehension_exercises = {
            "short passage": self.comprehension_short_passage,
            "long passage": self.comprehension_long_passage
        }
        while True:
            print("Select an exercise:")
            for i, exercise in enumerate(comprehension_exercises.keys()):
                print(f"{i+1}. {exercise}")
            choice = input("Enter the number of your chosen exercise: ")
            if choice.isdigit() and 1 <= int(choice) <= len(comprehension_exercises):
                exercise = list(comprehension_exercises.keys())[int(choice) - 1]
                comprehension_exercises[exercise]()
                break
            else:
                print("Invalid choice. Please try again.")

    def comprehension_short_passage(self):
        # Short passage exercise
        print("Short Passage Exercise")
        passages = {
            "English": "The sun is shining. The birds are singing. It is a beautiful day.",
            "Spanish": "El sol brilla. Los pájaros cantan. Es un día hermoso.",
            "French": "Le soleil brille. Les oiseaux chantent. C'est un jour magnifique.",
            "German": "Die Sonne scheint. Die Vögel singen. Es ist ein schöner Tag.",
            "Italian": "Il sole splende. Gli uccelli cantano. È una bella giornata."
        }
        print(passages[self.user_language])
        questions = {
            "English": ["What is the weather like?", "What are the birds doing?"],
            "Spanish": ["¿Qué tiempo hace?", "¿Qué están haciendo los pájaros?"],
            "French": ["Quel temps fait-il?", "Que font les oiseaux?"],
            "German": ["Wie ist das Wetter?", "Was machen die Vögel?"],
            "Italian": ["Che tempo fa?", "Cosa stanno facendo gli uccelli?"]
        }
        answers = {
            "English": ["The sun is shining.", "The birds are singing."],
            "Spanish": ["El sol brilla.", "Los pájaros cantan."],
            "French": ["Le soleil brille.", "Les oiseaux chantent."],
            "German": ["Die Sonne scheint.", "Die Vögel singen."],
            "Italian": ["Il sole splende.", "Gli uccelli cantano."]
        }
        score = 0
        for i, question in enumerate(questions[self.user_language]):
            answer = input(question + " ")
            if answer.lower() == answers[self.user_language][i].lower():
                print("Correct!")
                score += 1
            else:
                print(f"Sorry, the correct answer is '{answers[self.user_language][i]}'")
        self.user_progress["comprehension"] = score / len(questions[self.user_language])
        print(f"Your score is {score / len(questions[self.user_language]) * 100}%")

    def comprehension_long_passage(self):
        # Long passage exercise
        print("Long Passage Exercise")
        passages = {
            "English": "The sun is shining. The birds are singing. It is a beautiful day. The flowers are blooming, and the trees are swaying in the breeze. The children are playing outside, laughing and having fun.",
            "Spanish": "El sol brilla. Los pájaros cantan. Es un día hermoso. Las flores están floreciendo, y los árboles se balancean en la brisa. Los niños están jugando afuera, riendo y divirtiéndose.",
            "French": "Le soleil brille. Les oiseaux chantent. C'est un jour magnifique. Les fleurs sont en fleur, et les arbres se balancent dans la brise. Les enfants sont en train de jouer dehors, en riant et en s'amusant.",
            "German": "Die Sonne scheint. Die Vögel singen. Es ist ein schöner Tag. Die Blumen blühen, und die Bäume schwingen im Wind. Die Kinder spielen draußen, lachen und haben Spaß.",
            "Italian": "Il sole splende. Gli uccelli cantano. È una bella giornata. I fiori stanno fiorendo, e gli alberi si muovono nella brezza. I bambini stanno giocando fuori, ridendo e divertendosi."
        }
        print(passages[self.user_language])
        questions = {
            "English": ["What is the weather like?", "What are the birds doing?", "What are the children doing?"],
            "Spanish": ["¿Qué tiempo hace?", "¿Qué están haciendo los pájaros?", "¿Qué están haciendo los niños?"],
            "French": ["Quel temps fait-il?", "Que font les oiseaux?", "Que font les enfants?"],
            "German": ["Wie ist das Wetter?", "Was machen die Vögel?", "Was machen die Kinder?"],
            "Italian": ["Che tempo fa?", "Cosa stanno facendo gli uccelli?", "Cosa stanno facendo i bambini?"]
        }
        answers = {
            "English": ["The sun is shining.", "The birds are singing.", "The children are playing outside."],
            "Spanish": ["El sol brilla.", "Los pájaros cantan.", "Los niños están jugando afuera."],
            "French": ["Le soleil brille.", "Les oiseaux chantent.", "Les enfants sont en train de jouer dehors."],
            "German": ["Die Sonne scheint.", "Die Vögel singen.", "Die Kinder spielen draußen."],
            "Italian": ["Il sole splende.", "Gli