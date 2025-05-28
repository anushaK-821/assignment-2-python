import tkinter as tk
from tkinter import messagebox
import json
import os
from collections import deque

MAX_SLOTS = 1
REGISTRATION_FILE = "registrations.json"
WAITLIST_FILE = "waitlist.json"

class EventRegistration:
    def __init__(self):
        self.slots = MAX_SLOTS
        self.registrations = self.load_file(REGISTRATION_FILE)
        self.waitlist = deque(self.load_file(WAITLIST_FILE))

    def load_file(self, filename):
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        return []

    def save_to_file(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def register(self, name, email):
        if len(self.registrations) < self.slots:
            self.registrations.append({"name": name, "email": email})
            self.save_to_file(REGISTRATION_FILE, self.registrations)
            return True, f"Registration Confirmed for {name}"
        else:
            self.waitlist.append({"name": name, "email": email})
            self.save_to_file(WAITLIST_FILE, list(self.waitlist))
            return False, f"No slots left. {name} added to waitlist."

    def get_waitlist(self):
        return list(self.waitlist)

class EventApp:
    def __init__(self, root):
        self.system = EventRegistration()
        self.root = root
        self.root.title("Event Registration System")

        tk.Label(root, text="EVENT REGISTRATION", font=('Arial', 16, 'bold')).pack(pady=10)

        tk.Button(root, text="Register", width=25, command=self.register_ui).pack(pady=5)
        tk.Button(root, text="Show Waitlist", width=25, command=self.show_waitlist).pack(pady=5)

    def register_ui(self):
        top = tk.Toplevel(self.root)
        top.title("Register for Event")

        tk.Label(top, text="Name:").pack()
        name_entry = tk.Entry(top)
        name_entry.pack()

        tk.Label(top, text="Email:").pack()
        email_entry = tk.Entry(top)
        email_entry.pack()

        def register():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            if name and email:
                success, message = self.system.register(name, email)
                messagebox.showinfo("Registration", message)
                top.destroy()
            else:
                messagebox.showerror("Error", "All fields are required.")

        tk.Button(top, text="Submit", command=register).pack(pady=5)

    def show_waitlist(self):
        top = tk.Toplevel(self.root)
        top.title("Waitlist")
        waitlist = self.system.get_waitlist()
        if not waitlist:
            tk.Label(top, text="No one is on the waitlist.").pack()
        else:
            for idx, person in enumerate(waitlist, start=1):
                tk.Label(top, text=f"{idx}. {person['name']} ({person['email']})").pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = EventApp(root)
    root.mainloop()
