import datetime

class Patient:
    def __init__(self,pid,name,age,gender):
        self.pid=pid
        self.name=name
        self.age=age
        self.gender=gender

    def save(self):
        with open('patients.txt','a') as f:
            f.write(f'{self.pid},{self.name},{self.age},{self.gender}')

class Doctor:
    def __init__(self,did,name,specialization):
        self.did=did
        self.name=name
        self.specialization=specialization

    def save(self):
        with open('doctors.txt','a') as f:
            f.write(f'{self.did},{self.name},{self.specialization}')

class Appointments:
    def __init__(self,aid,did,pid,date,prescription):
        self.aid=aid
        self.did=did
        self.pid=pid
        self.date=date
        self.prescription=prescription

    def save(self):
        with open('appointments.txt','a') as f:
                f.write(f'{self.aid},{self.pid},{self.did},{self.date},{self.prescription}')

def register_patient():
    pid  = int(input('Enter the Patient ID: '))
    name = input('Enter the Patient name: ')
    age = input('Enter the Patient age: ')
    gender = input('Enter the Patient gender: ')
    p = Patient(pid,name,age,gender)
    p.save()
    print('Patient has been registered successfully!!')

def register_doctor():
    did = int(input('Enter the Doctors ID: '))
    name = input('Enter the name of the Dcoctor: ')
    specialization = input('Enter the Doctors specialization: ')
    d = Doctor(did,name,specialization)
    d.save()
    print('Doctor has been registered successfully!!')

def make_appointments():
    aid = input("Enter Appointment ID: ")
    pid = input("Enter Patient ID: ")
    did = input("Enter Doctor ID: ")
    date = input("Enter Appointment Date (YYYY-MM-DD): ")
    prescription = input("Enter Prescription : ")
    a = Appointments(aid, pid, did, date, prescription)
    a.save()
    print("Appointment created.")

def generate_daily_reports():
    today = datetime.date.today().isoformat()
    print(f'Appointments for {today}: ')
    try:
        with open('appointments.txt','r') as f:
            found = False
            for line in f:
                aid,pid,did,date,prescription = line.strip().split(',',4)
                if date == today:
                    print(f'Appointment ID:{aid},\n Patient ID:{pid},\n Doctor ID:{did},\n Prescription:{prescription}\n')

            if not found:
                print('No appointments are scheduled today')

    except FileNotFoundError:
        print('No data avaliable')

def main():
    while True:
        print('----Hospital mangement System----')
        print('\n 1.Register Patient')
        print('\n 2.Register Doctor')
        print('\n 3.Make Appointments')
        print('\n 4.Generate Todays Reports')
        print('\n 5.Exit')

        choice = input('Enter the choice: ')

        if choice=='1':
            register_patient()
        elif choice=='2':
            register_doctor()
        elif choice == "3":
            make_appointments()
        elif choice == "4":
            generate_daily_reports()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
            
