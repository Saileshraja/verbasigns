import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
import cv2
from easygui import buttonbox
import os
import sys
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
import string

def func():
    r = sr.Recognizer()

    # Known phrases mapped to ISL GIFs
    isl_gif = ['any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
               'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
               'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
               'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
               'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
               'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
               'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
               'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
               'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
               'shall we go together tomorrow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
               'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
               'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
               'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahmedabad', 'all', 'april', 'assam', 'august', 'australia', 'baroda', 'banana', 'banaras', 'bangalore',
               'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile', 'dasara',
               'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'february', 'friday', 'fruits', 'glass', 'grapes', 'gujarat', 'hello',
               'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'karnataka', 'kerala', 'krishna', 'liter', 'mango',
               'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
               'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'south africa',
               'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
               'voice', 'wednesday', 'weight']

    alphabet = list(string.ascii_lowercase)

    gif_path = r'C:/Users/suhas/Desktop/project/app/pro/ISL_Gifs'
    letter_path = r'C:/Users/suhas/Desktop/project/app/pro/letters'

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("Listening...")
            audio = r.listen(source)

            try:
                a = r.recognize_google(audio).lower()
                print("You said:", a)

                for c in string.punctuation:
                    a = a.replace(c, "")

                if a in ['goodbye', 'good bye', 'bye']:
                    print("Oops! Time to say goodbye.")
                    sys.exit()

                elif a in isl_gif:
                    class ImageLabel(tk.Label):
                        def load(self, im):
                            if isinstance(im, str):
                                im = Image.open(im)
                            self.loc = 0
                            self.frames = []

                            try:
                                for i in count(1):
                                    self.frames.append(ImageTk.PhotoImage(im.copy()))
                                    im.seek(i)
                            except EOFError:
                                pass

                            try:
                                self.delay = im.info['duration']
                            except:
                                self.delay = 100

                            if len(self.frames) == 1:
                                self.config(image=self.frames[0])
                            else:
                                self.next_frame()

                        def unload(self):
                            self.config(image=None)
                            self.frames = None

                        def next_frame(self):
                            if self.frames:
                                self.loc += 1
                                self.loc %= len(self.frames)
                                self.config(image=self.frames[self.loc])
                                self.after(self.delay, self.next_frame)

                    gif_file = os.path.join(gif_path, f"{a}.gif")
                    if os.path.exists(gif_file):
                        root = tk.Tk()
                        root.title("ISL Animation")
                        root.after(5000, root.destroy)  # Auto-close after 5 seconds
                        lbl = ImageLabel(root)
                        lbl.pack()
                        lbl.load(gif_file)
                        root.mainloop()
                    else:
                        print("GIF file not found for:", a)

                else:
                    print("Phrase not found. Showing letter-by-letter:")
                    for char in a:
                        if char in alphabet:
                            img_file = os.path.join(letter_path, f"{char}.jpg")
                            if os.path.exists(img_file):
                                img = Image.open(img_file)
                                plt.imshow(np.asarray(img))
                                plt.axis('off')
                                plt.draw()
                                plt.pause(0.8)
                                plt.close()
                            else:
                                print(f"Image for {char} not found.")
                        else:
                            continue

            except sr.UnknownValueError:
                print("Sorry, could not understand the audio.")
            except sr.RequestError:
                print("Could not request results; check internet connection.")
            except Exception as e:
                print("Unexpected error:", str(e))

# GUI launcher
while True:
    image = r"C:\Users\sailesh\Desktop\project\app\pro\signlang.png"
    msg = "HEARING IMPAIRMENT ASSISTANT"
    choices = ["Live Voice", "All Done!"]
    reply = buttonbox(msg, image=image, choices=choices)

    if reply == "Live Voice":
        func()
    elif reply == "All Done!":
        print("Thank you for using the ISL Assistant.")
        break
