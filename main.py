import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CameraMetadataApp(App):
    def build(self):
        self.camera_ip = '192.168.34.29'
        self.connected = False
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(
            text='Camera Metadata Manager',
            size_hint=(1, 0.1),
            font_size='24sp',
            bold=True
        )
        layout.add_widget(title)
        
        ip_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        ip_label = Label(text='Camera IP:', size_hint=(0.3, 1))
        self.ip_input = TextInput(
            text=self.camera_ip,
            size_hint=(0.5, 1),
            multiline=False
        )
        ip_layout.add_widget(ip_label)
        ip_layout.add_widget(self.ip_input)
        layout.add_widget(ip_layout)
        
        self.connect_btn = Button(
            text='Connect to Camera',
            size_hint=(1, 0.08),
            background_color=(0.13, 0.59, 0.95, 1)
        )
        self.connect_btn.bind(on_press=self.connect_camera)
        layout.add_widget(self.connect_btn)
        
        self.status_label = Label(
            text='Status: Not Connected',
            size_hint=(1, 0.06),
            color=(1, 0, 0, 1)
        )
        layout.add_widget(self.status_label)
        
        layout.add_widget(Label(size_hint=(1, 0.05)))
        
        copyright_label = Label(
            text='Copyright:',
            size_hint=(1, 0.06),
            bold=True
        )
        layout.add_widget(copyright_label)
        
        self.copyright_input = TextInput(
            hint_text='Enter copyright information',
            size_hint=(1, 0.15),
            multiline=True
        )
        layout.add_widget(self.copyright_input)
        
        copyright_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        
        get_copyright_btn = Button(text='Get')
        get_copyright_btn.bind(on_press=lambda x: self.get_metadata('copyright'))
        copyright_buttons.add_widget(get_copyright_btn)
        
        set_copyright_btn = Button(
            text='Set',
            background_color=(0.3, 0.69, 0.31, 1)
        )
        set_copyright_btn.bind(on_press=lambda x: self.set_metadata('copyright'))
        copyright_buttons.add_widget(set_copyright_btn)
        
        layout.add_widget(copyright_buttons)
        
        author_label = Label(
            text='Author:',
            size_hint=(1, 0.06),
            bold=True
        )
        layout.add_widget(author_label)
        
        self.author_input = TextInput(
            hint_text='Enter author name',
            size_hint=(1, 0.15),
            multiline=True
        )
        layout.add_widget(self.author_input)
        
        author_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), spacing=10)
        
        get_author_btn = Button(text='Get')
        get_author_btn.bind(on_press=lambda x: self.get_metadata('author'))
        author_buttons.add_widget(get_author_btn)
        
        set_author_btn = Button(
            text='Set',
            background_color=(0.3, 0.69, 0.31, 1)
        )
        set_author_btn.bind(on_press=lambda x: self.set_metadata('author'))
        author_buttons.add_widget(set_author_btn)
        
        layout.add_widget(author_buttons)
        
        return layout
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def connect_camera(self, instance):
        self.camera_ip = self.ip_input.text.strip()
        self.status_label.text = 'Status: Connecting...'
        self.status_label.color = (1, 1, 0, 1)
        
        try:
            url = f'https://{self.camera_ip}:443/ccapi/ver100/deviceinformation'
            response = requests.get(url, timeout=5, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                self.connected = True
                self.status_label.text = f'Status: Connected to {data.get("productname", "Camera")}'
                self.status_label.color = (0, 1, 0, 1)
                self.show_popup('Success', 'Connected to camera!')
            else:
                raise Exception(f'HTTP {response.status_code}')
                
        except Exception as e:
            self.connected = False
            self.status_label.text = 'Status: Connection Failed'
            self.status_label.color = (1, 0, 0, 1)
            self.show_popup('Error', f'Connection failed:\n{str(e)}')
    
    def get_metadata(self, field):
        if not self.connected:
            self.show_popup('Error', 'Please connect to camera first')
            return
        
        try:
            url = f'https://{self.camera_ip}:443/ccapi/ver100/functions/registeredname/{field}'
            response = requests.get(url, timeout=5, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                value = data.get(field, '')
                
                if field == 'copyright':
                    self.copyright_input.text = value
                elif field == 'author':
                    self.author_input.text = value
                
                if value:
                    self.show_popup('Success', f'{field.capitalize()} retrieved:\n{value}')
                else:
                    self.show_popup('Info', f'{field.capitalize()} is empty')
            else:
                raise Exception(f'HTTP {response.status_code}')
                
        except Exception as e:
            self.show_popup('Error', f'Failed to get {field}:\n{str(e)}')
    
    def set_metadata(self, field):
        if not self.connected:
            self.show_popup('Error', 'Please connect to camera first')
            return
        
        if field == 'copyright':
            value = self.copyright_input.text.strip()
        elif field == 'author':
            value = self.author_input.text.strip()
        
        if not value:
            self.show_popup('Error', 'Please enter a value')
            return
        
        try:
            url = f'https://{self.camera_ip}:443/ccapi/ver100/functions/registeredname/{field}'
            response = requests.put(
                url,
                json={field: value},
                timeout=5,
                verify=False
            )
            
            if response.status_code == 200:
                self.show_popup('Success', f'{field.capitalize()} set to:\n{value}')
            else:
                raise Exception(f'HTTP {response.status_code}')
                
        except Exception as e:
            self.show_popup('Error', f'Failed to set {field}:\n{str(e)}')

if __name__ == '__main__':
    CameraMetadataApp().run()
