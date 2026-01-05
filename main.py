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
import socket
import ssl
import json
from datetime import datetime

class CameraMetadataApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug_messages = []
        
    def log(self, message):
        """Add timestamped log message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        self.debug_messages.append(log_msg)
        
        if len(self.debug_messages) > 50:
            self.debug_messages.pop(0)
        
        if hasattr(self, 'debug_label'):
            self.debug_label.text = '\n'.join(self.debug_messages)
        
        print(log_msg)
        
    def build(self):
        self.camera_ip = '192.168.34.29'
        self.connected = False
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Top section - Connection and Metadata
        top_section = BoxLayout(orientation='vertical', size_hint=(1, 0.7), spacing=10, padding=[10,10,10,0])
        
        title = Label(
            text='Camera Metadata Manager',
            size_hint=(1, 0.08),
            font_size='24sp',
            bold=True
        )
        top_section.add_widget(title)
        
        # IP input
        ip_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=10)
        ip_label = Label(text='Camera IP:', size_hint=(0.3, 1))
        self.ip_input = TextInput(
            text=self.camera_ip,
            size_hint=(0.5, 1),
            multiline=False
        )
        ip_layout.add_widget(ip_label)
        ip_layout.add_widget(self.ip_input)
        top_section.add_widget(ip_layout)
        
        # Connect button
        self.connect_btn = Button(
            text='Connect to Camera',
            size_hint=(1, 0.07),
            background_color=(0.13, 0.59, 0.95, 1)
        )
        self.connect_btn.bind(on_press=self.connect_camera)
        top_section.add_widget(self.connect_btn)
        
        # Status
        self.status_label = Label(
            text='Status: Not Connected',
            size_hint=(1, 0.06),
            color=(1, 0, 0, 1)
        )
        top_section.add_widget(self.status_label)
        
        # Author input
        author_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=10)
        author_label = Label(text='Author:', size_hint=(0.3, 1))
        self.author_input = TextInput(
            text='',
            size_hint=(0.7, 1),
            multiline=False,
            hint_text='Enter author name'
        )
        author_layout.add_widget(author_label)
        author_layout.add_widget(self.author_input)
        top_section.add_widget(author_layout)
        
        # Copyright input
        copyright_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=10)
        copyright_label = Label(text='Copyright:', size_hint=(0.3, 1))
        self.copyright_input = TextInput(
            text='',
            size_hint=(0.7, 1),
            multiline=False,
            hint_text='Enter copyright info'
        )
        copyright_layout.add_widget(copyright_label)
        copyright_layout.add_widget(self.copyright_input)
        top_section.add_widget(copyright_layout)
        
        # Owner Name input
        owner_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=10)
        owner_label = Label(text='Owner Name:', size_hint=(0.3, 1))
        self.owner_input = TextInput(
            text='',
            size_hint=(0.7, 1),
            multiline=False,
            hint_text='Enter owner name'
        )
        owner_layout.add_widget(owner_label)
        owner_layout.add_widget(self.owner_input)
        top_section.add_widget(owner_layout)
        
        # Nickname input
        nickname_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=10)
        nickname_label = Label(text='Nickname:', size_hint=(0.3, 1))
        self.nickname_input = TextInput(
            text='',
            size_hint=(0.7, 1),
            multiline=False,
            hint_text='Enter camera nickname'
        )
        nickname_layout.add_widget(nickname_label)
        nickname_layout.add_widget(self.nickname_input)
        top_section.add_widget(nickname_layout)
        
        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.07), spacing=10)
        
        self.get_metadata_btn = Button(
            text='Get All',
            background_color=(0.2, 0.7, 0.3, 1),
            disabled=True
        )
        self.get_metadata_btn.bind(on_press=self.get_all_metadata)
        button_layout.add_widget(self.get_metadata_btn)
        
        self.update_metadata_btn = Button(
            text='Update All',
            background_color=(0.95, 0.6, 0.13, 1),
            disabled=True
        )
        self.update_metadata_btn.bind(on_press=self.update_all_metadata)
        button_layout.add_widget(self.update_metadata_btn)
        
        top_section.add_widget(button_layout)
        
        main_layout.add_widget(top_section)
        
        # Debug console section
        debug_section = BoxLayout(orientation='vertical', size_hint=(1, 0.3), spacing=5, padding=[10,0,10,10])
        
        debug_header = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), spacing=10)
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
        
        scroll = ScrollView(size_hint=(1, 0.8))
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
        self.log(f"Ready to connect")
        
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
    
    def https_request(self, method, path, data=None):
        """Make HTTPS request to camera"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.camera_ip, 443))
            
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ssl_sock = context.wrap_socket(sock, server_hostname=self.camera_ip)
            
            # Build request
            if data:
                payload = json.dumps(data)
                request = (
                    f"{method} {path} HTTP/1.1\r\n"
                    f"Host: {self.camera_ip}\r\n"
                    f"Content-Type: application/json\r\n"
                    f"Content-Length: {len(payload)}\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                    f"{payload}"
                ).encode()
            else:
                request = (
                    f"{method} {path} HTTP/1.1\r\n"
                    f"Host: {self.camera_ip}\r\n"
                    f"Connection: close\r\n"
                    f"\r\n"
                ).encode()
            
            ssl_sock.sendall(request)
            
            response = b""
            while True:
                chunk = ssl_sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            ssl_sock.close()
            
            response_text = response.decode('utf-8', errors='ignore')
            lines = response_text.split('\r\n')
            status_line = lines[0]
            
            # Extract JSON body
            json_start = response_text.find('{')
            json_body = None
            if json_start > 0:
                json_body = json.loads(response_text[json_start:])
            
            return status_line, json_body
            
        except Exception as e:
            raise Exception(f"Request failed: {e}")
    
    def connect_camera(self, instance):
        """Test connection to camera"""
        self.camera_ip = self.ip_input.text.strip()
        self.log(f"=== Connecting to {self.camera_ip} ===")
        self.status_label.text = 'Status: Connecting...'
        self.status_label.color = (1, 1, 0, 1)
        
        try:
            status, data = self.https_request('GET', '/ccapi/ver100/deviceinformation')
            
            if '200 OK' in status and data:
                self.connected = True
                self.status_label.text = 'Status: Connected!'
                self.status_label.color = (0, 1, 0, 1)
                self.get_metadata_btn.disabled = False
                self.update_metadata_btn.disabled = False
                
                product = data.get('productname', 'Unknown')
                self.log(f"✓ Connected to {product}")
                self.show_popup('Success', f'Connected to {product}!')
            else:
                raise Exception(f"Unexpected response: {status}")
            
        except Exception as e:
            self.connected = False
            self.status_label.text = 'Status: Failed'
            self.status_label.color = (1, 0, 0, 1)
            self.get_metadata_btn.disabled = True
            self.update_metadata_btn.disabled = True
            self.log(f"✗ Error: {e}")
            self.show_popup('Error', f'Connection failed: {e}')
    
    def get_all_metadata(self, instance):
        """Get all metadata from camera"""
        self.log(f"=== Getting all metadata ===")
        
        fields = ['author', 'copyright', 'ownername', 'nickname']
        
        for field in fields:
            try:
                status, data = self.https_request('GET', f'/ccapi/ver100/functions/registeredname/{field}')
                
                if '200 OK' in status and data:
                    value = data.get(field, '')
                    self.log(f"✓ {field}: '{value}'")
                    
                    if field == 'author':
                        self.author_input.text = value
                    elif field == 'copyright':
                        self.copyright_input.text = value
                    elif field == 'ownername':
                        self.owner_input.text = value
                    elif field == 'nickname':
                        self.nickname_input.text = value
                else:
                    self.log(f"✗ Failed to get {field}: {status}")
                    
            except Exception as e:
                self.log(f"✗ Error getting {field}: {e}")
        
        self.show_popup('Success', 'Metadata retrieved!')
    
    def update_all_metadata(self, instance):
        """Update all metadata on camera"""
        self.log(f"=== Updating metadata ===")
        
        fields = {
            'author': self.author_input.text.strip(),
            'copyright': self.copyright_input.text.strip(),
            'ownername': self.owner_input.text.strip(),
            'nickname': self.nickname_input.text.strip()
        }
        
        updated = []
        
        for field, value in fields.items():
            if value:  # Only update non-empty fields
                try:
                    status, data = self.https_request(
                        'PUT',
                        f'/ccapi/ver100/functions/registeredname/{field}',
                        {field: value}
                    )
                    
                    if '200 OK' in status:
                        self.log(f"✓ Updated {field} to '{value}'")
                        updated.append(field)
                    else:
                        self.log(f"✗ Failed to update {field}: {status}")
                        
                except Exception as e:
                    self.log(f"✗ Error updating {field}: {e}")
        
        if updated:
            self.show_popup('Success', f'Updated: {", ".join(updated)}')
        else:
            self.show_popup('Warning', 'No fields were updated')

if __name__ == '__main__':
    CameraMetadataApp().run()
