import mysql.connector # mysql library
import pandas as pd
import names # random name generator library https://github.com/treyhunner/names
import random
import numpy as np
import random_address

def main():
    cnx = mysql.connector.connect(user="root", password=input("Enter Password: "), database="MedicalMinds")
    generate_pharmacy(cnx)
    generate_doctor(cnx)
    generate_patient(cnx)
    generate_medication(cnx)
    generate_insurance(cnx)
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
        cursor.execute(add_doctor, (names.get_first_name(), names.get_last_name(), random.choice(doctor_types)))
    cursor.close()
        
def generate_patient(cnx: mysql.connector.MySQLConnection):
    cursor = cnx.cursor()
    gender = ["Male", "Female", "Other", "Undisclosed"]
    ssn = range(111111111, 1000000000)
    age = range(18, 100)
    height = np.arange(152.4, 213.0, step=0.1)
    weight = np.arange(117, 300, step=0.01)
    add_patient = "INSERT IGNORE INTO Patient (SSN, FirstName, LastName, Gender, Age, Height, Weight) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    for i in range(101):
        cursor.execute(add_patient, (random.choice(ssn), names.get_first_name(), names.get_last_name(), random.choice(gender), 
                                    random.choice(age), random.choice(height), random.choice(weight)))
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

        cursor.execute(add_insurance, (data["generic_name"], side_effects, schedule, data['medical_condition'], random.choice(application)))
    cursor.close()

def generate_insurance(cnx: mysql.connector.MySQLConnection):
    #Randomly generated data using a list of real US Health Insurance company names
    #I couldn't find any dataset with the values we wanted - Jacob
    schedule = ""
    cursor = cnx.cursor()
    add_insurance = "INSERT IGNORE INTO Insurance (IName, InitialDeductible, Copay, Coinsurance) VALUES (%s, %s, %s, %s)"
    df = pd.read_csv('insurance_companies.csv')
    df = df.where((pd.notnull(df)), None)
    for index, data in df.iterrows():
        deductible = round(random.uniform(300,1500),2)
        copay = round(random.uniform(15,50),2)
        coinsurance = (str)(random.randint(5,20)) + "%"

        cursor.execute(add_insurance, (data["insurance_company_name"], deductible, copay, coinsurance))
    cursor.close()

if __name__ == "__main__":
    main()
