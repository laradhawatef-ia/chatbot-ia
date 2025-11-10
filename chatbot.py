import random
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Téléchargement du tokenizer NLTK
nltk.download('punkt')

# Liste d'exemples d'échanges
questions = [
    "bonjour", "salut", "coucou",
    "comment ça va", "ça va",
    "merci", "au revoir", "bye"
]

reponses = [
    "Bonjour à toi ! 😊",
    "Salut ! Comment vas-tu ?",
    "Coucou ! Ravi de te parler.",
    "Je vais très bien, merci ! Et toi ?",
    "Je suis content que tu ailles bien !",
    "Avec plaisir 💫",
    "Au revoir, à bientôt 👋",
    "Bye ! Passe une excellente journée ☀️"
]

def repondre(message):
    message = message.lower()
    vect = CountVectorizer().fit_transform(questions + [message])
    simil = cosine_similarity(vect[-1], vect[:-1])
    index = simil.argmax()

    if simil[0, index] < 0.2:
        return "Je ne suis pas sûr de comprendre 😅"
    else:
        return reponses[index]

# Boucle de chat
print("🤖 Chatbot : Salut ! Pose-moi une question (ou tape 'quit' pour arrêter).")
while True:
    user_input = input("🧑 Toi : ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("🤖 Chatbot : À bientôt 👋")
        break
    print("🤖 Chatbot :", repondre(user_input))
  import json
import random
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Téléchargements nécessaires
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Charger le fichier JSON
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Préparer les listes de patterns et réponses
patterns = []
responses = []
tags = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern.lower())
        responses.append(intent['responses'])
        tags.append(intent['tag'])

# Fonction pour répondre
def repondre(message):
    message = message.lower()
    vect = CountVectorizer().fit_transform(patterns + [message])
    simil = cosine_similarity(vect[-1], vect[:-1])
    index = simil.argmax()
    
    if simil[0, index] < 0.2:
        return "Je ne suis pas sûr de comprendre 😅"
    else:
        return random.choice(responses[index])

# Boucle de chat
print("🤖 Chatbot : Salut ! Pose-moi une question (ou tape 'quit' pour arrêter).")
while True:
    user_input = input("🧑 Toi : ")
    if user_input.lower() in ["quit", "exit", "bye"]:
        print("🤖 Chatbot : À bientôt 👋")
        break
    print("🤖 Chatbot :", repondre(user_input))
  
