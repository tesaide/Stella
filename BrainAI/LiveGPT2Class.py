import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class LiveClass:
    def __init__(self, model_name="gpt2"):
        """
        Инициализация класса LiveClass для генерации ответов с использованием GPT-2.
        """
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
            self.model = GPT2LMHeadModel.from_pretrained(model_name)
            self.model_name = model_name
            print(f"Модель '{model_name}' успешно загружена.")
        except Exception as e:
            print(f"Ошибка при загрузке модели '{model_name}': {e}")
            raise

        # История сообщений
        self.chat_history = []

    def generate_response(self, user_message, max_length=150, temperature=0.9):
        """
        Генерация ответа на основе входного текста.

        :param user_message: Текстовый ввод (вопрос или начало диалога).
        :param max_length: Максимальная длина генерируемого текста.
        :param temperature: Параметр креативности генерации (0.1 - более детерминированно, 1.0 - более случайно).
        :return: Сгенерированный текст.
        """
        try:
            # Добавляем новое сообщение в историю
            self.chat_history.append(f"User: {user_message}")

            # Ограничиваем количество истории, чтобы избежать переполнения модели
            context = " ".join(self.chat_history[-10:])  # Например, последние 10 сообщений

            # Кодирование входного текста
            inputs = self.tokenizer.encode(context, return_tensors="pt")
            
            # Создание маски внимания
            attention_mask = (inputs != self.tokenizer.pad_token_id).long()
            
            # Генерация текста с do_sample=True
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,  # Устанавливаем do_sample=True для случайной генерации
                no_repeat_ngram_size=3,  # Убираем повторы
                top_p=0.9,  # Стратегия nucleus sampling для лучшего разнообразия
                top_k=50,  # Ограничиваем выборку наиболее вероятными токенами
                attention_mask=attention_mask  # Добавляем маску внимания
            )
            
            # Декодирование результата
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Обрабатываем текст перед выводом
            return self.filter_response(response)
        except Exception as e:
            print(f"Ошибка при генерации ответа: {e}")
            return "Произошла ошибка при генерации текста."

    def filter_response(self, response):
        """
        Фильтрация сгенерированного текста для удаления нежелательных или бессмысленных ответов.

        :param response: Сгенерированный текст.
        :return: Отфильтрованный текст.
        """
        # Удаляем повторы и лишние символы
        response = re.sub(r"(\b\w+\b)(?:\s+\1)+", r"\1", response)  # Удаляет повторяющиеся слова
        response = response.strip()

        # Фильтр недопустимых слов
     #   banned_words = ["рот", "ругательство", "нецензурное"]
      #  for word in banned_words:
       #     if word in response.lower():
        #        return "Извините, я не могу ответить на этот запрос."

        # Если ответ слишком короткий, добавляем стандартный
        if len(response.split()) < 3:
            response += " Можете уточнить свой вопрос?"

        # Добавляем ответ в историю
        self.chat_history.append(f"Stella: {response}")
        return response

# Пример использования класса
if __name__ == "__main__":
    live_class = LiveClass(model_name="gpt2")
    while True:
        user_input = input("Вы: ")
        response = live_class.generate_response(user_input)
        print(f"Stella: {response}")
