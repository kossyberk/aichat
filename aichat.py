from tkinter import Tk, Text, Scrollbar, Label, Entry, Button, END
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import pyperclip

#############################################################################################
GEMINI_API_KEY = "AIzaSyDZovUL-dc88HFAYdIBCfjL1dQokkLf20A"                                  #
genai.configure(api_key=GEMINI_API_KEY)                                                     #
model = genai.GenerativeModel(model_name="gemini-1.5-flash")                                #
r = sr.Recognizer()                                                                         #
engine = pyttsx3.init()                                                                     #
#############################################################################################

arayuz = Tk()
arayuz.geometry("500x550")
arayuz.title("Yapay Zeka Chat")

ai_label = Label(text="Yapay Zekanın Cevabı :")
ai_label.place(x=100, y=20)
ai_label.config(font="Arial, 15")

entry = Entry(width=50)
entry.place(x=50, y=300)


response_text = Text(arayuz, wrap="word", height=15, width=50)
response_text.place(x=50, y=50)


scrollbar = Scrollbar(arayuz, command=response_text.yview)
scrollbar.place(x=455, y=50, height=245)
response_text["yscrollcommand"] = scrollbar.set

mesajlabel = Label(text="", wraplength=400, justify="left", font="Arial, 12", fg="green")
mesajlabel.place(x=370, y=25)
#############################################################################################

def send_to_ai():
    user_input = entry.get()
    if not user_input.strip():
        response_text.delete("1.0", END)
        response_text.insert(END, "Lütfen bir soru veya mesaj yazın!")
        return

    response_text.delete("1.0", END)
    response_text.insert(END, "Cevap işleniyor, lütfen bekleyin...\n")
    
    try:
        response = model.generate_content(user_input)
        if response and hasattr(response, "text"):
            ai_response = response.text
        response_text.delete("1.0", END)
        response_text.insert(END, ai_response)
    except Exception as e:
        response_text.delete("1.0", END)
        response_text.insert(END, f"Hata oluştu: {e}")

def copy_response():
    content = response_text.get("1.0", END).strip()
    if content:
        pyperclip.copy(content)

def listen_for_command():
    with sr.Microphone() as source:
        r.dynamic_energy_threshold = True
        r.pause_threshold = 1 
        mesajlabel.config(text="Dinliyorum...")
        try:
            audio = r.listen(source)
            text = r.recognize_google(audio, language='tr-TR')
            entry.delete(0, END)
            entry.insert(0, text)
            send_to_ai() 
        except sr.UnknownValueError:
            mesajlabel.config(text="Üzgünüm, anlayamadım.", fg="red")

def set_turkish_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'turkish' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

def speak_response():
    ai_response = response_text.get("1.0", END).strip()
    if ai_response:
        set_turkish_voice()
        engine.say(ai_response)
        engine.runAndWait()

########################################################################################

gonder_button = Button(text="Gönder", command=send_to_ai)
gonder_button.place(x=375, y=295)

mikrofon_button = Button(text="Mikrofon", command=listen_for_command)
mikrofon_button.place(x=430, y=295)

kopyala_button = Button(text="Yanıtı Kopyala", command=copy_response)
kopyala_button.place(x=200, y=400)

sesli_yanit_button = Button(text="Sesli Yanıt", command=speak_response)
sesli_yanit_button.place(x=100, y=400)

arayuz.mainloop()
