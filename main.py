import tkinter as tk
from tkinter import ttk, scrolledtext
from zhipuai import ZhipuAI
import os
import threading
import datetime
import configparser

# ==================== Industrial Aesthetic Color Palette ====================
COLORS = {
    "bg_main": "#121212",          # Deep Midnight
    "bg_panel": "#1d1d1d",         # Matte Charcoal
    "bg_input": "#252525",         # Input Field Grey
    "border": "#333333",           # Border Color
    "accent": "#00e676",           # Cyber Green
    "accent_hover": "#00c853",     
    "text_primary": "#e0e0e0",     # Soft White
    "text_secondary": "#757575",   # Steel Grey
    "user_msg": "#2979ff",         # Circuit Blue
    "ai_msg": "#00e676",           # Cyber Green
    "error_msg": "#ff5252",        # Alert Red
    "send_btn_text": "#121212",    
}
# Load configuration file and read API_KEY
config = configparser.ConfigParser()
config.read('config.ini')

API_KEY = config.get('api', 'api_key', fallback=None)   ## Please visit the Zhipu AI website to apply for an API_KEY (https://open.bigmodel.cn)
if not API_KEY:
    raise ValueError("API_KEY is not configured. Please check the config.ini file.")

client = ZhipuAI(api_key=API_KEY)

messages = [
    {"role": "system", "content": "You are a helpful AI assistant."}
]

# ==================== Core Functions ====================
def send_message(event=None):
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        return

    input_text.delete("1.0", tk.END)
    adjust_input_height()

    append_chat("You", user_input, "user")
    send_btn.config(state=tk.DISABLED, text="...", bg=COLORS["border"])

    def fetch_reply():
        try:
            temp_messages = messages.copy()
            temp_messages.append({"role": "user", "content": user_input})
            response = client.chat.completions.create(
                model="glm-4.6",
                messages=temp_messages,
                temperature=0.7
            )
            ai_reply = response.choices[0].message.content

            chat_area.after(0, lambda: append_chat("AI", ai_reply, "assistant"))
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": ai_reply})
        except Exception as e:
            chat_area.after(0, lambda: append_chat("System Error", str(e), "error"))
        finally:
            send_btn.after(0, lambda: send_btn.config(
                state=tk.NORMAL, text="▶ Send", bg=COLORS["accent"]
            ))

    threading.Thread(target=fetch_reply, daemon=True).start()

def append_chat(sender, content, tag):
    """Append messages with timestamp and formatting."""
    chat_area.config(state=tk.NORMAL)
    timestamp = datetime.datetime.now().strftime("%H:%M")
    
    if chat_area.index('end-1c') != "1.0":
        chat_area.insert(tk.END, "\n", "spacer")
    
    chat_area.insert(tk.END, f"[{timestamp}] {sender}\n", f"{tag}_header")
    chat_area.insert(tk.END, f"{content}\n", tag)
    
    chat_area.see(tk.END)
    chat_area.config(state=tk.DISABLED)

def adjust_input_height(event=None):
    lines = int(input_text.index('end-1c').split('.')[0])
    new_height = min(max(lines, 3), 10)
    input_text.config(height=new_height)

def on_key_press(event):
    if event.keysym == "Return":
        if event.state & 0x0001:  # Shift + Enter
            input_text.insert(tk.INSERT, "\n")
            adjust_input_height()
            return "break"
        else:
            send_message()
            return "break"

# ==================== UI Construction ====================
root = tk.Tk()
root.title("GLM AI Console")
root.geometry("800x700")
root.minsize(600, 450)
root.configure(bg=COLORS["bg_main"])

FONT_MAIN = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")

# Header
header = tk.Frame(root, bg=COLORS["bg_panel"], height=42)
header.pack(fill=tk.X, padx=0, pady=0)
header.pack_propagate(False)

tk.Label(header, text="◈ GLM AI Assistant", bg=COLORS["bg_panel"], fg=COLORS["accent"], 
         font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=15, pady=8)

tk.Label(header, text="Online", bg=COLORS["bg_panel"], fg=COLORS["text_secondary"], 
         font=FONT_MAIN).pack(side=tk.RIGHT, padx=15, pady=8)

# Chat Area
chat_container = tk.Frame(root, bg=COLORS["bg_main"])
chat_container.pack(padx=12, pady=(12, 8), fill=tk.BOTH, expand=True)

chat_area = scrolledtext.ScrolledText(chat_container, wrap=tk.WORD, state=tk.DISABLED, 
                                      font=FONT_MAIN, bg=COLORS["bg_panel"], fg=COLORS["text_primary"], 
                                      insertbackground=COLORS["accent"], relief=tk.FLAT, padx=12, pady=12)
chat_area.pack(fill=tk.BOTH, expand=True)

chat_area.tag_config("user_header", foreground=COLORS["user_msg"], font=FONT_BOLD)
chat_area.tag_config("user", foreground=COLORS["text_primary"], font=FONT_MAIN, lmargin1=12)
chat_area.tag_config("assistant_header", foreground=COLORS["ai_msg"], font=FONT_BOLD)
chat_area.tag_config("assistant", foreground=COLORS["text_primary"], font=FONT_MAIN, lmargin1=12)
chat_area.tag_config("error_header", foreground=COLORS["error_msg"], font=FONT_BOLD)
chat_area.tag_config("error", foreground=COLORS["error_msg"], font=FONT_MAIN, lmargin1=12)
chat_area.tag_config("spacer", font=("Arial", 2))

# Bottom Input
bottom_frame = tk.Frame(root, bg=COLORS["bg_main"])
bottom_frame.pack(padx=12, pady=(0, 12), fill=tk.X)

input_frame = tk.Frame(bottom_frame, bg=COLORS["border"], padx=1, pady=1)
input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

input_text = tk.Text(input_frame, height=3, font=FONT_MAIN, wrap=tk.WORD, bg=COLORS["bg_input"], 
                     fg=COLORS["text_primary"], insertbackground=COLORS["accent"], relief=tk.FLAT, padx=10, pady=8)
input_text.pack(fill=tk.BOTH, expand=True)

input_text.bind("<KeyPress>", on_key_press)

send_btn = tk.Button(bottom_frame, text="▶ Send", command=send_message, font=FONT_BOLD, 
                     bg=COLORS["accent"], fg=COLORS["send_btn_text"], relief=tk.FLAT, 
                     cursor="hand2", width=10)
send_btn.pack(side=tk.RIGHT, fill=tk.Y)

hint = tk.Label(root, text="Enter to Send  |  Shift + Enter for New Line", 
                bg=COLORS["bg_main"], fg=COLORS["text_secondary"], font=("Segoe UI", 8))
hint.pack(side=tk.BOTTOM, pady=(0, 8))

append_chat("System", "Assistant initialized. How can I help you today?", "assistant")
root.mainloop()
