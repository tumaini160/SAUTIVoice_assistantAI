from django.shortcuts import render
from django.http import HttpResponse
import speech_recognition as sr
import os
import webbrowser
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_protect



@csrf_protect
@requires_csrf_token
@csrf_exempt

def voice_assistant(request):
    if request.method=='POST':
        voice_input=request.POST.get('voice_input','')#get user's voice input from form

        voice=sr.Recognizer()#speech recognition on user's voice
        with sr.Microphone()as source:#microphone is used as audio source
            voice.adjust_for_ambient_noise(source)
            audio_data=voice.listen(source)
        try:
            voice_input=voice.recognize_google(audio_data)
        except sr.UnknownValueError:
            voice_input='Sorry, i did not understand that'
        except sr.RequestError:
            voice_input='Sorry, my speech service is down'
        
        #perform actions based on user's voice input
        if "website" in voice_input:#get website name from user's command
            web=voice_input.split()[-2]
            webbrowser.open("https://" + web + ".com")#open website
            response="opening" + web
        elif "open" in voice_input and ("file" in voice_input or "folder"in voice_input):
            file=voice_input[:]#get file/folder name from user's command
            os.startfile(file)#open folder/file
            response=f"opening {file}"  
        elif "play" in voice_input and ("video" in voice_input or "audio" in voice_input or "song" in voice_input or "lyrics"):
            data=voice_input[1:]#get video/audio/song name from user's command
            webbrowser.open(f"https://www.google.com/search?q={data}" + "/")#open video/audio/song in browser
            response=f"opening {data}" 
        elif ("what" in voice_input or "how" in voice_input or "when" in voice_input or "where" in voice_input):
            question=voice_input.split() #get question name from user's command
            webbrowser.open(f"https://www.google.com/search?q={question}" + "/")#open question in browser
            response=f"opening {question}" 
        elif "" in voice_input:
            word=voice_input[:]
            webbrowser.open(f"https://www.google.com/search?q={word}")
            response=f"opening {word}"  
        else:
            response="Sorry, i did not understand!"
        
        context={'voice_input':voice_input, 'response':response}
        return render(request,'voice_ass.html',context)
    else:
        return render(request,"voice_ass.html")
