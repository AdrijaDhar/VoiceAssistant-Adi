# **Voice Assistant - Adi**  

Adi is a **voice-controlled personal assistant** designed to perform a wide range of tasks using **Natural Language Processing (NLP)** and **Machine Learning (ML)** models. It allows seamless interaction via **voice or text input** and integrates with both **MacOS applications and online services** to provide a personalized experience. With capabilities like **task automation, music playback, translations, news reading, email management, and reminders**, Adi aims to simplify daily activities.

---

## **Features**

### 1. **Voice and Text Input Support**  
- Supports both **spoken and typed commands** for interaction.
- Uses **SpeechRecognition** to capture and understand voice input.

### 2. **Task Automation**  
- Automates system-level commands such as **adjusting brightness, controlling volume, shutdown, restart, lock screen,** and more.
- Designed with **MacOS automation** for smooth execution of commands.

### 3. **Music Playback**  
- Plays music on **Spotify** and **YouTube** based on user preference.
- Uses **Spotipy API** to control Spotify and **web scraping** for YouTube playback.

### 4. **Web Search and Application Launching**  
- Performs **Google searches** for user queries.
- Launches installed Mac apps with **system-level commands**.

### 5. **Email and Notification Management**  
- Uses the **Google API** to read **unread emails aloud**.
- Retrieves and reads recent **MacOS notifications**.

### 6. **Weather and Time Updates**  
- Provides real-time **weather** and **time updates** using the **OpenWeatherMap API** and **World Time API**.

### 7. **Reminder Setting**  
- Creates reminders directly on the **Mac Calendar app** via voice input for efficient task management.

### 8. **News Reader and Morning Briefing**  
- Fetches top news headlines from **NewsAPI** and provides **morning briefings** summarizing key stories.

### 9. **Translation Support**  
- Translates text and spoken input between supported languages using **LibreTranslate**.
- Provides both **spoken and displayed translations**.

---

## **Machine Learning Models Used**

### 1. **Natural Language Processing (NLP)**  
- **SpaCy**: Used for **intent recognition and entity extraction**. The assistant processes **user queries** with advanced tokenization and dependency parsing.
- **BERT-based Models**: Implements **BERT for Sequence Classification** via Hugging Face’s library to enhance **contextual understanding**.

### 2. **Sentiment and Emotion Detection (Planned Feature)**  
- Integration with **VADER sentiment analysis** and **BERT models** to detect and respond empathetically to user emotions.

### 3. **Translation Models (Future Integration)**  
- Planning to integrate **MarianMT** models from Hugging Face to enable **offline translations** without API dependencies.

---

## **Technologies Used**

1. **Python**: Core programming language used across the project.
2. **SpeechRecognition**: Captures and interprets spoken input.
3. **gTTS**: Converts text responses into **speech output**.
4. **Spotipy API**: Integrates with **Spotify** for music playback.
5. **Google APIs**: Manages **email and notifications**.
6. **LibreTranslate**: Provides **translation services**.
7. **NewsAPI**: Fetches **news updates**.
8. **OpenWeatherMap API**: Provides **weather information**.
9. **World Time API**: Fetches **time updates** for any location.

---

## **Setup Instructions**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AdrijaDhar/VoiceAssistant-Adi.git
   cd VoiceAssistant-Adi
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys:**
   - Add **Spotify, NewsAPI, OpenWeatherMap, and Google API** credentials in the `config/` folder.
   - Example: Save your Spotify credentials in `config/spotify_credentials.json`.

4. **Run the Assistant:**
   ```bash
   python3 main.py
   ```
