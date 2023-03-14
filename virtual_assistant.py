import tkinter as tk
import pyttsx3
import speech_recognition as sr
import webbrowser
import wikipedia
import pyautogui
import cv2
import os
import pygame
from pygame.locals import *
import random
from pynput import keyboard
import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests

# Initialize the speech engine
engine = pyttsx3.init()

# Create the main window
root = tk.Tk()
root.geometry("800x800")
root.title("Virtual Assistant")

# Create the text box to display the conversation
conversation_box = tk.Text(root, height=15, width=50)
conversation_box.pack()

# Create the function to recognize speech and display it in the text box
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        conversation_box.insert(tk.END, "You: " + text + "\n")
        respond(text)
    except:
        conversation_box.insert(tk.END, "Error: Unable to recognize speech.\n")

# Create the function to respond to user input
def respond(text):
    if text == "what's your name":
        conversation_box.insert(tk.END, "Virtual Assistant: My name is Nhat dep trai , i am a botchat create by nhat!\n")
        engine.say(" My name is Nhat dep trai , i am a botchat create by nhat!")
        engine.runAndWait()
    if text == "hello" or text=="hi":
        conversation_box.insert(tk.END, "Virtual Assistant: Hello!\n")
        engine.say("Hello!")
        engine.runAndWait()
    elif text == "how are you":
        conversation_box.insert(tk.END, "Virtual Assistant: I'm doing well, thank you. How can I help you?\n")
        engine.say("I'm doing well, thank you. How can I help you?")
        engine.runAndWait()
    elif "open youtube" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Opening Youtube...\n")
        engine.say("Opening Youtube")
        engine.runAndWait()
        webbrowser.open_new("https://www.youtube.com/")
    elif "open google" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Opening Google...\n")
        engine.say("Opening Google")
        engine.runAndWait()
        webbrowser.open_new("https://www.google.com/")
    elif "open facebook" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Opening Facebook...\n")
        engine.say("Opening Facebook")
        engine.runAndWait()
        webbrowser.open_new("https://www.facebook.com/")
    elif "learn something through wiki" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: What do you want to learn?\n")
        engine.say("What do you want to learn?")
        engine.runAndWait()
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            results = wikipedia.summary(query, sentences=2)
            conversation_box.insert(tk.END, "Virtual Assistant: " + results + "\n")
            engine.say(results)
            engine.runAndWait()
        except:
            conversation_box.insert(tk.END, "Error: Unable to recognize speech.\n")
    elif "take a screenshot" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Taking a screenshot...\n")
        engine.say("Taking a screenshot")
        engine.runAndWait()
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        img = cv2.imread("screenshot.png")
        cv2.imshow("Screenshot", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif "take a photo" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Opening camera...\n")
        engine.say("Opening camera")
        engine.runAndWait()
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        cv2.imwrite("photo.png", frame)
        conversation_box.insert(tk.END, "Virtual Assistant: Photo taken!\n")
        engine.say("Photo taken!")
        engine.runAndWait()
        # Show the photo just taken
        photo_window = tk.Toplevel(root)
        photo_window.title("Photo")
        photo = tk.PhotoImage(file="photo.png")
        photo_label = tk.Label(photo_window, image=photo)
        photo_label.pack() 
    elif "open word" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Opening Word...\n")
        engine.say("Opening Word")
        engine.runAndWait()
        os.system("start winword") # open Microsoft Word

    elif "open game" in text or "play game" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: Opening project...\n")
        engine.say("Opening project")
        engine.runAndWait()
        #tham số hình dạng
        size = width, height = (800, 800)
        road_w = int(width/1.6)
        roadmark_w = int(width/80)
        # tham số vị trí
        right_lane = width/2 + road_w/4
        left_lane = width/2 - road_w/4
        # tham số hoạt hình
        speed = 1
        pygame.init()
        running = True
        screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Mariya's car game")
        car = pygame.image.load("car1.png")
        car_loc = car.get_rect(center=(right_lane, height*0.8))
        car2 = pygame.image.load("otherCar1.png")
        car2_loc = car2.get_rect(center=(left_lane, height*0.2))
        high_score = 0
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        counter = 0
        while running:
            counter += 1
            if counter == 5000:
                speed += 0.5
                counter = 0
                print("level up", speed)
            car2_loc[1] += speed
            if car2_loc[1] > height:
                if random.randint(0,1) == 1:
                    car2_loc.center = left_lane, -200
                else:
                    car2_loc.center = right_lane, -200
            if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 250:
                high_score = max(high_score, counter)
                print("GAME OVER! YOU LOST! Your Score : ",counter)
                print("High Score : ", high_score)
                running = False
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        running = True
                        counter = 0
                        car2_loc[1] = height*0.2
            screen.fill((60, 220, 0))
            replay_text = myfont.render('Replay', False, (0, 0, 0))
            replay_rect = replay_text.get_rect(center=(width / 2, height / 2))
            screen.blit(replay_text, replay_rect)
            pygame.draw.rect(screen,(50, 50, 50),(width/2-road_w/2, 0, road_w, height))
            pygame.draw.rect(screen,(255, 240, 60),(width/2 - roadmark_w/2, 0, roadmark_w, height))
            pygame.draw.rect(screen,(255, 255, 255),(width/2 - road_w/2 + roadmark_w*2, 0, roadmark_w, height))
            pygame.draw.rect(screen,(255, 255, 255),(width/2 + road_w/2 - roadmark_w*3, 0, roadmark_w, height))
            screen.blit(car, car_loc)
            screen.blit(car2, car2_loc)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False 
                if event.type == KEYDOWN:
                    if event.key in [K_a, K_LEFT]:
                        car_loc = car_loc.move([-int(road_w/2), 0])
                        if car_loc.centerx<=left_lane:
                            car_loc.centerx = left_lane
                    if event.key in [K_d, K_RIGHT]:
                        car_loc = car_loc.move([int(road_w/2), 0])
                        if car_loc.centerx>=right_lane:
                            car_loc.centerx = right_lane
        pygame.quit()

    elif "keyboard" in text or "keyboard recording" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: recording keyboard...\n")
        engine.say("Recording")
        engine.runAndWait()
        def on_press(key):
            if key == keyboard.Key.enter:
                with open("keys.txt", "a") as f:
                    f.write("Enter\n")
            elif key == keyboard.Key.backspace:
                with open("keys.txt", "a") as f:
                    f.write("Delete\n")
            else:
                with open("keys.txt", "a") as f:
                    f.write(f"{key}\n")
        def on_release(key):
            if key == keyboard.Key.esc:
                return False
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    elif "weather" in text or "how about today" in text:
        conversation_box.insert(tk.END, "Virtual Assistant: The Weather today ...\n")
        engine.say("Opening Weather today")
        engine.runAndWait()
        def get_weather_data(location):
            USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
            url = f'https://www.google.com/search?q=weather+{location.replace(" ","")}'
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            html = session.get(url)
            soup = bs(html.text, "html.parser")
            name = soup.find("div", attrs={'id': 'wob_loc'}).text
            time = soup.find("div", attrs={'id': 'wob_dts'}).text
            weather = soup.find("span", attrs={'id': 'wob_dc'}).text
            temp = soup.find("span", attrs={'id': 'wob_tm'}).text
            return name, time, weather, temp
        weather_column = sg.Column([[sg.Image('',key = '-IMAGE-', background_color = '#FFFFFF',)]],key = '-LEFT-',background_color = '#FFFFFF')
        info_column = sg.Column([[sg.Text('', key = '-LOCATION-', font = 'Calibri 30', background_color = '#FF0000', pad = 0, visible = False)],[sg.Text('', key = '-TIME-', font = 'Calibri 16', background_color = '#000000', text_color = '#FFFFFF', pad = 0, visible = False)],[sg.Text('', key = '-TEMP-', font = 'Calibri 16', pad = (0,10), background_color = '#FFFFFF', text_color = '#000000', justification = 'center', visible = False)]],key = '-RIGHT-',background_color = '#FFFFFF')
        main_layout = [[sg.Input(key = '-INPUT-',expand_x = True),sg.Button('submit', button_color = '#000000')],[weather_column,info_column]]
        sg.theme('reddit')
        window = sg.Window('Weather', main_layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'submit':
                name, time, weather, temp = get_weather_data(values['-INPUT-'])
                window['-LOCATION-'].update(name, visible = True)
                window['-TIME-'].update(time.split(' ')[0], visible = True)
                window['-TEMP-'].update(f'{temp} \u2103 ({weather})', visible = True)
                if weather in ('Sun','Sunny','Clear','Clear with periodic clouds', 'Mostly sunny'):
                    window['-IMAGE-'].update('symbols/sun.png')
                if weather in ('Partly Sunny','Mostly Sunny','Partly cloudy','Mostly cloudy','Cloudy','Overcast'):
                    window['-IMAGE-'].update('symbols/part sun.png')
                if weather in ('Rain','Chance of Rain','Light Rain','Showers','Scattered Showers','Rain and Snow','Hail'):
                    window['-IMAGE-'].update('symbols/rain.png')
                if weather in ('Scattered Thunderstorms','Chance of Storm','Storm','Thunderstorm','Chance of TStorm'):
                    window['-IMAGE-'].update('symbols/thunder.png')
                if weather in ('Mist','Dust','Fog','Smoke','Haze','Flurries'):
                    window['-IMAGE-'].update('symbols/fog.png')
                if weather in ('Freezing Drizzle','Chance of Snow','Sleet','Snow','Icy','Snow Showers'):
                    window['-IMAGE-'].update('symbols/snow.png')
        window.close()

    else:
        conversation_box.insert(tk.END, "Virtual Assistant: Sorry, I didn't understand what you said. Can you please try again?\n")
        engine.say("Sorry, I didn't understand what you said. Can you please try again?")
        engine.runAndWait()

# Create the function to handle the button click event
def on_button_click():
    recognize_speech()

# Create the function to handle the Enter key press event
def on_enter_pressed(event):
    text = input_box.get()
    conversation_box.insert(tk.END, "You: " + text + "\n")
    respond(text)

# Create the label and text box for typing input
input_label = tk.Label(root, text="Type your input:")
input_label.pack()
input_box = tk.Entry(root)
input_box.pack()
input_box.bind("<Return>", on_enter_pressed)

# Create the button to speak
speak_button = tk.Button(root, text="Speak", command=recognize_speech)
speak_button.pack()

# Create the button to type
type_button = tk.Button(root, text="Type", command=lambda: on_enter_pressed(None))
type_button.pack()

# Start the main loop
root.mainloop()
