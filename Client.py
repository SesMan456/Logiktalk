import pygame
from customtkinter import *
import threading
from socket import *
from PIL import Image


class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.current_theme = "dark"
        set_appearance_mode(self.current_theme)

        # Завантаження звуків
        try:
            self.message_sound = pygame.mixer.Sound("message.mp3")
            self.message_sound.set_volume(0.7)
        except:
            self.message_sound = None

        try:
            self.click_sound = pygame.mixer.Sound("click.mp3")
            self.click_sound.set_volume(0.5)
        except:
            self.click_sound = None

        try:
            self.connect_sound = pygame.mixer.Sound("connect.mp3")
            self.connect_sound.set_volume(0.6)
        except:
            self.connect_sound = None

        try:
            self.on_sound = pygame.mixer.Sound("on.mp3")
            self.on_sound.set_volume(0.5)
        except:
            self.on_sound = None

        try:
            self.off_sound = pygame.mixer.Sound("off.mp3")
            self.off_sound.set_volume(0.5)
        except:
            self.off_sound = None

        try:
            self.error_sound = pygame.mixer.Sound("error.mp3")
            self.error_sound.set_volume(0.6)
        except:
            self.error_sound = None

        self.message_sound_enabled = True
        self.click_sound_enabled = True
        self.connect_sound_enabled = True

        self.current_error_frame = None

        self.is_connected = False
        self.intro_finished = False

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

        CTkLabel(
            self.menu_content,
            text="Тема оформлення"
        ).pack(pady=(5, 5))

        self.theme_menu = CTkOptionMenu(
            self.menu_content,
            values=["Темна", "Світла"],
            command=self.change_theme,
            width=150
        )
        self.theme_menu.pack(pady=(0, 15))
        self.theme_menu.set("Темна")

        CTkLabel(self.menu_content, text="Ім'я користувача").pack()

        self.username_entry = CTkEntry(
            self.menu_content,
            width=160,
            placeholder_text="Ваше ім'я"
        )
        self.username_entry.pack(pady=(5, 15))

        self.message_switch = CTkSwitch(
            self.menu_content,
            text="Звук повідомлень",
            command=self.toggle_message_sound
        )
        self.message_switch.pack(pady=5)
        self.message_switch.select()

        self.click_switch = CTkSwitch(
            self.menu_content,
            text="Звук натискань",
            command=self.toggle_click_sound
        )
        self.click_switch.pack(pady=5)
        self.click_switch.select()

        # ЗАМІНА: Прибрано автоматичний виклик connect_to_server() тут.
        # Тепер підключення почнеться одразу після закінчення інтро.
        self.after(100, self.start_splash)

    def connect_to_server(self, err_frame=None, msg_label=None, reconnect_btn=None, loading_label=None):

        def _thread_target():
            try:
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.connect(('4.tcp.eu.ngrok.io', 22283))
                threading.Thread(target=self.recv_message, daemon=True).start()

                def onSuccess():
                    self.is_connected = True
                    if loading_label:
                        loading_label.destroy()
                    if err_frame:
                        err_frame.destroy()
                        self.current_error_frame = None

                    self.add_message("Успішно підключено до сервера!")

                    if self.intro_finished and self.connect_sound and self.connect_sound_enabled:
                        self.connect_sound.play()

                self.after(0, onSuccess)
            except Exception as e:
                error_msg = str(e)

                def onError():
                    self.is_connected = False
                    if loading_label:
                        loading_label.destroy()

                    # Звук помилки спрацьовує тільки при реальних збоях після інтро
                    if self.error_sound:
                        self.error_sound.play()

                    if err_frame and msg_label and reconnect_btn:
                        msg_label.configure(text=f"Помилка підключення: {error_msg}")
                        reconnect_btn.pack(anchor='w', pady=(2, 5))
                    else:
                        self.add_error_message(f"Помилка підключення: {error_msg}")

                self.after(0, onError)

        threading.Thread(target=_thread_target, daemon=True).start()

    def change_theme(self, choice):
        if choice == "Світла":
            self.current_theme = "light"
        else:
            self.current_theme = "dark"
        set_appearance_mode(self.current_theme)

    def toggle_menu(self):
        if self.click_sound and self.click_sound_enabled:
            self.click_sound.play()

        if self.is_show_menu:
            self.menu_content.place_forget()
            self.menu_frame.configure(width=50)
            self.btn.configure(text='▶️')
            self.is_show_menu = False
        else:
            self.menu_frame.configure(width=200)
            self.menu_content.place(x=10, y=50)
            self.btn.configure(text='◀️')
            self.is_show_menu = True

    def toggle_message_sound(self):
        self.message_sound_enabled = bool(self.message_switch.get())
        if self.message_sound_enabled:
            if self.on_sound: self.on_sound.play()
        else:
            if self.off_sound: self.off_sound.play()

    def toggle_click_sound(self):
        self.click_sound_enabled = bool(self.click_switch.get())
        if self.click_sound_enabled:
            if self.on_sound: self.on_sound.play()
        else:
            if self.off_sound: self.off_sound.play()

    def add_message(self, text):
        def _update():
            msg_label = CTkLabel(self.chat_field, text=text, anchor='w', justify='left')
            msg_label.pack(fill='x', padx=5, pady=2)

        self.after(0, _update)

    def add_error_message(self, text):
        def _update():
            if self.current_error_frame and self.current_error_frame.winfo_exists():
                self.current_error_frame.destroy()

            err_frame = CTkFrame(self.chat_field, fg_color="transparent")
            err_frame.pack(fill='x', padx=5, pady=2)
            self.current_error_frame = err_frame

            msg_label = CTkLabel(err_frame, text=text, anchor='w', justify='left', text_color="#FF5555")
            msg_label.pack(anchor='w', fill='x')

            reconnect_btn = CTkButton(
                err_frame,
                text="Перепідключитися",
                width=120,
                height=24,
                font=("Arial", 11),
                fg_color="#FFA500",
                hover_color="#FF8C00",
                text_color="#000000"
            )
            reconnect_btn.pack(anchor='w', pady=(2, 5))

            def on_click():
                if self.click_sound and self.click_sound_enabled:
                    self.click_sound.play()

                reconnect_btn.pack_forget()
                loading_label = CTkLabel(err_frame, text="Підключення...", font=("Arial", 11, "italic"),
                                         text_color="#FFA500")
                loading_label.pack(anchor='w', pady=(2, 5))

                self.connect_to_server(
                    err_frame=err_frame,
                    msg_label=msg_label,
                    reconnect_btn=reconnect_btn,
                    loading_label=loading_label
                )

            reconnect_btn.configure(command=on_click)

        self.after(0, _update)

    def send_message(self):
        name = (self.username_entry.get().strip() or "User")
        message = (self.message_entry.get().strip())

        if self.click_sound and self.click_sound_enabled:
            self.click_sound.play()

        if message:
            full_text = f"{name}: {message}"
            self.add_message(f"Вы: {message}")
            try:
                self.sock.send(full_text.encode())
            except:
                if self.error_sound:
                    self.error_sound.play()
                self.add_error_message("Не вдалося надіслати повідомлення: з'єднання втрачено.")
            self.message_entry.delete(0, 'end')

    def recv_message(self):
        while True:
            try:
                message = self.sock.recv(1024).decode()
                if message:
                    self.add_message(message)
                    if self.message_sound and self.message_sound_enabled:
                        self.after(0, self.message_sound.play)
                else:
                    break
            except:
                if self.error_sound:
                    self.after(0, self.error_sound.play)
                self.add_error_message("З'єднання з сервером розірвано.")
                break

    def start_splash(self):
        fade_in_time = 1200
        hold_time = 2500
        fade_out_time = 1000
        bg_fade_time = 800
        frame_delay = 20

        self.splash = CTkFrame(self, fg_color="#000000", corner_radius=0)
        self.splash.place(x=0, y=0, relwidth=1, relheight=1)
        self.splash.lift()

        try:
            image = Image.open("intro.png").convert("RGBA")
        except FileNotFoundError:
            image = Image.new("RGBA", (350, 250), (30, 30, 30, 255))

        image.thumbnail((350, 250))
        img_width, img_height = image.size

        self.splash_label = CTkLabel(self.splash, text="", fg_color="#000000")
        self.splash_label.place(relx=0.5, rely=0.5, anchor="center")

        def show_frame(alpha):
            layer = image.copy()
            alpha_channel = layer.split()[3].point(lambda p: int(p * max(0.0, min(1.0, alpha))))
            layer.putalpha(alpha_channel)

            ctk_img = CTkImage(light_image=layer, dark_image=layer, size=(img_width, img_height))
            self.splash_label.configure(image=ctk_img)
            self.splash_label.image = ctk_img

        def animate_logo(start, end, duration, callback):
            steps = max(1, duration // frame_delay)

            def frame(i=0):
                progress = i / steps
                smooth = progress * progress * (3 - 2 * progress)

                alpha = start + (end - start) * smooth
                show_frame(alpha)

                if hasattr(self, "intro_sound") and self.intro_sound:
                    try:
                        vol = (1.0 - smooth) if start > end else smooth
                        self.intro_sound.set_volume(vol)
                    except:
                        pass

                if i < steps:
                    self.after(frame_delay, lambda: frame(i + 1))
                elif callback:
                    callback()

            frame()

        def fade_bg_to_chat():
            self.splash_label.destroy()
            self.intro_finished = True

            # Тепер підключення до сервера запускається ВІДРАЗУ після завершення інтро
            self.connect_to_server()

            if self.is_connected and self.connect_sound and self.connect_sound_enabled:
                self.connect_sound.play()

            target_val = 36 if self.current_theme == "dark" else 235
            steps = max(1, bg_fade_time // frame_delay)

            def bg_frame(i=0):
                progress = i / steps
                smooth = progress * progress * (3 - 2 * progress)

                val = int(target_val * smooth)
                hex_color = f"#{val:02x}{val:02x}{val:02x}"
                self.splash.configure(fg_color=hex_color)

                if i < steps:
                    self.after(frame_delay, lambda: bg_frame(i + 1))
                else:
                    self.splash.destroy()

            bg_frame()

        def fade_out():
            animate_logo(1.0, 0.0, fade_out_time, fade_bg_to_chat)

        def hold():
            self.after(hold_time, fade_out)

        def play_intro():
            try:
                self.intro_sound = pygame.mixer.Sound("intro.mp3")
                self.intro_sound.play()
            except:
                self.intro_sound = None

            animate_logo(0.0, 1.0, fade_in_time, hold)

        show_frame(0.0)
        play_intro()


if __name__ == "__main__":
    win = MainWindow()
    win.mainloop()
