# Voice Assistant 🤖

A versatile voice-controlled assistant built with Python, designed to perform a variety of tasks through voice commands. Supports natural language interaction, web services integration, system controls, and more.

![Demo](https://img.shields.io/badge/Demo-Coming_Soon-blue) 
[![Python](https://img.shields.io/badge/Python-3.8%2B-green)](https://www.python.org/)

## Features ✨

- **Natural Interaction**: Ask questions, get Wikipedia summaries, and receive Google search results.
- **Web Browsing**: Open websites, YouTube videos, Google searches, and more.
- **Entertainment**: Play music, tell jokes, find movies, and fetch quotes.
- **Productivity**: 
  - Set reminders, alarms, and timers.
  - Manage notes and to-do lists.
  - Perform calculations and currency conversions.
- **System Control**:
  - Adjust volume, brightness, and screen locking.
  - Check battery status, CPU/memory usage, and system uptime.
  - Shutdown, restart, or sleep the system.
- **Customization**: Switch between male/female voices and customize speech rate.

## Prerequisites 📋

- **Python 3.8+**
- **Libraries**:
  ```bash
  pip install pyttsx3 speechrecognition wikipedia pywhatkit requests pyjokes forex-python python-dotenv pyautogui psutil speedtest-cli yfinance

. Windows OS (due to win32com dependency).
. API keys for:
  -OpenWeatherMap (weather data).
  -NewsAPI (news headlines).

Installation
1. Clone the repository:
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
2. Install dependencies:
   pip install -r requirements.txt

Usage 
-Run the script: python voice_assistant.py

Example Commands:

1.Basic Interaction:
 "Hello", "What's your name?", "Switch to female voice"

2.Web & Media:
 "Open YouTube", "Play music", "Search for cat images"

3.Productivity:
 "Set a reminder", "Add a note", "What's the weather in London?"

4.System Control:
 "Lock the screen", "Increase volume", "Check battery status"

Customization ⚙️
  -Voice Switching: Say "Switch voice" to toggle between male/female voices (if available).

  -API Integration: Modify the code to add more services (e.g., Spotify, Gmail).


  Made with ❤️ by DIpesh. Powered by Python and awesome open-source libraries.

---

**Notes**:
1. Replace `yourusername` in the clone URL with your GitHub username.
2. Add a `requirements.txt` file listing all dependencies.
3. Include a `LICENSE` file in your repository.
4. For a demo, add a screen recording or GIF under a "Demo" section.
