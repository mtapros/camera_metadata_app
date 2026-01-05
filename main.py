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
        
        # Test buttons
        test_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.12), spacing=10)
        
        self.test_socket_btn = Button(
            text='Test Socket',
            background_color=(0.8, 0.4, 0.2, 1)
        )
        self.test_socket_btn.bind(on_press=self.test_socket)
        test_layout.add_widget(self.test_socket_btn)
        
        self.test_ssl_btn = Button(
            text='Test SSL',
            background_color=(0.8, 0.6, 0.2, 1)
        )
        self.test_ssl_btn.bind(on_press=self.test_ssl_socket)
        test_layout.add_widget(self.test_ssl_btn)
        
        top_section.add_widget(test_layout)
        
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
        self.log(f"Python socket module available: {socket is not None}")
        self.log(f"SSL module available: {ssl is not None}")
        
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
    
    def test_socket(self, instance):
        """Test raw socket connection"""
        self.camera_ip = self.ip_input.text.strip()
        self.log(f"=== Testing RAW SOCKET to {self.camera_ip}:443 ===")
        
        try:
            self.log("Creating socket...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            self.log(f"Connecting to {self.camera_ip}:443...")
            sock.connect((self.camera_ip, 443))
            
            self.log("✓ Socket connected successfully!")
            self.show_popup('Success', 'Raw socket connection works!')
            
            sock.close()
            self.log("Socket closed")
            
        except socket.timeout:
            self.log("✗ Socket timeout")
            self.show_popup('Error', 'Socket connection timed out')
        except socket.error as e:
            self.log(f"✗ Socket error: {e}")
            self.log(f"Error type: {type(e)}")
            self.log(f"Error errno: {e.errno if hasattr(e, 'errno') else 'N/A'}")
            self.show_popup('Error', f'Socket error: {e}')
        except Exception as e:
            self.log(f"✗ Exception: {type(e).__name__}: {e}")
            self.show_popup('Error', f'Error: {e}')
    
    def test_ssl_socket(self, instance):
        """Test SSL wrapped socket connection"""
        self.camera_ip = self.ip_input.text.strip()
        self.log(f"=== Testing SSL SOCKET to {self.camera_ip}:443 ===")
        
        try:
            self.log("Creating socket...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            self.log(f"Connecting socket to {self.camera_ip}:443...")
            sock.connect((self.camera_ip, 443))
            self.log("✓ Socket connected")
            
            self.log("Creating SSL context...")
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.log(f"SSL context: verify_mode={context.verify_mode}")
            
            self.log("Wrapping socket with SSL...")
            ssl_sock = context.wrap_socket(sock, server_hostname=self.camera_ip)
            self.log("✓ SSL handshake complete!")
            
            self.log(f"SSL version: {ssl_sock.version()}")
            self.log(f"Cipher: {ssl_sock.cipher()}")
            
            self.show_popup('Success', 'SSL socket connection works!')
            
            ssl_sock.close()
            self.log("SSL socket closed")
            
        except socket.timeout:
            self.log("✗ Socket timeout")
            self.show_popup('Error', 'Connection timed out')
        except ssl.SSLError as e:
            self.log(f"✗ SSL error: {e}")
            self.show_popup('Error', f'SSL error: {e}')
        except socket.error as e:
            self.log(f"✗ Socket error: {e}")
            self.log(f"Error errno: {e.errno if hasattr(e, 'errno') else 'N/A'}")
            self.show_popup('Error', f'Socket error: {e}')
        except Exception as e:
            self.log(f"✗ Exception: {type(e).__name__}: {e}")
            self.show_popup('Error', f'Error: {e}')
    
    def connect_camera(self, instance):
        """Full HTTP request"""
        self.camera_ip = self.ip_input.text.strip()
        self.log(f"=== Full HTTPS request to {self.camera_ip}:443 ===")
        self.status_label.text = 'Status: Connecting...'
        self.status_label.color = (1, 1, 0, 1)
        
        try:
            self.log("Creating socket...")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            self.log("Connecting...")
            sock.connect((self.camera_ip, 443))
            
            self.log("Wrapping with SSL...")
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ssl_sock = context.wrap_socket(sock, server_hostname=self.camera_ip)
            
            self.log("Sending HTTP GET request...")
            request = (
                b"GET /ccapi/ver100/deviceinformation HTTP/1.1\r\n"
                b"Host: " + self.camera_ip.encode() + b"\r\n"
                b"Connection: close\r\n"
                b"\r\n"
            )
            ssl_sock.sendall(request)
            self.log("Request sent, waiting for response...")
            
            response = b""
            while True:
                chunk = ssl_sock.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            self.log(f"Received {len(response)} bytes")
            response_text = response.decode('utf-8', errors='ignore')
            
            # Parse response
            lines = response_text.split('\r\n')
            self.log(f"Status line: {lines[0]}")
            
            # Find JSON body
            json_start = response_text.find('{')
            if json_start > 0:
                json_body = response_text[json_start:]
                self.log(f"JSON body: {json_body[:200]}")
                
                if '"productname"' in json_body:
                    self.connected = True
                    self.status_label.text = 'Status: Connected!'
                    self.status_label.color = (0, 1, 0, 1)
                    self.show_popup('Success', 'Connected to camera!')
                else:
                    raise Exception("No productname in response")
            else:
                raise Exception("No JSON in response")
            
            ssl_sock.close()
            
        except Exception as e:
            self.connected = False
            self.status_label.text = 'Status: Failed'
            self.status_label.color = (1, 0, 0, 1)
            self.log(f"✗ Error: {type(e).__name__}: {e}")
            self.show_popup('Error', f'Connection failed: {e}')

if __name__ == '__main__':
    CameraMetadataApp().run()
