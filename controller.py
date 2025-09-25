import time
from view import DashboardView
from model_session import SessionModel

class DashboardController:
    def __init__(self):
        self.view = DashboardView()
        self.session_model = SessionModel()
        self.session_start_time = None
        self.bt_connected = False
        self._running = True

    def update_bt_status(self, status: bool):
        self.bt_connected = status
        self.view.set_bt_status(status)

        if status:  # new session
            self.session_start_time = time.time()
            self.view.set_session_id(self.session_model.current_session_id)
            self.view.new_session()  # Clear graph for new session
        else:  # session ended
            if self.session_start_time:
                duration = time.time() - self.session_start_time
                self.session_model.save_session(duration)
            self.session_start_time = None
            self.view.set_session_id("None")
            self.view.set_session_duration(0)

    def handle_data(self, value):
        if self.session_start_time:
            duration = int(time.time() - self.session_start_time)
            self.view.set_session_duration(duration)
            self.view.set_data_value(value, duration)

    def run(self):
        try:
            while self._running and not self.view._closed:
                # Simulate fake Bluetooth data
                if self.bt_connected:
                    self.handle_data(value=time.time() % 100)  # Fake data for now

                self.view.update()
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped")
