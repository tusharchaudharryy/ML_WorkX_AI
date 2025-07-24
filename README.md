# MLWorkX.AI - Your Voice-Driven Intelligent Assistant  

Welcome to **MLWorkX.AI**, an open-source voice-driven personal assistant designed to perform general queries, fetch real-time information, automate tasks, and even generate images — all through a friendly graphical interface. Whether you need web search results, task automations, or conversational AI, ELI.AI has got you covered.

---

##  Features

- **Conversational Chatbot**: Built on Google Gemini and Cohere, ELI.AI maintains a chat log and context to hold meaningful multi-turn conversations.
- **Real-Time Data Fetch**: When asked for up-to-date info (weather, news, etc.), it seamlessly queries online sources.
- **Task Automation**: Integrates with system utilities (open/close apps, play media, typing scripts) via a workflow engine.
- **Voice Interaction**: Uses `speech_recognition` for voice input and `edge-tts` / `pyttsx3`-style output for natural responses.
- **Image Generation**: Generates images on demand through a dedicated module (powered by OpenAI’s image APIs).
- **Modular Architecture**: Clear separation between Frontend (GUI), Backend (logic, speech, automation), and Data (chat logs).

---

## 🏗 Architecture Overview

```text
+-----------+      +---------------+      +--------------+
|  Frontend | <--> |   Main Logic  | <--> |  Backend      |
|  (GUI)    |      |  (Main.py)    |      |  modules:     |
+-----------+      +---------------+      |  - brain_core |
                                              - live_info_fetcher
                                              - workflow_engine
                                              - voice_input_processor
                                              - smart_assistant
                                              - voice_output_synth
                                              - image_generation
                                         +--------------+
                                         |   Data (logs)|
                                         +--------------+
```

1. **Frontend/GUI**: Handles the user interface, displays chat bubbles, microphone and assistant status.
2. **Main.py**: Orchestrates threads for listening, decision-making (DMM), and response generation.
3. **Backend Modules**:
   - **Brain Core**: Decision-making module (FirstLayerDMM) to classify queries.
   - **Live Info Fetcher**: Performs real-time web searches when needed.
   - **Workflow Engine**: Executes automations for commands like `open`, `play`, etc.
   - **Voice I/O**: `SpeechRecognition` for microphone input and `TextToSpeech` for spoken replies.
   - **ImageGeneration**: Spawns a subprocess to create images if requested.
4. **Data Folder**: Stores `ChatLog.json` and intermediate `.data` files to maintain context.

---

## ⚙️ Prerequisites

- **Python 3.9+**
- A valid **Google Gemini API Key** (for Gemini_Chatbot module)
- (Optional) **Cohere API Key** if using Cohere-backed components
- Windows, macOS, or Linux with microphone and speakers

---

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/tusharchaudharryy/ELI.AI.git
cd ELI.AI

# Create a virtual environment (recommended)
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r Requirements.txt
```

---

## 🔐 Configuration

1. **Create a `.env` file** in the project root with your credentials:

```text
# .env
USERNAME=YourName
ASSISTANT_NAME=ELI
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here  # if using Cohere
```

2. **Set up chat log** (automatically initialized on first run):
   - `Data/ChatLog.json` will be created if missing.
   - Intermediate files are stored in a temp directory automatically.

---

## ▶️ Usage

```bash
python Main.py
```

- The GUI will launch. Click the mic icon or press your configured hotkey to speak.
- Chat interactions appear on screen; responses are also spoken aloud.
- Ask general questions, request web searches, or trigger automations (e.g., "open browser", "play video").
- To generate an image, say something like "generate an image of a sunset over mountains".

---

## 📂 Project Structure

```text
ELI.AI/
├── Backend/                 # Core logic modules
├── Data/                    # Chat logs and temp data
├── Frontend/                # GUI and assets
├── Main.py                  # Entry point
├── Gemini_Chatbot.py        # Gemini-based chatbot module
├── Requirements.txt         # Python dependencies
├── .gitignore
└── .env.sample              # Template for environment variables
```

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests:

```bash
# Fork the repo
git checkout -b feature/my-feature
git commit -m "feat: add amazing feature"
git push origin feature/my-feature
# Open a Pull Request
```

Please follow the existing code style and write tests where applicable.

---

> Built with by Tushar Chaudhary. Feel free to reach out with questions or feedback!
