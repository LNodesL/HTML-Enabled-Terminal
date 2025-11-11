#!/usr/bin/env python3
"""
HTML Terminal - A terminal that can render HTML content
"""

import sys
import subprocess
import re
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QCheckBox)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont


class HTMLTerminal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.html_mode = True
        self.command_history = []
        self.history_index = -1
        self.current_dir = os.path.expanduser("~")
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("HTML Terminal")
        self.setGeometry(100, 100, 1000, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Top control bar
        control_layout = QHBoxLayout()
        
        # HTML Mode checkbox
        self.html_checkbox = QCheckBox("HTML Mode")
        self.html_checkbox.setChecked(True)
        self.html_checkbox.stateChanged.connect(self.toggle_html_mode)
        control_layout.addWidget(self.html_checkbox)
        
        # Clear button
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_terminal)
        control_layout.addWidget(clear_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # Web view for rendering
        self.web_view = QWebEngineView()
        
        # Enable local file access for images
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        
        layout.addWidget(self.web_view, stretch=1)
        
        # Initialize content
        self.terminal_content = []
        self.update_display()
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.prompt_label = QLineEdit()
        self.prompt_label.setReadOnly(True)
        self.prompt_label.setText(f"{os.getcwd()} $ ")
        self.prompt_label.setMaximumWidth(400)
        input_layout.addWidget(self.prompt_label)
        
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.execute_command)
        self.input_field.setPlaceholderText("Enter command or HTML...")
        input_layout.addWidget(self.input_field)
        
        layout.addLayout(input_layout)
        
        # Focus on input
        self.input_field.setFocus()
        
    def toggle_html_mode(self, state):
        self.html_mode = state == Qt.CheckState.Checked.value
        self.update_display()
        
    def clear_terminal(self):
        self.terminal_content = []
        self.update_display()
        
    def update_display(self):
        # Set base URL to current directory to allow local file access
        base_url = QUrl.fromLocalFile(os.getcwd() + "/")
        
        if self.html_mode:
            # Render as HTML
            html_content = self.build_html()
            self.web_view.setHtml(html_content, base_url)
        else:
            # Render as plain text
            plain_content = self.build_plain_text()
            html_wrapper = f"""
            <html>
            <head>
                <style>
                    body {{
                        background-color: #1e1e1e;
                        color: #d4d4d4;
                        font-family: 'Courier New', monospace;
                        font-size: 14px;
                        padding: 10px;
                        margin: 0;
                    }}
                    pre {{
                        margin: 0;
                        white-space: pre-wrap;
                        word-wrap: break-word;
                    }}
                </style>
            </head>
            <body>
                <pre>{plain_content}</pre>
            </body>
            </html>
            """
            self.web_view.setHtml(html_wrapper, base_url)
            
    def build_html(self):
        content_html = "".join(self.terminal_content)
        
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    background-color: #1e1e1e;
                    color: #d4d4d4;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                    font-size: 14px;
                    padding: 15px;
                    margin: 0;
                    line-height: 1.6;
                }}
                .terminal-line {{
                    margin-bottom: 10px;
                }}
                .command {{
                    color: #4ec9b0;
                    font-family: 'Courier New', monospace;
                    margin-bottom: 5px;
                }}
                .output {{
                    color: #d4d4d4;
                    margin-left: 20px;
                    margin-bottom: 10px;
                }}
                .error {{
                    color: #f48771;
                    margin-left: 20px;
                    margin-bottom: 10px;
                }}
                pre {{
                    background-color: #2d2d2d;
                    padding: 10px;
                    border-radius: 4px;
                    overflow-x: auto;
                }}
                code {{
                    background-color: #2d2d2d;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #569cd6;
                    margin-top: 10px;
                    margin-bottom: 10px;
                }}
                a {{
                    color: #3794ff;
                }}
                table {{
                    border-collapse: collapse;
                    margin: 10px 0;
                }}
                th, td {{
                    border: 1px solid #3c3c3c;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #2d2d2d;
                    color: #569cd6;
                }}
                img {{
                    max-width: 100%;
                    height: auto;
                    border-radius: 8px;
                    margin: 10px 0;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                }}
            </style>
        </head>
        <body>
            {content_html}
        </body>
        </html>
        """
        return html
        
    def build_plain_text(self):
        plain_lines = []
        for item in self.terminal_content:
            # Strip HTML tags for plain text view
            plain = re.sub('<[^<]+?>', '', item)
            plain_lines.append(plain)
        return "\n".join(plain_lines)
        
    def execute_command(self):
        command = self.input_field.text().strip()
        if not command:
            return
            
        self.input_field.clear()
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Display the command
        prompt = f"{os.getcwd()} $ "
        self.terminal_content.append(f'<div class="terminal-line"><div class="command">{prompt}{self.escape_html(command)}</div>')
        
        # Check if command is wrapped in HTML tags
        html_match = re.match(r'^<([a-zA-Z][a-zA-Z0-9]*)(?:\s[^>]*)?>(.+?)</\1>$', command, re.DOTALL)
        
        if html_match:
            # Extract the tag and the actual command
            tag = html_match.group(1)
            actual_command = html_match.group(2).strip()
            
            # Execute the actual command
            output, error, return_code = self.run_command(actual_command)
            
            # Wrap output in the HTML tag (render HTML if present in output)
            if output:
                rendered_output = self.render_if_html(output)
                self.terminal_content.append(f'<div class="output"><{tag}>{rendered_output}</{tag}></div>')
            if error:
                self.terminal_content.append(f'<div class="error"><{tag}>{self.escape_html(error)}</{tag}></div>')
                
        elif command.startswith('<') and '>' in command:
            # Looks like HTML, render it directly
            processed_html = self.process_image_tags(command)
            self.terminal_content.append(f'<div class="output">{processed_html}</div>')
            
        else:
            # Regular command execution
            output, error, return_code = self.run_command(command)
            
            if output:
                rendered_output = self.render_if_html(output)
                self.terminal_content.append(f'<div class="output">{rendered_output}</div>')
            if error:
                self.terminal_content.append(f'<div class="error">{self.escape_html(error)}</div>')
        
        self.terminal_content.append('</div>')
        
        # Update prompt
        self.prompt_label.setText(f"{os.getcwd()} $ ")
        
        # Update display
        self.update_display()
        
        # Scroll to bottom
        self.web_view.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")
        
    def run_command(self, command):
        """Execute a shell command and return output, error, and return code"""
        
        # Handle cd command specially
        if command.startswith('cd '):
            path = command[3:].strip()
            try:
                if path:
                    os.chdir(os.path.expanduser(path))
                else:
                    os.chdir(os.path.expanduser("~"))
                return "", "", 0
            except Exception as e:
                return "", str(e), 1
        elif command == 'cd':
            os.chdir(os.path.expanduser("~"))
            return "", "", 0
        
        # Handle clear
        if command == 'clear':
            self.clear_terminal()
            return "", "", 0
            
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                timeout=30
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out after 30 seconds", 1
        except Exception as e:
            return "", str(e), 1
            
    def escape_html(self, text):
        """Escape HTML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
    
    def render_if_html(self, text):
        """Render text as HTML if it contains HTML tags, otherwise escape it"""
        if self.html_mode and re.search(r'<[a-zA-Z][^>]*>', text):
            # Contains HTML tags and HTML mode is active, render it
            # Process image tags to handle local file paths
            text = self.process_image_tags(text)
            return text
        else:
            # No HTML tags or HTML mode is off, escape for safety
            return self.escape_html(text)
    
    def process_image_tags(self, html):
        """Process img tags to convert local file paths to file:// URLs"""
        def replace_img_src(match):
            full_tag = match.group(0)
            src_match = re.search(r'src=["\']([^"\']+)["\']', full_tag)
            if src_match:
                src = src_match.group(1)
                # Check if it's not already a URL (http://, https://, file://, data:)
                if not re.match(r'^(https?://|file://|data:)', src):
                    # Only convert absolute paths to file:// URLs
                    # Relative paths will be resolved by the base URL
                    if os.path.isabs(src):
                        # Convert absolute path to file:// URL
                        src = 'file://' + src
                        # Replace the src in the tag
                        full_tag = re.sub(r'src=["\']([^"\']+)["\']', f'src="{src}"', full_tag)
                    # else: leave relative paths as-is, they'll work with base URL
            return full_tag
        
        # Process all img tags
        html = re.sub(r'<img[^>]*>', replace_img_src, html)
        return html
        
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_Up:
            # Previous command
            if self.command_history and self.history_index > 0:
                self.history_index -= 1
                self.input_field.setText(self.command_history[self.history_index])
        elif event.key() == Qt.Key.Key_Down:
            # Next command
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.input_field.setText(self.command_history[self.history_index])
            else:
                self.history_index = len(self.command_history)
                self.input_field.clear()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    terminal = HTMLTerminal()
    terminal.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

