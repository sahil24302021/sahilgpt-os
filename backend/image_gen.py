import os
import time
from diffusers import DiffusionPipeline
import torch

# --- This is the new part ---
# Check if your Mac's GPU (Metal Performance Shaders) is available
if torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device for image generation: {device.upper()}")
# ---------------------------

model_id = "runwayml/stable-diffusion-v1-5"
model_cache_path = "data/sd_model_cache"
os.makedirs("data", exist_ok=True)

print("Loading Stable Diffusion model... This may take a few minutes.")
try:
    pipe = DiffusionPipeline.from_pretrained(
        model_id,
        cache_dir=model_cache_path,
        torch_dtype=torch.float32 
    )
    
    # --- This is the new part ---
    # Send the model to your GPU
    pipe = pipe.to(device)
    # ---------------------------
    
    print("Stable Diffusion model loaded successfully.")
except Exception as e:
    print(f"Error loading Stable Diffusion model: {e}")
    pipe = None

def generate_image(prompt: str) -> str:
    if pipe is None:
        return "Error: Stable Diffusion model could not be loaded."

    try:
        print(f"Generating image for prompt: '{prompt}'")
        
        # This will now run on the GPU and be much faster
        image = pipe(prompt).images[0]
        
        print("Image generation complete.")
        
        timestamp = int(time.time())
        image_filename = f"generated_image_{timestamp}.png"
        image_filepath = os.path.join("data", image_filename)
        
        image.save(image_filepath)
        print(f"Image saved to: {image_filepath}")
        return image_filepath
        
    except Exception as e:
        print(f"Error during image generation: {e}")
        return f"An error occurred: {e}"