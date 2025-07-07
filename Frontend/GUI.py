from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTextEdit, QLabel, QStackedWidget, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QFont, QMovie
import sys, os

# Load assistant name
try:
    from dotenv import dotenv_values
    env_vars = dotenv_values('.env')
    ASSISTANT_NAME = env_vars.get('AssistantName', 'Assistant')
except:
    ASSISTANT_NAME = 'Assistant'

# Paths
CURRENT_DIR = os.getcwd()
FILES_DIR = os.path.join(CURRENT_DIR, 'Frontend', 'Files')
GIF_DIR = os.path.join(CURRENT_DIR, 'Frontend', 'Graphics')
for d in (FILES_DIR, GIF_DIR): os.makedirs(d, exist_ok=True)
RESP_FILE = os.path.join(FILES_DIR, 'Responses.data')
STATUS_FILE = os.path.join(FILES_DIR, 'Status.data')
MIC_FILE = os.path.join(FILES_DIR, 'Mic.data')

# --- Backend helper functions ---
def SetMicrophoneStatus(state):
    with open(MIC_FILE, 'w', encoding='utf-8') as f: f.write(state)

def GetMicrophoneStatus():
    try: return open(MIC_FILE, 'r', encoding='utf-8').read().strip()
    except: return 'False'

def SetAssistantStatus(status):
    with open(STATUS_FILE, 'w', encoding='utf-8') as f: f.write(status)

def GetAssistantStatus():
    try: return open(STATUS_FILE, 'r', encoding='utf-8').read().strip()
    except: return 'Available ...'

def ShowTextToScreen(text):
    with open(RESP_FILE, 'w', encoding='utf-8') as f: f.write(text)

def TempDirectoryPath(filename):
    return os.path.join(FILES_DIR, filename)

def AnswerModifier(answer):
    return '\n'.join([line for line in answer.split('\n') if line.strip()])

def QueryModifier(query):
    q = query.lower().strip()
    questions = ["how","what","where","when","why","which","whose","whom","can you","what's","where's","how's"]
    if any(w in q for w in questions):
        if q[-1] not in ['?','.','!']: q += '?'
    else:
        if q[-1] not in ['.','!','?']: q += '.'
    return q.capitalize()

# --- GUI Components ---
class NavPanel(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.mic_on = True
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(100)
        SetMicrophoneStatus('True')

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        # Title + Alexa ring
        title_layout = QHBoxLayout()
        title = QLabel(f"🔮 {ASSISTANT_NAME} AI")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        gif_icon = QLabel()
        alexa_movie = QMovie(os.path.join(GIF_DIR, 'alexa_ring.gif'))
        alexa_movie.setScaledSize(QSize(24,24))
        gif_icon.setMovie(alexa_movie); alexa_movie.start()
        title_layout.addWidget(gif_icon)
        title_layout.addWidget(title)
        title_layout.addStretch(1)
        layout.addLayout(title_layout)
        # Nav buttons
        for name, idx in [("🏠 Home",0),("💬 Chat",1)]:
            btn = QPushButton(name)
            btn.setFixedHeight(36)
            btn.setStyleSheet("text-align: left; padding-left:10px;")
            btn.clicked.connect(lambda _, i=idx: self.stack.setCurrentIndex(i))
            layout.addWidget(btn)
        layout.addStretch(1)
        # Status and mic
        self.status_label = QLabel("Status: Idle")
        self.status_label.setStyleSheet("font-size: 12px;")
        self.mic_button = QPushButton("🎤 On")
        self.mic_button.setCheckable(True)
        self.mic_button.clicked.connect(self.toggle_mic)
        layout.addWidget(self.status_label)
        layout.addWidget(self.mic_button)
        self.setStyleSheet("background-color: #2A2D34; color: #E0E0E0;")

    def toggle_mic(self):
        self.mic_on = not self.mic_on
        if self.mic_on:
            self.mic_button.setText("🎤 On")
            SetMicrophoneStatus('True')
        else:
            self.mic_button.setText("🔇 Off")
            SetMicrophoneStatus('False')

    def update_status(self):
        self.status_label.setText(f"Status: {GetAssistantStatus()}")

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        # Welcome GIF
        gif_label = QLabel()
        movie = QMovie(os.path.join(GIF_DIR, 'welcome.gif'))
        movie.setScaledSize(QSize(300, 200))
        gif_label.setMovie(movie); movie.start()
        gif_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(gif_label)
        # Text
        title = QLabel(f"Welcome to {ASSISTANT_NAME}!")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Verdana', 20, QFont.Bold))
        sub = QLabel("Your AI companion awaits...")
        sub.setAlignment(Qt.AlignCenter)
        sub.setFont(QFont('Arial', 14))
        layout.addWidget(title); layout.addWidget(sub)
        layout.addStretch(1)
        self.setStyleSheet("background-color: #1E1F27; color: #F5F5F5;")

class ChatScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        # Listening GIF
        self.listen_gif = QLabel()
        listen_movie = QMovie(os.path.join(GIF_DIR, 'listening.gif'))
        listen_movie.setScaledSize(QSize(100, 100))
        self.listen_gif.setMovie(listen_movie); listen_movie.start()
        self.listen_gif.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.listen_gif)
        # Chat box
        self.chat_box = QTextEdit(); self.chat_box.setReadOnly(True)
        self.chat_box.setFont(QFont("Courier", 12))
        layout.addWidget(self.chat_box)
        self.setStyleSheet("background-color: #FFFFFF; color: #333333;")
        # Poll timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.load_messages)
        self.timer.start(100)
        self.last = ""

    def load_messages(self):
        try:
            text = open(RESP_FILE, 'r', encoding='utf-8').read().strip()
            if text and text != self.last:
                self.chat_box.append(text)
                # Reset mic automatically
                SetMicrophoneStatus('True')
                win = self.window()
                if hasattr(win, 'nav'):
                    win.nav.mic_on = True
                    win.nav.mic_button.setChecked(False)
                    win.nav.mic_button.setText("🎤 On")
                self.last = text
        except:
            pass

class AssistantWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{ASSISTANT_NAME} Assistant")
        self.resize(900, 600)
        central = QWidget(); self.setCentralWidget(central)

        # Main vertical layout to include floating bot GIF
        main_layout = QVBoxLayout(central)
        # Floating bot GIF at top
        bot_label = QLabel()
        bot_movie = QMovie(os.path.join(GIF_DIR, 'bot.gif'))
        bot_movie.setScaledSize(QSize(80, 80))
        bot_label.setMovie(bot_movie); bot_movie.start()
        bot_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(bot_label)

        # Horizontal nav + content
        content_layout = QHBoxLayout()
        self.stack = QStackedWidget()
        self.stack.addWidget(HomeScreen()); self.stack.addWidget(ChatScreen())
        nav = NavPanel(self.stack); nav.setFixedWidth(200)
        content_layout.addWidget(nav); content_layout.addWidget(self.stack)
        main_layout.addLayout(content_layout)

        self.nav = nav
        SetAssistantStatus("Available ...")
        self.setStyleSheet("background-color: #121212;")

# Entry point unchanged
def GraphicalUserInterface():
    app = QApplication(sys.argv)
    win = AssistantWindow()
    win.show()
    sys.exit(app.exec_())
