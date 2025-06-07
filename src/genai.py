import google.generativeai as genai
import PIL.Image
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Canvas
from tkinter import Tk, filedialog
import speech_recognition as sr
from gtts import gTTS


root = Tk()
root.geometry("500x600")#Geometry
root.title("ChatBot")#Title
root.config(bg='#f1fed4')#config meand color and all


def on_click(event):
    if sou_txt.get("1.0", "end-1c") == "Ask me anything":
        sou_txt.delete("1.0", "end-1c")


def on_focus_out(event):
    """Restore the default text if the Text widget is empty."""
    if sou_txt.get("1.0", "end-1c") == "":
        sou_txt.insert("1.0", "Ask me anything")



def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        t=f"{text}"
        sou_txt.delete(1.0,tk.END)
        sou_txt.insert(tk.END,t)
        return text
    except sr.UnknownValueError:
        messagebox.showinfo("Error","Speech recognition could not understand the audio.")
        return ""
    except sr.RequestError as e:
        messagebox.error("Error",f"Could not request results from Google Speech Recognition service; {e}")
        return ""
    

def text_to_speech():
    text=des_txt.get(1.0,tk.END)
    tts = gTTS(text=text, lang="eng", slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")




def select_image_file():
    root = Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user to select an image file using a file dialogue
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    return file_path    

def genai():
    genai.configure(api_key="AIzaSyC3Ldav3lDfnbAq5lnKECj7FP31WXC6CyA")
    model = genai.GenerativeModel("gemini-1.5-flash")
    enter=input("enter prompt: ")
    image_path =select_image_file()

    if os.path.exists(image_path):
        organ = PIL.Image.open(image_path)
        response = model.generate_content([f"{enter}", organ])
    else:
        response = model.generate_content(f"{enter}")

    return response.text



lbl_txt1 = Label(root,text="Gemini",font=("Rage Italic",40),bg='#f1fed4')
lbl_txt2 = Label(root,text="Bot",font=("Century",25),bg='#f1fed4')
lbl_txt1.place(x=100,y=15,height=60,width=250)
lbl_txt2.place(x=295,y=15,height=55,width=60)


#Creating label Source text
sou_txt = Text(root,font=("Times New roman",14), relief="flat")
sou_txt.insert("1.0", "Ask me anything")  # Default message as placeholder
sou_txt.tag_add("placeholder", "1.0", "end")
sou_txt.tag_configure("placeholder", font=("Times New Roman", 14, "italic"), foreground="gray")
sou_txt.place(x=10,y=490,height=100,width=480)  
sou_txt.bind("<FocusIn>", on_click)
sou_txt.bind("<FocusOut>", on_focus_out)


des_txt = Text(root,font=("Times New roman",14),wrap=WORD, relief="flat")
des_txt.place(x=10,y=100,height=385,width=480)


#Button for playing translated text
img2_path="play.png"
img2=PhotoImage(file=img2_path)
playbtn= Button(root,image=img2,command=text_to_speech)
playbtn.place(x=465,y=170,height=20,width=20)


img1_path="voice.png"
img1=PhotoImage(file=img1_path)
voicebtn= Button(root,image=img1,command=recognize_speech)
voicebtn.place(x=435,y=500,height=20,width=20)



img3_path="upload.png"
img3=PhotoImage(file=img3_path)
upldbtn= Button(root,image=img3, command=select_image_file)
upldbtn.place(x=465,y=500,height=20,width=20)

generatebtn = Button(root, justify="center", name="generate", command="genai")
generatebtn.place(x=10,y=500,height=20,width=80)

root.mainloop()