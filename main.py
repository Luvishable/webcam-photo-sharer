from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.clipboard import Clipboard
from kivy.lang import Builder
from filesharer import FileSharer
import webbrowser
import time


Builder.load_file("frontend.kv")


class CameraScreen(Screen):
    def start(self):
        """Starts the camera and changes the Button text"""
        # When the camera is off, we dont want the default camera widget in the bottom left
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture

    def stop(self):
        """Stops the camera and changes the Button text. Because if the camera is off,
        we want the text of the button 'start', otherwise stop."""
        # After turning off the camera, we dont want a white background color
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None

    def capture(self):
        # Name the captures according to the time they are taken
        current_time = time.strftime("%Y%m%d-%H%M%S")
        # Save them in a different directory. In this case 'files'
        self.filepath = f"files/{current_time}.png"
        # Turn the file into png and save it
        self.ids.camera.export_to_png(self.filepath)
        # When the user captures a photo, ImageScreen will be displayed.
        self.manager.current = "image_screen"
        # The captured photo will be displayed after switching to the ImageScreen
        self.manager.current_screen.ids.img.source = self.filepath


class ImageScreen(Screen):
    link_message = "Create a link first"
    def create_link(self):
        # Getting the filepath of the captured photo
        file_path = App.get_running_app().root.ids.camera_screen.filepath
        # Create FileSharer instance in order to get a link
        filesharer = FileSharer(filepath=file_path)
        self.url = filesharer.share()
        # Display the link in the ImageScreen's label section
        self.ids.link.text = self.url
    def copy_link(self):
        # If the user presses the button 'copy link' then the program will terminate
        # throw an error. If we want the program to go on running, we have to create
        # try except block and warn the user
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message
    def open_link(self):
        """Opens the link that created."""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message




class RootWidget(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


MainApp().run()
