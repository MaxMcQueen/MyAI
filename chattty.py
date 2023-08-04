import openai
import speech_recognition as sr
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from datetime import datetime

openai.api_key = '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'

def ask_openai(question):
    model_engine = "text-davinci-003"
    prompt = f"Q:{question}\nA:"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )
    message = completions.choices[0].text.strip()
    return message

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down."

class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("ChattyPal")
        self.window.geometry("400x600")

        # Create a frame for the header and date/time labels
        self.header_frame = tk.Frame(self.window, bg="#F0EAD6")
        self.header_frame.pack(side="top", fill="x")

        self.header_label = tk.Label(self.header_frame, text="ChattyPal", font=("Helvetica", 20, "bold"), bg="#F0EAD6", fg="#333333")
        self.header_label.pack(side="left", padx=10)

        self.datetime_label = tk.Label(self.header_frame, text="", font=("Helvetica", 14), bg="#F0EAD6", fg="#555555")
        self.datetime_label.pack(side="right", padx=10)

        self.update_datetime()  # Update the date and time initially

        self.chat_frame = tk.Frame(self.window, bg="#F0EAD6")
        self.chat_frame.pack(side="top", fill="both", expand=True)

        self.chat_history = tk.Text(self.chat_frame, wrap="word", state=DISABLED, bg="#FFFCF8", fg="#333333", font=("Helvetica", 14))
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.chat_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set)

        self.question_entry = tk.Entry(self.window, width=50, font=("Helvetica", 14), bd=3, relief=tk.FLAT, bg="#FFFCF8", fg="#007BFF")
        self.question_entry.pack(pady=10)

        self.ask_button = tk.Button(self.window, text="Ask", width=20, command=self.ask_question, font=("Helvetica", 14), bd=0, bg="#F39C12", fg="black", activebackground="#E67E22", relief=tk.FLAT)
        self.ask_button.pack(pady=10)

        self.listen_button = tk.Button(self.window, text="Speak", width=20, command=self.listen_question, font=("Helvetica", 14), bd=0, bg="#F39C12", fg="black", activebackground="#E67E22", relief=tk.FLAT)
        self.listen_button.pack(pady=10)

        self.clear_button = tk.Button(self.window, text="Clear", width=20, command=self.clear_all, font=("Helvetica", 14), bd=0, bg="#E74C3C", fg="black", activebackground="#C0392B", relief=tk.FLAT)
        self.clear_button.pack(pady=10)

        self.chat_history.tag_configure("right", justify="right")

        self.window.mainloop()

    def clear_all(self):
        self.chat_history.configure(state=NORMAL)
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state=DISABLED)

    def ask_question(self):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)
            self.question_entry.delete(0, tk.END)  # Clear the text entry area

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state=NORMAL)
        if self.chat_history.index('end') != None:
            current_time = datetime.now().strftime("%H:%M")
            self.chat_history.insert('end', current_time + ' ', ("small", "right", "white"))
            self.chat_history.window_create('end', window=tk.Label(self.chat_history, fg="white",
                                                                   text=question,
                                                                   wraplength=200, font=("Arial", 18),
                                                                   bg="#218aff", bd=4, justify="left"))
            self.chat_history.insert('end', '\n\n ', "left")
            self.chat_history.insert('end', current_time + ' ', ("small", "left", "white"))
            self.chat_history.window_create('end', window=tk.Label(self.chat_history, fg="white",
                                                                   text=response,
                                                                   wraplength=200, font=("Arial", 18),
                                                                   bg="#aeb9cc", bd=4, justify="right"))
            self.chat_history.insert('end', '\n\n ', "right")
            self.chat_history.tag_configure(foreground="#0000CC", font=("Arial", 12, 'bold'))
            self.chat_history.configure(state=DISABLED)
            self.chat_history.yview('end')

    def update_datetime(self):
        now = datetime.now()
        # Change the date format to show the month and day
        current_datetime = now.strftime("%B %d, %Y %H:%M")
        self.datetime_label.config(text=current_datetime)
        self.window.after(1000, self.update_datetime)

if __name__ == "__main__":
    gui = ChatbotGUI()
