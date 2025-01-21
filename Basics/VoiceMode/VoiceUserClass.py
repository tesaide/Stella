import speech_recognition
import os
import random 

# Методи бібліотеки SpeechRecognition, які ми можемо використовувати для розпізнавання мови в текст:
# recognize_bing(): Розпізнавання мови за допомогою Microsoft Bing Speech API (потрібен api key)
# recognize_google(): Розпізнавання мови за допомогою Google Speech API 
# recognize_google_cloud(): Розпізнавання мови за допомогою Google Cloud Speech API (потрібен api key)
# recognize_houndify(): Розпізнавання мови за допомогою Houndify API від SoundHound (потрібен api key)
# recognize_ibm(): Розпізнавання мови за допомогою IBM Speech to Text API (потрібен api key)
# recognize_sphinx(): Розпізнавання мови за допомогою PocketSphinx API (потрібен api key) 
# Створюємо об'єкт розпізнавача мови

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5  # Час затримки для визначення паузи між словами

def listen_command():
    """
    Функція для запису голосової команди за допомогою мікрофона.
    Повертає розпізнану команду у вигляді тексту або повідомлення про помилку.
    """
    try: 
        # Використовуємо мікрофон для запису
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)  # Оцінюємо навколишній шум
            audio = sr.listen(source=mic)  # Записуємо голос
            query = sr.recognize_google(audio_data=audio, language='uk-UA').lower()  # Розпізнаємо команду
        
        return query
    except speech_recognition.UnknownValueError:
        return 'Dawn... Не зрозумів, що ти сказав :/'

def greeting():
    """
    Функція для привітання користувача.
    Повертає рядок з привітанням.
    """
    return 'Привіт Богдане!'

def create_task():
    """
    Функція для додавання нової задачі до списку справ.
    Запитує користувача про нову задачу і додає її до файлу.
    Повертає повідомлення про додану задачу.
    """
    print('Що додамо в список справ?')

    query = listen_command()  # Отримуємо нову задачу

    # Шлях до файлу зі списком задач
    todo_file_path = os.path.join(os.path.dirname(__file__), 'todo-list.txt')

    try:
        with open(todo_file_path, 'r', encoding='utf-8') as file:
            task_number = len(file.readlines()) + 1  # Нумерація задач
    except FileNotFoundError:
        task_number = 1  # Якщо файл не знайдений, то починаємо з 1

    # Додаємо нову задачу в файл
    with open(todo_file_path, 'a', encoding='utf-8') as file:
        file.write(f'❗️{task_number}. {query}\n')

    return f'Задача {task_number}: "{query}" додана в todo-list!'

def play_music():
    """
    Функція для відтворення випадкового музичного файлу з папки "Music".
    Повертає повідомлення про музику, що грає.
    """
    music_folder = 'Music'  # Папка з музикою
    if not os.path.exists(music_folder):  # Перевіряємо, чи існує папка
        return "Папка з музикою не знайдена."

    files = os.listdir(music_folder)  # Отримуємо список файлів в папці
    if not files:
        return "У папці немає музичних файлів."

    random_file = f'{music_folder}/{random.choice(files)}'  # Вибираємо випадковий файл
    os.system(f'start {random_file}')  # Відкриваємо файл через стандартний плеєр
    
    return f'Танцюємо під {random_file.split("/")[-1]} 🔊'

def main():
    """
    Головна функція програми, що визначає, яку команду виконати.
    Викликає відповідні функції в залежності від голосової команди.
    """
    print("Будь ласка, скажи команду:")
    query = listen_command()  # Отримуємо команду користувача

    if query == 'привіт':
        print(greeting())  # Виконуємо привітання
    elif query == 'відкрий список':
        print(create_task())  # Створюємо нову задачу
    elif query == 'увімкни музику':
        print(play_music())  # Відтворюємо музику
    else:
        print(f'Не відома команда: "{query}"')  # Якщо команда невідома

if __name__ == '__main__':
    main()  # Запуск програми
