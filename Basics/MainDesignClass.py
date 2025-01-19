import tkinter as tk
from tkinter import ttk
import threading
from transformers import GPT2LMHeadModel, GPT2Tokenizer, BloomForCausalLM, BloomTokenizerFast
import os
import platform

# Классы для генерации ответов с использованием GPT-2 и BLOOM
class LiveGPT2Class:
    def __init__(self, model_name="gpt2"):
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.model = GPT2LMHeadModel.from_pretrained(model_name)
            print(f"Модель GPT-2 '{model_name}' успешно загружена.")
        except Exception as e:
            print(f"Ошибка при загрузке модели GPT-2 '{model_name}': {e}")
            raise

    def generate_response(self, user_message, max_length=50, temperature=0.7):
        try:
            inputs = self.tokenizer.encode(user_message, return_tensors="pt")
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            print(f"Ошибка при генерации ответа GPT-2: {e}")
            return "Произошла ошибка при генерации текста."

class LiveBloomClass:
    def __init__(self, model_name="bigscience/bloom-560m"):
        try:
            self.tokenizer = BloomTokenizerFast.from_pretrained(model_name)
            self.model = BloomForCausalLM.from_pretrained(model_name)
            print(f"Модель BLOOM '{model_name}' успешно загружена.")
        except Exception as e:
            print(f"Ошибка при загрузке модели BLOOM '{model_name}': {e}")
            raise

    def generate_response(self, user_message, max_length=50, temperature=0.7):
        try:
            inputs = self.tokenizer.encode(user_message, return_tensors="pt")
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            print(f"Ошибка при генерации ответа BLOOM: {e}")
            return "Произошла ошибка при генерации текста."

# Основное приложение
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stella AI")
        self.root.geometry("400x600")
        self.root.configure(bg="#ffffff")

        # Выбранная модель (пока None)
        self.live_class = None

        # Отображаем экран выбора модели
        self.show_model_selection_screen()

    def show_model_selection_screen(self):
        """Экран выбора модели."""
        self.selection_frame = tk.Frame(self.root, bg="#ffffff")
        self.selection_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            self.selection_frame,
            text="Выберите модель:",
            font=("Arial", 16),
            bg="#ffffff",
            fg="#333333",
        ).pack(pady=20)

        gpt_button = tk.Button(
            self.selection_frame,
            text="GPT-2",
            font=("Arial", 14),
            bg="#0088cc",
            fg="white",
            width=20,
            command=self.select_gpt2,
        )
        gpt_button.pack(pady=10)

        bloom_button = tk.Button(
            self.selection_frame,
            text="BLOOM",
            font=("Arial", 14),
            bg="#00cc88",
            fg="white",
            width=20,
            command=self.select_bloom,
        )
        bloom_button.pack(pady=10)

    def select_gpt2(self):
        """Инициализация GPT-2 и переход к основному экрану."""
        self.live_class = LiveGPT2Class()
        self.show_chat_screen()

    def select_bloom(self):
        """Инициализация BLOOM и переход к основному экрану."""
        self.live_class = LiveBloomClass()
        self.show_chat_screen()

    def show_chat_screen(self):
        """Основной экран чата."""
        # Удаляем экран выбора модели
        self.selection_frame.destroy()

        # Заголовок
        self.header = tk.Frame(self.root, bg="#0088cc", height=50)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.title_label = tk.Label(
            self.header, text="Stella AI", bg="#0088cc", fg="white", font=("Arial", 16)
        )
        self.title_label.pack(pady=10)

        # Поле для сообщений
        self.messages_frame = tk.Frame(self.root, bg="#f5f5f5")
        self.messages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.messages_canvas = tk.Canvas(
            self.messages_frame, bg="#f5f5f5", highlightthickness=0
        )
        self.messages_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.scrollbar = ttk.Scrollbar(
            self.messages_frame, orient=tk.VERTICAL, command=self.messages_canvas.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.messages_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.message_container = tk.Frame(self.messages_canvas, bg="#f5f5f5")
        self.messages_canvas.create_window((0, 0), window=self.message_container, anchor="nw")

        self.message_container.bind("<Configure>", self.update_scroll_region)

        # Поле ввода и кнопка отправки
        self.input_frame = tk.Frame(self.root, bg="#ffffff")
        self.input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(5, 10))

        self.entry = tk.Entry(
            self.input_frame, font=("Arial", 14), bg="#f0f0f0", bd=0, relief=tk.FLAT
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=5)

        self.send_button = tk.Button(
            self.input_frame,
            text="Отправить",
            bg="#0088cc",
            fg="white",
            font=("Arial", 12),
            command=self.send_message,
            relief=tk.FLAT,
            cursor="hand2",
        )
        self.send_button.pack(side=tk.RIGHT)

        # Привязываем событие нажатия клавиши Enter для отправки сообщения
        self.entry.bind("<Return>", self.on_enter_pressed)

    def update_scroll_region(self, event=None):
        self.messages_canvas.configure(scrollregion=self.messages_canvas.bbox("all"))

    def send_message(self):
        user_message = self.entry.get().strip()
        if user_message:
            self.add_message("Вы", user_message)
            self.entry.delete(0, tk.END)

            # Выполнение обработки сообщения в фоновом потоке
            threading.Thread(target=self.generate_and_display_response, args=(user_message,)).start()

    def on_enter_pressed(self, event=None):
        self.send_message()

    def generate_and_display_response(self, user_message):
        response = self.live_class.generate_response(user_message)
        self.add_message("Stella", response)

    def add_message(self, sender, message):
        message_frame = tk.Frame(self.message_container, bg="#f5f5f5")
        message_frame.pack(anchor="w", pady=5, padx=10)

        sender_label = tk.Label(
            message_frame,
            text=sender,
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            fg="#333333",
        )
        sender_label.pack(anchor="w")

        message_label = tk.Label(
            message_frame,
            text=message,
            font=("Arial", 12),
            bg="#d9f7be" if sender == "Вы" else "#f0f0f0",
            fg="#000000",
            wraplength=280,
            justify="left",
            padx=10,
            pady=5,
            relief=tk.FLAT,
            bd=0,
        )
        message_label.pack(anchor="w")

        self.messages_canvas.update_idletasks()
        self.messages_canvas.yview_moveto(1.0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
