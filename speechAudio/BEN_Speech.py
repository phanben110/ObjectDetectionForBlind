from gtts import gTTS
from playsound import playsound 
from multiprocessing import Process
# This module is imported so that we can 
# play the converted audio
import os

class SpeechAudio(): 
    def __init__(self, text, language='en', pathName="speechAudio"):
        # The text that you want to convert to audio
        self.text = text
        # Language in which you want to convert
        self.language = language
        self.pathName = pathName
        self.fileAudio = None 
        self.myobj = None
    
    def textToAuido(self):
        # Passing the text and language to the engine, 
        # here we have marked slow=False. Which tells 
        # the module that the converted audio should 
        self.myobj = gTTS(text=self.text, lang=self.language, slow=False)
        self.fileAudio = f"{self.pathName}speech.mp3"
        # Saving the converted audio in a mp3 file named
        self.myobj.save(self.fileAudio)

    def playAudio(self): 
        # Playing the converted file
        self.textToAuido()
        playsound(self.fileAudio)
    
    def speech(self):
        # this ussing multiprocessing to run 2 core 
        P = Process(name="playAudio", target=self.playAudio)
        P.start()
if __name__ == "__main__": 
    count = 0 
    while(1): 
        count +=1 
        if count == 1: 
            mytext = 'In front of you are 4 objects, keyboard, cup, mouse, and cellphone.'
            SpeechAudio(mytext,language='en',pathName='').speech()
        if count == 100000: 
            mytext = 'In front of you are 4 objects, keyboard, cup, mouse, and cellphone.'
            SpeechAudio(mytext,language='en',pathName='').speech()
        print (count)
#     
#  
#  
#
#def playAudio():
#    playsound("welcome.mp3")
#def run():
#count = 0 
#while(1):
#    if count == 1: 
#        run()
#    count +=1 
#    print (f"ben dep trai {count}")
