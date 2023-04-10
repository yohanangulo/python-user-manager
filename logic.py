import re
import smtplib
from email.message import EmailMessage
import threading
from twilio.rest import Client
from tkinter import messagebox
import keys

class Logic:
    def handle_submit(self):
        if not(self.add_user_name_input.get() and self.add_user_ln_input.get() and self.add_user_email.get() and self.add_user_phone.get()):
            return self.label_message.set('Fill all the blanks')
        elif len(self.phone_str_var.get()) < 10:
            return self.label_message.set('Check the phone number is correct')
        elif not re.search(r'^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$', self.add_user_email.get()):
            return self.label_message.set('Check the email address is correct')
        self.create_record()

    def create_record(self):
        self.record = {
            "name": self.add_user_name_input.get(),
            "lastname": self.add_user_ln_input.get(),
            "email": self.add_user_email.get(),
            "phoneNumber": self.add_user_phone.get(),
        }

        with open('db.txt', 'a') as db:
            db.write(f"{str(self.record)}\n")
            db.close()
        
        self.name_str_var.set('')
        self.lastname_str_var.set('')
        self.email_str_var.set('')
        self.phone_str_var.set('')
        self.add_user_name_input.focus()

        # msgbox

        self.welcome_message = "Dear {name} {lastname},\n\nWe are thrilled to have you as a new member of our community.\n\nThank you for registering with us and allowing us the opportunity to connect with you.".format(**self.record)

        send_email_thread = threading.Thread(target=self.send_email_message)
        send_email_thread.start()

        send_WA_thread = threading.Thread(target=self.send_WA_message)
        send_WA_thread.start()

        messagebox.showinfo('Successfull', 'New user added successfully')
        
    def send_WA_message(self):
        phone_number = self.record['phoneNumber'][1:] if self.record['phoneNumber'][0] == '0' else self.record['phoneNumber']
        
        account_sid = keys.account_sid
        auth_token = keys.auth_token
        client = Client(account_sid, auth_token)

        client.messages.create(
            from_='whatsapp:+14155238886',
            body=self.welcome_message,
            to='whatsapp:+58' + phone_number
        )

    def send_email_message(self):
        message = EmailMessage()
        message['Subject'] = 'Welcome to User Manager'
        message['From'] = 'anguloyohan98@gmail.com'
        message['To'] = self.record['email']

        message.set_content(self.welcome_message)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('anguloyohan98@gmail.com', keys.email_token)
        server.send_message(message)
        server.quit()

    def input_validation_pivot(self, var, index, mode):
        if var == 'name': self.validate_data(r"[a-zA-Z\s]+$", self.name_str_var, self.name_error)
        elif var == 'lastname': self.validate_data(r"[a-zA-Z\s]+$", self.lastname_str_var, self.lastname_error)
        elif var == 'email': self.label_message.set('')
        elif var == 'phone': self.validate_data(r"[0-9+]{0,11}", self.phone_str_var, self.phone_error)


    # testing this function
    def validate_data(self, reg, var, error_msg):
        if re.fullmatch(reg, var.get()) or var.get() == '':
            self.label_message.set('')
            if error_msg in self.messages: self.messages.remove(error_msg)
        else:
            if error_msg not in self.messages: self.messages.append(error_msg)
        self.print_typing_errors() 

    def print_typing_errors(self):
        if len(self.messages) > 0:
            self.label_message.set(self.messages[-1])
            self.register_user_btn.configure(state='disabled')
            return
        self.register_user_btn.configure(state='enabled')

    def get_users(self):
        with open('db.txt', 'r') as db:
            self.rows = db.readlines()
            db.close()
