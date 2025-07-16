from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.clock import Clock
import sys
import threading
import io
import os
from utils.main_processor import process_media
from utils.live_processor import process_live_stream

class LogBox(TextInput):
    pass

class OutputRedirector(io.StringIO):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def write(self, text):
        self.callback(text)
        return super().write(text)

class LauncherLayout(BoxLayout):
    vision_mode = StringProperty("file")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.vision_spinner = Spinner(
            text='file',
            values=('file', 'live'),
            size_hint=(1, None),
            height=44
        )
        self.add_widget(Label(text="Input Source:"))
        self.add_widget(self.vision_spinner)

        self.run_button = Button(text="Run Mira Lens", size_hint=(1, None), height=50)
        self.run_button.bind(on_press=self.on_run_pressed)
        self.add_widget(self.run_button)

        self.log_box = LogBox(readonly=True, size_hint=(1, 1))
        self.add_widget(self.log_box)

        # Redirect stdout
        sys.stdout = OutputRedirector(self.update_log)

    def update_log(self, text):
        Clock.schedule_once(lambda dt: self._append_log(text))

    def _append_log(self, text):
        self.log_box.text += text
        self.log_box.cursor = (0, len(self.log_box.text))
        self.log_box.scroll_y = 0

    def on_run_pressed(self, instance):
        vision_mode = self.vision_spinner.text

        def run_pipeline():
            if vision_mode == "file":
                folder = "test_assets"
                video_files = [f for f in os.listdir(folder) if f.endswith(".mp4")]
                if not video_files:
                    print("No MP4 files found in test_assets/")
                for file in video_files:
                    path = os.path.join(folder, file)
                    print(f"\nProcessing {file}...")
                    detections = process_media(input_path=path)
                    for d in detections:
                        print(d)

            elif vision_mode == "live":
                print("\nStarting live mode...")
                process_live_stream(chunk_duration=5.0)

        threading.Thread(target=run_pipeline).start()

class MiraLauncherApp(App):
    def build(self):
        return LauncherLayout()

if __name__ == "__main__":
    MiraLauncherApp().run()
