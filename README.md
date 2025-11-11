# HTML Terminal

A modern terminal application that can render HTML content alongside executing regular shell commands.

## Features

- **HTML Rendering**: Render HTML content directly in the terminal with proper styling
- **HTML Mode Toggle**: Switch between HTML rendering and plain text mode
- **Command Execution**: Execute normal terminal commands (bash, zsh, etc.)
- **HTML-Wrapped Commands**: Wrap commands in HTML tags to render their output with styling
  - Example: `<h1>echo 'Hello World'</h1>` - executes the command and wraps output in h1 tags
- **Command History**: Use up/down arrows to navigate through command history
- **Dark Theme**: Modern dark theme optimized for terminal use
- **Responsive**: HTML content is rendered responsively

![Screenshot of the HTML Enabled Terminal by nodes.](htmlterminal1.png)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

**Quick Start** (recommended):
```bash
python -m venv ./venv
./run.sh
```

Or activate the virtual environment and run manually:
```bash
python -m venv ./venv
source venv/bin/activate
python html_terminal.py
```

## Examples

### Regular Commands
```bash
ls -la
pwd
echo "Hello World"
```

### HTML Content
```html
<h1>This is a heading</h1>
<p>This is a <strong>paragraph</strong> with <em>formatting</em>.</p>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>
```

### HTML-Wrapped Commands
```bash
<h1>echo "Big Header"</h1>
<h2>date</h2>
<p>ls -la</p>
<code>pwd</code>
```

### Image Support
Display images from URLs or local files:
```html
<img src="https://picsum.photos/400/300" alt="Random image">
<img src="./my-image.png" alt="Local image">
<img src="/absolute/path/to/image.jpg" alt="Absolute path">
```

You can also combine images with commands:
```bash
<div><h2>My Screenshot</h2><img src="screenshot.png" width="500"></div>
```

### Toggle HTML Mode
- Check/uncheck the "HTML Mode" checkbox to switch between HTML rendering and plain text
- In plain text mode, HTML tags are stripped and content is displayed as plain text

## Keyboard Shortcuts

- **Enter**: Execute command
- **Up Arrow**: Previous command in history
- **Down Arrow**: Next command in history

## Technical Details

- Built with PyQt6 for cross-platform GUI support
- Uses QWebEngineView (Chromium-based) for HTML rendering
- Executes commands via subprocess in the current shell environment
- Supports directory navigation with `cd` command

