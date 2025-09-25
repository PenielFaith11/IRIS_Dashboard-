import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class DashboardView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IRIS Dashboard")
        self.root.geometry("500x400")

        self.bt_label = tk.Label(self.root, text="Bluetooth: ⭕ Disconnected", font=("Arial", 13))
        self.bt_label.pack(pady=8)

        self.session_id_label = tk.Label(self.root, text="Session ID: None", font=("Arial", 12))
        self.session_id_label.pack(pady=4)

        self.duration_label = tk.Label(self.root, text="Duration: 0 sec", font=("Arial", 12))
        self.duration_label.pack(pady=4)

        # Graph container
        self.fig, self.ax = plt.subplots(figsize=(4, 2))
        self.ax.set_title("Session Data")
        self.ax.set_xlabel("Time (sec)")
        self.ax.set_ylabel("Sensor Value")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=10)

        self.data_x = []
        self.data_y = []

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self._closed = False

    def set_bt_status(self, connected: bool):
        text = "🟢 Connected" if connected else "⭕ Disconnected"
        self.bt_label.config(text=f"Bluetooth: {text}")

    def set_session_id(self, session_id):
        self.session_id_label.config(text=f"Session ID: {session_id}")

    def set_session_duration(self, duration):
        self.duration_label.config(text=f"Duration: {duration} sec")

    def set_data_value(self, value, time_sec):
        self.data_x.append(time_sec)
        self.data_y.append(value)
        self.ax.clear()
        self.ax.plot(self.data_x, self.data_y, color="blue")
        self.ax.set_title("Session Data")
        self.ax.set_xlabel("Time (sec)")
        self.ax.set_ylabel("Sensor Value")
        self.canvas.draw()

    def new_session(self):
        # Start fresh for each session
        self.data_x = []
        self.data_y = []
        self.ax.clear()
        self.ax.set_title("Session Data")
        self.ax.set_xlabel("Time (sec)")
        self.ax.set_ylabel("Sensor Value")
        self.canvas.draw()

    def update(self):
        if not self._closed:
            self.root.update_idletasks()
            self.root.update()

    def on_close(self):
        self._closed = True
        try:
            self.root.destroy()
        except:
            pass
