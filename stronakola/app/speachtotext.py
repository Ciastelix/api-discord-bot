import speech_recognition as sr
from os import path, remove

class SpeachToText:
    path: str

    def __init__(self, path: str = "meeting.wav") -> bool:
        self.r = sr.Recognizer()
        self.path = path

    def generate(self) -> bool:
        with sr.AudioFile(self.path) as source:
            audio_text = self.r.listen(source)

            for _ in range(10):
                try:
                    text = self.r.recognize_google(audio_text, language="pl_PL")
                    with open(f"{self.path[:-4]}.txt", "w") as f:
                        f.write(text)
                        if path.exists(self.path):
                            remove(self.path)
                    return True
                except:
                    continue
        return False
