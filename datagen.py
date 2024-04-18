import mysql.connector  # mysql library
import pandas as pd
import names  # random name generator library https://github.com/treyhunner/names
import random
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import decimal
import helpers


def main():
    cnx = mysql.connector.connect(user="root", password=input(
        "Enter Password: "), database="MedicalMinds")
    generate_pharmacy(cnx)
    generate_doctor(cnx)
    generate_patient(cnx)
    generate_medication(cnx)
    generate_insurance(cnx)
    generate_prescriptions(cnx)
    generate_workplace(cnx)
    generate_works_at(cnx)
    generate_covered_by(cnx)
    generate_covers(cnx)
    generate_has(cnx)
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
    cursor = cnx.cursor(buffered=True)
    doctor_types = ["Cardiologist", "Nephrologist", "Dermatologist", "Neurologist", "Psychiatrist", 
                    "Gynecologist", "Gastroenterologist", "Geriatrician", "Nephrologist", "Oncologist", "Endocrinologist",
                    "Hematologist", "Otalaryngologist"]
    add_doctor = "INSERT IGNORE INTO Doctor (DFirstName, DLastName, DType) VALUES (%s, %s, %s)"
    doctor_type = None
    for i in range(101):
        if (i < 40):
            doctor_type = "General Practitioner"
        else:
            doctor_type = random.choice(doctor_types)
        cursor.execute(add_doctor, (names.get_first_name(), names.get_last_name(), doctor_type))
    cursor.close()


def generate_patient(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    gender = ["Male", "Female", "Other", "Undisclosed"]
    age = range(18, 100)
    height = np.arange(152.4, 213.0, step=0.1)
    weight = np.arange(117, 300, step=0.01)
    add_patient = "INSERT IGNORE INTO Patient (SSN, FirstName, LastName, Gender, Age, Height, Weight, PCare_doctorid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute("SELECT DoctorID FROM Doctor WHERE DType='General Practitioner'")
    doctor_ids = [row[0] for row in cursor.fetchall()]  # Fetch all DoctorIDs from the Doctor table
    for i in range(101):
        ssn = random.randint(111111111, 999999999)  # Generate a random SSN
        first_name = names.get_first_name()
        last_name = names.get_last_name()
        gender_choice = random.choice(gender)
        patient_age = random.choice(age)
        patient_height = random.choice(height)
        patient_weight = random.choice(weight)
        doctor_id = None
        if (i <= 40):
            doctor_id = random.choice(doctor_ids)
        cursor.execute(add_patient, (ssn, first_name, last_name, gender_choice, patient_age, patient_height, patient_weight, doctor_id))
    cursor.close()



def generate_medication(cnx: mysql.connector.MySQLConnection):
    # Uses data from: https://www.kaggle.com/datasets/jithinanievarghese/drugs-side-effects-and-medical-condition
    cursor = cnx.cursor(buffered=True)
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

        cursor.execute(add_insurance, (data["generic_name"], side_effects, schedule, data['medical_condition'], random.choice(application)))
    cursor.close()

def generate_insurance(cnx: mysql.connector.MySQLConnection):
    #Randomly generated data using a list of real US Health Insurance company names
    #I couldn't find any dataset with the values we wanted - Jacob
    cursor = cnx.cursor(buffered=True)
    add_insurance = "INSERT IGNORE INTO Insurance (IName, InitialDeductible, Copay, Coinsurance) VALUES (%s, %s, %s, %s)"
    df = pd.read_csv('insurance_companies.csv')
    df = df.where((pd.notnull(df)), None)
    for index, data in df.iterrows():
            for plans in range(random.randint(1,3)):
                for plan in range(plans):
                    plan_name = ""
                    match (plan):
                        case 0:
                            plan_name = f"{data['insurance_company_name']}:Plan A"
                        case 1:
                            plan_name = f"{data['insurance_company_name']}:Plan B"
                        case 2:
                            plan_name = f"{data['insurance_company_name']}:Plan C"
                    deductible = int(random.choice(np.arange(300,1501, 1)))
                    copay = int(random.choice(np.arange(15,51, 1)))
                    coinsurance = float(random.choice(np.arange(0.0, 0.6, 0.01)))
                    cursor.execute(add_insurance, (plan_name, deductible, copay, coinsurance))

def generate_workplace(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    workplace_types = ["Pediatric Center", "Psychiatric Center", "Hospital", "Clinic", "Urgent Care Center", "Surgery Center"]
    add_workplace = "INSERT IGNORE INTO Workplace (Address, WName, WType) VALUES (%s, %s, %s)"
    for i in range(101):
        address = f"{random.randint(100, 999)} {names.get_last_name()} St"  # Generating a random address
        cursor.execute(add_workplace, (address, names.get_last_name() + " " + random.choice(["Building", "Center", "Hospital"]), random.choice(workplace_types)))
    cursor.close()

def generate_prescriptions(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    add_prescription = "INSERT IGNORE INTO Prescribes (SSN, DoctorID, Generic_Name, Date_Prescribed, Reason, Dosage, Expiry) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute("SELECT pa.SSN FROM Patient pa LEFT JOIN Prescribes pr ON pa.SSN=pr.SSN WHERE pr.SSN IS NULL")
    excluded_patients = cursor.fetchall()
    cursor.execute("SELECT d.DoctorID FROM Doctor d LEFT JOIN Prescribes pr ON d.DoctorID=pr.DoctorID WHERE pr.DoctorID IS NULL")
    excluded_doctors = cursor.fetchall()
    cursor.execute("SELECT m.Generic_Name, m.Uses FROM Medication m LEFT JOIN Prescribes pr ON m.Generic_Name=pr.Generic_Name WHERE pr.Generic_Name IS NULL")
    excluded_medications = cursor.fetchall()
    while ((excluded_patients) and (excluded_doctors) and (excluded_medications)):
        patients_selection = random.randint(1,3)
        if (patients_selection > len(excluded_patients)):
            patients_selection = len(excluded_patients)
        doctors_selection = random.randint(1,3)
        if (doctors_selection > len(excluded_doctors)):
            doctors_selection = len(excluded_doctors)
        medications_selection = random.randint(1,3)
        if (medications_selection > len(excluded_medications)):
            medications_selection = len(excluded_medications)
        for i in range(patients_selection):
            for j in range(doctors_selection):
                for k in range(medications_selection):
                    date_prescribed, expiry, dosage = helpers.random_expiry_and_dosage()
                    cursor.execute(add_prescription, (excluded_patients[i][0], excluded_doctors[j][0], excluded_medications[k][0],
                                                      date_prescribed, excluded_medications[k][1], dosage, expiry))
        cursor.execute("SELECT pa.SSN FROM Patient pa LEFT JOIN Prescribes pr ON pa.SSN=pr.SSN WHERE pr.SSN IS NULL")
        excluded_patients = cursor.fetchall()
        cursor.execute("SELECT d.DoctorID FROM Doctor d LEFT JOIN Prescribes pr ON d.DoctorID=pr.DoctorID WHERE pr.DoctorID IS NULL")
        excluded_doctors = cursor.fetchall()
        cursor.execute("SELECT m.Generic_Name, m.Uses FROM Medication m LEFT JOIN Prescribes pr ON m.Generic_Name=pr.Generic_Name WHERE pr.Generic_Name IS NULL")
        excluded_medications = cursor.fetchall()
    if (excluded_patients):
        for patient in excluded_patients:
            cursor.execute("SELECT DoctorID, Generic_Name FROM Prescribes")
            doctor_id, generic_name = cursor.fetchmany(1)[0]
            cursor.execute(f"SELECT Uses FROM Medication WHERE Generic_Name='{generic_name}'")
            usage = cursor.fetchmany(1)[0][0]
            date_prescribed, expiry, dosage = helpers.random_expiry_and_dosage()
            cursor.execute(add_prescription, (patient[0], doctor_id, generic_name, date_prescribed, usage, dosage, expiry))
    if (excluded_doctors):
        for doctor in excluded_doctors:
            cursor.execute("SELECT SSN, Generic_Name FROM Prescribes ORDER BY Generic_Name DESC")
            ssn, generic_name = cursor.fetchmany(1)[0]
            cursor.execute(f"SELECT Uses FROM Medication WHERE Generic_Name='{generic_name}'")
            usage = cursor.fetchmany(1)[0][0]
            date_prescribed, expiry, dosage = helpers.random_expiry_and_dosage()
            cursor.execute(add_prescription, (ssn, doctor[0], generic_name, date_prescribed, usage, dosage, expiry))
    
def generate_works_at(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    add_works_at = "INSERT IGNORE INTO Works_at (DoctorID, Address) VALUES (%s, %s)"
    cursor.execute("SELECT d.DoctorID FROM Doctor d LEFT JOIN Works_at w ON d.DoctorID=w.DoctorID WHERE w.DoctorID IS NULL")
    excluded_doctors = cursor.fetchall()
    cursor.execute("SELECT wp.Address FROM Workplace wp LEFT JOIN Works_at w ON wp.Address=w.Address WHERE w.Address IS NULL")
    excluded_workplaces = cursor.fetchall()
    while (excluded_doctors and excluded_workplaces):
        workplace_selection = random.randint(1,2)
        if (workplace_selection > len(excluded_workplaces)):
            workplace_selection = len(excluded_workplaces)
        doctors_selection = random.randint(1,2)
        if (doctors_selection > len(excluded_doctors)):
            doctors_selection = len(excluded_doctors)
        for i in range(workplace_selection):
            for j in range(doctors_selection):
                cursor.execute(add_works_at, (excluded_doctors[j][0], excluded_workplaces[i][0]))
        cursor.execute("SELECT d.DoctorID FROM Doctor d LEFT JOIN Works_at w ON d.DoctorID=w.DoctorID WHERE w.DoctorID IS NULL")
        excluded_doctors = cursor.fetchall()
        cursor.execute("SELECT wp.Address FROM Workplace wp LEFT JOIN Works_at w ON wp.Address=w.Address WHERE w.Address IS NULL")
        excluded_workplaces = cursor.fetchall()
    if (excluded_doctors):
        for doctor in excluded_doctors:
            cursor.execute("SELECT Address FROM Works_at")
            address = cursor.fetchmany(1)[0][0]
            cursor.execute(add_works_at, (address, doctor[0]))
    if (excluded_workplaces):
        for workplace in excluded_workplaces:
            cursor.execute("SELECT DoctorID FROM Works_at ORDER BY DoctorID DESC")
            doctor_id = cursor.fetchmany(1)[0][0]
            cursor.execute(add_works_at, (workplace[0], doctor_id))        
    cursor.close()

def generate_covered_by(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    add_covered_by = "INSERT IGNORE INTO Covered_by (SSN, IName, DeductibleLeft) VALUES (%s, %s, %s)"
    cursor.execute("SELECT p.SSN FROM Patient p LEFT JOIN Covered_by c ON p.SSN=c.SSN WHERE c.SSN IS NULL")
    excluded_patients = cursor.fetchall()
    cursor.execute("SELECT i.IName, i.InitialDeductible FROM Insurance i LEFT JOIN Covered_by c ON i.IName=c.IName WHERE c.IName IS NULL")
    excluded_insurances = cursor.fetchall()
    while (excluded_patients and excluded_insurances):
        patient_selection = random.randint(1,2)
        if (patient_selection > len(excluded_patients)):
            patient_selection = len(excluded_patients)
        insurance_selection = random.randint(1,2)
        if (insurance_selection > len(excluded_insurances)):
            insurance_selection = len(excluded_insurances)
        for i in range(patient_selection):
            for j in range(insurance_selection):
                cursor.execute(add_covered_by, (excluded_patients[i][0], excluded_insurances[j][0], excluded_insurances[j][1]))
        cursor.execute("SELECT p.SSN FROM Patient p LEFT JOIN Covered_by c ON p.SSN=c.SSN WHERE c.SSN IS NULL")
        excluded_patients = cursor.fetchall()
        cursor.execute("SELECT i.IName, i.InitialDeductible FROM Insurance i LEFT JOIN Covered_by c ON i.IName=c.IName WHERE c.IName IS NULL")
        excluded_insurances = cursor.fetchall()
    if (excluded_patients):
        for patient in excluded_patients:
            cursor.execute("SELECT IName FROM Covered_by")
            insurance_name = cursor.fetchmany(1)[0][0]
            cursor.execute(f"SELECT InitialDeductible FROM Insurance WHERE IName='{insurance_name}'")
            initial_deductible = cursor.fetchmany(1)[0][0]
            cursor.execute(add_covered_by, (patient[0], insurance_name, initial_deductible))
    if (excluded_insurances):
        for insurance in excluded_insurances:
            cursor.execute("SELECT SSN FROM Covered_by ORDER BY SSN Desc")
            ssn = cursor.fetchmany(1)[0][0]
            cursor.execute(add_covered_by, (ssn, insurance[0], insurance[1]))
    
def generate_covers(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    add_covers = "INSERT IGNORE INTO Covers (Generic_Name, IName) VALUES (%s, %s)"
    cursor.execute("SELECT m.Generic_Name FROM Medication m LEFT JOIN Covers c ON m.Generic_Name=c.Generic_Name WHERE c.Generic_Name IS NULL")
    excluded_medications = cursor.fetchall()
    cursor.execute("SELECT i.IName FROM Insurance i LEFT JOIN Covers c ON i.IName=c.IName WHERE c.IName IS NULL")
    excluded_insurances = cursor.fetchall()
    while (excluded_medications and excluded_insurances):
        medication_selection = random.randint(30, 50)
        if (medication_selection > len(excluded_medications)):
            medication_selection = len(excluded_medications)
        insurance_selection = random.randint(1,2)
        if (insurance_selection > len(excluded_insurances)):
            insurance_selection = len(excluded_insurances)
        for i in range(medication_selection):
            for j in range(insurance_selection):
                cursor.execute(add_covers, (excluded_medications[i][0], excluded_insurances[j][0]))
        cursor.execute("SELECT m.Generic_Name FROM Medication m LEFT JOIN Covers c ON m.Generic_Name=c.Generic_Name WHERE c.Generic_Name IS NULL")
        excluded_medications = cursor.fetchall()
        cursor.execute("SELECT i.IName FROM Insurance i LEFT JOIN Covers c ON i.IName=c.IName WHERE c.IName IS NULL")
        excluded_insurances = cursor.fetchall()
    if (excluded_insurances):
        for insurance in excluded_insurances:
            cursor.execute("SELECT Generic_Name FROM Covers")
            generic_name = cursor.fetchmany(1)[0][0]
            cursor.execute(add_covers, (generic_name, insurance[0]))

def generate_has(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor(buffered=True)
    add_has = "INSERT IGNORE INTO Has (Generic_Name, PName, Retail_price) VALUES (%s, %s, %s)"
    cursor.execute("SELECT m.Generic_Name FROM Medication m LEFT JOIN Has h ON h.Generic_Name=m.Generic_Name WHERE h.Generic_Name IS NULL")
    excluded_medications = cursor.fetchall()
    cursor.execute("SELECT p.PName FROM Pharmacy p LEFT JOIN Has h ON h.PName=h.PName WHERE h.PName IS NULL")
    excluded_pharmacies = cursor.fetchall()
    while (excluded_medications and excluded_pharmacies):
        medication_selection = random.randint(100, 200)
        if (medication_selection > len(excluded_medications)):
            medication_selection = len(excluded_medications)
        pharmacy_selection = random.randint(30, 40)
        if (pharmacy_selection > len(excluded_pharmacies)):
            pharmacy_selection = len(excluded_pharmacies)
        for i in range(medication_selection):
            for j in range(pharmacy_selection):
                retail_price = random.choice(np.arange(5, 300, 0.01))
                cursor.execute(add_has, (excluded_medications[i][0], excluded_pharmacies[j][0], retail_price))
        cursor.execute("SELECT m.Generic_Name FROM Medication m LEFT JOIN Has h ON h.Generic_Name=m.Generic_Name WHERE h.Generic_Name IS NULL")
        excluded_medications = cursor.fetchall()
        cursor.execute("SELECT p.PName FROM Pharmacy p LEFT JOIN Has h ON h.PName=p.PName WHERE h.PName IS NULL")
        excluded_pharmacies = cursor.fetchall()
    if (excluded_pharmacies):
        for pharmacy in excluded_pharmacies:
            cursor.execute("SELECT Generic_Name, Retail_price FROM Has")
            generic_name, retail_price = cursor.fetchone(1)[0]
            cursor.execute(add_has, (generic_name, pharmacy[0], retail_price))

if __name__ == "__main__":
    main()
