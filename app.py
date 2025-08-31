import streamlit as st
import openai
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="🌍 Eco-Simulator", layout="wide")

# --- TITLE ---
st.title("🌍 Eco-Simulator")
st.write("Diskutuj o socio-ekonomických otázkach, spúšťaj simulácie a vytváraj grafy.")

# --- MEMORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
st.sidebar.title("⚙️ Nastavenia")
st.sidebar.write("Tu môžeš pridať vlastné parametre.")
years = st.sidebar.slider("Počet rokov na simuláciu", 5, 100, 30)
growth = st.sidebar.slider("Ročný rast populácie (%)", 0.1, 5.0, 1.0) / 100

# --- CHAT HISTORY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- USER INPUT ---
if user_input := st.chat_input("Napíš svoju otázku..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Premýšľam... 🤔"):
            # OpenAI odpoveď
            try:
                client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                completion = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are an eco-socio-economic assistant."},
                        {"role": "user", "content": user_input},
                    ],
                )
                answer = completion.choices[0].message["content"]
            except Exception as e:
                answer = f"⚠️ Nepodarilo sa získať odpoveď: {e}"

            st.markdown(answer)

            # Simulácia (jednoduchá ukážka)
            population = 5_000_000
            pop = []
            for _ in range(years):
                population *= (1 + growth)
                pop.append(population)

            fig, ax = plt.subplots()
            ax.plot(range(years), pop, label="Populácia")
            ax.set_xlabel("Roky")
            ax.set_ylabel("Populácia")
            ax.legend()
            st.pyplot(fig)

    st.session_state.messages.append({"role": "assistant", "content": answer})
