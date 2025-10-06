import time
import random
import PySimpleGUI as sg
from view import DashboardView

class ButtonController:
    """Controls button text, color, and window background based on driver state."""
    def __init__(self, window, circle_progress):
        self.window = window
        self.circle_progress = circle_progress

    def update(self, driver_state):
        """Update button, progress, circle, and window colors based on driver state."""
        if driver_state == "awake":
            text = "Alert,Looking Good! 😁"
            color = "green"

            progress = 1.0  # full progress
        elif driver_state == "sleepy":
            text = "Fatigue detected,Be Careful! 😐"
            color = "#ffc40c"

            progress = 0.5
        else:  # falling asleep
            text = "Drowsy,Danger😴"
            color = "red"
            progress = 0.1

        # Update GUI elements
        self.window["-BUTTON-"].update(text=text, button_color=("white", color))
        self.circle_progress.set(progress)  # update circular progress
        #self.window.TKroot.configure(bg=color)


class DashboardController:
    def __init__(self):
        self.view = DashboardView()
        self.session_start_time = time.time()
        self._running = True

        # Generate a session ID at startup
        self.session_id = f"IRIS{random.randint(1000, 9999)}"
        self.view.set_session_id(self.session_id)

        # --- Instantiate ButtonController with window and circular progress ---
        self.button_ctrl = ButtonController(self.view.window, self.view.circle_progress)

    def run(self):
        try:
            while self._running:
                event, _ = self.view.read(timeout=500)

                if event in (sg.WINDOW_CLOSED, "Exit"):
                    break

                # Update session duration
                duration = int(time.time() - self.session_start_time)
                self.view.set_session_duration(duration)

                # Replace this with real data from MPU6050/Database
                driver_state = random.choice(["awake", "sleepy", "falling_asleep"])

                # Update button, progress circle, and window via controller
                self.button_ctrl.update(driver_state)

            self.view.close()
        except KeyboardInterrupt:
            self.view.close()
