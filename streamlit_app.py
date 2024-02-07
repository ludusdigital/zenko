import streamlit as st
from openai import OpenAI

# Postavljanje API ključa
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Funkcija za resetovanje poruka
def reset_messages():
  st.session_state["messages"] = []


if "messages" not in st.session_state:
  st.session_state["messages"] = []


# Funkcija za odabir vrste prompta i postavljanje u session_state
def update_prompt_type():
  prompt_type = st.radio(
      "Ko želite da odgovori na ovaj komentar?",
      ["❤️ Psiholog", "😂 Standup komičar", "😏 Sarkastični uličar"],
      on_change=reset_messages)
  prompt = ""
  if prompt_type == "❤️ Psiholog":
    prompt = """
        Ti si ekspert komunikologije i psiholog za medjuljudske odnose. Za odgovore koristi NLP metode koje su podržavajuće i ne stvaraju konflikt. Koristi najnovije saznanja iz komunikologije. Ukoliko je potrebno traži informaciju od korisnika da ti kaže širi kontekst zašto je neko ostavio neki negativni komentar. Trudi se da budeš opušten. Nemoj nikad da započinješ odgovor sa 'Dragi' ili 'draga', uvek budi direktan.  Jezik: odgovaraj na srpskom jeziku, koristeći gramatiku srpskog jezika. Na kraju svakog odgovora dodaj emotikon koji je u kontekstu odgovora.
        """
  elif prompt_type == "😂 Standup komičar":
    prompt = """
        Ti si standup komičar koji je rođen sa misijom da širi smeh i šale svuda gde ideš. Tvoj zadatak je da na svaki negativan komentar koji ti se pošalje odgovoriš sarkastično. Tvoj stil je isti kao kod Dave Chappelle. U odgovoru dodaj i dozu humora poput 'Roast mastera'. Budi sarkastičan i nemilosrdan u humoru. Trudi se da budeš originalan i da ne koristiš stereotipne šale. Zapamti, smeh je najbolji lek! Jezik: odgovaraj na srpskom jeziku, koristeći gramatiku srpskog jezika. Na kraju svakog odgovora dodaj emotikon koji je u kontekstu odgovora.
        """
  elif prompt_type == "😏 Sarkastični uličar":
    prompt = """
        Ti si sarkastični uličar koji živi po principu "ma brate, samo opušteno". Tvoj zadatak je da na svaki negativan komentar koji ti se pošalje odgovoriš sarkazmom i ironijom. Koristi ulični sleng i ironiju da iznenadiš i nasmeješ negativne hejtere. Budi sarkastičan bez milosti. Jezik: odgovaraj na srpskom jeziku, koristeći gramatiku srpskog jezika. Na kraju svakog odgovora dodaj emotikon koji je u kontekstu odgovora.
        """
  st.session_state["selected_prompt"] = prompt


# Postavljanje naslova i podnaslova
st.title("ZENKO®")
st.caption(
    "Anti-hejt AI chatbot za podržavajuće odgovore na hejt komentare sa društvenih mreža.✨"
)

# Ažuriranje prompta na osnovu odabira korisnika
update_prompt_type()

# Prikazivanje poruka
for msg in st.session_state["messages"]:
  st.write(f'{msg["role"]}: {msg["content"]}')

if prompt := st.chat_input("Unesite negativni komentar sa društvene mreže..."):
  # Ovde koristite izabrani prompt kao deo poruke koja se šalje
  st.session_state["messages"].append({"role": "user", "content": prompt})
  st.chat_message("user").write(prompt)

  with st.spinner("🤔 Uskoro stiže hladan tuš za hejtera..."):
    # Pre slanja, dodajte izabrani prompt kao prvu poruku
    messages_with_prompt = [{
        "role": "system",
        "content": st.session_state["selected_prompt"]
    }] + st.session_state["messages"]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages_with_prompt)  # ChatGPT model
    msg = response.choices[0].message.content

  st.session_state["messages"].append({"role": "assistant", "content": msg})
  st.chat_message("assistant").write(msg)
