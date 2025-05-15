import board
import neopixel
import pwmio
import time
import touchio
from adafruit_motor import servo

# Pin-Definitionen
NEOPIXEL_PIN = board.GP12
SERVO_PIN = board.GP5
TOUCH_DOWN_PIN = board.GP14
TOUCH_UP_PIN = board.GP16

# NeoPixel einrichten (5x5 Matrix = 25 Pixel)
pixels = neopixel.NeoPixel(NEOPIXEL_PIN, 25, brightness=0.3, auto_write=False)

# Servo einrichten
pwm = pwmio.PWMOut(SERVO_PIN, duty_cycle=0, frequency=50)
servo_motor = servo.Servo(pwm, min_pulse=750, max_pulse=2250)

# Touch-Sensoren einrichten
touch_down = touchio.TouchIn(TOUCH_DOWN_PIN)
touch_up = touchio.TouchIn(TOUCH_UP_PIN)

# Startwert für Servo (Bereich 0-180)
servo_value = 90
servo_motor.angle = servo_value

# Farbdefinitionen
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
OFF = (0, 0, 0)

def update_neopixel_display(value):
    """
    Zeigt den Servo-Wert auf dem NeoPixel-Display an.
    Das Display ist 5x5, also 25 Pixel, und wir zeigen
    den Wert proportional an (0-180 auf 0-25 Pixel).
    """
    # Alle Pixel ausschalten
    pixels.fill(OFF)
    
    # Berechnen, wie viele Pixel basierend auf dem Servo-Wert leuchten sollen
    # Servo-Bereich: 0-180, Pixel: 0-25
    num_pixels = int((value / 180) * 25)
    
    # Farbe basierend auf Position wählen
    if value < 45:
        color = BLUE
    elif value < 90:
        color = GREEN
    elif value < 135:
        color = YELLOW
    else:
        color = RED
    
    # Pixel einschalten
    for i in range(num_pixels):
        pixels[i] = color
    
    # Aktualisieren des Displays
    pixels.show()

def map_range(value, in_min, in_max, out_min, out_max):
    """
    Hilfsfunktion zum Umrechnen von Wertebereichen
    """
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Hauptschleife
while True:
    # Touch-Sensoren auslesen
    if touch_down.value and servo_value > 0:
        servo_value = max(0, servo_value - 5)  # Servo-Wert verringern
        time.sleep(0.1)  # Entprellung
    
    if touch_up.value and servo_value < 180:
        servo_value = min(180, servo_value + 5)  # Servo-Wert erhöhen
        time.sleep(0.1)  # Entprellung
    
    # Servo aktualisieren
    servo_motor.angle = servo_value
    
    # NeoPixel-Display aktualisieren
    update_neopixel_display(servo_value)
    
    # Kurze Pause
    time.sleep(0.05)
