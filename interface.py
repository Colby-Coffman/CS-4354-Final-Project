import context as ct
import mysql.connector
import time
import datetime
import re

cnx: mysql.connector.connection.MySQLConnection = None
database_password = None
doctor = None
doctor_id = None
prescription = None
new_patient = None
patient_ssn = None
patient = None
payment_prescription_name = None
pharmacy_name = None
pharmacy_address = None

def main():
    while (True):
        context_output() # state machine loop
        if not ct.context:
            if cnx:
                cnx.commit()
                cnx.close()
            break

def context_output():
    global cnx
    match (ct.context):
        case "root_init":
            res = ct.root_init()
            if (res):
                global database_password
                database_password = res
        case "root_database_init":
            try:
                cnx = mysql.connector.connect(user="root", password=database_password,
                                            database="MedicalMinds")
                ct.context = 'root_display'
            except:
                print("Initialization failed!")
                time.sleep(1)
                ct.context = 'root_init'
        case 'root_display':
            ct.root_display()
        case 'doctor_init':
            res = ct.doctor_init()
            if (res):
                global doctor_id
                doctor_id = res
        case 'doctor_init_verify':
            global doctor
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM Doctor WHERE DoctorID={doctor_id}")
            doctor = cursor.fetchall()
            if (not doctor):
                print("Initialization failed!")
                time.sleep(1)
                ct.context = 'doctor_init'
            else:
                doctor = doctor[0]
                ct.context = 'doctor_display'
            cursor.close()
        case 'doctor_display':
            res = ct.doctor_display(doctor)
            if (res):
                if (type(res) == tuple):
                    global prescription
                    prescription = res
                else:
                    global new_patient
                    new_patient = res
        case 'doctor_prescriptions':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM Prescribes WHERE DoctorID={doctor_id}")
            prescriptions = cursor.fetchall()
            prescription_list = []
            for prescription_i in prescriptions:
                cursor.execute(f"SELECT FirstName, LastName FROM Patient WHERE SSN={prescription_i[0]}")
                first_name, last_name = cursor.fetchone()
                prescription_list.append((first_name, last_name, prescription_i[0], prescription_i[2],
                                          prescription_i[3], prescription_i[4], prescription_i[5],
                                          prescription_i[6]))
            ct.doctor_prescriptions(doctor, prescription_list)
            cursor.close()
        case 'make_prescriptions':
            cursor = cnx.cursor(buffered=True)
            try:
                cursor.execute(f"SELECT * FROM Patient WHERE SSN={prescription[0]}")
                valid_ssn = cursor.fetchone()
            except:
                valid_ssn = None
            try:
                cursor.execute(f"SELECT * FROM Medication WHERE Generic_Name='{prescription[1]}'")
                valid_generic = cursor.fetchone()
            except:
                valid_generic = None
            valid_expiry = None
            if (re.match('\d{4}-\d{2}-\d{2}', prescription[4])):
                valid_expiry = datetime.datetime.now().date()
                valid_expiry = True if str(valid_expiry) < prescription[4] else None
            if ((not valid_ssn) or (not valid_generic) or (not valid_expiry)):
                print("Initialization Failed!")
                time.sleep(1)
            else:
                add_prescription = "INSERT IGNORE INTO Prescribes (SSN, DoctorID, Generic_Name, Date_Prescribed, Reason, Dosage, Expiry) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                current_date = datetime.datetime.now()
                expiry = datetime.datetime.strptime(prescription[4], "%Y-%m-%d")
                expiry = expiry.replace(hour=current_date.hour, minute=current_date.minute, second=current_date.second)
                current_date = current_date.strftime("%Y-%m-%d %H:%M:%S")
                expiry = expiry.strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(add_prescription, (prescription[0], doctor_id, prescription[1],
                                                  current_date, prescription[2], prescription[3], expiry))
                cnx.commit()
            ct.context = 'doctor_display'
            cursor.close()
        case 'doctor_patients':
            cursor = cnx.cursor()
            cursor.execute(f"SELECT * FROM Patient WHERE PCare_doctorid={doctor_id}")
            patients = cursor.fetchall()
            ct.doctor_patients(doctor, patients)
            cursor.close()
        case 'doctor_pcare':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM Patient WHERE SSN={new_patient}")
            valid_patient = cursor.fetchone()
            if (not valid_patient):
                print("Initialization Failed!")
                time.sleep(1)
            else:
                try:
                    cursor.execute(f"UPDATE IGNORE Patient SET PCare_doctorid={doctor_id}"
                                    f" WHERE SSN={new_patient}")
                    cnx.commit()
                except:
                    print("Initialization Failed!")
                    time.sleep(1)
            cursor.close()
            ct.context = 'doctor_display'
        case 'patient_init':
            res = ct.patient_init()
            if (res):
                global patient_ssn
                patient_ssn = res
        case 'patient_init_verify':
            global patient
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM Patient WHERE SSN={patient_ssn}")
            patient = cursor.fetchall()
            if (not patient):
                print("Initialization failed!")
                time.sleep(1)
                ct.context = 'patient_init'
            else:
                patient = patient[0]
                ct.context = 'patient_display'
            cursor.close()
        case 'patient_display':
            ct.patient_display(patient)
        case 'patient_view_primary_care':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT PCare_doctorid FROM Patient WHERE SSN={patient_ssn}")
            new_pcare = cursor.fetchone()
            if (new_pcare):
                global patient
                new_patient_ssn = patient[0]
                new_patient_fname = patient[1]
                new_patient_lname = patient[2]
                new_patient_gender = patient[3]
                new_patient_age = patient[4]
                new_patient_height = patient[5]
                new_patient_weight = patient[6]
                patient = (new_patient_ssn, new_patient_fname, new_patient_lname, new_patient_gender, new_patient_age, new_patient_height, new_patient_weight, new_pcare[0])
            workplaces = None
            try:
                cursor.execute(f"SELECT * FROM Doctor WHERE DoctorID={patient[7]}")
                pcare = cursor.fetchone()
            except:
                pcare = None
            if (pcare):
                cursor.execute(f"SELECT * FROM Works_at wa INNER JOIN Workplace w ON wa.Address=w.Address WHERE DoctorID={pcare[0]}")
                workplaces = cursor.fetchall()
            ct.patient_view_primary_care(pcare, workplaces)
            cursor.close()
        case 'patient_view_prescribing_doctors':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT DISTINCT d.DoctorID, d.DFirstName, d.DLastName, d.DType FROM Prescribes p INNER JOIN"
                           f" Doctor d ON p.DoctorID=d.DoctorID WHERE p.SSN={patient_ssn}")
            doctors = cursor.fetchall()
            workplaces = None
            if (doctors):
                workplaces = {}
                for doctor in doctors:
                    cursor.execute(f"SELECT w.Address, w.WName, w.WType FROM Works_at wa INNER JOIN Workplace w ON"
                                   f" w.Address=wa.Address WHERE wa.DoctorID={doctor[0]}")
                    workplaces[doctor[0]] = cursor.fetchall()
            ct.patient_view_prescribing_doctors(doctors, workplaces)
            cursor.close()
        case 'patient_view_active_prescriptions':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT DISTINCT p.DoctorID, d.DFirstName, d.DLastName, p.Generic_Name, p.Date_Prescribed, p.Reason, p.Dosage, p.Expiry, m.Side_effects, m.Uses, m.Classification, m.Applications"
                           f" FROM Medication m INNER JOIN (Doctor d INNER JOIN Prescribes p ON p.DoctorID=d.DoctorID) ON m.Generic_Name=p.Generic_Name"
                           f" WHERE p.SSN={patient_ssn} AND p.Expiry>NOW()")
            prescriptions = cursor.fetchall()
            ct.patient_view_active_prescriptions(prescriptions)
            cursor.close()
        case 'patient_view_prescription_history':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT DISTINCT p.DoctorID, p.Generic_Name, p.Date_Prescribed, p.Expiry, p.Dosage"
                           f" FROM Prescribes p WHERE p.SSN={patient_ssn}")
            prescriptions = cursor.fetchall()
            ct.patient_view_prescription_history(prescriptions)
            cursor.close()
        case 'patient_view_insurance':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT cb.IName, cb.DeductibleLeft, i.InitialDeductible, i.Copay, i.Coinsurance"
                           f" FROM Covered_by cb INNER JOIN Insurance i ON cb.IName=i.IName"
                           f" WHERE cb.SSN={patient_ssn}")
            insurances = cursor.fetchall()
            coverage = None
            if (insurances):
                coverage = {}
                for insurance in insurances:
                    cursor.execute(f"SELECT Generic_Name FROM Covers WHERE IName='{insurance[0]}'")
                    coverage[insurance[0]] = cursor.fetchall()
            ct.patient_view_insurance(insurances, coverage)
            cursor.close()
        case 'patient_payment_portal':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT p.Generic_Name FROM Prescribes p WHERE p.SSN={patient_ssn} AND p.Expiry>NOW()")
            active_prescriptions = cursor.fetchall()
            res = ct.patient_payment_portal(active_prescriptions)
            if (res):
                global payment_prescription_name
                payment_prescription_name = res
            cursor.close()
        case 'payment_portal_select_pharmacy':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT p.PName, p.PAddress, h.Retail_price FROM Pharmacy p INNER JOIN Has h ON p.PName=h.PName WHERE h.Generic_Name='{payment_prescription_name}' ORDER BY h.Retail_price")
            pharmacies = cursor.fetchmany(5)
            res = ct.payment_portal_select_pharmacy(pharmacies)
            if (res):
                global pharmacy_name, pharmacy_address
                pharmacy_name = res[0]
                pharmacy_address = res[1]
            cursor.close()
        case 'payment_portal_validate_pharmacy_input':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM Pharmacy WHERE PName='{pharmacy_name}' AND PAddress='{pharmacy_address}'")
            pharmacies = cursor.fetchall()
            if (not pharmacies):
                print("Initialization Failed!")
                time.sleep(1)
                ct.context = 'patient_display'
            else:
                ct.context = 'payment_portal_select_insurance'
            cursor.close()
        case 'payment_portal_select_insurance':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT p.PName, p.PAddress, h.Retail_price FROM Pharmacy p INNER JOIN Has h ON p.PName=h.PName WHERE p.PName='{pharmacy_name}' AND p.PAddress='{pharmacy_address}' AND h.Generic_Name='{payment_prescription_name}'")
            pharmacy = cursor.fetchone()
            cursor.execute(f"SELECT i.IName, i.Copay, i.Coinsurance, cb.DeductibleLeft FROM Covered_by cb INNER JOIN (Insurance i INNER JOIN Covers c ON i.IName=c.IName) ON cb.IName=i.IName WHERE cb.SSN={patient_ssn} AND c.Generic_Name='{payment_prescription_name}'")
            insurances = cursor.fetchall()
            res = ct.payment_portal_select_insurance(payment_prescription_name, pharmacy, insurances)
            if (res):
                add_pays_for = "INSERT IGNORE INTO Pays_for (Generic_Name, SSN, IName, PName, Paid_Date, Payment) VALUES (%s, %s, %s, %s, %s, %s)"
                if (not res[0]):
                    cursor.execute(add_pays_for, (payment_prescription_name, patient_ssn, None, pharmacy[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pharmacy[2]))
                else:
                    if ((res[0][3] - pharmacy[2]) > 0):
                        cursor.execute(f"UPDATE Covered_by SET DeductibleLeft={res[0][3] - pharmacy[2]} WHERE SSN={patient_ssn} AND IName='{res[0][0]}'")
                        cursor.execute(add_pays_for, (payment_prescription_name, patient_ssn, res[0][0], pharmacy[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), pharmacy[2] + res[0][1]))
                    else:
                        cursor.execute(f"UPDATE Covered_by SET DeductibleLeft=0 WHERE SSN={patient_ssn} AND IName='{res[0][0]}'")
                        cursor.execute(add_pays_for, (payment_prescription_name, patient_ssn, res[0][0], pharmacy[0], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ((pharmacy[2] - res[0][3])*res[0][2])+res[0][1]))
                cnx.commit()
            cursor.close()
        case 'patient_view_payment_history':
            cursor = cnx.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM Pays_for WHERE SSN={patient_ssn} ORDER BY Paid_date")
            payments = cursor.fetchall()
            ct.patient_view_payment_history(payments)
            cursor.close()

if __name__ == "__main__":
    main()