import os
import subprocess
import sys

# Corrige sklearn manquant sur Streamlit Cloud
try:
    import sklearn
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn==1.3.2"])
    import sklearn

# Désactive les warnings watchdog
os.environ["STREAMLIT_WATCHDOG_WARNING"] = "false"

import streamlit as st
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
   
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
        return "Pouvez-vous m’en dire un peu plus pour que je comprenne mieux ?"
    else:
        return random.choice(responses[index])

# Interface Streamlit
st.title("SEXIA BY AWATEF")
st.write("Bonjour, je suis une intelligence artificielle conçue pour vous écouter et vous aider à réfléchir à ce que vous ressentez. Tout ce que vous partagerez ici restera confidentiel dans le cadre de cette conversation. Comment vous sentez-vous aujourd’hui ? ")


# Stocker l'historique des messages
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Entrée utilisateur
user_input = st.text_input("Vous : ", "")

if user_input:
    if user_input.lower() in ["quit", "exit", "bye"]:
        st.write("SEXIA : Vous pouvez revenir me parler quand vous en aurez besoin. Je serai là pour poursuivre la discussion.")
    else:
        response = repondre(user_input)
        st.session_state['history'].append(("Vous :", user_input))
        st.session_state['history'].append(("SEXIA :", response))

# Afficher l'historique
for speaker, message in st.session_state['history']:
    st.write(f"{speaker} {message}")
