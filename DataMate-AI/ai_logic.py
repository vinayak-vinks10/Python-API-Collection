import os
from dotenv import load_dotenv
import requests
import random
load_dotenv(dotenv_path=".env")   # 👈 YAHI ADD KARNA HAI

# ════════════════════════════════════════════════
#  LOCAL KEYWORD DATABASE
#  If user message matches any keyword → local reply
#  No match → API is called
# ════════════════════════════════════════════════
KEYWORD_DB = {

    "greetings": {
        "keywords": ["hello", "hi", "hey", "hii", "howdy", "sup",
                     "good morning", "good evening", "good night", "greetings"],
        "responses": [
            "Hey! How can I help you today? 😊",
            "Hello! What's on your mind? 🤖",
            "Hi there! Ask me anything 🚀"
        ]
    },

    "how_are_you": {
        "keywords": ["how are you", "how r u", "you okay", "are you fine",
                     "how's it going", "what's up", "all good"],
        "responses": [
            "I'm doing great, thanks for asking! How can I help you? 😄",
            "All systems running perfectly! What do you need? 🤖",
            "Always good! What can I do for you? 😊"
        ]
    },

    "identity": {
        "keywords": ["who are you", "what are you", "your name",
                     "introduce yourself", "are you a bot", "are you ai",
                     "are you human", "what is your name"],
        "responses": [
            "I'm Vinayak's personal AI Assistant! 🤖 Here to answer all your questions.",
            "I'm an AI chatbot built to help you with anything you need! 😊",
            "I'm your smart AI assistant — ask me anything! 🚀"
        ]
    },

    "thanks": {
        "keywords": ["thanks", "thank you", "thank u", "thx", "ty",
                     "appreciate", "helpful", "great job", "well done"],
        "responses": [
            "Happy to help! Let me know if you need anything else 😊",
            "You're welcome! Always here for you 🤖",
            "Glad I could help! Ask away anytime 🙌"
        ]
    },

    "goodbye": {
        "keywords": ["bye", "goodbye", "see you", "see ya", "later",
                     "take care", "gotta go", "cya", "ttyl"],
        "responses": [
            "Goodbye! Come back anytime 👋😊",
            "See you later! Take care 🤖",
            "Bye! Feel free to return whenever you need help 😄"
        ]
    },

    "python": {
        "keywords": ["python", "pip install", "def ", "import ",
                     "indentation error", "syntax error", "python code",
                     "for loop", "while loop", "list", "dictionary", "function"],
        "responses": [
            "Python question! 🐍 Share your code or error and I'll help you fix it.",
            "Happy to help with Python! What's the issue — syntax, logic, or a library? 💻",
            "Python is awesome! Paste your code or describe the problem 🔍"
        ]
    },

    "web_dev": {
        "keywords": ["html", "css", "javascript", "react", "nodejs",
                     "website", "frontend", "backend", "api", "json",
                     "bootstrap", "tailwind", "flexbox"],
        "responses": [
            "Web dev question! 🌐 HTML/CSS/JS — what do you need help with?",
            "Let's build something! Frontend, backend, or full stack? 💻",
            "Web development is my thing! Tell me the issue 🚀"
        ]
    },

    "ai_ml": {
        "keywords": ["machine learning", "deep learning", "neural network",
                     "artificial intelligence", "nlp", "computer vision",
                     "tensorflow", "pytorch", "dataset", "model training",
                     "overfitting", "classification", "regression"],
        "responses": [
            "AI/ML topic! 🧠 What do you want to know — concept or implementation?",
            "Machine learning is fascinating! Theory or code help? 🤖",
            "Great topic! Tell me more about what you're working on 🚀"
        ]
    },

    "math": {
        "keywords": ["math", "maths", "algebra", "calculus", "geometry",
                     "equation", "formula", "percentage", "square root",
                     "probability", "statistics", "trigonometry"],
        "responses": [
            "Math problem? Write it out and I'll solve it! 🔢",
            "I love math! Share the problem 📐",
            "Send the equation or concept — I'll explain it step by step ➕"
        ]
    },

    "jokes": {
        "keywords": ["joke", "funny", "make me laugh", "tell me a joke",
                     "comedy", "humor", "lol", "haha"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs! 😂",
            "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?' 😄",
            "Why was the math book sad? Because it had too many problems! 🤣",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads 😂"
        ]
    },

    "motivation": {
        "keywords": ["motivate me", "feeling low", "sad", "depressed",
                     "give up", "demotivated", "inspire me", "i'm tired",
                     "life advice", "struggling"],
        "responses": [
            "You've got this! Every expert was once a beginner 💪🔥",
            "Hard times are temporary. Keep pushing — your breakthrough is close! 🌟",
            "Believe in yourself. The fact that you're still trying means you haven't lost! 🚀",
            "'It always seems impossible until it's done.' — Nelson Mandela 💡"
        ]
    },

    "weather": {
        "keywords": ["weather", "temperature", "rain", "snow",
                     "sunny", "cloudy", "forecast", "humid", "storm"],
        "responses": [
            "I can't access live weather data 🌤️ Check Google Weather or weather.com!",
            "For real-time weather, try your phone's weather app ⛅",
        ]
    },

    "time_date": {
        "keywords": ["what time", "what is today", "what day", "current date",
                     "what year", "today's date", "what month"],
        "responses": [
            "I don't have access to real-time data ⏰ Check your device for the current time/date!",
            "Your phone or computer will have the exact time and date! 📅"
        ]
    },

    "health": {
        "keywords": ["health", "fitness", "workout", "gym", "diet",
                     "weight loss", "exercise", "yoga", "meditation",
                     "healthy", "calories", "protein"],
        "responses": [
            "Health is wealth! 💪 Need fitness tips, diet advice, or something specific?",
            "Happy to talk health & fitness! What's your goal? 🥗",
            "⚠️ For medical issues, always consult a doctor. For general tips, I'm here! 🏥"
        ]
    },

    "career": {
        "keywords": ["career", "job", "interview", "resume", "cv",
                     "salary", "internship", "fresher", "freelancing",
                     "startup", "promotion", "work from home"],
        "responses": [
            "Career question! 💼 Resume help, interview prep, or career planning?",
            "Let's talk career! What field are you in or aiming for? 🎯",
            "Happy to help with career advice! Tell me more about your situation 🚀"
        ]
    },

    "help": {
        "keywords": ["help", "what can you do", "your features",
                     "how to use", "capabilities", "guide me", "assist me"],
        "responses": [
            "I can help with:\n💻 Coding (Python, JS, Web Dev)\n🧮 Math & Science\n💼 Career Advice\n😄 Jokes\n💪 Motivation\n🌍 General Knowledge\n\nJust ask! 😊",
            "Ask me anything — coding, math, career, jokes, or just a chat! 🤖"
        ]
    },

}


# ════════════════════════════════════════════════
#  MATCHING LOGIC
# ════════════════════════════════════════════════
def find_local_response(message: str):
    msg = message.lower().strip()
    for category, data in KEYWORD_DB.items():
        for keyword in data["keywords"]:
            if keyword in msg:
                return random.choice(data["responses"])
    return None  # No match found


# ════════════════════════════════════════════════
#  API CALL (only when no keyword match)
# ════════════════════════════════════════════════
def call_api(message: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    API_KEY = os.getenv("API_KEY")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Chatbot"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",   # 🔥 MOST STABLE FREE MODEL
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant. Give short and clear answers."},
            {"role": "user", "content": message}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)

        if res.status_code == 200:
            data = res.json()
            return data["choices"][0]["message"]["content"]

        else:
            return f"Error: {res.status_code} - {res.text}"

    except Exception as e:
        return f"Error: {str(e)}"

# ════════════════════════════════════════════════
#  MAIN FUNCTION
# ════════════════════════════════════════════════
def get_response(user_message: str) -> str:
    # Step 1: Try local keyword match first
    local = find_local_response(user_message)
    if local:
        return local

    # Step 2: No match — call API
    return call_api(user_message)