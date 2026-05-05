# GLM Industrial Console

A minimalist, industrial-styled AI chat interface built with Python and Tkinter, powered by ZhipuAI (GLM).

## Features
- **Minimalist UI**: Dark-themed, industrial aesthetic with high-contrast accents.
- **Responsive Design**: Auto-adjusting input field with multi-line support.
- **Async Processing**: Non-blocking chat flow using threading.
- **Keyboard Shortcuts**: `Enter` to send, `Shift + Enter` for new lines.

## Prerequisites
- Python 3.8+
- A valid ZhipuAI API Key

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/nettonet/glm-industrial-console.git
   cd glm-industrial-console
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration
Set your API key as an environment variable:
- **Windows (CMD)**: `set ai_agent=your_api_key_here`
- **Linux/macOS**: `export ai_agent=your_api_key_here`

## Usage
Run the application:
```bash
python main.py
```

## License
[MIT License](LICENSE)
