import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import urllib.request
import urllib.error
import json
import ssl
from datetime import datetime

class CameraMetadataApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug_messages = []
        # Create SSL context that doesn't verify certificates
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        
    def log(self, message):
        """Add timestamped log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        self.debug_messages.append(log_msg)
        
        # Keep only last 50 messages
        if len(self.debug_messages) > 50:
            self.debug_messages.pop(0)
        
        # Update debug label if it exists
        if hasattr(self, 'debug_label'):
            self.debug_label.text = '\n'.join(self.debug_messages)
        
        # Also print to console/logcat
        print(log_msg)
        
    def build(self):
        self.camera_ip = '192.168.34.29'
        self.connected = False
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Top section
        top_section = BoxLayout(orientation='vertical', size_hint=(1, 0.6), spacing=10, padding=[10,10,10,0])
        
        title = Label(
            text='Camera Metadata Manager',
            size_hint=(1, 0.15),
            font_size='24sp',
            bold=True
        )
        top_section.add_widget(title)
        
        ip_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        ip_label = Label(text='Camera IP:', size_hint=(0.3, 1))
        self.ip_input = TextInput(
            text=self.camera_ip,
            size_hint=(0.5, 1),
            multiline=False
        )
        ip_layout.add_widget(ip_label)
        ip_layout.add_widget(self.ip_input)
        top_section.add_widget(ip_layout)
        
        self.connect_btn = Button(
            text='Connect to Camera',
            size_hint=(1, 0.12),
            background_color=(0.13, 0.59, 0.95, 1)
        )
        self.connect_btn.bind(on_press=self.connect_camera)
        top_section.add_widget(self.connect_btn)
        
        self.status_label = Label(
            text='Status: Not Connected',
            size_hint=(1, 0.1),
            color=(1, 0, 0, 1)
        )
        top_section.add_widget(self.status_label)
        
        copyright_label = Label(
            text='Copyright:',
            size_hint=(1, 0.08),
            bold=True
        )
        top_section.add_widget(copyright_label)
        
        self.copyright_input = TextInput(
            hint_text='Enter copyright information',
            size_hint=(1, 0.2),
            multiline=True
        )
        top_section.add_widget(self.copyright_input)
        
        copyright_buttons = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        
        get_copyright_btn = Button(text='Get')
        get_copyright_btn.bind(on_press=lambda x: self.get_metadata('copyright'))
        copyright_buttons.add_widget(get_copyright_btn)
        
        set_copyright_btn = Button(
            text='Set',
            background_color=(0.3, 0.69, 0.31, 1)
        )
        set_copyright_btn.bind(on_press=lambda x: self.set_metadata('copyright'))
        copyright_buttons.add_widget(set_copyright_btn)
        
        top_section.add_widget(copyright_buttons)
        
        main_layout.add_widget(top_section)
        
        # Debug console section
        debug_section = BoxLayout(orientation='vertical', size_hint=(1, 0.4), spacing=5, padding=[10,0,10,10])
        
        debug_header = BoxLayout(orientation='horizontal', size_hint=(1, 0.15), spacing=10)
        debug_title = Label(
            text='Debug Log:',
            size_hint=(0.7, 1),
            bold=True,
            halign='left',
            valign='middle'
        )
        debug_title.bind(size=debug_title.setter('text_size'))
        
        clear_btn = Button(
            text='Clear Log',
            size_hint=(0.3, 1),
            background_color=(0.8, 0.3, 0.3, 1)
        )
        clear_btn.bind(on_press=self.clear_log)
        
        debug_header.add_widget(debug_title)
        debug_header.add_widget(clear_btn)
        debug_section.add_widget(debug_header)
        
        scroll = ScrollView(size_hint=(1, 0.85))
        self.debug_label = Label(
            text='',
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            font_size='10sp'
        )
        self.debug_label.bind(texture_size=self.debug_label.setter('size'))
        self.debug_label.bind(size=self.debug_label.setter('text_size'))
        scroll.add_widget(self.debug_label)
        debug_section.add_widget(scroll)
        
        main_layout.add_widget(debug_section)
        
        self.log(f"App started on platform: {platform}")
        self.log(f"Default camera IP: {self.camera_ip}")
        self.log(f"SSL context created: verify_mode={self.ssl_context.verify_mode}")
        
        return main_layout
    
    def clear_log(self, instance):
        """Clear debug log"""
        self.debug_messages = []
        self.debug_label.text = ''
        self.log("Log cleared")
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def make_request(self, url, method='GET', data=None):
        """Make HTTP request using urllib"""
        self.log(f"Making {method} request to: {url}")
        
        try:
            if data:
                data = json.dumps(data).encode('utf-8')
                self.log(f"Request data: {data}")
            
            req = urllib.request.Request(url, data=data, method=method)
            if data:
                req.add_header('Content-Type', 'application/json')
            
            self.log("Opening URL connection...")
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=10) as response:
                self.log(f"Response status: {response.status}")
                response_data = response.read().decode('utf-8')
                self.log(f"Response data: {response_data[:200]}")
                return json.loads(response_data), response.status
                
        except urllib.error.HTTPError as e:
            self.log(f"HTTPError: {e.code} {e.reason}")
            raise Exception(f"HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            self.log(f"URLError: {e.reason}")
            raise Exception(f"URL Error: {e.reason}")
        except Exception as e:
            self.log(f"Exception type: {type(e).__name__}")
            self.log(f"Exception: {str(e)}")
            raise
    
    def connect_camera(self, instance):
        self.camera_ip = self.ip_input.text.strip()
        self.log(f"=== Connection attempt started ===")
        self.log(f"Target: {self.camera_ip}:443")
        self.status_label.text = 'Status: Connecting...'
        self.status_label.color = (1, 1, 0, 1)
        
        try:
            url = f'https://{self.camera_ip}:443/ccapi/ver100/deviceinformation'
            data, status = self.make_request(url)
            
            if status == 200:
                self.connected = True
                product_name = data.get("productname", "Camera")
                self.status_label.text = f'Status: Connected to {product_name}'
                self.status_label.color = (0, 1, 0, 1)
                self.log(f"SUCCESS: Connected to {product_name}")
                self.show_popup('Success', 'Connected to camera!')
            else:
                raise Exception(f'HTTP {status}')
                
        except Exception as e:
            self.connected = False
            self.status_label.text = 'Status: Connection Failed'
            self.status_label.color = (1, 0, 0, 1)
            error_msg = str(e)
            self.log(f"FAILED: {error_msg}")
            self.show_popup('Error', f'Connection failed:\n{error_msg[:150]}')
    
    def get_metadata(self, field):
        if not self.connected:
            self.show_popup('Error', 'Please connect to camera first')
            return
        
        try:
            url = f'https://{self.camera_ip}:443/ccapi/ver100/functions/registeredname/{field}'
            data, status = self.make_request(url)
            
            if status == 200:
                value = data.get(field, '')
                self.log(f"{field} value: {value}")
                
                if field == 'copyright':
                    self.copyright_input.text = value
                elif field == 'author':
                    self.author_input.text = value
                
                if value:
                    self.show_popup('Success', f'{field.capitalize()} retrieved:\n{value}')
                else:
                    self.show_popup('Info', f'{field.capitalize()} is empty')
            else:
                raise Exception(f'HTTP {status}')
                
        except Exception as e:
            error_msg = str(e)
            self.log(f"Error getting {field}: {error_msg}")
            self.show_popup('Error', f'Failed to get {field}:\n{error_msg[:150]}')
    
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
            data, status = self.make_request(url, method='PUT', data={field: value})
            
            if status == 200:
                self.log(f"Successfully set {field}")
                self.show_popup('Success', f'{field.capitalize()} set to:\n{value}')
            else:
                raise Exception(f'HTTP {status}')
                
        except Exception as e:
            error_msg = str(e)
            self.log(f"Error setting {field}: {error_msg}")
            self.show_popup('Error', f'Failed to set {field}:\n{error_msg[:150]}')

if __name__ == '__main__':
    CameraMetadataApp().run()
