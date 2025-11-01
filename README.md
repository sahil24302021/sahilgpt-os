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