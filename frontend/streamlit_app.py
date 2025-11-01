import streamlit as st
import sys
import os
import subprocess
import numpy as np
import time

# Add backend to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import face_utils, memory_db, llm_utils, code_runner, project_utils, image_gen, voice_utils

# --- CONFIGURATION ---
PROJECTS_BASE_DIR = os.path.expanduser("~/CODING") 

# --- Page Configuration ---
st.set_page_config(page_title="SAHILGPT OS", page_icon="🤖", layout="wide")

# --- Session State Initialization ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "page" not in st.session_state: st.session_state["page"] = "Home"

# --- UI Helper ---
def render_page(page_name):
    st.session_state["page"] = page_name
    st.rerun()

# --- Page Implementations ---
def home_page():
    st.title("Welcome to SAHILGPT OS 🤖")
    st.markdown("Your local, private AI assistant.")
    if face_utils.is_user_enrolled():
        st.success("Face enrollment found. You can proceed to login.")
        if st.button("Go to Login"): render_page("Login")
    else:
        st.warning("No face enrolled. Please enroll your face to use the assistant.")
        if st.button("Enroll My Face Now"): render_page("Enroll Face")

def enroll_page():
    st.title("👤 Face Enrollment")
    st.markdown("Upload 2-3 clear photos of your face.")
    uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if st.button("Enroll My Face"):
        if uploaded_files:
            with st.spinner("Processing..."):
                if face_utils.enroll_face(uploaded_files):
                    st.success("Enrollment successful!"); memory_db.add_memory("User enrolled face.")
                else:
                    st.error("Could not find a face in the images.")
        else:
            st.warning("Please upload at least one image.")
    if st.button("Back to Home"): render_page("Home")
    if st.button("Reset Enrollment", type="secondary"):
        face_utils.reset_enrollment(); st.success("Enrollment reset."); st.rerun()

def login_page():
    st.title("🔒 Face Scan Login")
    st.markdown("Please look at the camera to log in.")
    
    login_image = st.camera_input("Scan your face")
    
    if login_image:
        with st.spinner("Verifying..."):
            if face_utils.verify_face(login_image):
                st.session_state["auth"] = True
                st.session_state["page"] = "Dashboard"
                memory_db.add_memory("User logged in successfully via face scan.")
                st.success("Login successful! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Login failed. Face not recognized.")
                memory_db.add_memory("Failed login attempt via face scan.")

    if st.button("Back to Home"):
        render_page("Home")

def dashboard_page():
    if not st.session_state.get("auth"):
        st.warning("Access denied."); render_page("Login"); return
    st.title(f"Welcome, Sahil! 👋")
    st.markdown("Select a tool to get started.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("💬 Chat"); st.button("Start Chatting", on_click=render_page, args=("Chat",))
    with col2:
        st.subheader("‍💻 Code Runner"); st.button("Open Code Runner", on_click=render_page, args=("Code Runner",))
    with col3:
        st.subheader("🎨 Image Generation"); st.button("Generate Images", on_click=render_page, args=("Image Generation",))
    
    st.divider()
    st.subheader("🛠️ Project Tools")
    
    last_project_path = project_utils.find_last_project(PROJECTS_BASE_DIR)
    
    if last_project_path:
        st.success(f"Last project found: `{os.path.basename(last_project_path)}`")
        if st.button("Open Last Project in VSCode"):
            st.warning("Security Warning: Uncomment the code in `streamlit_app.py` to enable this feature.")
            st.code(f'# subprocess.run(["open", "-a", "Visual Studio Code", "{last_project_path}"])', language='python')
            memory_db.add_memory(f"User action: Open project '{last_project_path}'.")
    else:
        st.error(f"Could not find any projects in `{PROJECTS_BASE_DIR}`. Please check the path.")

def chat_page():
    if not st.session_state.get("auth"): st.warning("Access denied."); render_page("Login"); return
    st.title("💬 Chat with SAHILGPT")
    speak_output = st.toggle("Speak responses", value=True)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    processed_prompt = None
    if "voice_prompt" in st.session_state:
        processed_prompt = st.session_state.voice_prompt
        del st.session_state.voice_prompt
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        text_prompt = st.chat_input("What's on your mind?")
        if text_prompt:
            processed_prompt = text_prompt
    with col2:
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        if st.button("🎤"):
            with st.spinner("Listening..."):
                voice_prompt = voice_utils.transcribe_audio_from_mic()
                if voice_prompt:
                    st.session_state.voice_prompt = voice_prompt
                    st.rerun()
                else:
                    st.toast("Sorry, I couldn't hear that.")
    if processed_prompt:
        st.session_state.messages.append({"role": "user", "content": processed_prompt})
        with st.chat_message("user"):
            st.markdown(processed_prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = llm_utils.get_llm_response(processed_prompt)
                st.markdown(response)
                if speak_output:
                    audio_file_path = voice_utils.text_to_speech(response)
                    if audio_file_path:
                        st.audio(audio_file_path, autoplay=True)
        st.session_state.messages.append({"role": "assistant", "content": response})
        memory_db.add_memory(f"Chat: User said '{processed_prompt}'")

def code_runner_page():
    if not st.session_state.get("auth"): st.warning("Access denied."); render_page("Login"); return
    st.title("‍💻 Code Runner Sandbox")
    st.warning("This is a sandbox environment. The code runs locally on your machine.")
    default_code = 'import platform\n\nprint("Hello, Sahil!")\nprint(f"You are running Python {platform.python_version()}")'
    code_input = st.text_area("Enter Python code:", value=default_code, height=250)
    if st.button("Run Code"):
        with st.spinner("Executing..."):
            result = code_runner.run_code_safely(code_input)
            memory_db.add_memory("User ran code.")
            st.subheader("Output:"); st.code(result["stdout"], language='bash')
            if result["stderr"]: st.subheader("Errors:"); st.code(result["stderr"], language='bash')

# --- THIS IS THE NEW, CORRECTED IMAGE PAGE ---
def image_gen_page():
    if not st.session_state.get("auth"): st.warning("Access denied."); render_page("Login"); return
    
    st.title("🎨 Image Generation")
    st.markdown("Generate an image using a local Stable Diffusion model.")
    st.warning("This will be VERY slow on a CPU (5-15 minutes). Please be patient.")
    
    prompt = st.text_input("Enter a prompt for the image:")
    
    if st.button("Generate Image"):
        if prompt:
            with st.spinner(f"Generating '{prompt}'... This will take several minutes."):
                # The backend function now returns a FILE PATH
                image_filepath = image_gen.generate_image(prompt)
                
                # Check if the path is an error message or a real file
                if image_filepath.startswith("Error"):
                    st.error(image_filepath)
                else:
                    st.success("Generation complete!")
                    st.image(image_filepath) # Display the real image
                    memory_db.add_memory(f"User generated image with prompt: '{prompt}'")
        else:
            st.warning("Please enter a prompt.")

def memories_page():
    if not st.session_state.get("auth"): st.warning("Access denied."); render_page("Login"); return
    st.title("📝 Memory Log")
    memories = memory_db.list_memories()
    if not memories: st.info("No memories recorded yet.")
    else:
        for mem in memories:
            st.markdown(f"**{mem.timestamp.strftime('%Y-%m-%d %H:%M:%S')}** - `{mem.content}`")

# --- Sidebar and Page Router ---
with st.sidebar:
    st.title("SAHILGPT OS")
    st.markdown("---")
    
    if st.session_state.get("auth"):
        st.button("🏠 Dashboard", on_click=render_page, args=("Dashboard",))
        st.button("💬 Chat", on_click=render_page, args=("Chat",))
        st.button("‍💻 Code Runner", on_click=render_page, args=("Code Runner",))
        st.button("🎨 Image Generation", on_click=render_page, args=("Image Generation",))
        st.button("📝 Memories", on_click=render_page, args=("Memories",))
        if st.button("Logout"): 
            st.session_state.clear()
            render_page("Home")
    else:
        st.button("🏠 Home", on_click=render_page, args=("Home",))
        st.button("👤 Enroll Face", on_click=render_page, args=("Enroll Face",))
        st.button("🔒 Login", on_click=render_page, args=("Login",))

# Main page routing logic
page_map = {
    "Home": home_page, "Enroll Face": enroll_page, "Login": login_page,
    "Dashboard": dashboard_page, "Chat": chat_page, "Code Runner": code_runner_page,
    "Image Generation": image_gen_page, "Memories": memories_page
}
page_to_render = page_map.get(st.session_state.get("page", "Home"))
page_to_render()