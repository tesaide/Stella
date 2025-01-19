import os
import platform

class AICore:
    """
    Центральный класс AI, который отвечает за взаимодействие с другими модулями.
    """

    def __init__(self):
        """Инициализация центрального ядра AI."""
        self.modules = {}

    def register_module(self, name, module):
        """Регистрация нового модуля."""
        self.modules[name] = module

    def process_request(self, module_name, *args, **kwargs):
        """Обработка запроса через указанный модуль."""
        module = self.modules.get(module_name)
        if not module:
            raise ValueError(f"Модуль '{module_name}' не найден.")
        
        if not hasattr(module, 'handle_request'):
            raise AttributeError(f"Модуль '{module_name}' не имеет метода 'handle_request'.")

        return module.handle_request(*args, **kwargs)


class FileSearchModule:
    """
    Модуль для поиска файлов в системе.
    """

    def handle_request(self, filename):
        """Обрабатывает запрос на поиск файла по всей системе."""
        if not filename:
            return []

        # Определяем корневые директории для поиска
        if platform.system() == "Windows":
            drives = [f"{chr(d)}:/" for d in range(65, 91) if os.path.exists(f"{chr(d)}:/")]
        else:
            drives = ["/"]

        found_files = []
        filename_lower = filename.lower()  # Приводим имя файла к нижнему регистру

        for drive in drives:
            for root, dirs, files in os.walk(drive):
                # Исключаем системные папки
                dirs[:] = [d for d in dirs if d not in ('$Recycle.Bin', 'System Volume Information', 'Windows')]

                for file in files:
                    file_lower = file.lower()
                    # Проверяем имя файла без учета расширения
                    if filename_lower in file_lower:
                        found_files.append(os.path.join(root, file))

        return found_files


class ChatApp:
    def __init__(self, ai_core):
        self.ai_core = ai_core

    def generate_and_display_response(self, user_message):
        """Обрабатывает запрос пользователя и генерирует ответ."""
        if "найти файл" in user_message.lower():
            filename = user_message.lower().replace("найти файл", "").strip()
            response = self.search_file(filename)
        else:
            response = f"Ответ на запрос: {user_message}"

        print(f"Ответ: {response}")

    def search_file(self, filename):
        """Обрабатывает поиск файла и возвращает путь."""
        try:
            result = self.ai_core.process_request("file_search", filename)
            if result:
                return f"Окей, твой файл тут: {result[0]}"
            else:
                return "Файл не найден."
        except Exception as e:
            return f"Ошибка: {e}"


if __name__ == "__main__":
    ai_core = AICore()
    file_search_module = FileSearchModule()
    ai_core.register_module("file_search", file_search_module)

    # Создание экземпляра чат-приложения
    chat_app = ChatApp(ai_core)

    # Пример ввода от пользователя
    user_input = "найти файл example.txt"
    chat_app.generate_and_display_response(user_input)
