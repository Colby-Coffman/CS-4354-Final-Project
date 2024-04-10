import mysql.connector  # mysql library
import pandas as pd
import names  # random name generator library https://github.com/treyhunner/names
import random
import numpy as np
from datetime import datetime, timedelta
import decimal


def main():
    cnx = mysql.connector.connect(user="root", password=input(
        "Enter Password: "), database="MedicalMinds")
    generate_pharmacy(cnx)
    generate_doctor(cnx)
    generate_patient(cnx)
    generate_medication(cnx)
    generate_prescriptions(cnx)
    generate_workplace(cnx)
    cnx.commit()
    cnx.close()


def generate_pharmacy(cnx: mysql.connector.MySQLConnection):
    # Uses data from: https://www.johnsnowlabs.com/marketplace/us-pharmacy-drugstore-location/
    cursor = cnx.cursor()
    add_insurance = "INSERT IGNORE INTO Pharmacy (PName, PAddress) VALUES (%s, %s)"
    df = pd.read_csv('pharmacy.csv')
    for index, data in df.iterrows():
        cursor.execute(add_insurance, (data["Pharmacy_Name"], data['Address']))
    cursor.close()


def generate_doctor(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor()
    doctor_types = ["General Practitioner", "Pediatricians", "Cardiologist", "Nephrologist", "Dermatologist", "Neurologist",
                    "Psychiatrist", "Gynecologist", "Gastroenterologist", "Geriatrician", "Nephrologist", "Oncologist", "Endocrinologist",
                    "Hematologist", "Otalaryngologist"]
    add_doctor = "INSERT IGNORE INTO Doctor (DFirstName, DLastName, DType) VALUES (%s, %s, %s)"
    for i in range(101):
        cursor.execute(add_doctor, (names.get_first_name(),
                       names.get_last_name(), random.choice(doctor_types)))
    cursor.close()


def generate_patient(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor()
    gender = ["Male", "Female", "Other", "Undisclosed"]
    age = range(18, 100)
    height = np.arange(152.4, 213.0, step=0.1)
    weight = np.arange(117, 300, step=0.01)
    add_patient = "INSERT IGNORE INTO Patient (SSN, FirstName, LastName, Gender, Age, Height, Weight, PCare_doctorid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute("SELECT DoctorID FROM Doctor")
    doctor_ids = [row[0] for row in cursor.fetchall()]  # Fetch all DoctorIDs from the Doctor table
    for i in range(101):
        ssn = random.randint(111111111, 999999999)  # Generate a random SSN
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        gender_choice = random.choice(gender)
        patient_age = random.choice(age)
        patient_height = random.choice(height)
        patient_weight = random.choice(weight)
        doctor_id = random.choice(doctor_ids)  # Choose a random DoctorID
        cursor.execute(add_patient, (ssn, first_name, last_name, gender_choice, patient_age, patient_height, patient_weight, doctor_id))
    cursor.close()



def generate_medication(cnx: mysql.connector.MySQLConnection):
    # Uses data from: https://www.kaggle.com/datasets/jithinanievarghese/drugs-side-effects-and-medical-condition
    cursor = cnx.cursor()
    schedule = ""
    side_effects = ""
    application = ["Take once daily", "Take twice daily", "Take one after every meal", "Apply topically"]
    add_insurance = "INSERT IGNORE INTO Medication (Generic_Name, Side_effects, Classification, Uses, Applications) VALUES (%s, %s, %s, %s, %s)"
    df = pd.read_csv('drugs_side_effects_drugs_com.csv')
    df = df.where((pd.notnull(df)), None)
    for index, data in df.iterrows():
        if data["generic_name"] == None:
            continue
        if data['side_effects'] == None:
            side_effects = "Please ask your prescribing doctor about any complications"
        else:
            side_effects = data["side_effects"]
        if data['csa'] == '1':
            schedule = 'Schedule 1'
        elif data['csa'] == '2':
            schedule = 'Schedule 2'
        elif data['csa'] == '3':
            schedule = 'Schedule 3'
        elif data['csa'] == '4':
            schedule = 'Schedule 4'
        elif data['csa'] == '5':
            schedule = 'Schedule 5'
        else:
            schedule = "Unscheduled"

        cursor.execute(add_insurance, (data["generic_name"], data['side_effects'], data['drug_classes'], data['medical_condition'], schedule))
    cursor.close()

def generate_workplace(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor()
    workplace_types = ["Pediatric Center", "Psychiatric Center", "Hospital", "Clinic", "Urgent Care Center", "Surgery Center"]
    add_workplace = "INSERT IGNORE INTO Workplace (Address, WName, WType) VALUES (%s, %s, %s)"
    for i in range(101):
        address = f"{random.randint(100, 999)} {names.get_last_name()} St"  # Generating a random address
        cursor.execute(add_workplace, (address, names.get_last_name() + " " + random.choice(["Building", "Center", "Hospital"]), random.choice(workplace_types)))
    cursor.close()

def generate_prescriptions(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor()
    cursor.execute("SELECT SSN, PCare_doctorid FROM Patient WHERE PCare_doctorid IS NOT NULL")  # Filtering out patients with null PCare_doctorid
    patient_data = cursor.fetchall()

    cursor.execute("SELECT Generic_Name, Uses FROM Medication")
    medication_data = cursor.fetchall()
    medication_dict = {name: uses for name, uses in medication_data}
    
    add_prescription = "INSERT INTO Prescribes (SSN, DoctorID, Generic_Name, Date_Prescribed, Reason, Dosage, Expiry) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    
    current_date = datetime.now()
    expiry_date = current_date + timedelta(days=30)  # Assuming prescriptions expire after 30 days

    for ssn, doctor_id in patient_data:
        generic_name = random.choice(list(medication_dict.keys()))
        reason = medication_dict[generic_name]
        date_prescribed = current_date.strftime("%Y-%m-%d %H:%M:%S")
        expiry = expiry_date.strftime("%Y-%m-%d %H:%M:%S")  # Corrected format     
        dosage = round(random.uniform(0.1, 10.0), 2)  # Random decimal dosage between 0.1 and 10.0  
        cursor.execute(add_prescription, (ssn, doctor_id, generic_name, date_prescribed, reason, dosage, expiry))

    cnx.commit()
    cursor.close()

if __name__ == "__main__":
    main()
