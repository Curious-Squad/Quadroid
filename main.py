import openai
import speech_recognition as sr
import time
from playsound import playsound
import os
from Functions.speak_text import speak_text
 
x=0 #a flag to check if control is out of assistant
ll=[]
go=False # to check if wake up call is done
c1=False #to allow first question after wake up call
sleep=False
# Initialize OpenAI API
openai.api_key = "OPENAI_API_KEY"  #ENTER YOUR OPENAI_API_KEY HERE

mss=[{'role':'system','content':'you are a smart ai assistant and your name is Quadroid ,and you are created by KV Number 1 Saltlake Curious Squad, and you are to help humans day to day life'}]

def generate_response(prompt):
    
    mss.append(
        {"role": "user", "content": prompt},
    )
    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=mss
    )
    reply = chat.choices[0].message.content
    mss.append({"role": "assistant", "content": reply})
    return reply

def plays(soundfile):
    sound_file = os.path.join(os.path.dirname(__file__), 'sound effect', soundfile)
    playsound(sound_file)

def main():
    global go
    global c1
    global x
    global sleep
    while True:
        tt=time.time()
        if go == False:
         if x == 0:
             print()
             plays("response.wav")
         with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            x=1
        try:
            if go == False:
             transcription = recognizer.recognize_google(audio)
        
             if "hey" in transcription.lower() :  
                plays("wake-up.mp3")
                go=True
                c1=True
                tt1=time.time() 
                #time.sleep(2)
                
            while go: 
                plays("interface.mp3") 
                print()
                print("Say Something...")
                speak_text("Say Something")
                
                x=0  
                filename = os.path.join(os.path.dirname(__file__), "input.wav")
                   
                with sr.Microphone() as source:
                 recognizer = sr.Recognizer()
                 source.pause_threshold = 60
                 audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)

                 with open(filename, "wb") as f:
                     f.write(audio.get_wav_data())
                audio_file= open(filename, "rb")
                transcript = openai.Audio.translate("whisper-1", audio_file)
                text=transcript["text"]
                print("tttex",tt-time.time())

                if text == "Thank you." :
                    speak_text("You're welcome! Feel free to ask if you have any more questions")
                    continue

                elif "sleep" in text.lower():
                    go=False
                    sleep=True
                    print("Going to Sleep..")
                    speak_text("OK, Going to sleep, Call me When You Need Me")   

                elif text:
                    plays("response.wav")
                    tt1=time.time()
                    c1=False
                    print(f"You said: {text}")
                    tt=time.time()

                    # generate the response
                    response = generate_response(text)
                    print(f"Quadroid: {response}")
                    print(tt-time.time())

                    # read response using GPT-3
                    speak_text(response)
                    print("Listening...")

                else:
                    print("You Said Nothing, Please Try Again")
                    speak_text("Please Try Again")
                    continue

        except Exception as e:
                if not sleep:
                    speak_text("Didn't Got That, Please Try Again")
                    print("An error occurred: {}".format(e))

if __name__=="__main__":
    main()