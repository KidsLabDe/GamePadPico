import board
import neopixel
import time
import random

# Configure the matrix
PIXEL_PIN = board.GP12
PIXEL_WIDTH = 5
PIXEL_HEIGHT = 5
NUM_PIXELS = PIXEL_WIDTH * PIXEL_HEIGHT
BRIGHTNESS = 0.05

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False)

def xy_to_index(x, y):
    """Convert x,y coordinates to pixel index"""
    if y % 2 == 0:
        return y * PIXEL_WIDTH + x
    else:
        return y * PIXEL_WIDTH + (PIXEL_WIDTH - 1 - x)

def rainbow_cycle(wait):
    """Rainbow animation across all pixels"""
    for j in range(255):
        for x in range(PIXEL_WIDTH):
            for y in range(PIXEL_HEIGHT):
                idx = xy_to_index(x, y)
                rc_index = (x * 256 // PIXEL_WIDTH) + j
                pixels[idx] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    """Generate rainbow colors"""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def ripple(color, wait):
    """Create a ripple effect from center"""
    center_x = PIXEL_WIDTH // 2
    center_y = PIXEL_HEIGHT // 2
    
    for distance in range(max(PIXEL_WIDTH, PIXEL_HEIGHT)):
        pixels.fill((0, 0, 0))
        for x in range(PIXEL_WIDTH):
            for y in range(PIXEL_HEIGHT):
                if abs(x - center_x) + abs(y - center_y) == distance:
                    pixels[xy_to_index(x, y)] = color
        pixels.show()
        time.sleep(wait)

def random_sparkle(wait):
    """Random twinkling effect"""
    pixels.fill((0, 0, 0))
    for _ in range(NUM_PIXELS // 3):
        i = random.randint(0, NUM_PIXELS - 1)
        pixels[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    pixels.show()
    time.sleep(wait)

def snake(color, wait):
    """Snake moving through the matrix"""
    for i in range(NUM_PIXELS):
        pixels.fill((0, 0, 0))
        pixels[i] = color
        if i > 0:
            pixels[i-1] = (color[0]//4, color[1]//4, color[2]//4)
        pixels.show()
        time.sleep(wait)

# Main animation loop
while True:
    # Rainbow cycle
    for _ in range(2):
        rainbow_cycle(0.01)
    
    # Ripple effect
    for _ in range(5):
        ripple((0, 0, 255), 0.1)  # Blue ripple
        ripple((255, 0, 0), 0.1)  # Red ripple
        ripple((0, 255, 0), 0.1)  # Green ripple
    
    
    # Random sparkles
    for _ in range(50):
        random_sparkle(0.05)
    
    # Snake animation
    for _ in range(3):
        snake((255, 0, 0), 0.1)  # Red snake
        snake((0, 255, 0), 0.1)  # Green snake
        snake((0, 0, 255), 0.1)  # Blue snake
