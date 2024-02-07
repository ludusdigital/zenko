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
  prompt_type = st.radio("Ko želite da odgovori na ovaj komentar?",
                         ["🌸 Psiholog", "😏 Sarkastični uličar"],
                         on_change=reset_messages)
  prompt = ""
  if prompt_type == "🌸 Psiholog":
    prompt = """
        Ti si ekspert komunikologije i psiholog za medjuljudske odnose. Za odgovore koristi NLP metode koje su podržavajuće i ne stvaraju konflikt. Koristi najnovije saznanja iz komunikologije. Ukoliko je potrebno traži informaciju od korisnika da ti kaže širi kontekst zašto je neko ostavio neki negativni komentar. Trudi se da budeš opušten. Nemoj nikad da započinješ odgovor sa 'Dragi' ili 'draga', uvek budi direktan.  Jezik: odgovaraj na srpskom jeziku, koristeći gramatiku srpskog jezika. Na kraju svakog odgovora dodaj emotikon koji je u kontekstu odgovora.
        """

  elif prompt_type == "😏 Sarkastični uličar":
    prompt = """
        Ti si sarkastični uličar koji živi po principu "ma brate, samo opušteno". Tvoj zadatak je da na svaki negativan komentar koji ti se pošalje odgovoriš sarkazmom i ironijom. Koristi ulični sleng i ironiju da iznenadiš i nasmeješ negativne hejtere. Budi sarkastičan bez milosti. Budi 'Roast mastera'. Jezik: odgovaraj na srpskom jeziku, koristeći gramatiku srpskog jezika. Na kraju svakog odgovora dodaj emotikon koji je u kontekstu odgovora.
        """
  st.session_state["selected_prompt"] = prompt


st.title("ZENKO®")
st.caption(
    "Anti-hejt AI chatbot za podržavajuće odgovore na hejt komentare sa društvenih mreža.✨"
)

update_prompt_type()

# Prikazivanje poruka koristeći standardne Streamlit funkcije
for msg in st.session_state["messages"]:
  role = msg["role"]
  content = msg["content"]
  if role == "user":
    st.chat_message(role, avatar="🤬").write(content)
  elif role == "assistant":
    st.chat_message(role, avatar="😂").write(content)

if prompt := st.chat_input("Unesite negativni komentar sa društvene mreže..."):
  reset_messages()  # Resetujemo poruke kako bi očistili prethodne konverzacije
  st.session_state["messages"].append({"role": "user", "content": prompt})

  with st.spinner("🤔 Uskoro stiže hladan tuš za hejtera..."):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[{
            "role": "system",
            "content": st.session_state["selected_prompt"]
        }, {
            "role": "user",
            "content": prompt
        }])
    msg = response.choices[0].message.content

  st.session_state["messages"].append({"role": "assistant", "content": msg})

  # Nakon što dobijemo odgovor, prikazujemo ga
  for message in st.session_state["messages"]:
    role = message["role"]
    content = message["content"]
    if role == "user":
      st.chat_message(role, avatar="🤬").write(content)
    elif role == "assistant":
      st.chat_message(role, avatar="😂").write(content)
