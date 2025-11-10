import streamlit as st
import json
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Charger le fichier JSON
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Préparer les listes de patterns et réponses
patterns = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern.lower())
        responses.append(intent['responses'])

# Fonction de réponse
def repondre(message):
    message = message.lower()
    vect = CountVectorizer().fit_transform(patterns + [message])
    simil = cosine_similarity(vect[-1], vect[:-1])
    index = simil.argmax()
    if simil[0, index] < 0.2:
        return "Je ne suis pas sûr de comprendre 😅"
    else:
        return random.choice(responses[index])

# Interface Streamlit
st.title("🤖 SEXIA BY AWATEF")
st.write("Comment pourrai je vous ai aidez?")

# Stocker l'historique des messages
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Entrée utilisateur
user_input = st.text_input("🧑 Toi : ", "")

if user_input:
    if user_input.lower() in ["quit", "exit", "bye"]:
        st.write("🤖 Chatbot : À bientôt 👋")
    else:
        response = repondre(user_input)
        st.session_state['history'].append(("🧑 Toi :", user_input))
        st.session_state['history'].append(("🤖 Chatbot :", response))

# Afficher l'historique
for speaker, message in st.session_state['history']:
    st.write(f"{speaker} {message}")
