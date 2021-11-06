import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import pyqtSlot
import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage
import os
import webbrowser
import requests, json
from datetime import datetime
from datetime import timedelta
from PyDictionary import PyDictionary
from time import sleep
from pygame import mixer
import random
from google_trans_new import google_translator



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PETER MY ASSISTANT'
        self.left = 400
        self.top = 100
        self.width = 950
        self.height = 550
        self.listener = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.email_list = {
            'john': 'chukschibyke92@gmail.com',
        }
        self.whatnum = {
            'john': '+2348138647575',
            'henry': '+2347011944478'
        }
        self.language = {
            'french': 'fr',
            'english': 'en',
            'polish': 'pl',
            'chinese': 'zh',
            'portuguese': 'pt',
            'spanish': 'es',
            'german': 'de',
            'danish': 'da',
            'igbo': 'ig',
            'yoruba': 'yo'
        }
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        self.API_KEY = "3b191807e7d41a4fc486ce229a53e5ea"

        self.dictionary=PyDictionary()

        self.email_word = ['email', 'mail']
        self.document_word = ['document', 'read']
        self.whatsapp_word = ['schedule', 'message']
        self.browser_word = ['search', 'something', 'google']
        self.weather_word = ['weather', 'location', 'report', 'show']
        self.shut_word = ['shutdown', 'off', 'system']
        self.dictionary_word = ['meaning', 'word', 'dictionary']
        self.end_word = ['worry', 'nothing', 'close']
        self.translation = ['translate', 'language']

        self.positive = ['yes', 'like', 'probably', 'yeah']
        self.negative = ['no', 'think', 'never']
        self.neutral = ['sleep', 'hibernate', 'rest', 'you']

        self.caller = ['james', 'peter', 'there', 'asleep', 'me', 'with']

        self.mixer = mixer
        self.mixer.init()

        self.sad = ["sad", "bad", "not"]
        self.sadmusic = ["ed", "jealous", "joe"]

        self.happy = ["happy", "good", "okay"]
        self.happymusic = ["just", "rema", "tekno"]

        self.inbetween = ["there", "normal", "anything"]
        self.inbetweenmusic = ["vib", "wiz"]

        self.song = ["music", "song", "play"]
        self.endsong = ["stop", "playing", "current"]

        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: #0f0f3d;")
        self.label = QLabel(self)

        image = QImage('toy.png')

        self.label.setPixmap(QPixmap.fromImage(image))


        self.label.setGeometry(30, 50, 555, 400)

        self.label2 = QLabel(self)
        self.label2.setText("HI...... I WAS CREATED BY THE 'GODFATHER' \n"
                            "I AM STILL IN THE DEVELOPMENT PROCESS, SO \n"
                            "DO NOT EXPECT ME TO DO ALL THINGS FOR YOU NOW... \n"
                            "DONT BE LAZY....\n"
                            "AM JUST A DESKTOP ROBOT.................")
        self.label2.setGeometry(390, 100, 550, 200)
        self.label2.setStyleSheet("QLabel"
                                 "{"
                                  "font-size: 20px;"
                                 "color: white;"
                                 "}")

        self.label3 = QLabel(self)
        self.label3.setText("..................GODFATHER SIGNATURE....................")
        self.label3.setGeometry(340, 450, 550, 100)
        self.label3.setStyleSheet("QLabel"
                                  "{"
                                  "color: white;"
                                  "}")

        #setting title of the gui and giving it dimension
        self.setWindowIcon(QIcon("toy.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.show()

        sleep(10)

        self.welcome()

    @pyqtSlot()
    def talk(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_info(self):
        try:
            with sr.Microphone() as source:
                self.listener.adjust_for_ambient_noise(source, duration=3)
                print('listening....')
                # self.listener.energy_threshold = 400
                # self.listener.dynamic_energy_threshold = False
                voice = self.listener.listen(source)
                print("done listening")
                info = self.listener.recognize_google(voice, language='en')
                print(info)
                return info.lower()
        except Exception as ex:
            self.talk("you have a poor internet connection, and i can not function properly"
                      "due to that effect, i am shutting down.")
            quit()

    def send_mail(self, receiver, subject, message):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)

            server.starttls()

            server.login('zlatanchibyke32@gmail.com', 'Zlatan6532')

            email = EmailMessage()
            email['From'] = 'zlatanchibyke32@gmail.com'
            email['To'] = receiver
            email['Subject'] = subject
            email.set_content(message)

            server.send_message(email)
        except:
            self.talk('please check your network connection, and try again')
            self.get_email_info()

    def get_email_info(self):
        self.talk('To whom you want to send email')
        name = self.get_info()
        receiver = self.email_list[name]
        self.talk('What is the subject of your message')
        subject = self.get_info()
        self.talk('Give me the message to send')
        message = self.get_info()

        self.send_mail(receiver, subject, message)

        self.talk('Your email was sent successfully')
        self.talk('Do you want to send more email')

        send_more = self.get_info()

        if any(ele in send_more for ele in self.positive) is True:
            self.get_email_info()
        elif any(ele in send_more for ele in self.negative) is True:
            self.start_me()
        elif any(ele in send_more for ele in self.neutral) is True:
            self.rest()
        else:
            quit()

    def whatsapp(self):
        import pywhatkit

        self.talk('Who am i sending the message to')
        name = self.get_info()
        receiver = self.whatnum[name]
        self.talk('What should i say to your contact')
        message = self.get_info()

        try:
            now = datetime.now()
            b = now + timedelta(minutes=5)
            hour = int(b.strftime("%H"))
            minute = int(b.strftime("%M"))

            pywhatkit.sendwhatmsg(receiver, message, hour, minute)
            self.talk('Your message was delivered')
        except:
            self.talk('check your network connection')
        finally:
            self.talk('can i rest now')
            send_more = self.get_info()

            if any(ele in send_more for ele in self.positive) is True:
                self.rest()
            elif any(ele in send_more for ele in self.negative) is True:
                self.start_me()
            elif any(ele in send_more for ele in self.neutral) is True:
                self.rest()
            else:
                quit()

    def open_doc(self):
        self.talk('what is the name of document you want me to access')
        doc = self.get_info()
        try:
            os.startfile('C:\\Users\\HP\\Documents\\'+doc+'.docx')
        except:
            self.talk('Document was not found')
        finally:
            self.talk('i did that to the best i can, can i rest now')

            send_more = self.get_info()

            if any(ele in send_more for ele in self.neutral) is True:
                self.rest()
            elif any(ele in send_more for ele in self.positive) is True:
                self.rest()
            elif any(ele in send_more for ele in self.negative) is True:
                self.start_me()
            else:
                quit()

    def open_browser(self):
        self.talk('what do you want to look up for')
        word = self.get_info()
        url = "https://www.google.com.tr/search?q={}".format(word)
        try:
            chrome_browser = webbrowser.get("C:/Program Files/Mozilla Firefox/firefox.exe %s")
            chrome_browser.open_new_tab(url)
        except:
            self.talk('please check your network connection')
        finally:
            self.talk('i did that to the best i can, can i rest now')

            send_more = self.get_info()

            if any(ele in send_more for ele in self.neutral) is True:
                self.rest()
            elif any(ele in send_more for ele in self.positive) is True:
                self.rest()
            elif any(ele in send_more for ele in self.negative) is True:
                self.start_me()
            else:
                quit()

    def shutdown_sys(self):
        self.talk('Are you sure you want to shut down your system')

        send_more = self.get_info()

        if any(ele in send_more for ele in self.positive) is True:
            os.system("shutdown /s /t 1")
        elif any(ele in send_more for ele in self.neutral) is True:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif any(ele in send_more for ele in self.negative) is True:
            self.start_me()
        else:
            quit()

    def get_weather(self):
        self.talk('i will give you weather report for your current city, wait let me access the data right away')
        city = "owerri"
        URL = self.BASE_URL + "q=" + city + "&appid=" + self.API_KEY
        try:
            response = requests.get(URL)
            if response.status_code == 200:
                data = response.json()
                main = data['main']

                file = open("weather.txt", "w")

                temperature = str(main['temp'])
                humidity = str(main['humidity'])
                pressure = str(main['pressure'])

                report = data['weather']
                report = str(report[0]['description'])

                file.write('........' + city + '..........\n'
                            'Temperature: ' + temperature + '\n'
                            'Humidity: ' + humidity + '\n'
                            'Pressure: ' + pressure + '\n'
                            'Report: ' + report)
                file.close()
                os.startfile('C:\\Users\\HP\\PycharmProjects\\pyqtgui\\assistance\\weather.txt')
            else:
                self.talk('Can not get weather data at this time. please check your internet connection')
        except:
            self.talk('Can not get weather data at this time. please check your internet connection')
        finally:
            self.talk('i did that to the best i can, can i rest now')

            send_more = self.get_info()

            if any(ele in send_more for ele in self.positive) is True:
                self.rest()
            elif any(ele in send_more for ele in self.neutral) is True:
                self.rest()
            elif any(ele in send_more for ele in self.negative) is True:
                self.start_me()
            else:
                quit()

    def getwordmeaning(self):
        x = 1
        y = 1
        self.talk('give me the word to help you get the meaning')
        word = self.get_info()
        try:
            word = self.dictionary.meaning(word)

            noun = word['Noun']
            verb = word['Verb']

            if len(noun) > 0:
                wordlen = str(len(noun))
                self.talk('Your word as a noun')
                self.talk('i have found ' + wordlen + ' different meanings of your word')
                for a in noun:
                    x = str(x)
                    self.talk(x + " " + a)
                    x = int(x)
                    x += 1

            if len(verb) > 0:
                wordlen = str(len(verb))
                self.talk('Your word as a verb')
                self.talk('i have found ' + wordlen + ' different meanings of your word')
                for a in noun:
                    y = str(y)
                    self.talk(y + " " + a)
                    y = int(y)
                    y += 1
        except:
            self.talk('please check your internet connection')
        finally:
            self.talk('you want to get the meaning of another word')

            send_more = self.get_info()

            if any(ele in send_more for ele in self.positive) is True:
                self.getwordmeaning()
            elif any(ele in send_more for ele in self.negative) is True:
                self.start_me()
            elif any(ele in send_more for ele in self.neutral) is True:
                self.rest()
            else:
                quit()

    def musicplay(self):
        self.talk("Tell me, are you feeling sad or happy, let me know what music to play for you")
        user = self.get_info()
        if any(ele in user for ele in self.sad) is True:
            song = random.choice(self.sadmusic)
            try:
                self.mixer.music.load(song+".mp3")
                self.mixer.music.play()
                while self.mixer.music.get_busy():
                    sleep(1)
            except:
                self.talk('Am sorry i Could not find a suitable music for you')
            finally:
                self.talk('i think i will rest now')
                self.rest()
        elif any(ele in user for ele in self.happy) is True:
            song = random.choice(self.happymusic)
            try:
                self.mixer.music.load(song+".mp3")
                self.mixer.music.play()
                while self.mixer.music.get_busy():
                    sleep(1)
            except:
                self.talk('Am sorry i Could not find a suitable music for you')
            finally:
                self.talk('i think i will rest now')
                self.rest()
        elif any(ele in user for ele in self.inbetween) is True:
            song = random.choice(self.inbetweenmusic)
            try:
                self.mixer.music.load(song+".mp3")
                self.mixer.music.play()
                while self.mixer.music.get_busy():
                    sleep(1)
            except:
                self.talk('Am sorry i Could not find a suitable music for you')
            finally:
                self.talk('i think i will rest now')
                self.rest()
        else:
            self.talk('Am sorry i Could not find a suitable music for you')
            self.talk('i think i will rest now')
            self.rest()

    def stopsong(self):
        if self.mixer.music.get_busy():
            self.mixer.stop()
            self.mixer.quit()
            self.talk('i think i will rest now')
            self.rest()
        else:
            self.talk('no music is currently playing, i think i will rest now')
            self.rest()

    def translateword(self):
        self.talk("What can i translate for you")
        user = self.get_info()
        self.talk("What language would you want to be translated to")
        receiver = self.get_info()
        langinput = self.language[receiver]
        translator = google_translator()
        self.talk("i will translate that in a minute")
        try:
            translate_text = translator.translate(user, lang_tgt=langinput)
            print(translate_text)
            self.talk(translate_text)
        except:
            self.talk('please check your internet connection')
        finally:
            self.talk('Do you want to try again')
            send_more = self.get_info()

            if any(ele in send_more for ele in self.positive) is True:
                self.translateword()
            elif any(ele in send_more for ele in self.negative) is True:
                self.start_me()
            elif any(ele in send_more for ele in self.neutral) is True:
                self.rest()
            else:
                quit()


    def rest(self):
        self.talk('i would be silent for now until i get a request')
        silent = True
        while silent:
            user = self.get_info()
            if any(ele in user for ele in self.caller) is True:
                self.talk('am here, you just woke me up')
                break
        self.start_me()

    def welcome(self):
        self.talk('I am Peter or you can call me James your assistant, and i am here to help you')
        self.talk('I can send emails, open word document, schedule messages,'
                  ' search things in google, get weather information, play music, shut system down,'
                  'i could give you meanings of a word and i can translate something for you to another language.')
        self.start_me()

    def start_me(self):
        self.talk('Okay, what can i do for you at the moment')
        userinput = self.get_info()

        if any(ele in userinput for ele in self.email_word) is True:
            self.get_email_info()
        elif any(ele in userinput for ele in self.document_word) is True:
            self.open_doc()
        elif any(ele in userinput for ele in self.whatsapp_word) is True:
            self.whatsapp()
        elif any(ele in userinput for ele in self.browser_word) is True:
            self.open_browser()
        elif any(ele in userinput for ele in self.weather_word) is True:
            self.get_weather()
        elif any(ele in userinput for ele in self.shut_word) is True:
            self.shutdown_sys()
        elif any(ele in userinput for ele in self.dictionary_word) is True:
            self.getwordmeaning()
        elif any(ele in userinput for ele in self.song) is True:
            self.musicplay()
        elif any(ele in userinput for ele in self.endsong) is True:
            self.stopsong()
        elif any(ele in userinput for ele in self.translation) is True:
            self.translateword()
        elif any(ele in userinput for ele in self.end_word) is True:
            quit()
        else:
            quit()






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())