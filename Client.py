import pygame
from customtkinter import *
import threading
from socket import *
from PIL import Image

class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.message_sound = pygame.mixer.Sound("message.mp3")
        self.click_sound = pygame.mixer.Sound("click.mp3")

        self.message_sound.set_volume(0.7)
        self.click_sound.set_volume(0.5)

        self.message_sound_enabled = True
        self.click_sound_enabled = True

        self.geometry('600x400')
        self.title("Logitalk")
        self.resizable(False, False)

        self.is_show_menu = False
        self.chat_field = CTkScrollableFrame(self, width=520, height=310)
        self.chat_field.place(x=65, y=10)

        self.message_entry = CTkEntry(self, placeholder_text='Введіть повідомлення:', width=450, height=40)
        self.message_entry.place(x=65, y=340)

        self.send_button = CTkButton(self, text='>', width=50, height=40, command=self.send_message)
        self.send_button.place(x=530, y=340)

        self.menu_frame = CTkFrame(self, width=50, height=400)
        self.menu_frame.place(x=0, y=0)
        self.menu_frame.pack_propagate(False)

        self.btn = CTkButton(self.menu_frame, text='▶️', command=self.toggle_menu, width=35)
        self.btn.place(x=7, y=10)

        self.menu_content = CTkFrame(
            self.menu_frame,
            width=180,
            height=330,
            fg_color="transparent"
        )

        CTkLabel(
            self.menu_content,
            text="Налаштування",
            font=("Arial", 16, "bold")
        ).pack(pady=(10, 15))

        # Имя пользователя
        CTkLabel(self.menu_content, text="Ім'я користувача").pack()

        self.username_entry = CTkEntry(
            self.menu_content,
            width=160,
            placeholder_text="Ваше ім'я"
        )
        self.username_entry.pack(pady=(5, 15))

        # Звук сообщений
        self.message_switch = CTkSwitch(
            self.menu_content,
            text="Звук повідомлень",
            command=self.toggle_message_sound
        )
        self.message_switch.pack(pady=10)
        self.message_switch.select()

        # Звук кликов
        self.click_switch = CTkSwitch(
            self.menu_content,
            text="Звук натискань",
            command=self.toggle_click_sound
        )
        self.click_switch.pack(pady=10)
        self.click_switch.select()

        # Громкость сообщений
        CTkLabel(
            self.menu_content,
            text="Гучність повідомлень"
        ).pack(pady=(15, 0))

        self.message_volume = CTkSlider(
            self.menu_content,
            from_=0,
            to=1,
            command=self.change_message_volume,
            width=150
        )
        self.message_volume.pack(pady=5)
        self.message_volume.set(0.7)

        # Громкость кликов
        CTkLabel(
            self.menu_content,
            text="Гучність натискань"
        ).pack(pady=(10, 0))

        self.click_volume = CTkSlider(
            self.menu_content,
            from_=0,
            to=1,
            command=self.change_click_volume,
            width=150
        )
        self.click_volume.pack(pady=5)
        self.click_volume.set(0.5)

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(('7.tcp.eu.ngrok.io', 26006))
            threading.Thread(target=self.recv_message, daemon=True).start()
        except Exception as e:
            self.add_message(f"Помилка підключення: {e}")

        # Запускаємо інтро
        self.after(100, self.start_splash)

    def toggle_menu(self):
        if self.is_show_menu:
            self.menu_content.place_forget()
            self.menu_frame.configure(width=50)
            if self.click_sound_enabled:
                self.click_sound.play()
            self.btn.configure(text='▶️')
            self.is_show_menu = False
        else:
            self.menu_frame.configure(width=200)
            self.menu_content.place(x=10, y=50)
            if self.click_sound_enabled:
                self.click_sound.play()
            self.btn.configure(text='◀️')
            self.is_show_menu = True

    def toggle_message_sound(self):
        self.message_sound_enabled = bool(self.message_switch.get())

    def toggle_click_sound(self):
        self.click_sound_enabled = bool(self.click_switch.get())

    def change_message_volume(self, value):
        self.message_sound.set_volume(float(value))

    def change_click_volume(self, value):
        self.click_sound.set_volume(float(value))

    def add_message(self, text):
        def _update():
            msg_label = CTkLabel(self.chat_field, text=text, anchor='w', justify='left')
            msg_label.pack(fill='x', padx=5, pady=2)

        self.after(0, _update)

    def send_message(self):
        name = (self.username_entry.get().strip() or "User")
        message = (self.message_entry.get().strip())
        if self.click_sound_enabled:
            self.click_sound.play()
        if message:
            full_text = f"{name}: {message}"
            self.add_message(f"Я: {message}")
            try:
                self.sock.send(full_text.encode())
            except:
                pass
            self.message_entry.delete(0, 'end')

    def recv_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.add_message(message)
                    if self.message_sound_enabled:
                        self.after(0, self.message_sound.play)
            except:
                break

    def start_splash(self):
        fade_in_time = 1500
        hold_time = 4200
        fade_out_time = 1500
        frame_delay = 20

        self.splash = CTkFrame(self, fg_color="black", corner_radius=0)
        self.splash.place(x=0, y=0, relwidth=1, relheight=1)
        self.splash.lift()

        try:
            image = Image.open("intro.png").convert("RGBA")
        except FileNotFoundError:
            image = Image.new("RGBA", (350, 250), (255, 255, 255, 255))

        image.thumbnail((350, 250))
        img_width, img_height = image.size

        self.splash_label = CTkLabel(
            self.splash,
            text="",
            fg_color="black"
        )
        self.splash_label.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        def show_frame(alpha):
            layer = image.copy()
            alpha_channel = layer.split()[3].point(lambda p: int(p * max(0.0, min(1.0, alpha))))
            layer.putalpha(alpha_channel)

            # Використовуємо CTkImage замість ImageTk.PhotoImage
            ctk_img = CTkImage(light_image=layer, dark_image=layer, size=(img_width, img_height))

            self.splash_label.configure(image=ctk_img, fg_color="black")
            self.splash_label.image = ctk_img  # Зберігаємо посилання, щоб збірка сміття не видалила зображення

        def animate(start, end, duration, callback):
            steps = max(1, duration // frame_delay)

            def frame(i=0):
                alpha = start + (end - start) * i / steps
                show_frame(alpha)

                if i < steps:
                    self.after(frame_delay, lambda: frame(i + 1))
                else:
                    if callback:
                        callback()

            frame()

        def finish_intro():
            self.splash.destroy()

        def fade_out():
            animate(1.0, 0.0, fade_out_time, finish_intro)

        def hold():
            self.after(hold_time, fade_out)

        def play_intro():
            try:
                intro_sound = pygame.mixer.Sound("intro.mp3")
                intro_sound.play()
            except:
                pass
            animate(0.0, 1.0, fade_in_time, hold)

        show_frame(0.0)
        play_intro()


win = MainWindow()
win.mainloop()