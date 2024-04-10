import tkinter as tk
from tkinter import messagebox, ttk
import logging

# Configure the root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create a file handler for writing logs to a file
file_handler = logging.FileHandler('social_network.log', mode='w')
file_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Create a stream handler for logging to the terminal
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)



class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.friends = set()
        self.messages = []

    def update_password(self, new_password):
        self.password = new_password
        print("Password updated successfully.")

    def add_friend(self, friend):
        self.friends.add(friend)

    def remove_friend(self, friend):
        self.friends.discard(friend)

    def send_message(self, recipient, message):
        recipient.messages.append((self.username, message))

    def show_new_messages(self):
        new_messages = []
        for message in self.messages:
            new_messages.append(message)
        self.messages = []  # Reset messages after showing them
        return new_messages


class SocialNetwork:
    def __init__(self):
        self.users = {}
        self.logged_in_user = None

        # Initial users
        self.register("Petra", "everhating")
        self.register("Radek", "thechairman")


    def register(self, username, password):
        if username in self.users:
            return False
        
        new_user = User(username, password)
        for user in self.users.values():
            new_user.add_friend(user)
            user.add_friend(new_user)
        self.users[username] = new_user
        return True


    def authenticate(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.logged_in_user = user
            return True
        return False


    def update_password(self, new_password):
        if self.logged_in_user:
            self.logged_in_user.update_password(new_password)
            return True
        return False


    def send_message(self, recipient_username, message):
        if self.logged_in_user and recipient_username in self.users:
            recipient = self.users[recipient_username]
            self.logged_in_user.send_message(recipient, message)
            return True
        return False

    def show_new_messages(self):
        if self.logged_in_user:
            new_messages = self.logged_in_user.show_new_messages()
            if new_messages:
                for sender, message in new_messages:
                    print(f"New message from {sender}: {message}")
            else:
                print("No new messages.")
            return True
        return False


class SocialNetworkGUI:
    def __init__(self, master):
        self.network = SocialNetwork()
        self.master = master
        self.master.title("SocialApp")
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)
        
        tk.Label(self.frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1)
        
        tk.Label(self.frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        self.login_button = tk.Button(self.frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0)
        
        self.register_button = tk.Button(self.frame, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1)

        # Elements for sending messages
        self.message_frame = tk.Frame(self.master)
        tk.Label(self.message_frame, text="Recipient:").grid(row=0, column=0)
        self.recipient_var = tk.StringVar(self.master)
        self.recipient_dropdown = ttk.Combobox(self.message_frame, textvariable=self.recipient_var)
        self.recipient_dropdown.grid(row=0, column=1)
        
        tk.Label(self.message_frame, text="Message:").grid(row=1, column=0)
        self.message_entry = tk.Entry(self.message_frame, width=50)
        self.message_entry.grid(row=1, column=1)
        
        self.send_message_button = tk.Button(self.message_frame, text="Send Message", command=self.send_message)
        self.send_message_button.grid(row=2, column=0, columnspan=2)
        self.message_frame.pack_forget()  # Hide the message frame initially
        
        self.messages_text = tk.Text(self.master, state='disabled', height=10, width=50)
        self.messages_text.pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        logging.info(f"Attempting login for user: {username}")
        if self.network.authenticate(username, password):
            logging.info(f"Login successful for user: {username}")
            self.display_messages()
            self.show_message_sending_ui()
            self.refresh_messages()
        else:
            logging.warning(f"Login failed for user: {username}")
            messagebox.showerror("Login failed", "Incorrect username or password")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        logging.info(f"Attempting registration for user: {username}")
        if self.network.register(username, password):
            logging.info(f"Registration successful for user: {username}")
            messagebox.showinfo("Registration successful", "You can now login.")
        else:
            logging.warning(f"Registration failed for user: {username}. Username may already be taken.")
            messagebox.showerror("Registration failed", "Username may already be taken")
            
    def display_messages(self):
        self.messages_text.config(state='normal')
        self.messages_text.delete(1.0, tk.END)
        for message in self.network.logged_in_user.show_new_messages():
            self.messages_text.insert(tk.END, f"{message[0]}: {message[1]}\n")
        self.messages_text.config(state='disabled')

    def show_message_sending_ui(self):
        # Update the recipient dropdown list
        self.recipient_dropdown['values'] = list(self.network.users.keys())
        self.message_frame.pack()

    def send_message(self):
        recipient = self.recipient_var.get()
        message = self.message_entry.get()
        if recipient and message and self.network.send_message(recipient, message):
            messagebox.showinfo("Success", "Message sent successfully.")
            self.messages_text.config(state='normal')
            self.messages_text.insert(tk.END, f"[To {recipient}]: {message}\n")  # Show sent message
            self.messages_text.config(state='disabled')
            self.message_entry.delete(0, tk.END) 
        else:
            messagebox.showerror("Error", "Failed to send message. Please check the recipient's username and try again.")


    def refresh_messages(self):
        if self.network.logged_in_user:
            new_messages = self.network.logged_in_user.show_new_messages()
            if new_messages:
                self.messages_text.config(state='normal')
                for sender, message in new_messages:
                    self.messages_text.insert(tk.END, f"[From {sender}]: {message}\n")
                self.messages_text.config(state='disabled')
            # Schedule this method to be called again after a certain amount of time
            self.master.after(5000, self.refresh_messages)  # 5000 milliseconds = 5 seconds




if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkGUI(root)
    root.mainloop()
# EoF