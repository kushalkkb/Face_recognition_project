from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
import cv2
import numpy as np
import face_recognition
from datetime import datetime
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import sqlite3
import os

# Define your database connection and cursor outside the app class
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create users table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT
            )''')
conn.commit()

# KV language string defining the screens and their layout
kv_string = '''
ScreenManager:
    WelcomeScreen:
    StudentScreen:
    TeacherScreen:
    LoginScreen:
    SignupScreen:
    RegisterNameScreen:
    BranchSemScreen:
    BranchSemScreen2:
    PhotoSelectionScreen:
    DisplayPhotosScreen:
    FaceRecognitionScreen:  # Add FaceRecognitionScreen here

<WelcomeScreen>:
    name: 'welcome'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Are you a Teacher or a Student?'
            halign: 'center'
            font_size: 20

        Button:
            text: 'Student'
            on_release: root.manager.current = 'student'
            size_hint: 0.8, None
            height: 48

        Button:
            text: 'Teacher'
            on_release: root.manager.current = 'teacher'
            size_hint: 0.8, None
            height: 48

<StudentScreen>:
    name: 'student'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Welcome, Student!'
            halign: 'center'
            font_size: 20

        Button:
            text: 'Enter registered Name'
            on_release: root.manager.current = 'register_number'
            size_hint: 0.8, None
            height: 48

        Button:
            text: 'Back'
            on_release: root.manager.current = 'welcome'

<TeacherScreen>:
    name: 'teacher'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Welcome, Teacher!'
            halign: 'center'
            font_size: 20

        Button:
            text: 'Login'
            on_release: root.manager.current = 'login'

        Button:
            text: 'Signup'
            on_release: root.manager.current = 'signup'

        Button:
            text: 'Back'
            on_release: root.manager.current = 'welcome'

<LoginScreen>:
    name: 'login'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        TextInput:
            id: username_field
            hint_text: 'Enter username'
            multiline: False

        TextInput:
            id: password_field
            hint_text: 'Enter password'
            multiline: False
            password: True

        Button:
            text: 'Login'
            on_release: app.login()

        Button:
            text: 'Back'
            on_release: root.manager.current = 'welcome'

<SignupScreen>:
    name: 'signup'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        TextInput:
            id: new_username_field
            hint_text: 'Enter new username'
            multiline: False

        TextInput:
            id: new_password_field
            hint_text: 'Enter new password'
            multiline: False
            password: True

        Button:
            text: 'Signup'
            on_release: app.signup()

        Button:
            text: 'Back'
            on_release: root.manager.current = 'welcome'

<RegisterNameScreen>:
    name: 'register_number'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Enter your registration name'
            halign: 'center'
            font_size: 20

        TextInput:
            id: register_number_field
            hint_text: 'Registration name'
            multiline: False

        Button:
            text: 'Submit'
            on_release: app.check_registration_number(register_number_field.text)

        Button:
            text: 'Back'
            on_release: root.manager.current = 'student'

<BranchSemScreen>:
    name: 'branchsem'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Select Branch'
            halign: 'center'
            font_size: 20

        Button:
            text: 'CS'
            on_release: app.show_semesters('CS')

        Button:
            text: 'ME'
            on_release: app.show_semesters('ME')

        Button:
            text: 'CE'
            on_release: app.show_semesters('CE')

        Button:
            text: 'EC'
            on_release: app.show_semesters('EC')

        Button:
            text: 'Back'
            on_release: root.manager.current = 'login'

<BranchSemScreen2>:
    name: 'branchsem2'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Select Semester'
            halign: 'center'
            font_size: 20

        Button:
            text: '1'
            on_release: app.show_selected_semester('1')

        Button:
            text: '2'
            on_release: app.show_selected_semester('2')

        Button:
            text: '3'
            on_release: app.show_selected_semester('3')

        Button:
            text: '4'
            on_release: app.show_selected_semester('4')

        Button:
            text: '5'
            on_release: app.show_selected_semester('5')

        Button:
            text: '6'
            on_release: app.show_selected_semester('6')

        Button:
            text: 'Back'
            on_release: root.manager.current = 'branchsem'

<PhotoSelectionScreen>:
    name: 'photo_selection'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            text: 'Photo Selection'
            halign: 'center'
            font_size: 20

        FileChooserIconView:
            id: file_chooser
            on_selection: root.update_selected_files()

        Image:
            id: selected_image
            source: ''

        TextInput:
            id: name_input
            hint_text: 'Enter a name for the photos'
            multiline: False

        Button:
            text: 'Select Photos'
            on_release: root.select_photos()

        Button:
            text: 'Display Photo Names'
            on_release: root.display_photo_names()

        Button:
            text: 'Choose Another Photo'
            on_release: root.choose_another_photo()

        Button:
            text: 'Start Recognition'
            on_release: root.manager.current = 'face_recognition'  # Go to face recognition screen

        Button:
            text: 'Back'
            on_release: root.manager.current = 'branchsem2'

<DisplayPhotosScreen>:
    name: 'display_photos'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: 'vertical'
                id: photos_list

        Button:
            text: 'Continue'
            on_release: root.go_to_previous_screen()

<FaceRecognitionScreen>:
    name: 'face_recognition'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        id: video_display_layout

        Button:
            text: 'Start Recognition'
            on_release: root.start_recognition()

        Button:
            text: 'Stop Recognition'
            on_release: root.stop_recognition()

        Button:
            text: 'Show Details'
            on_release: root.show_details()

        Button:
            text: 'Back'
            on_release: root.manager.current = 'photo_selection'

'''

# Define screens using the Screen class from Kivy
class WelcomeScreen(Screen):
    pass

class StudentScreen(Screen):
    pass

class TeacherScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SignupScreen(Screen):
    pass

class RegisterNameScreen(Screen):
    pass

class BranchSemScreen(Screen):
    pass

class BranchSemScreen2(Screen):
    pass

class PhotoSelectionScreen(Screen):
    photos = []  # Initialize an empty list to store photo paths and details

    # Modify the update_selected_files method to update selected files
    def update_selected_files(self):
        selected_files = self.ids.file_chooser.selection
        if selected_files:
            self.ids.selected_image.source = selected_files[0]

    # Modify the select_photos method to store photo details
    def select_photos(self, *args):
        selected_files = self.ids.file_chooser.selection
        if not selected_files:
            self.show_dialog('Please select at least one photo.')
            return

        name = self.ids.name_input.text.strip()
        if not name:
            self.show_dialog('Please enter a name for the photos.')
            return

        # Add the selected photos' paths to the photos list
        for file_path in selected_files:
            # Get the current date and time
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Store photo details: name, path, and timestamp
            self.photos.append({'name': name, 'path': file_path, 'timestamp': current_datetime})

        # Encode the known face from the selected photo
        known_image = face_recognition.load_image_file(selected_files[0])
        known_face_encoding = face_recognition.face_encodings(known_image)[0]

        # Set the known face encoding in FaceRecognitionScreen
        face_recognition_screen = self.manager.get_screen('face_recognition')
        face_recognition_screen.set_known_face_encoding(known_face_encoding)

        self.show_dialog('Photos saved successfully!')

    # Add a method to retrieve photo details
    def get_photo_details(self):
        return self.photos

    def choose_another_photo(self):
        # Add functionality to choose another photo
        self.ids.selected_image.source = ''

    def display_photo_names(self):
        if self.photos:
            photo_names = [os.path.basename(photo['path']) for photo in self.photos]
            self.show_dialog('\n'.join(photo_names))
        else:
            self.show_dialog('No photos found.')

    def show_dialog(self, message):
        dialog = Popup(title='Photo Names',
                       content=Label(text=message),
                       size_hint=(None, None), size=(400, 400))
        dialog.open()

class DisplayPhotosScreen(Screen):
    def go_to_previous_screen(self):
        self.manager.current = 'photo_selection'

class FaceRecognitionScreen(Screen):
    def _init_(self, **kwargs):
        super(FaceRecognitionScreen, self)._init_(**kwargs)
        self.is_recognition_running = False  
        self.video_capture = cv2.VideoCapture(0)
        self.video_display = None
        self.is_recognition_running = False
        self.loh_known_face_encoding = None  # Initialize as None

    def start_recognition(self):
        if not self.is_recognition_running:
            self.video_display = VideoDisplay(capture=self.video_capture)
            self.ids.video_display_layout.add_widget(self.video_display)
            self.video_display.start_recognition()

    def stop_recognition(self):
        if self.is_recognition_running:
            self.is_recognition_running = False
            self.video_display.stop_recognition()
            self.ids.video_display_layout.remove_widget(self.video_display)
            self.video_capture.release()

    def show_details(self):
        # Retrieve photo details from PhotoSelectionScreen
        photo_selection_screen = self.manager.get_screen('photo_selection')
        photo_details = photo_selection_screen.get_photo_details()

        # Display photo details
        if photo_details:
            details_text = "Photo Details:\n\n"
            for photo in photo_details:
                details_text += f"Name: {photo['name']}\n"
                details_text += f"Timestamp: {photo['timestamp']}\n"
                details_text += f"Path: {photo['path']}\n\n"
            self.show_dialog(details_text)
        else:
            self.show_dialog('No photos found.')

    def set_known_face_encoding(self, face_encoding):
        self.loh_known_face_encoding = face_encoding

    def get_known_face_encoding(self):
        return self.loh_known_face_encoding

    def show_dialog(self, message):
        dialog = Popup(title='Photo Details',
                       content=Label(text=message),
                       size_hint=(None, None), size=(600, 400))
        dialog.open()

class VideoDisplay(Image):
    def _init_(self, capture, **kwargs):
        super(VideoDisplay, self)._init_(**kwargs)
        self.capture = capture
        self.is_running = False

    def start_recognition(self):
        Clock.schedule_interval(self.update, 1.0 / 30.0)
        self.is_running = True

    def stop_recognition(self):
        Clock.unschedule(self.update)
        self.is_running = False

    def update(self, dt):
        ret, frame = self.capture.read()

        if ret:
            # Convert the image to RGB format for face recognition
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                # Compare face encoding with the known face encoding
                face_recognition_screen = self.parent.parent  # Get FaceRecognitionScreen instance
                known_face_encoding = face_recognition_screen.get_known_face_encoding()
                if known_face_encoding is not None:
                    match = face_recognition.compare_faces([known_face_encoding], face_encoding)[0]

                    name = "Unknown"
                    if match:
                        name = "Known"

                    # Draw rectangle and label on the face
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Display the resulting frame
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture1

class MyApp(App):
    def build(self):
        self.root = Builder.load_string(kv_string)
        return self.root

    def login(self):
        username = self.root.get_screen('login').ids.username_field.text
        password = self.root.get_screen('login').ids.password_field.text

        # Check if the username and password match in the database
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = c.fetchone()

        # Show login success or failure dialog based on the query result
        if result:
            self.root.current = 'branchsem'  # Move to branch and semester selection screen
        else:
            self.show_dialog('Login Failed!')

    def signup(self):
        new_username = self.root.get_screen('signup').ids.new_username_field.text
        new_password = self.root.get_screen('signup').ids.new_password_field.text

        # Insert new user data into the database
        c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (new_username, new_password, 'student'))
        conn.commit()

        # Show signup success dialog
        self.show_dialog('Signup Successful!')

    def check_registration_number(self, registered_name):
        c.execute("SELECT name FROM photos")
        all_names = c.fetchall()
        if registered_name in [name[0] for name in all_names]:
            self.show_dialog(f'Welcome, {registered_name}!')
        else:
            self.show_dialog('Name not found in the database!')

    def show_dialog(self, message):
        dialog = Popup(title='Alert',
                       content=Label(text=message),
                       size_hint=(None, None), size=(400, 400))
        dialog.open()

    def show_semesters(self, branch):
        # Here, you can implement logic to display semesters based on the selected branch
        print(f'Selected branch: {branch}')
        self.root.current = 'branchsem2'  # Move to semester selection screen

    def show_selected_semester(self, semester):
        print(f'Selected semester: {semester}')
        self.root.current = 'photo_selection'  # Move to photo selection screen

    def go_to_previous_screen(self):
        if self.root.current == 'branchsem2':
            self.root.current = 'branchsem'  # Go back to the branch selection screen
        elif self.root.current == 'branchsem':
            self.root.current = 'login'  # Go back to the login screen

if __name__ == '__main__':
    MyApp().run()