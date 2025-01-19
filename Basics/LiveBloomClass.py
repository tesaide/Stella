from transformers import BloomForCausalLM, BloomTokenizerFast

class LiveBloomClass:
    def __init__(self, model_name="bigscience/bloom-560m"):
        """
        Инициализация класса LiveBloomClass для генерации ответов с использованием BLOOM.
        """
        try:
            # Загружаем токенизатор и модель BLOOM
            self.tokenizer = BloomTokenizerFast.from_pretrained(model_name)
            self.model = BloomForCausalLM.from_pretrained(model_name)
            self.model_name = model_name
            print(f"Модель '{model_name}' успешно загружена.")
        except Exception as e:
            print(f"Ошибка при загрузке модели '{model_name}': {e}")
            raise

    def generate_response(self, user_message, max_length=50, temperature=0.7):
        """
        Генерация ответа на основе входного текста.

        :param user_message: Текстовый ввод (вопрос или начало диалога).
        :param max_length: Максимальная длина генерируемого текста.
        :param temperature: Параметр креативности генерации (0.1 - более детерминированно, 1.0 - более случайно).
        :return: Сгенерированный текст.
        """
        try:
            # Кодирование входного текста
            inputs = self.tokenizer.encode(user_message, return_tensors="pt")
            # Генерация текста
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
            )
            # Декодирование результата
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            print(f"Ошибка при генерации ответа: {e}")
            return "Произошла ошибка при генерации текста."
