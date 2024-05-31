from pathlib import Path
from tkinter import Tk, Canvas, Button, END, PhotoImage, Frame, Label, Entry, Text, messagebox
import cv2, sqlite3, os
from PIL import Image, ImageTk
from datetime import datetime
import subprocess
import pipeline

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("~~/assets")
FILE_PATH = OUTPUT_PATH / Path(r"~~/patient_data.db")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
show_Patients = False
show_Camera = False
liveIndicator_active = True
show_Home = False
show_archive = False



def open_login_screen():
    window.destroy()  # Close the main window
    subprocess.Popen(["python", "main.py"])

def update_patient_idVar(patient_id):
    global patient_idVar
    patient_idVar = patient_id

def initialize_data(cursor, conn):
    # Sample patient data
    sample_data = [
        {
            'id' : 1,
            'first_name': 'Patient 1',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 2,
            'first_name': 'Patient 2',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 3,
            'first_name': 'Patient 3',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 4,
            'first_name': 'Patient 4',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 5,
            'first_name': 'Patient 5',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 6,
            'first_name': 'Patient 6',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 7,
            'first_name': 'Patient 7',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
        {
            'id' : 8,
            'first_name': 'Patient 8',
            'middle_name': '',
            'last_name': '',
            'barangay': '',
            'city': '',
            'province': '' ,
            'age': '',
            'gender': '',
            'birthday': '',
            'cellphone': '',
            'height': '',
            'weight': ''   
        },
    ]

    # Create the patients table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            barangay TEXT,
            city TEXT,
            province TEXT,
            age TEXT,
            gender TEXT,
            birthday TEXT,
            cellphone TEXT,
            height TEXT,
            weight TEXT
        )
    ''')

    for data in sample_data:
        cursor.execute('''
            INSERT INTO patients (id, first_name, middle_name, last_name, barangay, city, province, age, gender, birthday, cellphone, height, weight)
            VALUES (:id, :first_name, :middle_name, :last_name, :barangay, :city, :province, :age, :gender, :birthday, :cellphone, :height, :weight)
        ''', data)

    conn.commit()
    print("Reset successfully.")

if os.path.exists(FILE_PATH):
    # If the file exists, open the connection and cursor
    conn = sqlite3.connect(FILE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        middle_name TEXT,
        last_name TEXT,
        barangay TEXT,
        city TEXT,
        province TEXT,
        age TEXT,
        gender TEXT,
        birthday TEXT,
        cellphone TEXT,
        height TEXT,
        weight TEXT        
    )
''')
else:
    # If the file doesn't exist, perform your initialization code and then open the connection and cursor
    conn = sqlite3.connect(FILE_PATH)
    cursor = conn.cursor()
    initialize_data(cursor, conn)

editSaveButton = True

def setStateSave():
    entries = [entry_fn, entry_mn, entry_ln, entry_barangay, entry_city, entry_age,
               entry_gender, entry_birthday, entry_cellphone, entry_height, entry_weight,
               entry_province]
    
    for entry in entries:
        entry.config(state="readonly")

def setStateEdit():
    entries = [entry_fn, entry_mn, entry_ln, entry_barangay, entry_city, entry_age,
               entry_gender, entry_birthday, entry_cellphone, entry_height, entry_weight,
               entry_province]
    
    for entry in entries:
        entry.config(state="normal")


def editSave():
    global editSaveButton
    if editSaveButton:
        editButton.config(image=saveButton_image)
        editSaveButton = False
        setStateEdit()
    else:
        editButton.config(image=editButton_image)
        editSaveButton = True
        setStateSave()

        # Insert the patient data into the database
        patient_data = {
            'id' : patient_idVar,
            'first_name': entry_fn.get(),
            'middle_name': entry_mn.get(),
            'last_name': entry_ln.get(),
            'barangay': entry_barangay.get(),
            'city': entry_city.get(),
            'province': entry_province.get(),
            'age': entry_age.get(),
            'gender': entry_gender.get(),
            'birthday': entry_birthday.get(),
            'cellphone': entry_cellphone.get(),
            'height': entry_height.get(),
            'weight': entry_weight.get()
        }

        conn = sqlite3.connect('patient_data.db')
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE patients
            SET first_name = :first_name,
                middle_name = :middle_name,
                last_name = :last_name,
                barangay = :barangay,
                city = :city,
                province = :province,
                age = :age,
                gender = :gender,
                birthday = :birthday,
                cellphone = :cellphone,
                height = :height,
                weight = :weight
            WHERE id = :id
        ''', patient_data)

        conn.commit()
        conn.close()



def toggle_Home():
    global show_Home
    show_Home = not show_Home
    if show_Home:
        cameraButton.place(x=1214.0, y=919.0, width=182.0, height=129.0)
        patientsButton.place(x=1036.0, y=919.0, width=178.0, height=129.0)
        closeHomeButton.place(x=1157.0, y=924.0, width=121.0, height=120.0)
        openHomeButton.place_forget()
    else:
        cameraButton.place_forget()
        patientsButton.place_forget()
        closeHomeButton.place_forget()  
        openHomeButton.place(x=1157.0, y=924.0, width=121.0, height=120.0)

def toggle_Patients():
    global show_Patients
    show_Patients = not show_Patients
    if show_Patients:
        video_placeholder.place_forget()  # Hide video placeholder
        canvas.itemconfigure(liveIndicator, state="hidden")  # Hide liveIndicator
        canvas.itemconfigure(liveText, state="hidden")  # Hide liveText
        canvas.itemconfigure(fallDetectionArchive, state="hidden")
        stop_liveIndicator()  # Stop the toggle_liveIndicator function
        patientDataFrame.place_forget()
        archiveFrame.place_forget()
        cursor.execute("SELECT first_name, last_name, gender, age FROM patients")
        patient_data = cursor.fetchall()
        button_8.config(text=f"{patient_data[0][0]} {patient_data[0][1]}\n{patient_data[0][2]}\n{patient_data[0][3]}")
        button_9.config(text=f"{patient_data[1][0]} {patient_data[1][1]}\n{patient_data[1][2]}\n{patient_data[1][3]}")
        button_10.config(text=f"{patient_data[2][0]} {patient_data[2][1]}\n{patient_data[2][2]}\n{patient_data[2][3]}")
        button_11.config(text=f"{patient_data[3][0]} {patient_data[3][1]}\n{patient_data[3][2]}\n{patient_data[3][3]}")
        button_12.config(text=f"{patient_data[4][0]} {patient_data[4][1]}\n{patient_data[4][2]}\n{patient_data[4][3]}")
        button_13.config(text=f"{patient_data[5][0]} {patient_data[5][1]}\n{patient_data[5][2]}\n{patient_data[5][3]}")
        button_14.config(text=f"{patient_data[6][0]} {patient_data[6][1]}\n{patient_data[6][2]}\n{patient_data[6][3]}")
        button_15.config(text=f"{patient_data[7][0]} {patient_data[7][1]}\n{patient_data[7][2]}\n{patient_data[7][3]}")

        patientsFrame.place(x=572, y=133)
        

def toggle_Camera():
    global show_Camera
    show_Camera = not show_Camera
    if show_Camera:
        video_placeholder.place(x=572.0, y=133.0)  # Show video placeholder
        canvas.itemconfigure(liveIndicator, state="normal")  # Show liveIndicator
        canvas.itemconfigure(liveText, state="normal")  # Show liveText
        canvas.itemconfigure(fallDetectionArchive, state="hidden")
        start_liveIndicator()  # Start the toggle_liveIndicator function
        patientsFrame.place_forget()
        patientDataFrame.place_forget()
        archiveFrame.place_forget()


def show_archive_frame():
    global show_archive
    show_archive = not show_archive
    if show_archive:
        canvas.itemconfigure(fallDetectionArchive, state="normal")
        video_placeholder.place_forget()  # Hide video placeholder
        canvas.itemconfigure(liveIndicator, state="hidden")  # Hide liveIndicator
        canvas.itemconfigure(liveText, state="hidden")  # Hide liveText
        stop_liveIndicator()  # Stop the toggle_liveIndicator function
        patientDataFrame.place_forget()
        archiveFrame.place(x=572, y=133)
            

def display_camera_feed():
    ret, frame = cap.read()
    if ret:
        frame = cv2.resize(frame, (1286, 786))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
        img = ImageTk.PhotoImage(image=Image.fromarray(frame_rgb))
        video_placeholder.create_image(0, 0, anchor="nw", image=img)
        video_placeholder.image = img
        window.after(10, display_camera_feed)
    else:
        print("Failed to capture frame from camera.")

def update_date_time():
    #current_time = "13:38:56"
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%m-%d-%Y")
    date_time_text = f"Time: {current_time}\nDate: {current_date}"
    canvas.itemconfigure(date_time_text_item, text=date_time_text)
    window.after(1000, update_date_time)

def toggle_liveIndicator():
    if liveIndicator_active:
        canvas.itemconfigure(liveIndicator, state="hidden" if canvas.itemcget(liveIndicator, "state") == "normal" else "normal")
        window.after(1000, toggle_liveIndicator)

def start_liveIndicator():
    global liveIndicator_active
    liveIndicator_active = True
    toggle_liveIndicator()

def stop_liveIndicator():
    global liveIndicator_active
    liveIndicator_active = False


def update_patient_data(patient_id):
    cursor.execute("SELECT first_name, middle_name, last_name, barangay, city, province, age, gender, birthday, cellphone, height, weight FROM patients WHERE id = ?", (patient_id,))
    result = cursor.fetchone()

    if result is not None:
        first_name = result[0]
        middle_name = result[1]
        last_name = result[2]
        barangay = result[3]
        city = result[4]
        province = result[5]
        age = result[6]
        gender = result[7]
        birthday = result[8]
        cellphone = result[9]
        height = result[10]
        weight = result[11]

        patient_name = " ".join([first_name, last_name])

        label_patient.config(text=patient_name)
        label_age.config(text=age)
        label_female.config(text=gender)
        setStateEdit()
        entry_fn.delete(0, END)
        entry_fn.insert(0, first_name)

        entry_mn.delete(0, END)
        entry_mn.insert(0, middle_name)

        entry_ln.delete(0, END)
        entry_ln.insert(0, last_name)

        entry_barangay.delete(0, END)
        entry_barangay.insert(0, barangay)

        entry_city.delete(0, END)
        entry_city.insert(0, city)

        entry_age.delete(0, END)
        entry_age.insert(0, age)

        entry_gender.delete(0, END)
        entry_gender.insert(0, gender)

        entry_birthday.delete(0, END)
        entry_birthday.insert(0, birthday)

        entry_cellphone.delete(0, END)
        entry_cellphone.insert(0, cellphone)

        entry_height.delete(0, END)
        entry_height.insert(0, height)

        entry_weight.delete(0, END)
        entry_weight.insert(0, weight)

        entry_province.delete(0, END)
        entry_province.insert(0, province)

        patientDataFrame.place(x=572.0, y=133.0, width=1286.0, height=786.0)
        entry_fn.place(x=230, y=358, width=350, height=20)
        entry_mn.place(x=230, y=396, width=350, height=20)
        entry_ln.place(x=230, y=434, width=350, height=20)
        entry_barangay.place(x=231, y=472, width=350, height=20)
        entry_city.place(x=231, y=510, width=350, height=20)
        entry_age.place(x=782, y=358, width=350, height=20)
        entry_gender.place(x=782, y=396, width=350, height=20)
        entry_birthday.place(x=782, y=434, width=350, height=20)
        entry_cellphone.place(x=783, y=472, width=350, height=20)
        entry_height.place(x=782, y=510, width=350, height=20)
        entry_weight.place(x=782, y=543, width=350, height=20)
        entry_province.place(x=231, y=543, width=350, height=20)

        setStateSave()
    else:
        print(f"No patient found with ID {patient_id}")


window = Tk()
window.title("Oversee")
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(
    544.0,
    108.0,
    1886.0,
    997.0,
    fill="#D9D9D9",
    outline=""
)

video_placeholder = Canvas(
    canvas,
    bg="#000000",
    height=786,
    width=1286,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
video_placeholder.place(x=572.0, y=133.0)

exitButton_image = PhotoImage(file=relative_to_assets("exitButton.png"))
exitButton = Button(
    image=exitButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=open_login_screen,
    relief="flat",
    bg="#FFFFFF"  # Set the background color to #FFFFFF
)
exitButton.place(
    x=103.0,
    y=981.0,
    width=134.0,
    height=32.0
)

archiveButton_image = PhotoImage(file=relative_to_assets("archiveButton.png"))
archiveButton = Button(
    image=archiveButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=show_archive_frame,
    relief="flat",
    bg="#FFFFFF"  # Set the background color to #FFFFFF
)
archiveButton.place(
    x=105.0,
    y=544.952880859375,
    width=174.0,
    height=32.0
)

settingsButton_image = PhotoImage(file=relative_to_assets("settingsButton.png"))
settingsButton = Button(
    image=settingsButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat",
    bg="#FFFFFF"  # Set the background color to #FFFFFF
)
settingsButton.place(
    x=100.0,
    y=597.0,
    width=188.0,
    height=38.0
)

userDefault_image = PhotoImage(file=relative_to_assets("userDefault.png"))
userDefault = canvas.create_image(
    255.0,
    336.0,
    image=userDefault_image
)

cameraButton_image = PhotoImage(file=relative_to_assets("cameraButton.png"))
cameraButton = Button(
    image=cameraButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_Camera,
    relief="flat"
)
cameraButton.place_forget()  # Initially hide button 4

patientsButton_image = PhotoImage(file=relative_to_assets("patientsButton.png"))
patientsButton = Button(
    image=patientsButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_Patients,
    relief="flat"
)
patientsButton.place_forget()  # Initially hide button 5

closeHomeButton_image = PhotoImage(file=relative_to_assets("closeHomeButton.png"))
closeHomeButton = Button(
    image=closeHomeButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_Home,
    relief="flat"
)
closeHomeButton.place_forget()  # Hide button 6

openHomeButton_image = PhotoImage(file=relative_to_assets("openHomeButton.png"))
openHomeButton = Button(
    image=openHomeButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_Home,
    relief="flat"
)
openHomeButton.place(x=1157.0, y=924.0, width=121.0, height=120.0)  # Show button 7

logoMini_image = PhotoImage(file=relative_to_assets("logoMini.png"))
logoMini = canvas.create_image(
    213.0,
    111.0,
    image=logoMini_image
)

liveIndicator_image = PhotoImage(file=relative_to_assets("liveIndicator.png"))
liveIndicator = canvas.create_image(
    602.0,
    958.0,
    image=liveIndicator_image
)

liveText_image = PhotoImage(
    file=relative_to_assets("liveText.png"))
liveText = canvas.create_image(
    660.0,
    958.0,
    image=liveText_image
)

date_time_text_item = canvas.create_text(
    1858.0,
    930.0,
    anchor="ne",
    justify="right",
    text="Time and Date",
    fill="#000000",
    font=("RobotoMono-Bold", 27 * -1)
)
patientsFrame = Frame(
    window,
    bg="#FFFFFF",
    width=1286,
    height=786,
    highlightthickness=0,
    relief="ridge"
)

cursor.execute("SELECT first_name, last_name, gender, age FROM patients")
patient_data = cursor.fetchall()

button_image_8 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_8 = Button(
    patientsFrame,
    image=button_image_8,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(1),update_patient_idVar(1)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[0][0]} {patient_data[0][1]}\n{patient_data[0][2]}\n{patient_data[0][3]}",
    compound="center",
    justify="left"
)
button_8.place(
    x=34.0,
    y=39.0,
    width=546.0,
    height=158.0
)

button_image_9 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_9 = Button(
    patientsFrame,
    image=button_image_9,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(2),update_patient_idVar(2)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[1][0]} {patient_data[1][1]}\n{patient_data[1][2]}\n{patient_data[1][3]}",
    compound="center",
    justify="left"
)
button_9.place(
    x=679.0,
    y=39.0,
    width=546.0,
    height=158.0
)

button_image_10 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_10 = Button(
    patientsFrame,
    image=button_image_10,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(3),update_patient_idVar(3)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[2][0]} {patient_data[2][1]}\n{patient_data[2][2]}\n{patient_data[2][3]}",
    compound="center",
    justify="left"
)
button_10.place(
    x=34.0,
    y=222.0,
    width=546.0,
    height=158.0
)

button_image_11 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_11 = Button(
    patientsFrame,
    image=button_image_11,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(4),update_patient_idVar(4)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[3][0]} {patient_data[3][1]}\n{patient_data[3][2]}\n{patient_data[3][3]}",
    compound="center",
    justify="left"
)
button_11.place(
    x=679.0,
    y=222.0,
    width=546.0,
    height=158.0
)

button_image_12 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_12 = Button(
    patientsFrame,
    image=button_image_12,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(5),update_patient_idVar(5)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[4][0]} {patient_data[4][1]}\n{patient_data[4][2]}\n{patient_data[4][3]}",
    compound="center",
    justify="left"
)
button_12.place(
    x=34.0,
    y=405.0,
    width=546.0,
    height=158.0
)

button_image_13 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_13 = Button(
    patientsFrame,
    image=button_image_13,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(6),update_patient_idVar(6)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[5][0]} {patient_data[5][1]}\n{patient_data[5][2]}\n{patient_data[5][3]}",
    compound="center",
    justify="left"
)
button_13.place(
    x=679.0,
    y=405.0,
    width=546.0,
    height=158.0
)

button_image_14 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_14 = Button(
    patientsFrame,
    image=button_image_14,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(7),update_patient_idVar(7)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[6][0]} {patient_data[6][1]}\n{patient_data[6][2]}\n{patient_data[6][3]}",
    compound="center",
    justify="left"
)
button_14.place(
    x=34.0,
    y=588.0,
    width=546.0,
    height=158.0
)

button_image_15 = PhotoImage(file=relative_to_assets("patientsInfoButton.png"))
button_15 = Button(
    patientsFrame,
    image=button_image_15,
    borderwidth=130,
    highlightthickness=0,
    command=lambda: [update_patient_data(8),update_patient_idVar(8)],
    relief="flat",
    font=("Inter Bold", 24),
    foreground="#FFFFFF",
    text=f"{patient_data[7][0]} {patient_data[7][1]}\n{patient_data[7][2]}\n{patient_data[7][3]}",
    compound="center",
    justify="left"
)
button_15.place(
    x=679.0,
    y=588.0,
    width=546.0,
    height=158.0
)

line = canvas.create_line(460, 0, 460, 1080, fill="#09547D", width=8)
line = canvas.create_line(470, 20, 470, 1060, fill="#D9D9D9", width=4)



# Open the camera and start displaying the feed
#cap = cv2.VideoCapture("Stream Linkj")
cap = cv2.VideoCapture(0)
display_camera_feed()

# Start updating the date and time
update_date_time()

# Start toggling liveIndicator visibility
toggle_liveIndicator()


patientDataFrame = Frame(
    window,
    bg="#09547D",
    bd=0,
    highlightthickness=0,
    relief="ridge"
)




patientDataBG_image = PhotoImage(file=relative_to_assets("patientDataBG.png"))
patientDataBG = Label(
    patientDataFrame,
    image=patientDataBG_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat"
)
patientDataBG.place(
    x=0,
    y=24,
    width=1286,
    height=737
)
editButton_image = PhotoImage(
    file=relative_to_assets("editButton.png"))
saveButton_image = PhotoImage(
    file=relative_to_assets("saveButton.png"))

editButton = Button(
    patientDataFrame,
    image=editButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=editSave,
    relief="flat"
)


editButton.place(
    x=1158.0,
    y=282.0,
    width=90.0,
    height=38.0
)

backButton_image = PhotoImage(
    file=relative_to_assets("backButton.png"))

backButton = Button(
    patientDataFrame,
    image=backButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=toggle_Patients,
    relief="flat",
    bg="#09547D",
    activebackground="#09547D"
)
backButton.place(
    x=1057.0,
    y=664.0,
    width=229.0,
    height=60.0
)

label_female = Label(
    patientDataFrame,
    text="Female",
    fg="#FFFFFF",
    bg="#09547D",
    font=("RobotoRoman Regular", 24)
)
label_female.place(
    x=1061.0,
    y=145.0,
    anchor="ne"
)

label_age = Label(
    patientDataFrame,
    text="00",
    fg="#FFFFFF",
    bg="#09547D",
    font=("RobotoRoman Regular", 24)
)
label_age.place(
    x=1061.0,
    y=180.0,
    anchor="ne"
)

label_patient = Label(
    patientDataFrame,
    text="Patient 1",
    fg="#FFFFFF",
    bg="#09547D",
    font=("RobotoRoman Bold", 30)
)
label_patient.place(
    x=1061.0,
    y=101.0,
    anchor="ne"
)
entry_fn = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_mn = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_ln = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_barangay = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_city = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_age = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_gender = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_birthday = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_cellphone = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_height = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_weight = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)
entry_province = Entry(patientDataFrame, font=("Inter Bold", 12), justify="left", bg="#DEDEDE", relief="flat", highlightthickness=3)

archiveFrame = Frame(
    window,
    bg="#FFFFFF",
    width=1286.0,
    height=786.0,
    highlightthickness=0
)
fallDetectionArchive_image = PhotoImage(
    file=relative_to_assets("fallDetectionArchive.png"))
fallDetectionArchive = canvas.create_image(
    544.0,
    39.0,
    anchor='nw',
    image=fallDetectionArchive_image
)
canvas.itemconfigure(fallDetectionArchive, state="hidden")  

archiveBG_image = PhotoImage(file=relative_to_assets("ArchiveBg.png"))
archiveBG = Label(
    archiveFrame,
    image=archiveBG_image,
    borderwidth=0,
    highlightthickness=0,
    relief="flat",
    bg="#FFFFFF"
)
archiveBG.place(
    x=0,
    y=14,
    width=1286,
    height=684
)
deleteDeleteButton_image = PhotoImage(
    file=relative_to_assets("deleteDeleteButton.png"))
deleteDeleteButton = Button(
    archiveFrame,
    image=deleteDeleteButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("delete clicked"),
    relief="flat"
)
deleteDeleteButton.place(
    x=1037.0,
    y=720.0,
    width=90.0,
    height=37.894775390625
)

is_saved = False  # Variable to track the current state of the button

def saveFallImage():
    global is_saved
    if is_saved:
        saveFallButton.config(image=editButton_image)
        is_saved = False
    else:
        saveFallButton.config(image=saveButton_image)
        is_saved = True

saveSaveButton_image = PhotoImage(
    file=relative_to_assets("editButton.png"))
saveFallButton = Button(
    archiveFrame,
    image=saveSaveButton_image,
    borderwidth=0,
    highlightthickness=0,
    command=saveFallImage,
    relief="flat"
)
saveFallButton.place(
    x=1152.0,
    y=720.0,
    width=90.0,
    height=37.894775390625
)

patientName = Entry(archiveFrame, font=("Inter Regular", 20), justify="center", bg="#FFFFFF", relief="flat", highlightthickness=0)
timeFall = Entry(archiveFrame, font=("Inter Regular", 20), justify="center", bg="#FFFFFF", relief="flat", highlightthickness=0)
reports = Entry(archiveFrame, font=("Inter Regular", 20), justify="center", bg="#FFFFFF", relief="flat", highlightthickness=0)
response = Entry(archiveFrame, font=("Inter Regular", 20), justify="center", bg="#FFFFFF", relief="flat", highlightthickness=0)
patientName.place(x=11, y=70, width=302, height=34)
timeFall.place(x=348, y=70, width=340, height=34)
reports.place(x=717, y=70, width=273, height=34)
response.place(x=1002, y=70, width=264, height=34)

setStateSave()

window.resizable(False, False)
window.mainloop()
