import tkinter as tk
from tkinter import ttk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from PIL import Image, ImageTk
import torch

# Supported target languages
language_codes = {
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "English": "en"
}

# Translation function
def translate_text():
    tgt_lang = language_codes[target_lang.get()]
    input_text = input_box.get("1.0", tk.END).strip()

    if tgt_lang == "en":
        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, input_text)
        output_box.config(state='disabled')
        return

    model_name = f"Helsinki-NLP/opus-mt-en-{tgt_lang}"
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        inputs = tokenizer([input_text], return_tensors="pt", padding=True)
        translated_tokens = model.generate(**inputs, max_length=128)
        translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)

        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, translated_text)
        output_box.config(state='disabled')
    except:
        output_box.config(state='normal')
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, "Translation model not available.")
        output_box.config(state='disabled')

# Clear all function
def clear_all():
    input_box.delete("1.0", tk.END)
    output_box.config(state='normal')
    output_box.delete("1.0", tk.END)
    output_box.config(state='disabled')

# Create main window
window = tk.Tk()
window.title("🌐 English Translator")
window.geometry("800x600")

# Load and set background image
bg_image = Image.open(r"C:\Users\darpan yaduvanshi\Downloads\translation-services-translate-wlf7u3xq6oj2veta.jpg")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(window, image=bg_photo)
bg_label.image = bg_photo
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Dark overlay frame
overlay = tk.Frame(window, bg="#000000", bd=0)
overlay.place(x=50, y=50, width=700, height=500)

# Fonts and colors
font_label = ("Segoe UI", 12)
font_text = ("Segoe UI", 11)
text_bg = "#1e1e1e"
text_fg = "#ffffff"
btn_bg = "#4CAF50"
btn_fg = "white"

# Title
title = tk.Label(overlay, text="🌍 English Translator", font=("Segoe UI", 18, "bold"), fg="white", bg="#000000")
title.pack(pady=10)

# Target language dropdown
tk.Label(overlay, text="To Language:", font=font_label, bg="#000000", fg="white").pack()
target_lang = tk.StringVar(value="Hindi")
ttk.Style().configure("TCombobox", padding=5)
lang_dropdown = ttk.Combobox(overlay, textvariable=target_lang, values=list(language_codes.keys()), state="readonly", width=20)
lang_dropdown.pack(pady=5)

# Input text
tk.Label(overlay, text="Enter English Text:", font=font_label, bg="#000000", fg="white").pack(pady=(10, 0))
input_box = tk.Text(overlay, height=5, width=75, font=font_text, bg=text_bg, fg=text_fg, insertbackground="white")
input_box.pack()

# Buttons frame for Translate and Clear All
btn_frame = tk.Frame(overlay, bg="#000000")
btn_frame.pack(pady=10)

translate_btn = tk.Button(btn_frame, text="🔁 Translate", command=translate_text,
                          bg=btn_bg, fg=btn_fg, activebackground="#45a049",
                          font=("Segoe UI", 12, "bold"), padx=10, pady=5)
translate_btn.pack(side=tk.LEFT, padx=10)

clear_btn = tk.Button(btn_frame, text="🧹 Clear All", command=clear_all,
                      bg="#f44336", fg="white", activebackground="#d32f2f",
                      font=("Segoe UI", 12, "bold"), padx=10, pady=5)
clear_btn.pack(side=tk.LEFT, padx=10)

# Output text
tk.Label(overlay, text="Translated Text:", font=font_label, bg="#000000", fg="white").pack()
output_box = tk.Text(overlay, height=5, width=75, font=font_text, bg=text_bg, fg=text_fg, state="disabled")
output_box.pack()

# Run the GUI
window.mainloop()
