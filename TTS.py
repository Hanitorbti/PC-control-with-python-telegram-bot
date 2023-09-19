import pyttsx3

def say(text,file=''):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    if file == '':
        engine.say(text)
    else:
        engine.save_to_file(text,file+".wav")
    engine.runAndWait()
