import face_recognition
import numpy as np
from cryptography.fernet import Fernet
import os
from PIL import Image
import io

# Define file paths
DATA_DIR = "data"
KEY_PATH = os.path.join(DATA_DIR, "secret.key")
ENCODING_PATH = os.path.join(DATA_DIR, "user_face_encoding.enc")

# --- Key Management (Unchanged) ---
def generate_key():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    key = Fernet.generate_key()
    with open(KEY_PATH, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    if not os.path.exists(KEY_PATH):
        return generate_key()
    with open(KEY_PATH, "rb") as key_file:
        return key_file.read()

# --- Encryption (Unchanged) ---
def encrypt_data(data, key):
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    return f.decrypt(encrypted_data)

# --- Face Enrollment (Unchanged, uses flipped image) ---
def enroll_face(image_files):
    face_encodings = []
    for image_file in image_files:
        try:
            image_pil = Image.open(image_file)
            image_pil_flipped = image_pil.transpose(Image.FLIP_LEFT_RIGHT)
            image = np.array(image_pil_flipped)
            
            encodings = face_recognition.face_encodings(image)
            
            if encodings:
                face_encodings.append(encodings[0])
        except Exception as e:
            print(f"Error processing an image: {e}")
            continue

    if not face_encodings:
        return False 

    avg_encoding = np.mean(face_encodings, axis=0)
    encoding_bytes = avg_encoding.tobytes()
    key = load_key()
    encrypted_encoding = encrypt_data(encoding_bytes, key)
    
    with open(ENCODING_PATH, "wb") as f:
        f.write(encrypted_encoding)
        
    return True

# --- Face Login/Matching (Unchanged, for file uploads) ---
def verify_face(login_image_file):
    if not os.path.exists(ENCODING_PATH):
        return False
    try:
        key = load_key()
        with open(ENCODING_PATH, "rb") as f:
            encrypted_encoding = f.read()
        decrypted_encoding_bytes = decrypt_data(encrypted_encoding, key)
        stored_encoding = np.frombuffer(decrypted_encoding_bytes)
        
        login_image_pil = Image.open(login_image_file)
        login_image_pil_flipped = login_image_pil.transpose(Image.FLIP_LEFT_RIGHT)
        login_image = np.array(login_image_pil_flipped)
        
        login_encodings = face_recognition.face_encodings(login_image)
        if not login_encodings:
            return False
        
        matches = face_recognition.compare_faces([stored_encoding], login_encodings[0], tolerance=0.5)
        return matches[0]
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

# --- *** NEW FUNCTION FOR LIVE VIDEO *** ---
def verify_face_from_frame(frame: np.ndarray) -> bool:
    """
    Verifies a face from a live video frame (numpy array).
    """
    if not os.path.exists(ENCODING_PATH):
        return False # No user enrolled

    try:
        # 1. Load the stored (encrypted) encoding
        key = load_key()
        with open(ENCODING_PATH, "rb") as f:
            encrypted_encoding = f.read()
        decrypted_encoding_bytes = decrypt_data(encrypted_encoding, key)
        stored_encoding = np.frombuffer(decrypted_encoding_bytes)

        # 2. Flip the video frame to match the mirrored enrollment
        # (face_recognition needs RGB, but streamlit-webrtc gives BGR, so convert)
        frame_rgb = frame[:, :, ::-1] # Convert BGR to RGB
        frame_pil = Image.fromarray(frame_rgb)
        frame_pil_flipped = frame_pil.transpose(Image.FLIP_LEFT_RIGHT)
        login_image = np.array(frame_pil_flipped)

        # 3. Find faces in the flipped frame
        # We find locations first as it's faster
        login_face_locations = face_recognition.face_locations(login_image, model="cnn")
        if not login_face_locations:
            return False
            
        # 4. Get encodings for the found faces
        login_encodings = face_recognition.face_encodings(login_image, login_face_locations)

        # 5. Compare against the stored encoding
        matches = face_recognition.compare_faces([stored_encoding], login_encodings[0], tolerance=0.5)
        
        return matches[0]

    except Exception as e:
        # This will fail often on blurry frames, so we just print and continue
        # print(f"Error during frame verification: {e}")
        return False

# --- Helper Functions (Unchanged) ---
def is_user_enrolled():
    return os.path.exists(ENCODING_PATH)

def reset_enrollment():
    if os.path.exists(KEY_PATH):
        os.remove(KEY_PATH)
    if os.path.exists(ENCODING_PATH):
        os.remove(ENCODING_PATH)