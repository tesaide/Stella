import speech_recognition

# Методи бібліотеки SpeechRecognition, які ми можемо використовувати для розпізнавання мови в текст:
# recognize_bing(): Розпізнавання мови за допомогою Microsoft Bing Speech API (потрібен api key)
# recognize_google(): Розпізнавання мови за допомогою Google Speech API 
# recognize_google_cloud(): Розпізнавання мови за допомогою Google Cloud Speech API (потрібен api key)
# recognize_houndify(): Розпізнавання мови за допомогою Houndify API від SoundHound (потрібен api key)
# recognize_ibm(): Розпізнавання мови за допомогою IBM Speech to Text API (потрібен api key)
# recognize_sphinx(): Розпізнавання мови за допомогою PocketSphinx API (потрібен api key)

# Встановлення бібліотек:
# pip install SpeechRecognition
# pip install pyaudio

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

with speech_recognition.Microphone() as mic:
    sr.adjust_for_ambient_noise(source=mic, duration=0.5)
    audio = sr.listen(source=mic)
    query = sr.recognize_google(audio_data=audio, language='uk-UA')
    
print(query)
