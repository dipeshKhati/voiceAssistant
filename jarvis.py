#import pyttsx3
import win32com.client
from datetime import datetime, timedelta  # Corrected import
import os
import asyncio
import time
import sys
import wikipedia
import webbrowser
import pywhatkit
import speech_recognition as sr
from googlesearch import search  # Corrected import
import requests
import pyjokes  # For jokes
from forex_python.converter import CurrencyRates  # For currency conversion
import smtplib  # For email functionality
import math  # For mathematical operations
import pyautogui  # For controlling the system (such as volume)
import winsound  # For sound notifications
from googletrans import Translator  # For text translation
import pyperclip  # For clipboard functionality
import pyautogui  # For taking screenshots
from PIL import ImageGrab
from win32com.client import constants

import yfinance as yf
import psutil
import json
import speedtest


male_voice_index = None
female_voice_index = None
current_voice_index = 0  # Start with default voice


# Initialize text-to-speech engine
#engine = pyttsx3.init('sapi5')
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[0].id)  # Explicitly set voice
#engine.setProperty('rate', 180)  # Adjust speech rate


#def speak(audio):
   # engine.say(audio)
   # print(audio)
   #engine.runAndWait()

#def speak(audio):
    #print(audio)
    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    #speaker.Speak(audio, 0)

# ====== Modified speak function ======

def initialize_voices():
    global male_voice_index, female_voice_index
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()

    for idx, voice in enumerate(voices):
        description = voice.GetDescription().lower()
        if "david" in description or "male" in description:
            male_voice_index = idx
        elif "zira" in description or "female" in description:
            female_voice_index = idx

    # Set defaults if not found
    if male_voice_index is None and len(voices) > 0:
        male_voice_index = 0
    if female_voice_index is None and len(voices) > 1:
        female_voice_index = 1


# Call this once at startup
initialize_voices()

def speak(audio):
    print(audio)
    try:
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        voices = speaker.GetVoices()

        if current_voice_index < len(voices):
            speaker.Voice = voices[current_voice_index]
            voice_name = voices[current_voice_index].GetDescription()
        else:
            voice_name = "default voice"

        speaker.Rate = 0
        speaker.Volume = 100
        print(f"Using voice: {voice_name}")
        speaker.Speak(audio, 0)

    except Exception as e:
        print(f"Error in speech synthesis: {e}")

# Voice switching function
def switch_voice():
    global current_voice_index
    if current_voice_index == male_voice_index and female_voice_index is not None:
        current_voice_index = female_voice_index
        speak("Switching to female voice")
    elif current_voice_index == female_voice_index and male_voice_index is not None:
        current_voice_index = male_voice_index
        speak("Switching to male voice")
    else:
        speak("Voice switching not available")

def takecommand(timeout=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=timeout)  # Add timeout
        except sr.WaitTimeoutError:
            return None

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in').lower()
        print(f"User said: {query}\n")
        return query
    except sr.UnknownValueError:
        print("No speech detected.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        speak("There was an error processing your request")
        return None

def handle_command(query):
    # Process the query as in the main loop
    if 'shutdown' in query:
        speak("Shutting down system. Goodbye Sir!")
        sys.exit()
    # Add other command checks here...
    else:
        speak(f"Interrupted with command: {query}")

def wishMe():
    hour = datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning Sir!")
    elif 12 <= hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")

    speak("I am your voice assistant. How may I assist you today?")

def answer_question(query):
    try:
        # Clean the query for Wikipedia search
        clean_query = query.replace("what is", "").replace("who is", "").strip()

        # Try Wikipedia first
        results = wikipedia.summary(clean_query, sentences=2, auto_suggest=True)
        return f"According to Wikipedia: {results}"

    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]  # Show first 3 options
        return f"Multiple results found: {', '.join(options)}. Please be more specific."

    except wikipedia.exceptions.PageError:
        # Fallback to Google search with proper parameters
        try:
            search_results = list(search(clean_query, num=1, stop=1, pause=2))  # Corrected parameter name
            if search_results:
                return f"I found this on Google: {search_results[0]}"
            return "Sorry, I couldn't find any relevant information."

        except Exception as e:
            return f"Search error: {str(e)}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

def get_weather(city):
    api_key = "9d707a177816df7adf14b1b7af4d5a0d"  # Replace with your own API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    data = response.json()
    if data['cod'] == 200:
        main = data['main']
        weather = data['weather'][0]['description']
        temperature = main['temp']
        return f"The temperature in {city} is {temperature}°C with {weather}."
    else:
        return "Sorry, I couldn't retrieve the weather for that location."

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def close_camera():
    try:
        os.system("taskkill /f /im WindowsCamera.exe")
        speak("Camera closed successfully.")
    except Exception as e:
        speak("Failed to close the camera.")
        print(f"Error: {e}")

def currency_converter(amount, from_currency, to_currency):
    cr = CurrencyRates()
    converted_amount = cr.convert(from_currency, to_currency, amount)
    return f"{amount} {from_currency} is equal to {converted_amount} {to_currency}."

def send_email(to, subject, message):
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    sender_email = "your_email@example.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to, text)
        server.quit()
        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email. Error: {e}"

def get_news():
    speak("Fetching the latest news for you...")
    api_key = "530f750e863c4e23becce6d8d81467bd"  # Replace with your own API key
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"

    try:
        response = requests.get(url).json()
        # Check if the 'articles' key exists in the response
        if 'articles' in response:
            articles = response['articles']
            for article in articles[:5]:  # Read first 5 articles
                speak(f"Title: {article['title']}")
                speak(f"Description: {article['description']}")
        else:
            speak("Sorry, I couldn't retrieve the news at the moment.")
    except Exception as e:
        speak(f"An error occurred while fetching the news: {str(e)}")

def find_movies_online():
    speak("What movie are you looking for?")
    movie_query = takecommand()
    if movie_query:
        search_results = search(f"watch {movie_query} online free", num=5)
        speak("Here are some results I found:")
        for result in search_results:
            speak(result)
            # Allow user to interrupt after each link
            query = takecommand(timeout=2)  # Listen for 2 seconds
            if query:
                # Process the new command here or break
                speak("Stopping movie search.")
                return  # Exit the function
        speak("Please visit one of these links to watch the movie.")

def calculate_expression(query):
    try:
        # Extract the expression part
        expression = query.replace("calculate", "").strip()

        if not expression:
            speak("Please provide an expression to calculate. Example: 'calculate 5 plus 3'")
            return None

        # Convert natural language terms and symbols to mathematical operators
        expression = expression.replace("plus", "+").replace("add", "+") \
            .replace("minus", "-").replace("subtract", "-") \
            .replace("times", "*").replace("multiply", "*").replace("x", "*") \
            .replace("divided by", "/") \
            .replace("modulo", "%") \
            .replace("power", "**") \
            .replace("^", "**")

        # Remove any non-math characters for security
        allowed_chars = set("0123456789+-*/.%() ")
        cleaned_expression = "".join([c for c in expression if c in allowed_chars])

        if not cleaned_expression:
            raise ValueError("No valid expression found")

        result = str(eval(cleaned_expression))
        return f"The result is {result}"

    except ZeroDivisionError:
        return "Error: Division by zero is not allowed"
    except SyntaxError:
        return "Invalid mathematical expression format. Please use words like 'plus', 'minus', or symbols like +, -, *, /"
    except Exception as e:
        return "Sorry, I couldn't process that calculation. Please try again with a valid expression."

def increase_volume():
    pyautogui.press("volumeup")
    speak("Volume increased.")

def decrease_volume():
    pyautogui.press("volumedown")
    speak("Volume decreased.")

def mute_volume():
    pyautogui.press("volumemute")
    speak("Volume muted.")

def set_reminder():
    speak("What would you like me to remind you about?")
    reminder_text = takecommand()
    speak("In how many minutes should I remind you?")
    reminder_time = takecommand()
    try:
        reminder_minutes = int(reminder_time)
        speak(f"Reminder set for {reminder_text} in {reminder_minutes} minutes.")
        time.sleep(reminder_minutes * 60)
        speak(f"Reminder: {reminder_text}")
    except ValueError:
        speak("Please provide a valid time in minutes.")

def play_alarm_sound():
    speak("Playing alarm sound.")
    winsound.Beep(1000, 2000)  # 1000Hz frequency, 2 seconds duration

def take_screenshot():
    speak("Taking screenshot now.")
    screenshot = ImageGrab.grab()
    screenshot.save("screenshot.png")
    speak("Screenshot saved.")

async def translate_text():  # Make the function async
    speak("What text would you like me to translate?")
    text_to_translate = takecommand()
    if not text_to_translate:
        return
    speak("Which language would you like to translate it to?")
    target_language = takecommand()
    if not target_language:
        return

    translator = Translator()
    try:
        # Assuming translate() is an async method (hypothetical async library)
        translation = await translator.translate(text_to_translate, dest=target_language)
        speak(f"Here is the translation: {translation.text}")
    except AttributeError:
        # Fallback for synchronous libraries (e.g., standard googletrans)
        translation = translator.translate(text_to_translate, dest=target_language)
        speak(f"Here is the translation: {translation.text}")

def get_clipboard_content():
    content = pyperclip.paste()
    speak(f"The clipboard contains: {content}")

def search_images():
    speak("What image would you like to search for?")
    search_query = takecommand()
    if search_query:
        search_results = list(search(f"images of {search_query}"))  # Convert generator to list
        speak("Here are some results I found:")
        for result in search_results[:5]:  # Limit to 5 results
            speak(result)
            # Check for user interruption after each result
            query = takecommand(timeout=2)  # Listen for 2 seconds
            if query:
                speak("Stopping image search.")
                return  # Exit the function to process the new command
        speak("Search completed.")

def search_videos():
    speak("What video would you like to search for on YouTube?")
    search_query = takecommand()
    if search_query:
        webbrowser.open(f"https://www.youtube.com/results?search_query={search_query}")

def tell_time():
    current_time = datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}")

def open_application():
    speak("Which application would you like to open?")
    app_name = takecommand().lower()
    if "chrome" in app_name:
        os.startfile("C:/Program Files/Google/Chrome/Application/chrome.exe")  # Change path as per your system
    elif "notepad" in app_name:
        os.startfile("notepad.exe")
    elif "calculator" in app_name:
        os.startfile("calc.exe")
    else:
        speak("Sorry, I couldn't find the application.")

# New Feature: Stock Price Check
def get_stock_price():
    speak("Please say the stock symbol you want to check.")
    symbol = takecommand()
    if symbol:
        try:
            stock = yf.Ticker(symbol.upper())
            price = stock.info.get("regularMarketPrice")
            if price:
                speak(f"The current price of {symbol.upper()} is {price} dollars.")
            else:
                speak("I couldn't retrieve the price for that symbol.")
        except Exception as e:
            speak("An error occurred while fetching the stock price.")
            print(e)
    else:
        speak("No stock symbol detected.")

# New Feature: Quote of the Day
def get_quote_of_the_day():
    speak("Fetching a quote for you...")
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            quote = data.get("content")
            author = data.get("author")
            speak(f"Here is a quote by {author}: {quote}")
        else:
            speak("Sorry, I couldn't fetch a quote at the moment.")
    except Exception as e:
        speak("An error occurred while fetching a quote.")
        print(e)

# New Feature: Notes Management
NOTES_FILE = "notes.txt"

def add_note():
    speak("What note would you like to add?")
    note = takecommand()
    if note:
        with open(NOTES_FILE, "a", encoding="utf-8") as f:
            f.write(note + "\n")
        speak("Note added.")
    else:
        speak("No note was detected.")

def read_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            notes = f.read()
        if notes.strip():
            speak("Here are your notes:")
            speak(notes)
        else:
            speak("Your notes file is empty.")
    else:
        speak("No notes found. You can add a note by saying 'add note'.")

# New Feature: System Information
def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    speak(f"CPU usage is at {cpu_usage} percent.")
    speak(f"Memory usage is at {memory.percent} percent.")


def adjust_brightness():
    speak("What brightness level would you like to set? (0 to 100)")
    try:
        response = takecommand()
        if not response:
            raise ValueError("No response detected")

        # Extract numerical value from spoken response
        brightness = int(''.join(filter(str.isdigit, response)))

        if 0 <= brightness <= 100:
            os.system(
                f"powershell (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness({brightness},0)")
            speak(f"Screen brightness set to {brightness}.")
        else:
            speak("Please provide a value between 0 and 100.")

    except ValueError as ve:
        if "No response" in str(ve):
            speak("No brightness level detected. Please try again.")
        else:
            speak("Please provide a valid number between 0 and 100.")
    except Exception as e:
        speak("Sorry, I couldn't adjust the brightness. Please check your system settings.")
        print(f"Error: {e}")

# File Management: Create, Delete, List Files
def create_file():
    speak("What would you like to name the new file?")
    file_name = takecommand()
    if file_name:
        with open(file_name + ".txt", "w", encoding="utf-8") as file:
            speak("What content would you like to write in the file?")
            content = takecommand()
            file.write(content)
            speak(f"File {file_name}.txt created with your content.")
    else:
        speak("No file name provided.")

def delete_file():
    speak("What is the name of the file you want to delete?")
    file_name = takecommand()
    try:
        if os.path.exists(file_name + ".txt"):
            os.remove(file_name + ".txt")
            speak(f"File {file_name}.txt deleted.")
        else:
            speak(f"The file {file_name}.txt doesn't exist.")
    except Exception as e:
        speak(f"Error: {e}")

def list_files():
    files = [f for f in os.listdir() if f.endswith('.txt')]
    if files:
        speak("Here are the text files in your directory:")
        for file in files:
            speak(file)
    else:
        speak("No text files found in the current directory.")

# Search for Restaurants near a location
def search_restaurants():
    speak("Please provide your location.")
    location = takecommand()
    if location:
        query = f"restaurants near {location}"
        results = list(search(query, num=5, stop=5, pause=2))
        speak("Here are some restaurants I found:")
        for result in results:
            speak(result)
    else:
        speak("Location not provided.")

# Open Specific Website by name
def open_specific_web_page():
    speak("Please provide the name of the website you would like to open.")
    website_name = takecommand()
    if website_name:
        url = f"http://{website_name}.com"
        webbrowser.open(url)
        speak(f"Opening {website_name} website.")
    else:
        speak("Website name not provided.")

# System Uptime
def system_uptime():
    uptime_seconds = int(time.time() - psutil.boot_time())
    uptime_str = str(timedelta(seconds=uptime_seconds))
    speak(f"The system has been running for {uptime_str}.")

# Battery Status
def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        speak(f"Battery is at {battery.percent} percent and is {'charging' if battery.power_plugged else 'not charging'}.")
    else:
        speak("Battery information is not available.")

def lock_screen():
    """Locks the system screen."""
    speak("Locking the screen.")
    os.system("rundll32.exe user32.dll,LockWorkStation")

def restart_system():
    """Restarts the system."""
    speak("Restarting the system.")
    os.system("shutdown /r /t 1")

def sleep_system():
    """Puts the system to sleep."""
    speak("Putting the system to sleep.")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def get_definition():
    """Fetches the definition of a word using an online dictionary API."""
    speak("Which word would you like defined?")
    word = takecommand()
    if word:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # Fetch the first definition from the first meaning
                definition = data[0]['meanings'][0]['definitions'][0]['definition']
                speak(f"The definition of {word} is: {definition}")
            else:
                speak("Sorry, I couldn't find the definition for that word.")
        except Exception as e:
            speak("An error occurred while fetching the definition.")
            print(e)
    else:
        speak("No word detected.")

# To-Do List Management
TODO_FILE = "todo.json"

def add_task():
    """Adds a new task to the to-do list."""
    speak("What task would you like to add?")
    task = takecommand()
    if not task:
        speak("I did not catch any task.")
        return
    tasks = []
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
        except Exception:
            tasks = []
    tasks.append(task)
    with open(TODO_FILE, "w") as f:
        json.dump(tasks, f)
    speak("Task added.")

def read_tasks():
    """Reads out the current to-do list."""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
            if tasks:
                speak("Your tasks are:")
                for idx, task in enumerate(tasks, start=1):
                    speak(f"Task {idx}: {task}")
            else:
                speak("You have no tasks.")
        except Exception:
            speak("There was an error reading your tasks.")
    else:
        speak("You have no tasks.")

def remove_task():
    """Removes a task from the to-do list based on its number."""
    if os.path.exists(TODO_FILE):
        try:
            with open(TODO_FILE, "r") as f:
                tasks = json.load(f)
            if not tasks:
                speak("You have no tasks to remove.")
                return
            speak("Which task number would you like to remove?")
            task_num = takecommand()
            try:
                index = int(task_num) - 1
                if 0 <= index < len(tasks):
                    removed_task = tasks.pop(index)
                    with open(TODO_FILE, "w") as f:
                        json.dump(tasks, f)
                    speak(f"Removed task: {removed_task}")
                else:
                    speak("Invalid task number.")
            except Exception:
                speak("I didn't catch a valid number.")
        except Exception:
            speak("There was an error processing your tasks.")
    else:
        speak("You have no tasks.")

def open_file_by_name():
    """Opens a file specified by the user (provide full name and extension)."""
    speak("Which file would you like to open? Please provide the full file name with its extension.")
    file_name = takecommand()
    if file_name:
        if os.path.exists(file_name):
            os.startfile(file_name)
            speak(f"Opening {file_name}.")
        else:
            speak("File not found.")
    else:
        speak("I did not catch the file name.")

def check_internet_speed():
    """Checks and reports the internet download and upload speeds."""
    speak("Checking internet speed, please wait.")
    try:
        st = speedtest.Speedtest()
        download_speed = st.download() / 1e6  # Convert to Mbps
        upload_speed = st.upload() / 1e6
        speak(f"Download speed is {download_speed:.2f} Mbps and upload speed is {upload_speed:.2f} Mbps.")
    except Exception as e:
        speak("An error occurred while checking the internet speed.")
        print(e)
# --------------------

if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand()

        if query is None:
            continue

        # Add these voice commands
        elif any(cmd in query for cmd in ['switch voice', 'change voice', 'toggle voice']):
            switch_voice()

        elif 'female voice' in query and female_voice_index is not None:
            current_voice_index = female_voice_index
            speak("Changed to female voice")

        elif 'male voice' in query and male_voice_index is not None:
            current_voice_index = male_voice_index
            speak("Changed to male voice")

        # Process commands
        elif 'wikipedia' in query:
            try:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't find that information.")

        elif 'news' in query:
            get_news()

        elif 'playlist' in query:
            webbrowser.open("https://www.jiosaavn.com/featured/english-top-songs/LdbVc1Z5i9E_")

        elif 'hello' in query or 'hi' in query:
            hour = datetime.now().hour

            if 0 <= hour < 12:
                speak("Good morning! What's the plan for today?")
            elif 12 <= hour < 18:
                speak("Good afternoon! How's your day going?")
            else:
                speak("Good evening! How can I help you?")

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open google' in query:
            speak("What would you like me to search on Google?")
            search_query = takecommand()
            if search_query:
                pywhatkit.search(search_query)

        elif 'play music' in query:
            music_dir = r'C:\Program Files\OneDrive\Desktop\music'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city = takecommand()
            weather_report = get_weather(city)
            speak(weather_report)

        elif 'joke' in query:
            tell_joke()

        elif 'open camera' in query or 'camera' in query:
            try:
                speak("Opening camera.")
                os.system("start microsoft.windows.camera:")
            except Exception as e:
                speak("Sorry, I couldn't open the camera.")
                print(f"Error: {e}")

            # Add this new condition for closing the camera
        elif 'close camera' in query or 'turn off camera' in query:
            close_camera()

        elif 'currency' in query:
            speak("Please provide the amount and currency details.")
            amount = float(input("Enter amount: "))
            from_currency = input("From currency: ")
            to_currency = input("To currency: ")
            conversion_result = currency_converter(amount, from_currency, to_currency)
            speak(conversion_result)

        elif 'send email' in query:
            speak("Please provide the recipient's email address.")
            recipient = takecommand()
            speak("What is the subject of the email?")
            subject = takecommand()
            speak("What is the message for the email?")
            message = takecommand()
            response = send_email(recipient, subject, message)
            speak(response)

        elif 'find movie' in query or 'watch movie' in query:
            find_movies_online()

        elif 'movie' in query:
            pywhatkit.playonyt(" new movie")


        elif 'calculate' in query:

            speak("Please say the mathematical expression you want to calculate")

            expression_query = takecommand(timeout=10)  # Give 10 seconds to respond

            if expression_query:

                result = calculate_expression(expression_query)

                speak(result)

            else:

                speak("No expression detected for calculation")

        elif 'increase volume' in query:
            increase_volume()

        elif 'decrease volume' in query:
            decrease_volume()

        elif 'mute volume' in query:
            mute_volume()

        elif 'set reminder' in query:
            set_reminder()

        elif 'play alarm' in query:
            play_alarm_sound()

        elif 'open photo' in query:
            photo_path = r"C:\Program Files\OneDrive\Pictures\Camera Roll\SHAREit\Picture"
            if os.path.exists(photo_path):
                os.startfile(photo_path)
            else:
                speak("Sorry, the photo directory was not found.")

        elif 'take screenshot' in query:
            take_screenshot()


        elif 'what is your name' in query:
            speak("Sorry, I don't have name, I am here to assist you.")

        elif 'translate' in query:

            asyncio.run(translate_text())

        elif 'clipboard' in query:
            get_clipboard_content()

        elif 'search images' in query or 'search image' in query:
            search_images()

        elif 'search videos' in query or 'search video' in query:
            search_videos()

        elif 'open facebook' in query:
            webbrowser.open("facebook.com")

        elif 'close facebook' in query:
            speak("okay sir, closing facebook")
            os.system("taskkill /f /im msedge.exe")

        elif 'play song' in query:
            pywhatkit.playonyt("top best english song")

        elif 'play nepali song' in query:
            pywhatkit.playonyt("top 10 best nepali songs")

        elif 'close this' in query:
            speak("okay sir, closing ")
            os.system("taskkill /f /im chrome.exe")

        elif 'time' in query:
            tell_time()

        elif 'open application' in query:
            open_application()

        elif 'shutdown' in query or 'power off' in query:
            speak("Shutting down system. Goodbye Sir!")
            time.sleep(1)
            sys.exit()

        # Answer general questions using Google or Wikipedia
        elif 'what is' in query or 'how much money for' in query or 'who is' in query or 'where is' in query or 'when' in query or 'when was' in query or 'work in new zealand' in query or 'yoobee' in query or 'y o o b e e' in query:
            response = answer_question(query)
            speak(response)

            # New commands for added features:
        elif 'stock price' in query:
            get_stock_price()
        elif 'quote' in query:
            get_quote_of_the_day()
        elif 'add note' in query:
            add_note()
        elif 'read notes' in query:
            read_notes()
        elif 'system info' in query:
            get_system_info()

        elif 'adjust brightness' in query:
            adjust_brightness()
        elif 'create file' in query:
            create_file()
        elif 'delete file' in query:
            delete_file()
        elif 'list files' in query:
            list_files()
        elif 'restaurants' in query:
            search_restaurants()
        elif 'open website' in query:
            open_specific_web_page()
        elif 'system time' in query:
            system_uptime()
        elif 'battery status' in query:
            get_battery_status()

        elif 'lock screen' in query:
            lock_screen()

        elif 'restart system' in query:
            restart_system()

        elif 'sleep system' in query or 'hibernate' in query:
            sleep_system()

            # New dictionary/definition feature:
        elif 'define' in query or 'definition' in query:
            get_definition()

            # New to-do list management:
        elif 'add task' in query:
            add_task()

        elif 'read task' in query or 'show task' in query:
            read_tasks()

        elif 'remove task' in query or 'delete task' in query:
            remove_task()

            # New file opener:
        elif 'open file' in query:
            open_file_by_name()

            # New internet speed checker:
        elif 'internet speed' in query or 'check speed' in query:
            check_internet_speed()

        else:
            speak("I didn't understand that command. Could you please repeat?")

