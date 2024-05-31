from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
from PIL import Image, ImageTk
import time
import subprocess

# Set the path to the directory containing your image assets
ASSETS_PATH = Path(__file__).resolve().parent / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / path

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

class CanvasImage:
    def __init__(self, canvas, image_path, x, y):
        self.canvas = canvas
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.photo = None
        self.alpha_photo = None
        self.x = x
        self.y = y
        self.hidden = False

    def load_photo(self):
        self.photo = ImageTk.PhotoImage(self.image)

    def fade_in(self, speed=0.05):
        alpha = 0.0
        while alpha < 1.0:
            self.apply_alpha(alpha)
            self.canvas.update()
            time.sleep(speed)
            alpha += 0.05

    def apply_alpha(self, alpha):
        image_with_alpha = self.image.copy().convert("RGBA")
        alpha_data = image_with_alpha.split()[3]
        alpha_data = alpha_data.point(lambda p: int(p * alpha))
        image_with_alpha.putalpha(alpha_data)
        self.alpha_photo = ImageTk.PhotoImage(image_with_alpha)
        self.canvas.itemconfigure(self.image_item, image=self.alpha_photo)

    def render(self):
        self.load_photo()
        self.image_item = self.canvas.create_image(self.x, self.y, image=self.photo)

    def hide(self):
        if not self.hidden:
            self.hidden = True
            self.canvas.itemconfigure(self.image_item, state="hidden")

    def show(self):
        if self.hidden:
            self.hidden = False
            self.canvas.itemconfigure(self.image_item, state="normal")

def slide_image(canvas, image, target_x, target_y, speed=3):
    x, y = image.x, image.y
    distance_x = target_x - x
    distance_y = target_y - y
    steps = int(max(abs(distance_x), abs(distance_y)) / speed)

    if steps > 0:
        step_x = distance_x / steps
        step_y = distance_y / steps

        for _ in range(steps):
            x += step_x
            y += step_y
            canvas.coords(image.image_item, x, y)
            canvas.update()
            time.sleep(0.01)

def open_login_screen(window):
    window.destroy()  # Close the main window
    subprocess.Popen(["python", "D:/GLYCELLE/THESIS FINAL OUTPUTS/Sytem Code/application code/cctvDashboard.py"])

def check_credentials(window, username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()

    # Replace the following lines with your actual credentials check logic
    valid_username = "admin"
    valid_password = "password"

    if username == valid_username and password == valid_password:
        messagebox.showinfo("Login", "Login Successful")
        window.after(4000, open_login_screen, window)
    else:
        messagebox.showerror("Login", "Invalid Credentials")

def main():
    window = Tk()
    window.title("Oversee")
    window.geometry("1200x660")  # Adjusted window size
    window.configure(bg="#FFFFFF")

    canvas = Canvas(
        window,
        bg="#FFFFFF",
        height=660,
        width=1200,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )
    canvas.place(x=0, y=0)

    # Splash Screen Animation
    logoAnimation = CanvasImage(canvas, relative_to_assets("logoAnimation.png"), 650.0, 330.0)
    logoAnimation.render()

    window.resizable(False, False)
    window.update()

    slide_image(canvas, logoAnimation, 400.0, 329.0)
    logoAnimation.fade_in()

    textAnimation = CanvasImage(canvas, relative_to_assets("logoAnimation2.png"), 655.0, 390.0)
    textAnimation.render()
    textAnimation.fade_in()

    logoAnimation.hide()
    textAnimation.hide()
    time.sleep(1)

    # Logo for Login
    logo_image = PhotoImage(file=relative_to_assets("logo.png"))
    resized_logo_image = logo_image.subsample(2)
    logo = canvas.create_image(800.0, 85.0, image=resized_logo_image, anchor="nw")

    # Password Entry Field
    passwordEntry_image = PhotoImage(file=relative_to_assets("passwordEntry.png"))
    resized_PWentry_image = passwordEntry_image.subsample(2)
    passwordEntry_bg = canvas.create_image(950.0, 330.0, image=resized_PWentry_image)
    password_entry = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, show="*", font=("Roboto", 8))
    password_entry.place(x=802.0, y=310.0, width=300.0, height=38.0)

    canvas.create_text(801.0, 215.0, anchor="nw", text="Username", fill="#000000", font=("RobotoItalic Medium", 8))

    canvas.create_text(801.0, 295.0, anchor="nw", text="Password", fill="#000000", font=("RobotoItalic Medium", 8))

    background_image = PhotoImage(file=relative_to_assets("background.png"))
    image_2 = canvas.create_image(240.0, 330.0, image=background_image)

    # Username Entry Field
    usernameEntry_image = PhotoImage(file=relative_to_assets("usernameEntry.png"))
    resized_UNentry_image = usernameEntry_image.subsample(2)
    usernameEntry_bg = canvas.create_image(950.0, 250.0, image=resized_UNentry_image)
    username_entry = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=("Roboto", 8))
    username_entry.place(x=802.0, y=230.0, width=300.0, height=38.0)

    canvas.create_text(801.0, 355.0, anchor="nw", text="Forgot password?", fill="#4A4A4A", font=("RobotoItalic Regular", 8))

    # Log-in Button Controls
    login_image = PhotoImage(file=relative_to_assets("loginButton.png"))
    resized_login_image = login_image.subsample(2)

    # Create login button
    login_button = Button(window, image=resized_login_image, borderwidth=0, command=lambda: check_credentials(window, username_entry, password_entry), relief="flat")
    login_button.place(x=1010, y=350, width = 82, height = 40)

    window.resizable(False, False)
    window.title("Oversee")
    window.mainloop()

if __name__ == "__main__":
    main()
