pip install kivy
pip install requests



import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
import random
import time

# Dummy data
users_db = {}  # Placeholder for user database

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")

        # Welcome Label
        self.welcome_label = Label(text="Welcome to Pychat! Please log in.")
        layout.add_widget(self.welcome_label)

        # OTP Login
        self.otp_input = TextInput(hint_text="Enter OTP", multiline=False)
        layout.add_widget(self.otp_input)

        login_button = Button(text="Login")
        login_button.bind(on_press=self.on_login)
        layout.add_widget(login_button)

        # Settings
        self.settings_button = Button(text="Settings")
        self.settings_button.bind(on_press=self.show_settings)
        layout.add_widget(self.settings_button)

        self.add_widget(layout)

    def on_login(self, instance):
        otp = self.otp_input.text
        if otp == self.generate_otp():
            self.welcome_label.text = "Logged in successfully!"
            self.manager.current = 'chat_screen'
        else:
            self.show_popup("Invalid OTP", "Please enter a valid OTP.")

    def generate_otp(self):
        return str(random.randint(100000, 999999))  # Dummy OTP generation

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical")
        content.add_widget(Label(text=message))
        close_button = Button(text="Close")
        close_button.bind(on_press=self.close_popup)
        content.add_widget(close_button)

        self.popup = Popup(title=title, content=content, size_hint=(0.5, 0.5))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

    def show_settings(self, instance):
        self.manager.current = 'settings_screen'

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        volume_spinner = Spinner(
            text="Volume",
            values=('Low', 'Medium', 'High'),
            size_hint=(None, None),
            size=(100, 44)
        )
        layout.add_widget(volume_spinner)
        
        profile_button = Button(text="Update Profile")
        layout.add_widget(profile_button)

        self.add_widget(layout)

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical")
        
        self.message_input = TextInput(hint_text="Type your message...", multiline=True)
        layout.add_widget(self.message_input)

        send_button = Button(text="Send Message")
        send_button.bind(on_press=self.on_send_message)
        layout.add_widget(send_button)
        
        group_button = Button(text="Create Group")
        group_button.bind(on_press=self.on_create_group)
        layout.add_widget(group_button)
        
        self.add_widget(layout)

    def on_send_message(self, instance):
        message = self.message_input.text
        if message:
            print(f"Sending message: {message}")
            # Logic for sending messages to server or saving them
        else:
            self.show_popup("Error", "Message cannot be empty.")

    def on_create_group(self, instance):
        self.show_popup("Create Group", "Enter group details.")
        # Logic for creating a new group

class PychatApp(App):
    def build(self):
        self.sm = ScreenManager()

        self.sm.add_widget(MainScreen(name='main_screen'))
        self.sm.add_widget(SettingsScreen(name='settings_screen'))
        self.sm.add_widget(ChatScreen(name='chat_screen'))

        return self.sm

if __name__ == '__main__':
    PychatApp().run()