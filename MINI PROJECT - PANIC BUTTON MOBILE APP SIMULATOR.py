import tkinter as tk
from tkinter import messagebox
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import speech_recognition as sr
import imaplib 
import email
from email.header import decode_header
import time

#Make sure the contact is a valid email address
contacts = ["srao59743@gmail.com","sanju.310sanjay@gmail.com","tharunkarthikeya98@gmail.com"]

# Function to send the email alert
def send_email_alert():
    sender_email = "srao59743@gmail.com"  #Your email
    sender_password = "ekjp ryjt cpge ozku"   #Your app password

    subject = "Emergency Alert - Panic Button Activated!"
    body = "This is an emergency alert. The panic button was activated, and immediate help is required!"
    
    for contact in contacts:
        try:
           #Create the email
           msg = MIMEMultipart()
           msg['From'] = sender_email
           msg['To'] = contact
           msg['Subject'] = subject

           msg.attach(MIMEText(body, 'plain'))

           #Set up the SMTP server
           server = smtplib.SMTP('smtp.gmail.com', 587)
           server.starttls()
           server.login(sender_email, sender_password)

           #Send the email
           server.sendmail(sender_email, contact, msg.as_string())

           server.quit()
        except Exception as e:
           messagebox.showerror("Error", f"Failed to send email to {contact}. Error: {str(e)}")
           return
    messagebox.showinfo("Success", "Panic Button Activated! Emergency email sent to all contacts.")

#Function to trigger the panic alert
def panic_alert():
    # First, simulate sending the email alert
    send_email_alert()

#Voice command function to trigger panic alert
def listen_for_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        if "panic" or "help" in command.lower():
            print("Panic or Help command recognized, triggering alert...")
            panic_alert()
        else:
            print("No panic command detected.")
    except Exception as e:
        print(f"Error recognizing voice: {e}")

#2-way communication: Check for response
def check_for_response():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("srao59743@gmail.com","ekjp ryjt cpge ozku")
        mail.select("inbox")

        # Adding a delay to allow responses to be received
        print("Waiting for any response emails...")
        time.sleep(10)  # Delay for 10 seconds

        # Search only for UNSEEN (unread) messages
        status, messages = mail.search(None, "UNSEEN")
    
        if status == "OK":
            email_ids = messages[0].split()
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg =  email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")

                        print(f"Received email with subject: {subject}")

                        # List of possible confirmation phrases
                        confirmation_phrases = [
                            "confirmed", "on my way", "help on the way",
                            "arriving in", "there soon", "will be there","re: emergency alert", "emergency alert - panic button"
                        ]

                        # Check if any of the confirmation phrases are in the email subject
                        if any(phrase in subject.lower() for phrase in confirmation_phrases):
                           print("Emergency contact confirmed assistance!")
                           messagebox.showinfo("Response","Emergency contact confirmed assistance!")
                           return
                        else:
                            print("No confirmation received yet.")      
        mail.logout()
    except Exception as e:
        print(f"Error checking for response: {e}")

#main GUI application window
root=tk.Tk()
root.title("Panic Button Simulator")
root.geometry("300x300")  #set window size

#label
label=tk.Label(root, text="Press the Panic Button or use voice command in an Emergency!", font=("Helvetica", 12))
label.pack(pady=20)

# Panic button
panic_button = tk.Button(root, text="PANIC BUTTON", font=("Helvetica", 16), bg="red", fg="white", command=panic_alert)
panic_button.pack(pady=20)

#Add a button for checking response
check_button = tk.Button(root, text="Check for Response", font=("Helvetica", 12), command=check_for_response)
check_button.pack(pady=20)

#Add a button for voice command activation
voice_button = tk.Button(root, text="Activate by voice", font=("Helvetica", 12), command=listen_for_voice_command)
voice_button.pack(pady=10)

#Show the contacts in the window
contacts_label = tk.Label(root, text="Predefined Contacts:", font=("Helvetica", 10))
contacts_label.pack(pady=10)
contacts_text = "\n".join(contacts)
contacts_display = tk.Label(root, text=contacts_text, font=("Helvetica", 10))
contacts_display.pack()

# Update GUI with confirmation message
def show_confirmation_in_gui():
    confirmation_label = tk.Label(root, text="Emergency contact confirmed assistance!", font=("Helvetica", 12), fg="green")
    confirmation_label.pack(pady=10)

# Modify the check_for_response function to include show_confirmation_in_gui call
def check_for_response():
    # [Code from previous function here]
    
    # Within your if condition where confirmation is received:
    show_confirmation_in_gui()


#Run the application
root.mainloop()