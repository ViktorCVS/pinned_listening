import os
import io
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pygame
from wave import open as wave_open

class PinnedListeningApp:
    def __init__(self, root):
        self.root = root
        root.title("Pinned Listening")

        pygame.mixer.init()
        self.audio_path = None
        self.duration = 0
        self.updating = False
        self.pins = {}
        self.play_start = 0
        self.is_paused = False

        # Controls frame
        frm = tk.Frame(root)
        frm.pack(padx=10, pady=10)
        self.open_btn = tk.Button(frm, text="Open WAV", command=self.open_file)
        self.open_btn.grid(row=0, column=0, padx=5)
        self.play_btn = tk.Button(frm, text="Play", state="disabled", command=self.play)
        self.play_btn.grid(row=0, column=1, padx=5)
        self.pause_btn = tk.Button(frm, text="Pause", state="disabled", command=self.pause)
        self.pause_btn.grid(row=0, column=2, padx=5)
        self.stop_btn = tk.Button(frm, text="Stop", state="disabled", command=self.stop)
        self.stop_btn.grid(row=0, column=3, padx=5)
        self.pin_btn = tk.Button(frm, text="Pin", state="disabled", command=self.create_pin)
        self.pin_btn.grid(row=0, column=4, padx=5)
        self.remove_pins_btn = tk.Button(frm, text="Remove", state="disabled", command=self.remove_all_pins)
        self.remove_pins_btn.grid(row=0, column=5, padx=5)

        # Slider
        self.scale = tk.Scale(root, from_=0, to=1, orient="horizontal", length=400,
                              state="disabled", showvalue=False,
                              troughcolor="#d0d0d0", sliderlength=20,
                              width=10, bd=0, highlightthickness=0)
        self.scale.pack(padx=10, fill="x")
        self.scale.bind("<ButtonRelease-1>", self.on_seek_event)

        # Time label
        self.time_label = tk.Label(root, text="00:00:00")
        self.time_label.pack(pady=(5, 0))

        # Entry + buttons
        entry_frame = tk.Frame(root)
        entry_frame.pack(pady=(5, 10))
        self.time_entry = tk.Entry(entry_frame, width=8, state="disabled")
        self.time_entry.grid(row=0, column=0, padx=5)
        self.go_btn = tk.Button(entry_frame, text="Go", state="disabled", command=self.goto_time)
        self.go_btn.grid(row=0, column=1, padx=(0,5))
        self.go_pause_btn = tk.Button(entry_frame, text="Go/Pause", state="disabled", command=self.goto_time_pause)
        self.go_pause_btn.grid(row=0, column=2)

        self.root.bind("<Button-1>", self.on_root_click)

        # Status
        self.status = tk.Label(root, text="No file loaded")
        self.status.pack()

    def open_file(self):
        audio_dir = os.path.join(os.path.dirname(__file__), "audio")
        os.makedirs(audio_dir, exist_ok=True)
        fp = filedialog.askopenfilename(initialdir=audio_dir, filetypes=[("WAV files","*.wav")])
        if not fp: return
        # load file into buffer
        data = open(fp, 'rb').read()
        bio = io.BytesIO(data)
        # duration
        with wave_open(io.BytesIO(data), 'rb') as wav:
            frames = wav.getnframes()
            rate = wav.getframerate()
            self.duration = frames / float(rate)
        # load in pygame
        pygame.mixer.music.load(bio)
        # reset state
        self.audio_path = fp
        self.play_start = 0
        self.scale.config(to=int(self.duration), state="normal")
        self.scale.set(0)
        self.time_label.config(text="00:00:00")
        pygame.mixer.music.stop()
        self.is_paused = False
        # enable
        for w in (self.play_btn, self.pause_btn, self.stop_btn,
                  self.pin_btn, self.remove_pins_btn,
                  self.scale, self.time_entry, self.go_btn, self.go_pause_btn):
            w.config(state="normal")
        self.status.config(text=os.path.basename(fp))
        if not self.updating:
            self.updating = True
            self.update_slider()

    def play(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.play()
            pygame.mixer.music.set_pos(self.play_start)
        self.is_paused = False

    def pause(self):
        pygame.mixer.music.pause()
        self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.scale.set(0)
        self.time_label.config(text="00:00:00")
        self.is_paused = False
        self.audio_path = None
        self.remove_all_pins()
        for w in (self.play_btn, self.pause_btn, self.stop_btn,
                  self.pin_btn, self.remove_pins_btn,
                  self.scale, self.time_entry, self.go_btn, self.go_pause_btn):
            w.config(state="disabled")
        self.status.config(text="No file loaded")

    def on_seek_event(self, event):
        sec = self.scale.get()
        self.play_start = sec
        pygame.mixer.music.pause()
        pygame.mixer.music.set_pos(sec)
        pygame.mixer.music.unpause()
        self.is_paused = False

    def goto_time(self):
        sec = self._parse_time(self.time_entry.get().strip())
        if sec is None or not (0 <= sec <= self.duration): return
        self.play_start = sec
        pygame.mixer.music.play(); pygame.mixer.music.set_pos(sec)
        self.is_paused = False
        self.clear_entry()

    def goto_time_pause(self):
        sec = self._parse_time(self.time_entry.get().strip())
        if sec is None or not (0 <= sec <= self.duration): return
        self.play_start = sec
        pygame.mixer.music.play(); pygame.mixer.music.set_pos(sec)
        pygame.mixer.music.pause()
        self.is_paused = True
        # update timer display immediately
        self.scale.set(int(sec))
        t = int(sec)
        h = t // 3600
        m = (t % 3600) // 60
        s = t % 60
        self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        self.clear_entry()

    def _parse_time(self, val):
        parts = val.split(':')
        try:
            if len(parts)==1: return float(parts[0])
            if len(parts)==2:
                m,s = parts; return int(m)*60 + float(s)
            if len(parts)==3:
                h,m,s = parts; return int(h)*3600 + int(m)*60 + float(s)
        except:
            messagebox.showerror("Erro","Formato inválido! Use SS, M:SS ou H:MM:SS.")
        return None

    def clear_entry(self):
        self.time_entry.delete(0, tk.END)
        self.time_entry.selection_clear()
        self.root.focus()

    def update_slider(self):
        if self.audio_path and not self.is_paused:
            pos_ms = pygame.mixer.music.get_pos()
            cur = self.play_start + pos_ms/1000.0 if pos_ms>=0 else self.play_start
            self.scale.set(min(int(cur), int(self.duration)))
            t = int(cur)
            h = t // 3600; m = (t % 3600) // 60; s = t % 60
            self.time_label.config(text=f"{h:02d}:{m:02d}:{s:02d}")
        self.root.after(200, self.update_slider)

    def create_pin(self):
        raw = simpledialog.askstring("Set Shortcut","Digite atalho (ex:1,a,Control-p)")
        if not raw: return
        raw = raw.strip()
        if raw.startswith('<') and raw.endswith('>'):
            pat = raw
        elif len(raw)==1 and raw.isalnum():
            pat = f"<KeyPress-{raw}>"
        else:
            pat = f"<{raw}>"
        self.pins[pat] = self.play_start
        try:
            self.root.bind_all(pat, lambda e, s=self.play_start: self.on_pin_play(e, s), add='+')
        except:
            pass

    def on_pin_play(self, event, sec):
        if self.root.focus_displayof() is None or isinstance(self.root.focus_get(), tk.Entry):
            return
        self.play_start = sec
        pygame.mixer.music.play(); pygame.mixer.music.set_pos(sec)
        self.is_paused = False

    def remove_all_pins(self):
        for pat in list(self.pins): self.root.unbind_all(pat)
        self.pins.clear()

    def on_root_click(self, event):
        if event.widget is not self.time_entry:
            self.time_entry.selection_clear(); self.root.focus()


def main():
    root = tk.Tk()
    PinnedListeningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
