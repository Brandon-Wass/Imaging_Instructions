#!/usr/bin/env python3
import tkinter as tk

def create_overlay():
    root = tk.Tk()
    root.title("System Notification")

    # Fullscreen overlay
    root.attributes("-fullscreen", True)
    root.configure(background='purple')

    # Message Label
    message = tk.Label(root, text="Resizing Filesystem, please wait...",
                       font=("Helvetica", 40, "bold"),
                       fg="black", bg="grey")
    message.pack(expand=True)

    # Keep the window open for a set duration
    root.after(10000, root.destroy)  # 10 seconds
    root.mainloop()

def main():
    create_overlay()

if __name__ == "__main__":
    main()