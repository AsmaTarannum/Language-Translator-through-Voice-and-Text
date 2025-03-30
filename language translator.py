import tkinter as tk
from tkinter import ttk, messagebox
import speech_recognition as sr
from googletrans import Translator, LANGUAGES
from gtts import gTTS
import pygame
import pyttsx3
import os
import locale  # Import locale to get system's default language

# Initialize the main window
root = tk.Tk()
root.title("Translator App")
root.geometry("600x600")  # Increased height to accommodate the logo

# Load logo image
logo_image = tk.PhotoImage(file='C:/Users/asma/Documents/Real Time Project/code[1]/logo.png')  # Replace "logo.png" with the path to your logo image

# Create a label for the logo
logo_label = tk.Label(root, image=logo_image)
logo_label.pack()

# Initialize the translator and recognizer
translator = Translator()
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Initialize Pygame for audio playback
pygame.mixer.init()

# Function to get the default system language
def get_default_system_language():
    system_locale = locale.getdefaultlocale()  # Get default locale
    if system_locale and system_locale[0]:
        # The language code is returned as a string like 'en_US', extract 'en'
        language_code = system_locale[0].split('_')[0]
        return LANGUAGES.get(language_code, 'english')  # Default to 'english' if not found
    return 'english'  # Fallback to English if no locale found

# Function to translate text
def translate_text():
    try:
        text_to_translate = input_text.get("1.0", tk.END).strip()
        if not text_to_translate:
            messagebox.showerror("Error", "No text to translate!")
            return

        target_language = language_var.get()
        if not target_language:
            messagebox.showerror("Error", "No language selected!")
            return

        translation = translator.translate(text_to_translate, dest=target_language)
        translated_text = translation.text
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text)
        output_text.config(state=tk.DISABLED)
        
        # Save the translated text to an mp3 file
        tts = gTTS(translated_text)
        tts.save("output.mp3")
        
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Play the transliterated text using Pygame
        pygame.mixer.music.load(os.path.abspath("output.mp3"))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Speak the transliterated text
        engine.say(translated_text)
        engine.runAndWait()
        
        # Stop the music and uninitialize Pygame
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove("output.mp3")
        
    except Exception as e:
        print(e)
        messagebox.showerror("Error", str(e))

# Function to handle microphone input
def use_microphone():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            messagebox.showinfo("Info", "Please speak now...")
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text)
            messagebox.showinfo("Info", "Text recognized: " + text)
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        messagebox.showerror("Error", "Could not request results from Google Speech Recognition service; {0}".format(e))

# Function to show confirmation
def confirm_input():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        messagebox.showerror("Error", "No text entered!")
        return
    
    confirmation = messagebox.askyesno("Confirm Input", f"Is this the text you want to translate?\n\n{user_input}")
    if confirmation:
        language_label.pack()
        language_menu.pack()
        translate_button.pack()

# Widgets
input_label = tk.Label(root, text="Enter text or use microphone:")
input_label.pack()

input_text = tk.Text(root, height=5, width=50)
input_text.pack()

mic_button = tk.Button(root, text="Use Microphone", command=use_microphone)
mic_button.pack()

confirm_button = tk.Button(root, text="Confirm Text", command=confirm_input)
confirm_button.pack()

# Set default language (retrieved from the system)
default_language = get_default_system_language()

# Initialize the language_var with the default language
language_var = tk.StringVar(root)
language_var.set(default_language)

# Language selection
language_label = tk.Label(root, text="Select language to translate to:")
languages = list(LANGUAGES.values())
language_menu = ttk.Combobox(root, textvariable=language_var, values=languages, state='readonly')

# Translate button
translate_button = tk.Button(root, text="Translate", command=translate_text)

# Output text
output_label = tk.Label(root, text="Translated text:")
output_label.pack()

output_text = tk.Text(root, height=5, width=50, state=tk.DISABLED)
output_text.pack()

# Run the application
root.mainloop()
