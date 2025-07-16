import pygame
import ctypes
import numpy as np
import sys

# CUDA setup
try:
    from numba import cuda
    GPU_AVAILABLE = cuda.is_available()
except:
    GPU_AVAILABLE = False

# Globals
app_running = False
screen = None
scene_entity = None  # No 3D in Pygame

def Init(window_name: str) -> None:
    """Initialize the Pygame app."""
    global screen, app_running
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption(window_name)
    app_running = True
    print("[INFO] Pygame app initialized.")
    TryGPUAcceleration()

def LoadScene(model_name: str) -> None:
    """Stub function — 3D models not supported in Pygame."""
    print(f"[ERROR] LoadScene('{model_name}') not supported in Pygame (no 3D engine).")

def LoadImage(image_path: str, scale_value: float = 1.0) -> None:
    """Load and display a 2D image."""
    global screen
    print(f"[INFO] Loading image: {image_path}")
    try:
        image = pygame.image.load(image_path)
        if scale_value != 1.0:
            width = int(image.get_width() * scale_value)
            height = int(image.get_height() * scale_value)
            image = pygame.transform.scale(image, (width, height))
        screen.blit(image, (0, 0))
        pygame.display.flip()
        print("[INFO] Image loaded successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to load image: {e}")

def AddSkybox() -> None:
    """Stub: Skybox not available in Pygame."""
    print("[INFO] Skybox not supported in Pygame. Skipping.")

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
    """Start the Pygame loop."""
    global app_running
    if not app_running:
        print("[ERROR] App not initialized. Call Init() first.")
        return

    print("[INFO] Starting Pygame loop...")
    while app_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[INFO] Quitting application.")
                pygame.quit()
                sys.exit()

def CheckVersion_Game() -> None:
    print("[INFO] CheckVersion_Game: no version banner implemented.")

def AddTextBox(text, duration=0, font_size=24, box_color=(0, 0, 0), text_color=(255, 255, 255)):
    """
    Draws a textbox with the given text. 
    If duration > 0, it stays on screen for that many seconds.
    """
    global screen
    font = pygame.font.SysFont('Arial', font_size)
    rendered_text = font.render(text, True, text_color)

    # Padding around the text
    padding = 20
    text_width = rendered_text.get_width()
    text_height = rendered_text.get_height()
    box_width = text_width + padding
    box_height = text_height + padding

    # Position (bottom center)
    box_x = (screen.get_width() - box_width) // 2
    box_y = screen.get_height() - box_height - 50

    # Create the text box surface
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    # Draw box and text
    pygame.draw.rect(screen, box_color, box_rect)
    screen.blit(rendered_text, (box_x + padding//2, box_y + padding//2))
    pygame.display.flip()

    # If duration > 0, pause for that many seconds
    if duration > 0:
        pygame.time.delay(int(duration * 1000))  # convert to milliseconds
        # Clear box after delay
        screen.fill((0, 0, 0))  # or re-blit the background
        pygame.display.flip()

