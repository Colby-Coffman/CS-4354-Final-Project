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


if __name__ == "__main__":
    main()