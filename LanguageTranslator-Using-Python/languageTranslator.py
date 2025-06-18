from tkinter import *
from translate import Translator
import speech_recognition as sr
import pyttsx3
import pyperclip

# Language code mapping
language_codes = {
    'English': 'en',
    'Hindi': 'hi',
    'Gujarati': 'gu',
    'Spanish': 'es',
    'German': 'de',
    'Telugu': 'te',
    'Tamil': 'ta',
    'French': 'fr',
    'Japanese': 'ja',
    'Chinese': 'zh'
}

# Init TTS engine
engine = pyttsx3.init()

# Main Translate function
def translate():
    try:
        from_lang = language_codes[lan1.get()]
        to_lang = language_codes[lan2.get()]
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        translation = translator.translate(var.get())
        var1.set(translation)
    except Exception as e:
        var1.set("Error: " + str(e))

# Speech input
def talk():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        status.set("Listening...")
        root.update()
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        var.set(text)
        status.set("Recognized: " + text)
        translate()
    except sr.UnknownValueError:
        var.set("Could not understand audio")
        status.set("Try again.")
    except sr.RequestError as e:
        var.set("Speech Error")
        status.set(f"Error: {e}")

# Text to Speech
def speak_output():
    text = var1.get()
    if text:
        engine.say(text)
        engine.runAndWait()

# Clear inputs
def clear_fields():
    var.set("")
    var1.set("")
    status.set("Cleared")

# Copy output to clipboard
def copy_output():
    pyperclip.copy(var1.get())
    status.set("Copied to clipboard!")

# Theme switcher
def toggle_theme():
    global is_dark
    is_dark = not is_dark
    bg = "#2e2e2e" if is_dark else "#ffffff"
    fg = "#ffffff" if is_dark else "#000000"
    root.config(bg=bg)
    mainframe.config(bg=bg)
    for widget in mainframe.winfo_children():
        widget.config(bg=bg, fg=fg)
    status_label.config(bg=bg, fg=fg)
    theme_btn.config(text="Switch to Light" if is_dark else "Switch to Dark")

# Setup GUI
root = Tk()
root.title("Advanced Language Translator")
root.resizable(False, False)
is_dark = False

mainframe = Frame(root, padx=20, pady=20)
mainframe.grid()

# Variables
var = StringVar()
var1 = StringVar()
status = StringVar(value="Ready")

# Input Text
Label(mainframe, text="Enter Text").grid(row=0, column=0, sticky=W)
Entry(mainframe, textvariable=var, width=50).grid(row=0, column=1, columnspan=3)

# Language Selection
Label(mainframe, text="From").grid(row=1, column=0, sticky=E)
lan1 = StringVar(value='English')
OptionMenu(mainframe, lan1, *language_codes.keys()).grid(row=1, column=1)

Label(mainframe, text="To").grid(row=1, column=2, sticky=E)
lan2 = StringVar(value='Hindi')
OptionMenu(mainframe, lan2, *language_codes.keys()).grid(row=1, column=3)

# Output
Label(mainframe, text="Translation").grid(row=2, column=0, sticky=W)
Entry(mainframe, textvariable=var1, width=50, state='readonly').grid(row=2, column=1, columnspan=3)

# Buttons
Button(mainframe, text='Translate', width=15, command=translate).grid(row=3, column=0, pady=10)
Button(mainframe, text='Speak Input', width=15, command=talk).grid(row=3, column=1)
Button(mainframe, text='Speak Output', width=15, command=speak_output).grid(row=3, column=2)
Button(mainframe, text='Copy Output', width=15, command=copy_output).grid(row=3, column=3)

Button(mainframe, text='Clear', width=15, command=clear_fields).grid(row=4, column=1)
theme_btn = Button(mainframe, text='Switch to Dark', width=15, command=toggle_theme)
theme_btn.grid(row=4, column=2)

# Status bar
status_label = Label(root, textvariable=status, bd=1, relief=SUNKEN, anchor=W)
status_label.grid(row=10, column=0, sticky="we")

root.mainloop()
