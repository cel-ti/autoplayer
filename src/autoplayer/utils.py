import ctypes
import keyboard

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except: #noqa
        return False

def wait_for_key(key="k", timeout=5):
    """
    Blocks the program execution in 1-second intervals until the specified key is pressed or a timeout occurs.

    Parameters:
        key (str): The key to listen for (default is 'k')
        timeout (int): The total timeout in seconds after which to stop listening if no key is pressed

    Returns:
        bool: True if the key was pressed within the timeout, False otherwise.
    """
    lock = keyboard._UninterruptibleEvent()  # Create an uninterruptible event

    # Define a callback function that sets the event when the key is triggered
    def on_key_press():
        lock.set()

    # Register the key press event and associate it with the callback function
    remove = keyboard.on_press_key(key, lambda _: on_key_press())

    # Use a counter with a while loop to wait in 1-second blocks
    counter = 0
    while counter < timeout:
        if lock.wait(1):  # Wait for 1 second
            pressed = True
            break
        counter += 1
        pressed = False

    # Always ensure to remove the key event after waiting to avoid side effects
    keyboard.unhook(remove)

    return pressed
