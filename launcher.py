from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from kivy.clock import Clock
from utils.video_processor import run_video
from utils.main_processor import process_media
from main import run_audio_pipeline
import sys
import threading
import io

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
    mode = StringProperty("all")
    vision_mode = StringProperty("file")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = 10

        self.mode_spinner = Spinner(
            text='all',
            values=('all', 'vision', 'audio'),
            size_hint=(1, None),
            height=44
        )
        self.add_widget(Label(text="Select Mode:"))
        self.add_widget(self.mode_spinner)

        self.vision_spinner = Spinner(
            text='file',
            values=('file', 'live'),
            size_hint=(1, None),
            height=44
        )
        self.add_widget(Label(text="Vision Mode (if used):"))
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
        mode = self.mode_spinner.text
        vision_mode = self.vision_spinner.text

        def run_pipeline():
            # Hardcoded path for now; later make this user-selectable
            source_path = "test_assets/forest_clip.mp4"

            detections = process_media(input_path=source_path)

            for d in detections:
                print(d)


        threading.Thread(target=run_pipeline).start()

class MiraLauncherApp(App):
    def build(self):
        return LauncherLayout()

if __name__ == "__main__":
    MiraLauncherApp().run()
