class Doctor:

    def __init__(self, did, name, specialization):
        self.did = did
        self.name = name
        self.specialization = specialization

    def display(self):
        print(f"{self.did}\t{self.name}\t{self.specialization}")


class Patient:

    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

    def display(self):
        print(f"{self.pid}\t{self.name}")


class Appointment:

    def __init__(self, aid, patient, doctor, date, time):
        self.aid = aid
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time

    def display(self):
        print(
            f"{self.aid}\t{self.patient.name}\t{self.doctor.name}\t{self.date}\t{self.time}"
        )


class doctorAppointment:

    def __init__(self):
        self.doctors = []
        self.patients = []
        self.appointments = []

    # ----- Add Doctor -----
    def add_doctor(self):

        did = int(input("Enter Doctor ID : "))
        name = input("Enter Doctor Name : ")
        specialization = input("Enter Doctor Specialization : ")

        self.doctors.append(
            Doctor(did, name, specialization)
        )

        print("Doctor Added Successfully!")

    # ----- Add Patient -----
    def add_patient(self):

        pid = int(input("Enter Patient ID : "))
        name = input("Enter Patient Name : ")

        self.patients.append(
            Patient(pid, name)
        )

        print("Patient Added Successfully!")

    # ----- Find Doctor -----
    def find_doctor(self, did):

        for d in self.doctors:
            if d.did == did:
                return d

        return None

    # ----- Find Patient -----
    def find_patient(self, pid):

        for p in self.patients:
            if p.pid == pid:
                return p

        return None

    # ----- Book Appointment -----
    def BookAppointment(self):

        aid = int(input("Enter Appointment ID : "))
        pid = int(input("Enter Patient ID : "))
        did = int(input("Enter Doctor ID : "))
        date = input("Enter Date : ")
        time = input("Enter Time : ")

        patient = self.find_patient(pid)
        doctor = self.find_doctor(did)

        if not patient or not doctor:
            print("Patient or Doctor Not Found!")
            return

        # Check doctor availability
        for a in self.appointments:

            if (
                a.doctor.did == did
                and a.date == date
                and a.time == time
            ):

                print("Doctor Not Available at this time")
                return

        self.appointments.append(
            Appointment(aid, patient, doctor, date, time)
        )

        print("Appointment Booked Successfully!")

    # ----- Cancel Appointment -----
    def cancel_appointment(self):

        aid = int(input("Enter Appointment ID : "))

        for a in self.appointments:

            if a.aid == aid:
                self.appointments.remove(a)

                print("Appointment Cancelled Successfully!")
                return

        print("Appointment Not Found!")

    # ----- View Appointments -----
    def view_appointments(self):

        print("\nAID\tPatient\tDoctor\tDate\tTime")
        print("------------------------------------------")

        for a in self.appointments:
            a.display()

    # ----- View Doctors -----
    def view_doctors(self):

        print("\nID\tName\tSpecialization")
        print("--------------------------------")

        for d in self.doctors:
            d.display()


# ----- Main Program -----

dp = doctorAppointment()

while True:

    print("\n===== Doctor Appointment System =====")

    print("1. Add Doctor")
    print("2. Add Patient")
    print("3. Book Appointment")
    print("4. Cancel Appointment")
    print("5. View Appointments")
    print("6. View Doctors")
    print("7. Exit")

    choice = int(input("Enter Your Choice : "))

    if choice == 1:
        dp.add_doctor()

    elif choice == 2:
        dp.add_patient()

    elif choice == 3:
        dp.BookAppointment()

    elif choice == 4:
        dp.cancel_appointment()

    elif choice == 5:
        dp.view_appointments()

    elif choice == 6:
        dp.view_doctors()

    elif choice == 7:
        print("System Closed 😊")
        break

    else:
        print("Invalid Choice!")         