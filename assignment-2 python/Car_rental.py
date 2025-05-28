import tkinter as tk
from tkinter import messagebox
import datetime
import json
import os

class Car:
    def __init__(self, car_id, model, rate, available=True):
        self.car_id = car_id
        self.model = model
        self.rate = rate
        self.available = available

    def to_dict(self):
        return {
            "car_id": self.car_id,
            "model": self.model,
            "rate": self.rate,
            "available": self.available
        }

class CarRentalSystem:
    def __init__(self):
        self.cars = [
            Car(1, "Hyundai", 50),
            Car(2, "Ford", 60),
            Car(3, "Audi", 70),
            Car(4, "Kia", 80),
            Car(5, "Jeep", 90)

        ]
        self.history_file = "rental_history.json"

    def get_available_cars(self):
        return [car for car in self.cars if car.available]

    def book_car(self, car_id, customer, days):
        car = next((c for c in self.cars if c.car_id == car_id and c.available), None)
        if not car:
            return False, "Car not available."

        rent_date = datetime.date.today()
        return_date = rent_date + datetime.timedelta(days=int(days))
        amount = car.rate * int(days)
        car.available = False

        rental_data = {
            "car_id": car.car_id,
            "model": car.model,
            "customer": customer,
            "rent_date": str(rent_date),
            "return_date": str(return_date),
            "amount": amount
        }
        self._save_history(rental_data)
        return True, f"Car booked! Total: ${amount}"

    def return_car(self, car_id):
        car = next((c for c in self.cars if c.car_id == car_id and not c.available), None)
        if car:
            car.available = True
            return True, "Car returned successfully."
        return False, "Car not found or already returned."

    def _save_history(self, entry):
        history = self.get_history()
        history.append(entry)
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=4)

    def get_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

class RentalApp:
    def __init__(self, root):
        self.system = CarRentalSystem()
        self.root = root
        self.root.title("Car Rental System")

        tk.Label(root, text="CAR RENTAL SYSTEM", font=('Arial', 16, 'bold')).pack(pady=10)

        tk.Button(root, text="Available Cars", width=25, command=self.list_cars).pack(pady=5)
        tk.Button(root, text="Book a Car", width=25, command=self.book_car_ui).pack(pady=5)
        tk.Button(root, text="Return a Car", width=25, command=self.return_car_ui).pack(pady=5)
        tk.Button(root, text="History", width=25, command=self.show_history).pack(pady=5)

    def list_cars(self):
        top = tk.Toplevel(self.root)
        top.title("Available Cars")
        for car in self.system.get_available_cars():
            tk.Label(top, text=f"ID: {car.car_id} | Model: {car.model} | Rate: ${car.rate}/day").pack()

    def book_car_ui(self):
        top = tk.Toplevel(self.root)
        top.title("Book a Car")

        tk.Label(top, text="Car ID:").pack()
        car_id_entry = tk.Entry(top)
        car_id_entry.pack()

        tk.Label(top, text="Customer Name:").pack()
        customer_entry = tk.Entry(top)
        customer_entry.pack()

        tk.Label(top, text="Days:").pack()
        days_entry = tk.Entry(top)
        days_entry.pack()

        def book():
            try:
                cid = int(car_id_entry.get())
                name = customer_entry.get()
                days = int(days_entry.get())
                success, msg = self.system.book_car(cid, name, days)
                messagebox.showinfo("Booking", msg)
                top.destroy()
            except:
                messagebox.showerror("Error", "Invalid input.")

        tk.Button(top, text="Confirm Booking", command=book).pack(pady=5)

    def return_car_ui(self):
        top = tk.Toplevel(self.root)
        top.title("Return Car")

        tk.Label(top, text="Enter Car ID to Return:").pack()
        car_id_entry = tk.Entry(top)
        car_id_entry.pack()

        def ret():
            try:
                cid = int(car_id_entry.get())
                success, msg = self.system.return_car(cid)
                messagebox.showinfo("Return", msg)
                top.destroy()
            except:
                messagebox.showerror("Error", "Invalid Car ID.")

        tk.Button(top, text="Return Car", command=ret).pack(pady=5)

    def show_history(self):
        top = tk.Toplevel(self.root)
        top.title("Rental History")
        history = self.system.get_history()
        if not history:
            tk.Label(top, text="No rental history found.").pack()
        for h in history:
            text = f"{h['customer']} rented {h['model']} from {h['rent_date']} to {h['return_date']} - ${h['amount']}"
            tk.Label(top, text=text).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = RentalApp(root)
    root.mainloop()
