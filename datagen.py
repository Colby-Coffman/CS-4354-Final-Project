import mysql.connector
import pandas as pd

def main():
    cnx = mysql.connector.connect(user="root", password=input("Enter Password: "), database="MedicalMinds")
    generate_pharmacy(cnx)
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

if __name__ == "__main__":
    main()