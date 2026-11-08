import tkinter as tk
from tkinter import filedialog, messagebox
import pygame
import os
import random

pygame.mixer.init()

playlist = []
current_song = 0
repeat_mode = False

def add_songs():
    global playlist
    files = filedialog.askopenfilenames(title="Select Music", filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
    for file in files:
        if file not in playlist:
            playlist.append(file)
            playlist_box.insert(tk.END, os.path.basename(file))

def remove_song():
    global playlist, current_song
    selected = playlist_box.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a song to remove.")
        return
    index = selected[0]
    playlist_box.delete(index)
    del playlist[index]
    if current_song >= len(playlist):
        current_song = max(0, len(playlist) - 1)

def play_song():
    global current_song
    selected = playlist_box.curselection()
    if selected:
        current_song = selected[0]
    if not playlist:
        messagebox.showwarning("No Songs", "Please add songs first.")
        return
    song = playlist[current_song]
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    song_label.config(text="Playing: " + os.path.basename(song))
    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_song)
    playlist_box.see(current_song)

def pause_song():
    pygame.mixer.music.pause()
    song_label.config(text="Paused")

def resume_song():
    pygame.mixer.music.unpause()
    if playlist:
        song_label.config(text="Playing: " + os.path.basename(playlist[current_song]))

def stop_song():
    pygame.mixer.music.stop()
    song_label.config(text="Stopped")

def next_song():
    global current_song
    if not playlist:
        return
    if repeat_mode:
        play_song()
        return
    current_song += 1
    if current_song >= len(playlist):
        current_song = 0
    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_song)
    playlist_box.see(current_song)
    play_song()

def previous_song():
    global current_song
    if not playlist:
        return
    current_song -= 1
    if current_song < 0:
        current_song = len(playlist) - 1
    playlist_box.selection_clear(0, tk.END)
    playlist_box.selection_set(current_song)
    playlist_box.see(current_song)
    play_song()

def toggle_repeat():
    global repeat_mode
    repeat_mode = not repeat_mode
    repeat_btn.config(text="Repeat: ON" if repeat_mode else "Repeat: OFF",
                      bg="lightgreen" if repeat_mode else "SystemButtonFace")

def set_volume(value):
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)

def shuffle_playlist():
    global playlist, current_song
    if len(playlist) < 2:
        return
    random.shuffle(playlist)
    playlist_box.delete(0, tk.END)
    for song in playlist:
        playlist_box.insert(tk.END, os.path.basename(song))
    current_song = 0
    playlist_box.selection_set(0)

# ---------------------------------------------------------
# Window
# ---------------------------------------------------------
root = tk.Tk()
root.title("Offline Music Player")
root.geometry("650x600")
root.resizable(False, False)

tk.Label(root, text="🎵 OFFLINE MUSIC PLAYER", font=("Arial", 23, "bold")).pack(pady=20)

song_label = tk.Label(root, text="No song playing", font=("Arial", 11))
song_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)
playlist_box = tk.Listbox(frame, width=55, height=12, font=("Arial", 11))
playlist_box.pack()

plist_btn_frame = tk.Frame(root)
plist_btn_frame.pack(pady=5)
tk.Button(plist_btn_frame, text="Add Songs", command=add_songs, width=14).grid(row=0, column=0, padx=5)
tk.Button(plist_btn_frame, text="Remove Song", command=remove_song, width=14).grid(row=0, column=1, padx=5)
tk.Button(plist_btn_frame, text="Shuffle", command=shuffle_playlist, width=14).grid(row=0, column=2, padx=5)

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame, text="⏮ Previous", command=previous_song, width=12).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="▶ Play", command=play_song, width=12).grid(row=0, column=1, padx=5)
tk.Button(control_frame, text="⏸ Pause", command=pause_song, width=12).grid(row=0, column=2, padx=5)
tk.Button(control_frame, text="⏯ Resume", command=resume_song, width=12).grid(row=1, column=1, pady=10)
tk.Button(control_frame, text="⏹ Stop", command=stop_song, width=12).grid(row=1, column=2, pady=10)
tk.Button(control_frame, text="Next ⏭", command=next_song, width=12).grid(row=1, column=0, pady=10)

repeat_btn = tk.Button(control_frame, text="Repeat: OFF", command=toggle_repeat, width=12)
repeat_btn.grid(row=2, column=1, pady=5)

tk.Label(root, text="Volume").pack()
volume = tk.Scale(root, from_=0, to=100, orient="horizontal", command=set_volume, length=300)
volume.set(70)
volume.pack()

root.mainloop()