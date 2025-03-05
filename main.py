import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import pronouncing
import re
from translate import Translator


class ModernVocabularyApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("WordForge")
        self.geometry("800x600")
        self.configure(bg="#2D2D2D")
        self.words = {}
        self.current_test = []
        self.test_index = 0
        self.score = 0

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self._setup_styles()

        self.load_words()
        self.create_widgets()
        self.center_window()

    def _setup_styles(self):
        self.colors = {
            'primary': '#4A90E2',
            'secondary': '#6C757D',
            'success': '#28A745',
            'danger': '#DC3545',
            'background': '#2D2D2D',
            'text': '#FFFFFF',
            'entry_bg': '#404040'
        }

        self.style.configure('TFrame', background=self.colors['background'])
        self.style.configure('TLabel',
                             background=self.colors['background'],
                             foreground=self.colors['text'],
                             font=('Helvetica', 12))

        self.style.configure('Primary.TButton',
                             foreground=self.colors['text'],
                             background=self.colors['primary'],
                             font=('Helvetica', 12, 'bold'),
                             padding=10,
                             borderwidth=0)

        self.style.map('Primary.TButton', background=[('active', '#357ABD')])

        self.style.configure('Secondary.TButton',
                             foreground=self.colors['text'],
                             background=self.colors['secondary'],
                             font=('Helvetica', 10),
                             padding=5)

        self.style.configure('Entry.TEntry',
                             fieldbackground=self.colors['entry_bg'],
                             foreground=self.colors['text'],
                             insertcolor=self.colors['text'],
                             bordercolor=self.colors['primary'],
                             lightcolor=self.colors['primary'],
                             darkcolor=self.colors['primary'])

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def get_transcription(self, word):
        """Получает транскрипцию английского слова."""
        try:
            phones = pronouncing.phones_for_word(word.lower())
            if phones:
                transcription = phones[0]
                transcription = re.sub(r'(\D)1', r'\1ˈ', transcription)
                transcription = re.sub(r'(\D)2', r'\1ˌ', transcription)
                transcription = transcription.replace(' ', '')
                transcription = re.sub(r'\d', '', transcription)
                return f"/[{transcription}]/"
            else:
                return "/-/"
        except Exception:
            return "/-/"

    def load_words(self):
        if os.path.exists('words.json'):
            with open('words.json', 'r', encoding='utf-8') as f:
                self.words = json.load(f)
                
                for eng_word, word_data in self.words.items():
                    if isinstance(word_data, str):
                        rus_trans = word_data
                        transcription = self.get_transcription(eng_word)
                        self.words[eng_word] = {
                            "translation": rus_trans,
                            "transcription": transcription
                        }
                
                self.save_words()

    def save_words(self):
        with open('words.json', 'w', encoding='utf-8') as f:
            json.dump(self.words, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(pady=50, expand=True)

        ttk.Label(self.main_frame,
                  text="WordForge",
                  font=('Helvetica', 24, 'bold')).pack(pady=20)

        ttk.Button(self.main_frame,
                   text="➕ Добавить слово",
                   style='Primary.TButton',
                   command=self.show_add_word).pack(pady=10, ipadx=20)

        ttk.Button(self.main_frame,
                   text="📝 Начать тест слов",
                   style='Primary.TButton',
                   command=self.start_test).pack(pady=10, ipadx=20)

        ttk.Button(self.main_frame,
                   text="📝 Начать тест предложений",
                   style='Primary.TButton',
                   command=self.start_sentence_test).pack(pady=10, ipadx=20)

        ttk.Button(self.main_frame,
                   text="🚪 Выход",
                   style='Secondary.TButton',
                   command=self.destroy).pack(pady=20)

        self.add_frame = ttk.Frame(self)

        ttk.Label(self.add_frame,
                  text="Добавление нового слова",
                  font=('Helvetica', 18)).pack(pady=20)

        input_frame = ttk.Frame(self.add_frame)
        input_frame.pack(pady=20)

        ttk.Label(input_frame, text="Английское слово:").grid(row=0,
                                                              column=0,
                                                              padx=10,
                                                              pady=10)
        self.eng_entry = ttk.Entry(input_frame, style='Entry.TEntry', width=25)
        self.eng_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(input_frame, text="Русский перевод:").grid(row=1,
                                                             column=0,
                                                             padx=10,
                                                             pady=10)
        self.rus_entry = ttk.Entry(input_frame, style='Entry.TEntry', width=25)
        self.rus_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Кнопка для автоматического перевода
        ttk.Button(input_frame,
                  text="🔄 Перевести",
                  style='Secondary.TButton',
                  command=self.auto_translate).grid(row=1, column=2, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Транскрипция:").grid(row=2,
                                                         column=0,
                                                         padx=10,
                                                         pady=10)
        self.transcription_entry = ttk.Entry(input_frame, style='Entry.TEntry', width=25)
        self.transcription_entry.grid(row=2, column=1, padx=10, pady=10)
        
        # Кнопка для автоматического получения транскрипции
        ttk.Button(input_frame,
                  text="🔄 Получить транскрипцию",
                  style='Secondary.TButton',
                  command=self.generate_transcription).grid(row=2, column=2, padx=10, pady=10)

        button_frame = ttk.Frame(self.add_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="💾 Сохранить",
                   style='Primary.TButton',
                   command=self.save_word).pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame,
                   text="🔙 Назад",
                   style='Secondary.TButton',
                   command=self.show_main).pack(side=tk.LEFT, padx=10)

        self.test_frame = ttk.Frame(self)

        self.question_label = ttk.Label(self.test_frame,
                                        font=('Helvetica', 18, 'bold'),
                                        wraplength=600)
        self.question_label.pack(pady=40)

        self.answer_entry = ttk.Entry(self.test_frame,
                                      style='Entry.TEntry',
                                      font=('Helvetica', 14),
                                      width=30)
        self.answer_entry.pack(pady=20)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())

        self.result_label = ttk.Label(self.test_frame,
                                      font=('Helvetica', 14),
                                      anchor=tk.CENTER)
        self.result_label.pack(pady=20)

        button_frame = ttk.Frame(self.test_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame,
                   text="✅ Проверить",
                   style='Primary.TButton',
                   command=self.check_answer).pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame,
                   text="🔙 Назад",
                   style='Secondary.TButton',
                   command=self.show_main).pack(side=tk.LEFT, padx=10)

    def show_main(self):
        self.add_frame.pack_forget()
        self.test_frame.pack_forget()
        self.main_frame.pack(expand=True)

    def show_add_word(self):
        self.main_frame.pack_forget()
        self.eng_entry.delete(0, tk.END)
        self.rus_entry.delete(0, tk.END)
        self.add_frame.pack(expand=True)

    def generate_transcription(self):
        eng_word = self.eng_entry.get().strip().lower()
        if eng_word:
            transcription = self.get_transcription(eng_word)
            self.transcription_entry.delete(0, tk.END)
            self.transcription_entry.insert(0, transcription)
        else:
            messagebox.showerror("Ошибка", "Введите английское слово")
    
    def auto_translate(self):
        eng_word = self.eng_entry.get().strip().lower()
        if eng_word:
            try:
                translator = Translator(to_lang="ru")
                translation = translator.translate(eng_word)
                translation = translation.strip().lower()
                if "INVALID CREDENTIALS" in translation:
                    messagebox.showerror("Ошибка", "Проблема с сервисом перевода. Пожалуйста, введите перевод вручную.")
                    return
                self.rus_entry.delete(0, tk.END)
                self.rus_entry.insert(0, translation)
                self.generate_transcription()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось перевести слово: {str(e)}")
        else:
            messagebox.showerror("Ошибка", "Введите английское слово")
    
    def save_word(self):
        eng = self.eng_entry.get().strip().lower()
        rus = self.rus_entry.get().strip().lower()
        transcription = self.transcription_entry.get().strip()

        if eng and rus:
            if not transcription:
                transcription = self.get_transcription(eng)
                
            self.words[eng] = {
                "translation": rus,
                "transcription": transcription
            }
            self.save_words()
            messagebox.showinfo("Успешно", "Слово добавлено в словарь!")
            self.show_main()
        else:
            messagebox.showerror("Ошибка", "Английское слово и перевод должны быть заполнены")

    def start_test(self):
        if not self.words:
            messagebox.showwarning("Ошибка", "Сначала добавьте слова!")
            return

        self.current_test = [(word, data["translation"]) 
                            for word, data in self.words.items()]
        random.shuffle(self.current_test)
        self.test_index = 0
        self.score = 0
        self.show_next_question()

    def generate_sentence(self):
        if not self.words:
            return ""

        eng_words = list(self.words.keys())
        sentence_length = random.randint(3, 5)
        selected_words = random.sample(eng_words, sentence_length)

        sentence = " ".join(selected_words) + "."
        return sentence

    def translate_sentence(self, sentence):
        words = sentence.split()
        translated_words = [
            self.words.get(word.lower(), {}).get("translation", word) 
            if word.lower() in self.words else word
            for word in words
        ]
        return " ".join(translated_words) + "."

    def start_sentence_test(self):
        if not self.words:
            messagebox.showwarning("Ошибка", "Сначала добавьте слова!")
            return

        self.current_test = [
            (self.generate_sentence(),
             self.translate_sentence(self.generate_sentence()))
            for _ in range(5)
        ]
        random.shuffle(self.current_test)
        self.test_index = 0
        self.score = 0
        self.show_next_question()

    def show_next_question(self):
        self.main_frame.pack_forget()
        self.test_frame.pack(expand=True)

        if self.test_index < len(self.current_test):
            question, answer = self.current_test[self.test_index]
            transcription = self.words.get(question, {}).get("transcription", "")
            
            self.question_label.config(text=f"Переведите: {question}\n{transcription}")
            
            self.answer_entry.delete(0, tk.END)
            self.result_label.config(text="")
            self.answer_entry.focus()
        else:
            self.show_results()

    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_test[self.test_index][1].lower()

        if user_answer == correct_answer:
            self.score += 1
            self.result_label.config(text="Правильно! ✅",
                                     foreground=self.colors['success'])
        else:
            self.result_label.config(
                text=f"❌ Неправильно. Правильный ответ: {correct_answer}",
                foreground=self.colors['danger'])

        self.test_index += 1
        self.after(3000, self.show_next_question)

    def show_results(self):
        self.test_frame.pack_forget()
        result_text = (
            f"Тест завершен!\n\n"
            f"Правильных ответов: {self.score}/{len(self.current_test)}\n"
            f"Успешность: {self.score/len(self.current_test)*100:.1f}%")
        messagebox.showinfo("Результаты", result_text)
        self.show_main()


if __name__ == "__main__":
    app = ModernVocabularyApp()
    app.mainloop()
