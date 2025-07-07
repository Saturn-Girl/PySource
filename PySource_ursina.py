from ursina import *
import ctypes
import numpy as np

# CUDA setup
try:
    from numba import cuda
    GPU_AVAILABLE = cuda.is_available()
except:
    GPU_AVAILABLE = False

# Globals
app = None
scene_entity = None  # Reference to the currently loaded 3D model

def Init() -> None:
    """Initialize the Ursina app with an editor camera (WASD + mouse)."""
    global app
    app = Ursina()
    EditorCamera()
    print("[INFO] Ursina app initialized.")
    camera.orthographic = True  # Makes it 2D
    camera.enabled = False    # Disables the 3D camera
    EditorCamera().enabled = False  # Also make sure dev camera is off
    TryGPUAcceleration()

def LoadScene(model_name: str) -> None:
    """Load and display a 3D model into the scene."""
    global scene_entity
    print(f"[INFO] Loading model: {model_name}")

    model = load_model(model_name)
    if model:
        scene_entity = Entity(model=model, scale=1, color=color.white)
        print("[INFO] Model loaded successfully.")
    else:
        print("[ERROR] Model not found or failed to load.")

def LoadImage(image_path: str, scale_value: float = 1.0) -> None:
    """Load and display a 2D image as a quad in the scene."""
    print(f"[INFO] Loading image: {image_path}")
    try:
        texture = load_texture(image_path)
        Entity(model='quad', texture=texture, scale=scale_value, position=(0, 0, -1))
        print("[INFO] Image loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load image: {e}")

def AddSkybox() -> None:
    """Add a skybox to the scene."""
    Sky()
    print("[INFO] Skybox added.")

def LoadLibrary(library_name: str) -> None:
    """Load a dynamic/shared library using ctypes."""
    try:
        ctypes.CDLL(library_name)
        print(f"[INFO] Library '{library_name}' loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load library '{library_name}': {e}")

def TryGPUAcceleration() -> None:
    """Try to run GPU acceleration test using CUDA-Python."""
    if GPU_AVAILABLE:
        print("[INFO] GPU with CUDA detected — enabling RTX-like acceleration.")

        @cuda.jit
        def invert_image(image):
            x, y = cuda.grid(2)
            if x < image.shape[0] and y < image.shape[1]:
                for i in range(3):  # RGB channels
                    image[x, y, i] = 255 - image[x, y, i]

        try:
            dummy_image = np.random.randint(0, 255, size=(128, 128, 3), dtype=np.uint8)
            threads_per_block = (16, 16)
            blocks_per_grid_x = (dummy_image.shape[0] + threads_per_block[0] - 1) // threads_per_block[0]
            blocks_per_grid_y = (dummy_image.shape[1] + threads_per_block[1] - 1) // threads_per_block[1]

            invert_image[(blocks_per_grid_x, blocks_per_grid_y), threads_per_block](dummy_image)
            print("[CUDA] Image processed successfully using GPU!")
        except Exception as e:
            print(f"[CUDA ERROR] Failed to run CUDA kernel: {e}")
    else:
        print("[INFO] No CUDA-compatible GPU detected. RTX features disabled.")

def Start() -> None:
    """Start the Ursina game loop."""
    if app:
        print("[INFO] Starting Ursina app...")
        app.run()
    else:
        print("[ERROR] App not initialized. Call Init() first.")

def CheckVersion_Game() -> None:
    print(Source_logo)
