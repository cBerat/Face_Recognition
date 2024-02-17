import customtkinter
import cv2
import sqlite3
from PIL import Image, ImageTk
import os
from tkinter import messagebox
import streamlit as st
import face_recognition
from customtkinter import CTkToplevel
import numpy as np

known_face_encodings = []
known_face_names = []

def signUp(fullName, stdNo, checkBox):
    try:
        global img
        if fullName.isascii() and stdNo.isascii():
            if checkBox == 1:
                if fullName != "" and stdNo != "":
                    photo_control = True
                    if photo_control:
                        with open(filepath, 'rb') as f:
                            img = f.read()
                        cursor.execute('''INSERT INTO students (fullName, stdNo, photo) VALUES(?, ?, ?) ''', (fullName, stdNo, img))
                        db_connect.commit()
                        messagebox.showinfo("Success!", f"{fullName} is added to our servers")
                    else:
                        messagebox.showwarning("Warning!", "Please select an image")
                else:
                    messagebox.showerror("Error!", "Fill in all the blanks!")
            else:
                messagebox.showwarning("Warning!", "Please read the terms")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            messagebox.showerror("Error! ", "This record with the student number already exists. Please check your student number.")
        else:
            messagebox.showerror("Error! ", "An unknown error occurred", str(e))
    except Exception as e:
        messagebox.showerror("Error!", "Please check inputs")

def signUpScreen(app=None):
    mainMenuClear()
    global unameStr
    frame2.pack_forget()
    for att in frame.winfo_children():
        att.destroy()
    frame.pack(pady=20, padx=60, fill="both", expand=True)
    label = customtkinter.CTkLabel(master=frame, text="Sign Up System")
    label.pack(pady=12, padx=10)
    uname = customtkinter.CTkEntry(master=frame, placeholder_text="Full Name")
    uname.pack(pady=12, padx=10)
    unameStr = uname.get()
    stdNo = customtkinter.CTkEntry(master=frame, placeholder_text="Student Number")
    stdNo.pack(pady=12, padx=10)
    label_widget = customtkinter.CTkLabel(master=frame, text="Select Image")
    label_widget.pack(pady=12, padx=10)
    button1 = customtkinter.CTkButton(master=frame, text="Open Camera", command=signUp, font=("Bold Arial", 16),
                                      text_color="black", fg_color="green", hover_color="white")
    button1.pack(pady=12, padx=10)
    button2 = customtkinter.CTkButton(master=frame, text="Select From File", command=selectFromFile,
                                      font=("Bold Arial", 16),
                                      text_color="black", fg_color="green", hover_color="white")
    button2.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text="Sign Up",
                                     command=lambda: signUp(f"{str(uname.get())}", f"{str(stdNo.get())}", checkboxVar.get()))
    button.pack(pady=12, padx=10)
    checkboxVar = customtkinter.IntVar()
    checkbox = customtkinter.CTkCheckBox(master=frame, text="I have read and accepted", variable=checkboxVar)
    checkbox.pack(pady=12, padx=10)
    closeBtn = customtkinter.CTkButton(master=frame, width=9, height=5, text=" Close ", command=close)
    closeBtn.pack(pady=12, padx=10)

def close():
    frame.pack_forget()
    for att in frame.winfo_children():
        att.destroy()
    frame2.pack_forget()
    for att in frame2.winfo_children():
        att.destroy()
    getMainMenu()

def selectFromFile():
    signUpScreen()
    opendialog = True
    if opendialog:
        x = customtkinter.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select an image",
                                                     filetypes=[('JPEG Files', ".jpeg"), ("PNG Files", ".png"),
                                                                ("JPG Files", ".jpg"), ("All Files", "*.*")])
        img = Image.open(x)
        global filepath
        filepath = x
        img.thumbnail((150, 150))
        img = ImageTk.PhotoImage(image=img)
        imgLabel = customtkinter.CTkLabel(master=frame, text="Student Photo")
        imgLabel.configure(image=img)
        imgLabel.pack()
    else:
        pass

def loginScreen():
    mainMenuClear()
    face_recognition_model = "hog"
    face_recognition_window = CTkToplevel(frame2)
    face_recognition_window.title("Face Recognition")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        face_locations = face_recognition.face_locations(frame, model=face_recognition_model)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                logged_as(name)

            for (top, right, bottom, left), name in zip(face_locations, [name]):
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        cv2.imshow("Face Recognition", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def logged_as(name):
    print(f"Logged in as {name}")

def load_known_faces():
    cursor.execute("SELECT fullName, photo FROM students")
    records = cursor.fetchall()

    for record in records:
        name, photo_data = record
        strip_name = name.strip("()',")
        byte_ph = bytes(photo_data)
        img_array = np.frombuffer(byte_ph, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        face_locations = face_recognition.face_locations(img)
        if face_locations:
            encoding = face_recognition.face_encodings(img, [face_locations[0]])[0]
            known_face_names.append(strip_name)
            known_face_encodings.append(encoding)

def mainMenuClear():
    mainMenu.pack_forget()
    for att in mainMenu.winfo_children():
        att.destroy()

def getMainMenu():
    img = Image.open(r"C:\Users\cankd\Desktop\design_project2\design_project2\eru.png")
    img.thumbnail((750, 750))
    img = ImageTk.PhotoImage(image=img)

    imgLabel = customtkinter.CTkLabel(master=mainMenu, text="")
    imgLabel.configure(image=img)
    imgLabel.pack(pady=150, padx=0)
    mainMenu.pack(pady=20, padx=60, fill="both", expand=True)

if __name__ == '__main__':
    db_connect = sqlite3.connect("students.db")
    cursor = db_connect.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students (fullName TEXT, stdNo TEXT PRIMARY KEY, photo BINARY)")

    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("dark-blue")
    
    root = customtkinter.CTk()
    w = 650
    h = 850
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    
    mainMenu = customtkinter.CTkFrame(master=root)
    
    label1 = customtkinter.CTkLabel(master=root, text="Welcome", text_color="dark cyan", font=("Bold Arial", 20))
    label1.pack(pady=12, padx=10)
    
    signUpBtn = customtkinter.CTkButton(master=root, text="Sign Up", text_color="black", fg_color="cyan",
                                        hover_color="dark cyan", font=('Bold Arial', 24), command=signUpScreen)
    signUpBtn.pack(pady=12, padx=10)
    
    root.title("Erciyes University Access System")
    
    loginBtn = customtkinter.CTkButton(master=root, text="Login", text_color="black", fg_color="cyan",
                                       hover_color="dark cyan", font=('Bold Arial', 24), command=loginScreen)
    loginBtn.pack(pady=12, padx=10)
    
    filepath = ""
    
    # Ana menü eru fotosu
    load_known_faces()
    getMainMenu()
    
    frame = customtkinter.CTkFrame(master=root)  # signup screen için
    frame2 = customtkinter.CTkFrame(master=root)  # login screen için
    
    # entry initialize
    unameStr = ''
    root.mainloop()