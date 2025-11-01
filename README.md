# SAHILGPT OS 🤖

A 100% private, offline-first personal AI assistant that runs entirely on your Mac. Built with Python and Streamlit, this project features secure face scan login, a local LLM, voice chat, local image generation, and more, all without sending any of your data to the cloud.



## 🌟 Core Features

* **🔐 Face Scan Login:** Uses `face-recognition` to securely encrypt and store your face encoding. The app only unlocks when it sees you (using the mirrored, natural-looking photo).
* **💬 Local AI Chat:** Connects to a local `Ollama` server (running `Llama 3.1: 8B`) for 100% private conversations.
* **🗣️ Voice I/O:** Use your voice to talk to the AI (via `openai-whisper`) and hear its responses spoken back to you (via `gTTS`).
* **🎨 Image Generation:** Generates images locally using `Stable Diffusion`, accelerated by your Mac's GPU (MPS) for faster generation.
* **‍💻 Code Sandbox:** Safely run and test Python code snippets in an isolated environment (does not support `input()` commands).
* **📝 Memory Database:** A local `SQLite` database that logs your interactions.
* **🛠️ Project Tracker:** Scans your coding directory and finds the last project you worked on for a one-click "open" button.

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Local LLM:** Ollama (Llama 3.1: 8B)
* **Image Gen:** Diffusers (Stable Diffusion 1.5)
* **Voice (STT):** `openai-whisper` (local model)
* **Voice (TTS):** `gTTS`
* **Face Auth:** `face-recognition` & `cryptography`
* **Database:** SQLite & `SQLAlchemy`
* **AI Backend:** `torch` & `accelerate`

---

## 📦 Installation

### 1. System Prerequisites (macOS)

You must install these system-level tools first.

```bash
# 1. Install Xcode Command Line Tools
xcode-select --install

# 2. Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"

# 3. Install required libraries
brew install python@3.11 cmake pkg-config portaudio ffmpeg


 Project Setup
# 1. Clone this repository
git clone [https://github.com/YourUsername/sahilgpt-os.git](https://github.com/YourUsername/sahilgpt-os.git)
cd sahilgpt-os

# 2. Create a Python 3.11 virtual environment
python3.11 -m venv venv

# 3. Activate the environment
source venv/bin/activate

# 4. Install all Python packages
pip install -r requirements.txt


Build Error Troubleshooting (dlib)
If the pip install fails on dlib, your cmake is too new. Run these commands to fix it:

# 1. Set this environment variable
export CMAKE_ARGS="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"

# 2. Install dlib by itself, ignoring the cache
pip install dlib==19.24.4 --no-cache-dir

# 3. Run the installer again to get the rest of the packages
pip install -r requirements.txt


Of course. Here is the complete, final README.md file for your project.

Copy and paste all the text inside the code block below into a new file named README.md in your sahilgpt_os folder.

Markdown

# SAHILGPT OS 🤖

A 100% private, offline-first personal AI assistant that runs entirely on your Mac. Built with Python and Streamlit, this project features secure face scan login, a local LLM, voice chat, local image generation, and more, all without sending any of your data to the cloud.



## 🌟 Core Features

* **🔐 Face Scan Login:** Uses `face-recognition` to securely encrypt and store your face encoding. The app only unlocks when it sees you (using the mirrored, natural-looking photo).
* **💬 Local AI Chat:** Connects to a local `Ollama` server (running `Llama 3.1: 8B`) for 100% private conversations.
* **🗣️ Voice I/O:** Use your voice to talk to the AI (via `openai-whisper`) and hear its responses spoken back to you (via `gTTS`).
* **🎨 Image Generation:** Generates images locally using `Stable Diffusion`, accelerated by your Mac's GPU (MPS) for faster generation.
* **‍💻 Code Sandbox:** Safely run and test Python code snippets in an isolated environment (does not support `input()` commands).
* **📝 Memory Database:** A local `SQLite` database that logs your interactions.
* **🛠️ Project Tracker:** Scans your coding directory and finds the last project you worked on for a one-click "open" button.

---

## ⚙️ Tech Stack

* **Frontend:** Streamlit
* **Local LLM:** Ollama (Llama 3.1: 8B)
* **Image Gen:** Diffusers (Stable Diffusion 1.5)
* **Voice (STT):** `openai-whisper` (local model)
* **Voice (TTS):** `gTTS`
* **Face Auth:** `face-recognition` & `cryptography`
* **Database:** SQLite & `SQLAlchemy`
* **AI Backend:** `torch` & `accelerate`

---

## 📦 Installation

### 1. System Prerequisites (macOS)

You must install these system-level tools first.

```bash
# 1. Install Xcode Command Line Tools
xcode-select --install

# 2. Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"

# 3. Install required libraries
brew install python@3.11 cmake pkg-config portaudio ffmpeg
2. Project Setup
Bash

# 1. Clone this repository
git clone [https://github.com/YourUsername/sahilgpt-os.git](https://github.com/YourUsername/sahilgpt-os.git)
cd sahilgpt-os

# 2. Create a Python 3.11 virtual environment
python3.11 -m venv venv

# 3. Activate the environment
source venv/bin/activate

# 4. Install all Python packages
pip install -r requirements.txt
3. Build Error Troubleshooting (dlib)
If the pip install fails on dlib, your cmake is too new. Run these commands to fix it:

Bash

# 1. Set this environment variable
export CMAKE_ARGS="-DCMAKE_POLICY_VERSION_MINIMUM=3.5"

# 2. Install dlib by itself, ignoring the cache
pip install dlib==19.24.4 --no-cache-dir

# 3. Run the installer again to get the rest of the packages
pip install -r requirements.txt

🏃‍♂️ How to Run

SAHILGPT OS has two parts: the AI server (Ollama) and the App (Streamlit).

1. Run the Local AI Server (Ollama)
Download and install Ollama for macOS.

Open the Ollama application.

Open your terminal and pull the AI model. (This is a 4.7GB download).

Bash

ollama pull llama3.1:8b
Leave the Ollama app running in your menu bar.

2. Run the SAHILGPT App
Make sure your venv is active (source venv/bin/activate).

Run the Streamlit app.

Bash

streamlit run frontend/streamlit_app.py
Your browser will open to http://localhost:8501.

3. First-Time Setup (Required)
When the app opens, go to the "Enroll Face" page from the sidebar.

(Recommended) Click "Reset Enrollment" to clear any old data.

Upload 2-3 clear photos of your face and click "Enroll My Face".

Go to the "Login" page and click the "Scan your face" button.

You're in!
