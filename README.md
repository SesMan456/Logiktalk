# 💬 Logitalk

**Logitalk** is a modern, user-friendly desktop chat client built with Python using **CustomTkinter** for the UI and **Pygame** for sound effects.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-UI-orange)
![Pygame](https://img.shields.io/badge/Pygame-Audio-green)

---

## ✨ Key Features

- **Dark & Light Themes** — seamlessly switch between dark and light UI modes to match your preference.
- **Sound Effects** — integrated audio feedback for incoming messages, button clicks, server connections, and errors (powered by `pygame.mixer`).
- **Customizable Audio Controls** — toggle message and click sounds on or off anytime via the collapsible side menu.
- **One-Click Reconnect** — if the connection drops, a convenient **Reconnect** button appears right in the chat to quickly restore the session.
- **Animated Splash Screen** — smooth fade-in and fade-out intro animation on startup.
- **Custom Nicknames** — set your display name directly from the settings panel before chatting.

---

## 🛠 Tech Stack

This project is written in **Python** and uses the following libraries:
- [`CustomTkinter`](https://github.com/TomSchimansky/CustomTkinter) — modern wrapper around Tkinter for sleek UI components.
- [`Pygame`](https://www.pygame.org/) — handles audio playback and volume transitions.
- `socket` & `threading` — manages non-blocking TCP client-server communication.
- `Pillow` (PIL) — processes images for the animated splash screen.

---

## 📂 Project Structure

For the full audio-visual experience, place the following media files in the same directory as the main script (the app handles missing files gracefully if any are omitted):
- `intro.png` — logo/image displayed on the splash screen.
- `intro.mp3` — startup sound effect.
- `message.mp3` — incoming message notification sound.
- `click.mp3` — UI button click sound.
- `connect.mp3` — successful server connection sound.
- `on.mp3` / `off.mp3` — toggle switch sound effects.
- `error.mp3` — connection or send error alert sound.

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/SesMan456/Logiktalk](https://github.com/SesMan456/Logiktalk)
   cd logitalk
