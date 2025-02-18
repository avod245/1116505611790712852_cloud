import time
import subprocess
import psutil
import pygame
import tkinter as tk
from tkinter import messagebox

class CODBot:
    def __init__(self):
        self.process_id = None
        self.controller = None
        self.running = False

    def log(self, message):
        """Display messages in the console and on the GUI."""
        print(message)

    def open_game(self):
        """Open the game if it's not already running."""
        try:
            if not self.is_game_running():
                subprocess.run(["C:\\Program Files (x86)\\Steam\\steamapps\\common\\Call of Duty HQ\\cod.exe"])
                self.log("Game started.")
            else:
                self.log("Game is already running.")
        except Exception as e:
            self.log(f"Error launching game: {str(e)}")

    def is_game_running(self):
        """Check if the game process is running."""
        for proc in psutil.process_iter(['pid', 'name']):
            if 'cod.exe' in proc.info['name'].lower():
                self.process_id = proc.info['pid']
                return True
        return False

    def connect_controller(self):
        """Attempt to detect the controller using pygame."""
        pygame.init()
        try:
            pygame.joystick.init()
            if pygame.joystick.get_count() > 0:
                self.controller = pygame.joystick.Joystick(0)
                self.controller.init()
                self.log("Controller connected!")
            else:
                self.log("No controllers found.")
        except Exception as e:
            self.log(f"Error detecting controller: {str(e)}")

    def start_bot(self):
        """Start the bot to interact with the game."""
        self.open_game()
        time.sleep(5)  # Give the game some time to load
        self.connect_controller()

        if self.controller:
            self.running = True
            while self.running:
                self.perform_actions()
                time.sleep(1)  # Adjust sleep time as necessary
        else:
            self.log("Controller not connected. Exiting bot.")
    
    def perform_actions(self):
        """Define actions for the bot (movement, interaction)."""
        if self.controller:
            # Example action: get the controller state
            x_axis = self.controller.get_axis(0)  # Left analog stick X-axis
            y_axis = self.controller.get_axis(1)  # Left analog stick Y-axis
            self.log(f"Controller Axis: X={x_axis}, Y={y_axis}")
            
            # Simulate a button press, e.g., A button (index 0)
            button_a = self.controller.get_button(0)
            if button_a:
                self.log("A button pressed!")
            else:
                self.log("A button not pressed.")
        else:
            self.log("No controller detected. Cannot perform actions.")
    
    def stop_bot(self):
        """Stop the bot."""
        self.running = False
        self.log("Bot stopped.")

class CODBotUI:
    def __init__(self, root, bot):
        self.root = root
        self.bot = bot
        self.root.title("Call of Duty Bot")
        
        # Start button
        self.start_button = tk.Button(self.root, text="Start Bot", command=self.start_bot)
        self.start_button.pack(pady=10)

        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        # Log output area
        self.log_area = tk.Text(self.root, height=10, width=50, wrap=tk.WORD)
        self.log_area.pack(pady=10)

    def log(self, message):
        """Update the log output area."""
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.yview(tk.END)  # Scroll to the bottom

    def start_bot(self):
        """Start the bot from the UI."""
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.bot.start_bot()
    
    def stop_bot(self):
        """Stop the bot from the UI."""
        self.bot.stop_bot()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    bot = CODBot()
    root = tk.Tk()
    ui = CODBotUI(root, bot)
    root.mainloop()
