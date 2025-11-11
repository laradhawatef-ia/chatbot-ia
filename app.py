import streamlit as st
import json
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

# --- Charger le fichier JSON des intentions ---
with open("intents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# --- Préparer les listes de patterns et réponses ---
patterns = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern.lower())
        responses.append(intent['responses'])

# --- Fonction de similarité cosinus sans scipy ---
def cosine_similarity_manual(v1, v2):
    dot = np.dot(v1, v2.T)
    norm = np.linalg.norm(v1) * np.linalg.norm(v2)
    return dot / norm if norm != 0 else 0

# --- Fonction principale de réponse ---
def repondre(message):
    message = message.lower()
    vectorizer = CountVectorizer().fit(patterns + [message])
    vectors = vectorizer.transform(patterns + [message]).toarray()
    
    user_vec = vectors[-1]
    similarities = [cosine_similarity_manual(user_vec, v) for v in vectors[:-1]]

    best_index = np.argmax(similarities)
    best_score = similarities[best_index]

    if best_score < 0.2:
        return "Pouvez-vous m’en dire un peu plus pour que je comprenne mieux ?"
    else:
        return random.choice(responses[best_index])

# --- Interface Streamlit ---
st.title("💬 SEXIA BY AWATEF")
st.write("""
Bonjour, je suis une intelligence artificielle conçue pour vous écouter et vous aider à réfléchir à ce que vous ressentez.  
Tout ce que vous partagerez ici restera confidentiel dans le cadre de cette conversation.  
Comment vous sentez-vous aujourd’hui ?
""")

# --- Stocker l'historique des messages ---
if "history" not in st.session_state:
    st.session_state["history"] = []

# --- Entrée utilisateur ---
user_input = st.text_input("Vous :", "")

if user_input:
    if user_input.lower() in ["quit", "exit", "bye"]:
        st.write("**SEXIA :** Vous pouvez revenir me parler quand vous en aurez besoin. Je serai là pour poursuivre la discussion.")
    else:
        response = repondre(user_input)
        st.session_state["history"].append(("Vous :", user_input))
        st.session_state["history"].append(("SEXIA :", response))

# --- Afficher l'historique ---
for speaker, message in st.session_state["history"]:
    st.write(f"**{speaker}** {message}")

