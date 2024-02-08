import streamlit as st
from openai import OpenAI

# Postavljanje API ključa
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
# Funkcija za resetovanje poruka
def reset_messages():
  st.session_state["messages"] = []


if "messages" not in st.session_state:
  st.session_state["messages"] = []

st.set_page_config(page_title="ZENKO | Anti-hejt AI chatbot", page_icon="💬")

st.markdown("""
    <style>
    .bottom-center-text {
        position: fixed;
        bottom: 20px;
        left: 0;
        text-align: center;
        padding: 0 20px;
        width: 100%;
        z-index: 9999;
    }
    </style>
    """,
            unsafe_allow_html=True)
st.caption(
    '<div class="bottom-center-text">Ako želite da naučite da pravite ovakve AI chatbot-ove, prijavite se na moju <a href="https://forms.gle/fw7U1MjrQ9GafAFz9">AI grupu na Discordu</a>. Čekam vas!</div>',
    unsafe_allow_html=True)

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
        Ti si ekspert za odgovaranje na negativne komentare sa društvenih mreža na sarkastičan način. Zovu te i 'Roast master'. Tvoj zadatak je da na svaki negativan komentar koji ti se pošalje odgovoriš sarkazmom i ironijom. Koristi ulični sleng i ironiju da iznenadiš i nasmeješ negativne hejtere. Budi sarkastičan bez milosti. Jezik: odgovaraj na srpskom jeziku, koristeći gramatiku srpskog jezika. Na kraju svakog odgovora dodaj emotikon koji je u kontekstu odgovora.
        """
  st.session_state["selected_prompt"] = prompt


st.title("💬 ZENKO®")
st.markdown(
    "Anti-hejt AI chatbot by [Miloš Ludus](https://www.instagram.com/milosludus) za podržavajuće odgovore na hejt komentare sa društvenih mreža.✨"
)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

update_prompt_type()

# Prikazivanje poruka koristeći standardne Streamlit funkcije
for msg in st.session_state["messages"]:
  role = msg["role"]
  content = msg["content"]
  if role == "user":
    st.chat_message(role, avatar="🤬").write(content)
  elif role == "assistant":
    st.chat_message(role, avatar="🛁").write(content)

if prompt := st.chat_input("Unesite negativni komentar 🤬..."):
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
      st.chat_message(role, avatar="🛁").write(content)
