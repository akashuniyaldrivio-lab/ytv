import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import os

# Color themes
LIGHT_THEME = {
    'bg': '#FFFFFF',
    'fg': '#0F0F0F',
    'header_bg': '#FFFFFF',
    'header_fg': '#FF0000',
    'entry_bg': '#F1F1F1',
    'entry_fg': '#0F0F0F',
    'button_bg': '#FF0000',
    'button_fg': '#FFFFFF',
    'button_hover': '#CC0000',
    'secondary_btn_bg': '#E5E5E5',
    'secondary_btn_fg': '#0F0F0F',
    'status_bg': '#FFFFFF'
}

DARK_THEME = {
    'bg': '#0F0F0F',
    'fg': '#F1F1F1',
    'header_bg': '#0F0F0F',
    'header_fg': '#FF0000',
    'entry_bg': '#212121',
    'entry_fg': '#F1F1F1',
    'button_bg': '#FF0000',
    'button_fg': '#FFFFFF',
    'button_hover': '#CC0000',
    'secondary_btn_bg': '#3F3F3F',
    'secondary_btn_fg': '#F1F1F1',
    'status_bg': '#0F0F0F'
}

class YTVDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YTV Downloader")
        self.root.geometry("550x420")
        self.root.resizable(False, False)
        
        self.is_dark = True
        self.current_theme = DARK_THEME
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Create all UI elements"""
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header with dark mode toggle
        self.header_frame = tk.Frame(self.main_frame)
        self.header_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.header_label = tk.Label(self.header_frame, text="▶ YTV Downloader", 
                                     font=("Helvetica", 20, "bold"))
        self.header_label.pack(side=tk.LEFT)
        
        self.theme_btn = tk.Button(self.header_frame, text="☀️", font=("Helvetica", 16),
                                   relief="flat", bd=0, cursor="hand2",
                                   command=self.toggle_theme)
        self.theme_btn.pack(side=tk.RIGHT)
        
        # URL Input
        url_frame = tk.Frame(self.main_frame)
        url_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.url_label = tk.Label(url_frame, text="Paste Video Link:", 
                                  font=("Helvetica", 10))
        self.url_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.url_entry = tk.Entry(url_frame, font=("Helvetica", 11), 
                                  relief="flat", bd=2)
        self.url_entry.pack(fill=tk.X, ipady=8)
        
        # Path Selection
        path_frame = tk.Frame(self.main_frame)
        path_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.path_label = tk.Label(path_frame, text="Save to Folder:", 
                                   font=("Helvetica", 10))
        self.path_label.pack(anchor=tk.W, pady=(0, 5))
        
        path_input_frame = tk.Frame(path_frame)
        path_input_frame.pack(fill=tk.X)
        
        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(path_input_frame, textvariable=self.path_var,
                                   font=("Helvetica", 11), relief="flat", bd=2)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, 
                            ipady=8, padx=(0, 10))
        
        self.browse_btn = tk.Button(path_input_frame, text="Browse", 
                                    font=("Helvetica", 10, "bold"),
                                    relief="flat", cursor="hand2",
                                    command=self.browse_folder)
        self.browse_btn.pack(side=tk.RIGHT, ipadx=15, ipady=8)
        
        # Download Button
        self.download_btn = tk.Button(self.main_frame, text="DOWNLOAD VIDEO",
                                      font=("Helvetica", 13, "bold"),
                                      relief="flat", cursor="hand2",
                                      command=self.start_download)
        self.download_btn.pack(fill=tk.X, pady=(0, 15), ipady=12)
        
        # Status Label
        self.status_label = tk.Label(self.main_frame, text="Status: Ready to download",
                                     font=("Helvetica", 10, "italic"))
        self.status_label.pack(pady=10)
        
        # Bind hover effects
        self.download_btn.bind('<Enter>', self.on_download_hover)
        self.download_btn.bind('<Leave>', self.on_download_leave)
    
    def apply_theme(self):
        """Apply current theme colors to all widgets"""
        theme = self.current_theme
        
        # Root and main frame
        self.root.config(bg=theme['bg'])
        self.main_frame.config(bg=theme['bg'])
        
        # Header
        self.header_frame.config(bg=theme['bg'])
        self.header_label.config(bg=theme['header_bg'], fg=theme['header_fg'])
        self.theme_btn.config(bg=theme['bg'], fg=theme['fg'], 
                             activebackground=theme['bg'])
        
        # URL section
        for frame in [self.url_entry.master, self.path_entry.master.master]:
            frame.config(bg=theme['bg'])
        
        self.url_label.config(bg=theme['bg'], fg=theme['fg'])
        self.url_entry.config(bg=theme['entry_bg'], fg=theme['entry_fg'],
                             insertbackground=theme['fg'])
        
        # Path section
        self.path_label.config(bg=theme['bg'], fg=theme['fg'])
        self.path_entry.master.config(bg=theme['bg'])
        self.path_entry.config(bg=theme['entry_bg'], fg=theme['entry_fg'],
                              insertbackground=theme['fg'])
        
        self.browse_btn.config(bg=theme['secondary_btn_bg'], 
                              fg=theme['secondary_btn_fg'],
                              activebackground=theme['secondary_btn_fg'],
                              activeforeground=theme['secondary_btn_bg'])
        
        # Download button
        self.download_btn.config(bg=theme['button_bg'], fg=theme['button_fg'],
                                activebackground=theme['button_hover'],
                                activeforeground=theme['button_fg'])
        
        # Status
        self.status_label.config(bg=theme['status_bg'], fg=theme['fg'])
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        self.is_dark = not self.is_dark
        self.current_theme = DARK_THEME if self.is_dark else LIGHT_THEME
        self.theme_btn.config(text="☀️" if self.is_dark else "🌙")
        self.apply_theme()
    
    def on_download_hover(self, event):
        """Change button color on hover"""
        self.download_btn.config(bg=self.current_theme['button_hover'])
    
    def on_download_leave(self, event):
        """Restore button color"""
        self.download_btn.config(bg=self.current_theme['button_bg'])
    
    def browse_folder(self):
        """Opens a system dialog to select the download folder."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.path_var.set(folder_selected)
    
    def download_video_thread(self):
        """Runs the actual download in a separate thread to keep UI responsive."""
        url = self.url_entry.get()
        save_path = self.path_var.get()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube link.")
            return
        
        if not save_path:
            messagebox.showerror("Error", "Please select a download folder.")
            return
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{save_path}/%(title)s.%(ext)s',
        }
        
        self.status_label.config(text="Status: Downloading...", fg="#1E90FF")
        self.download_btn.config(state=tk.DISABLED)
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.config(text="Status: Download Complete! ✓", fg="#00C853")
            messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            self.status_label.config(text="Status: Error occurred ✗", fg="#FF0000")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.download_btn.config(state=tk.NORMAL)
    
    def start_download(self):
        """Wrapper to start the thread."""
        threading.Thread(target=self.download_video_thread, daemon=True).start()

# Run the App
if __name__ == "__main__":
    root = tk.Tk()
    app = YTVDownloader(root)
    root.mainloop()