from consolemenu import *
from consolemenu.items import *

context = "root_init"

def root_init():
    global context
    menu = ConsoleMenu("MedicalMinds Demo Interface",
                        prologue_text="Welcome to the MedicalMinds"
    " Demo Interface. Select the desired functionality to continue",
                        exit_menu_char='q')
    root_init_database_access = FunctionItem("Initialize Database", input, ['\nEnter Database Password: '],
                                            should_exit=True)

    menu.append_item(root_init_database_access)
    menu.show()
    match (menu.selected_option):
        case 0:
            context = "root_database_init"
            database_password = root_init_database_access.get_return()
            menu.exit()
            return database_password
        case 1:
            context = None

def root_display():
    global context
    menu = ConsoleMenu("MedicalMinds Portal", prologue_text="Welcome to the main portal"
    " of the medical minds demo interface. Please select an appropriate user portal below",
                        exit_menu_char='q')
    doctor_selection = SelectionItem("Doctor Portal", 0)
    patient_selection = SelectionItem("Patient Portal", 1)
    menu.append_item(doctor_selection)
    menu.append_item(patient_selection)
    menu.show()
    match (menu.selected_option):
        case 0:
            context = "doctor_init"
            menu.exit()
        case 1:
            context = "patient_init"
            menu.exit()
        case 2:
            context = None

def doctor_init():
    global context
    menu = ConsoleMenu("Doctor Portal", prologue_text="Welcome to the"
    " doctor portal. Please enter your DoctorID to continue through the available options",
                        exit_menu_char='q')
    doctor_init_verify = FunctionItem("Login", input, ["\nPlease enter your DoctorId: "],
                                        should_exit=True)
    menu.append_item(doctor_init_verify)
    menu.show()
    match (menu.selected_option):
        case 0:
            context = 'doctor_init_verify'
            doctor_id = int(doctor_init_verify.get_return())
            menu.exit()
            return doctor_id
        case 1:
            context = None

def prescribe_input():
    ssn = input("Please Patient SSN: ")
    generic_name = input("Please input the generic name of the medication: ")
    reason = input("Please enter the reason for prescription: ")
    dosage = input("Please input the prescription dosage: ")
    expiry = input("Please enter the expiry of the prescription in YYYY-MM-DD format: ")
    return (ssn, generic_name, reason, dosage, expiry)

def doctor_display(doctor):
    global context
    menu = ConsoleMenu(f"Welcome {doctor[1]} {doctor[2]}", prologue_text=""
    f"Welcome to the medical minds doctor interface {doctor[1]} {doctor[2]}."
    " Here you can view your patients (if you are a primary care physician). View your prescriptions"
    ". And make prescriptions.",
                        exit_menu_char='q')
    view_prescriptions = SelectionItem("View Prescriptions", 0)
    make_prescription = FunctionItem("Make prescription", prescribe_input, should_exit=True)
    menu.append_item(view_prescriptions)
    menu.append_item(make_prescription)
    view_patients = None
    assign_pcare = None
    gp = False
    if (doctor[3] == "General Practitioner"):
        view_patients = SelectionItem("View Patients", 2)
        assign_pcare = FunctionItem("Assign new patient", input, ['Enter the SSN of your new patient: '],
                                    should_exit=True)
        gp = True
        menu.append_item(view_patients)
        menu.append_item(assign_pcare)
    menu.show()
    selected_item = menu.selected_item
    if (selected_item == view_prescriptions):
        context = 'doctor_prescriptions'
        menu.exit()
    elif (selected_item == make_prescription):
        context = 'make_prescriptions'
        menu.exit()
        return make_prescription.get_return()
    elif (gp and (selected_item == view_patients)):
        context = 'doctor_patients'
        menu.exit()
    elif (gp and (selected_item == assign_pcare)):
        context = 'doctor_pcare'
        menu.exit()
        return assign_pcare.get_return()
    else:
        context = 'doctor_init'
        menu.exit()
    
def doctor_prescriptions(doctor, prescriptions):
    global context
    prologue = ""
    for prescription in prescriptions:
        prologue += f"Patient: {prescription[0]} {prescription[1]}\n"
        prologue += f"SSN: {prescription[2]}\n"
        prologue += f"Medication Prescribed: {prescription[3]}\n"
        prologue += f"Date Prescribed: {prescription[4]}\n"
        prologue += f"Reason: {prescription[5]}\n"
        prologue += f"Dosage: {prescription[6]}\n"
        prologue += f"Expiry: {prescription[7]}\n"
        prologue += "------------------\n"
    menu = ConsoleMenu(f"Prescriptions From {doctor[1]} {doctor[2]}", prologue_text=prologue,
                       exit_menu_char="q")
    menu.show()
    context = 'doctor_display'
    menu.exit()

def doctor_patients(doctor, patients):
    global context
    prologue = ""
    if (not patients):
        menu = ConsoleMenu("Assigned Patients", prologue_text="No patients assigned",
                           exit_menu_char='q')
        menu.show()
        context = 'doctor_display'
        menu.exit()
    else:
        for patient in patients:
            prologue += f"Patient Name: {patient[1]} {patient[2]}\n"
            prologue += f"Patient Gender: {patient[3]}\n"
            prologue += f"Patient Age: {patient[4]}\n"
            prologue += f"Patient Height: {patient[5]}\n"
            prologue += f"Patient Weight: {patient[6]}\n"
            prologue += "------------------\n"
        menu = ConsoleMenu("Assigned Patients", prologue_text=prologue,
                           exit_menu_char='q')
        menu.show()
        context = 'doctor_display'
        menu.exit()

def patient_init():
    global context
    menu = ConsoleMenu("Patient Portal", prologue_text="Welcome to the"
    " patient portal. Please enter your SSN to continue through the available options",
                        exit_menu_char='q')
    patient_init_verify = FunctionItem("Login", input, ["\nPlease enter your SSN: "],
                                        should_exit=True)
    menu.append_item(patient_init_verify)
    menu.show()
    match (menu.selected_option):
        case 0:
            context = 'patient_init_verify'
            patient_ssn = int(patient_init_verify.get_return())
            menu.exit()
            return patient_ssn
        case 1:
            context = None

def patient_display(patient):
    global context
    menu = ConsoleMenu(f"Welcome {patient[1]} {patient[2]}", prologue_text=""
    f"Welcome to the medical minds patient interface {patient[1]} {patient[2]}."
    " Here you can view your primary care doctors. Information pertaining to your prescribing doctors."
    " Prescriptions and prescription history. Insurance information. And even pay for a prescription at a"
    " pharmacy of your choice in advance or view your payment history.",
                        exit_menu_char='q')
    view_primary_care = SelectionItem("View primary care", 0)
    view_prescribing_doctors = SelectionItem("View prescribing doctors", 1)
    view_active_prescriptions = SelectionItem("View active prescriptions", 2)
    view_prescription_history = SelectionItem("View prescription history", 3)
    view_insurance = SelectionItem("View insurance information", 4)
    payment_portal = SelectionItem("Access payment portal", 5)
    view_payment_history = SelectionItem("View payment history", 6)
    menu.append_item(view_primary_care)
    menu.append_item(view_prescribing_doctors)
    menu.append_item(view_active_prescriptions)
    menu.append_item(view_prescription_history)
    menu.append_item(view_insurance)
    menu.append_item(payment_portal)
    menu.append_item(view_payment_history)
    menu.show()
    selected_item = menu.selected_item
    if (selected_item == view_primary_care):
        context = 'patient_view_primary_care'
    elif (selected_item == view_prescribing_doctors):
        context = 'patient_view_prescribing_doctors'
    elif (selected_item == view_active_prescriptions):
        context = 'patient_view_active_prescriptions'
    elif (selected_item == view_prescription_history):
        context = 'patient_view_prescription_history'
    elif (selected_item == view_insurance):
        context = 'patient_view_insurance'
    elif (selected_item == payment_portal):
        context = 'patient_payment_portal'
    elif (selected_item == view_payment_history):
        context = 'patient_view_payment_history'
    else:
        context = 'patient_init'
    menu.exit()

def patient_view_primary_care(pcare, workplaces):
    prologue = ""
    if (not pcare):
        prologue += "You have not been assigned a primary care physician"
    else:
        prologue += f"Primary care name: {pcare[1]} {pcare[2]}\n"
        i = 1
        for workplace in workplaces:
            prologue += f"Workplace {i}--\n"
            prologue += f"Address: {workplace[1]}\n"
            prologue += f"Name: {workplace[3]}\n"
            prologue += f"Type: {workplace[4]}\n"
            i += 1
    menu = ConsoleMenu("Primary Care Info", prologue_text=prologue, exit_menu_char='q')
    menu.show()
    menu.exit()
    global context
    context = 'patient_display'

def patient_view_prescribing_doctors(doctors, workplaces):
    prologue = ""
    if (not doctors):
        prologue = "You have not been prescribed any medications"
    else:
        for doctor in doctors:
            prologue += f"Doctor Name: {doctor[1]} {doctor[2]}\n"
            prologue += f"Doctor Type: {doctor[3]}\n"
            i = 1
            for workplace in workplaces[doctor[0]]:
                prologue += f"Workplace {i}--\n"
                prologue += f"Address: {workplace[0]}\n"
                prologue += f"Name: {workplace[1]}\n"
                prologue += f"Type: {workplace[2]}\n"
            prologue += "------------------\n"
    menu = ConsoleMenu("Prescribing Doctors", prologue_text=prologue, exit_menu_char='q')
    menu.show()
    menu.exit()
    global context
    context = 'patient_display'

def patient_view_active_prescriptions(prescriptions):
    prologue = ""
    if (not prescriptions):
        prologue += "No Active prescriptions\n"
    else:
        for prescription in prescriptions:
            prologue += f"Prescribing DoctorID: {prescription[0]}\n"
            prologue += f"Prescribing doctor name: {prescription[1]} {prescription[2]}\n"
            prologue += f"Prescription generic name: {prescription[3]}\n"
            prologue += f"Date prescribed: {prescription[4]}\n"
            prologue += f"Reason prescribed: {prescription[5]}\n"
            prologue += f"Dosage: {prescription[6]}\n"
            prologue += f"Prescription expiry: {prescription[7]}\n"
            prologue += f"Drug side effects: {prescription[8]}\n"
            prologue += f"Drug uses: {prescription[9]}\n"
            prologue += f"Drug classification: {prescription[10]}\n"
            prologue += f"Applications: {prescription[11]}\n"
            prologue += "------------------\n"
    menu = ConsoleMenu("Active Prescriptions", prologue_text=prologue, exit_menu_char="q")
    menu.show()
    menu.exit()
    global context
    context = 'patient_display'

def patient_view_prescription_history(prescriptions):
    prologue = ""
    if (not prescriptions):
        prologue += "No prescriptions found\n"
    else:
        for prescription in prescriptions:
            prologue += f"Prescribing DoctorID: {prescription[0]}\n"
            prologue += f"Generic name: {prescription[1]}\n"
            prologue += f"Date prescribed: {prescription[2]}\n"
            prologue += f"Expiry date: {prescription[3]}\n"
            prologue += f"Dosage: {prescription[4]}\n"
            prologue += "------------------\n"
    menu = ConsoleMenu("Prescription History", prologue_text=prologue, exit_menu_char='q')
    menu.show()
    menu.exit()
    global context
    context = 'patient_display'

def _medication_coverage(insurances, coverage):
    prologue = ""
    for insurance in insurances:
        prologue += f"Insurance name: {insurance[0]}\n"
        prologue += "Medications covered: "
        for medication in coverage[insurance[0]]:
            prologue += f"{medication[0]}, "
        prologue += "\n------------------\n"
    menu = ConsoleMenu("Medications covered", prologue_text=prologue, exit_menu_char='q')
    menu.show()
    menu.exit()

def patient_view_insurance(insurances, coverage):
    prologue = ""
    if (not insurances):
        prologue += "You are not insured\n"
    for insurance in insurances:
        prologue += f"Insurance plan: {insurance[0]}\n"
        prologue += f"Plan deductible left: {insurance[1]}\n"
        prologue += f"Plan initial deductible: {insurance[2]}\n"
        prologue += f"Plan copay: {insurance[3]}\n"
        prologue += f"Plan coinsurance: {insurance[4]}\n"
        prologue += "------------------\n"
    menu = ConsoleMenu("Insurance Information", prologue_text=prologue, exit_menu_char='q')
    show_medication_coverage = SelectionItem("Show medication coverage", 0)
    menu.append_item(show_medication_coverage)
    menu.show()
    menu.exit()
    global context
    if (menu.selected_item == show_medication_coverage):
        _medication_coverage(insurances, coverage)
        context = 'patient_view_insurance'
    else:
        context = 'patient_display'

def patient_payment_portal(active_prescriptions):
    prologue = ""
    if (not active_prescriptions):
        prologue += "No active prescriptions\n"
        menu = ConsoleMenu("Payment Portal", prologue_text=prologue, exit_menu_char='q')
        menu.show()
        menu.exit()
        return
    menu = ConsoleMenu("Payment Portal", prologue_text="Select an active prescription below", exit_menu_char='q')
    option_table = {}
    i = 0
    for prescription in active_prescriptions:
        prescription_option = SelectionItem(prescription[0], i)
        menu.append_item(prescription_option)
        option_table[i] = prescription[0]
        i += 1
    menu.show()
    menu.exit()
    global context
    try:
        context = 'payment_portal_select_pharmacy'
        return option_table[menu.selected_option]
    except:
        context = 'patient_display'
        return

def _pharmacy_input():
    pname = input("Enter a valid pharmacy name: ")
    paddress = input("Enter a valid pharmacy address: ")
    return (pname, paddress)

def payment_portal_select_pharmacy(pharmacies):
    global context
    menu = ConsoleMenu("Select A Pharmacy", prologue_text="Select a given pharmacy below, or input your own valid location", exit_menu_char='q')
    i = 0
    options_table = {}
    for pharmacy in pharmacies:
        label = ""
        label += f"Pharmacy Name: {pharmacy[0]}\n"
        label += f"Pharmacy Address: {pharmacy[1]}\n"
        label += f"Retail Price: {pharmacy[2]}\n"
        pharmacy_select = SelectionItem(label, i)
        options_table[i] = pharmacy
        menu.append_item(pharmacy_select)
        i += 1
    enter_pharmacy = FunctionItem("Pharmacy Input", _pharmacy_input, should_exit=True)
    options_table[i] = "Pharmacy Input"
    menu.append_item(enter_pharmacy)
    menu.show()
    menu.exit()
    try:
        item = options_table[menu.selected_option]
    except:
        item = None
    if (not item):
       context = "patient_display"
       return 
    if (item == "Pharmacy Input"):
        context = "payment_portal_validate_pharmacy_input"
        return enter_pharmacy.get_return()
    else:
        context = 'payment_portal_select_insurance'
        return item

def _make_payment(insurance, pharmacy, payment_prescription_name):
    prologue = ""
    prologue += f"Paid for: {payment_prescription_name}\n"
    prologue += f"At: {pharmacy[0]}\n"
    prologue += f"Addr: {pharmacy[1]}\n"
    prologue += f"At retail price: {pharmacy[2]}\n"
    price = pharmacy[2]
    if (not insurance):
        prologue += "No insurance used\n"
    else:
        prologue += f"Used insurance: {insurance[0]}\n"
        prologue += f"Copay: {insurance[1]}\n"
        if ((insurance[3] - price) > 0):
            prologue += f"Deductible after: {insurance[3] - price}\n"
            prologue += f"Total cost: {price + insurance[1]}\n"
        else:
            prologue += f"Deductible after: 0\n"
            prologue += f"Coinsurance rate: {insurance[2]}\n"
            prologue += f"Total cost: {((price - insurance[3])*insurance[2])+insurance[1]}\n"
    menu = ConsoleMenu("Payment Screen", prologue_text=prologue, exit_menu_char='q')
    menu.show()
    menu.exit()
    return price


def payment_portal_select_insurance(payment_prescription_name, pharmacy, insurances):
    prologue = f"Prescription selected: {payment_prescription_name}\n"
    prologue += f"Pharmacy Selected: {pharmacy[0]}\n"
    prologue += f"Pharmacy Address: {pharmacy[1]}\n"
    prologue += f"Medication Price: {pharmacy[2]}\n"
    prologue += "------------------\n"
    prologue += "Select an insurance (if possible)"
    menu = ConsoleMenu("Insurance Selection", prologue_text=prologue, exit_menu_char='q')
    options_table = {}
    i = 0
    for insurance in insurances:
        label = ""
        label += f"Insurance name: {insurance[0]}\n"
        label += f"Deductible Left: {insurance[3]}\n"
        label += f"Copay: {insurance[1]}\n"
        label += f"Coinsurance: {insurance[2]}\n"
        insurance_selection = SelectionItem(label, i)
        options_table[i] = insurance
        menu.append_item(insurance_selection)
        i += 1
    no_insurance = SelectionItem("Continue Without Insurance", i)
    options_table[i] = "No Insurance"
    menu.append_item(no_insurance)
    menu.show()
    menu.exit()
    global context
    try:
        item = options_table[menu.selected_option]
    except:
        item = None
    if (not item):
        context = 'patient_display'
        return
    if (item == "No Insurance"):
        context = 'patient_display'
        _make_payment(None, pharmacy, payment_prescription_name)
        return (None, pharmacy, payment_prescription_name)
    else:
        context = 'patient_display'
        _make_payment(item, pharmacy, payment_prescription_name)
        return (item, pharmacy, payment_prescription_name)

def patient_view_payment_history(payments):
    prologue = ""
    if (not payments):
        prologue += "No payment history to view\n"
    else:
        for payment in payments:
            prologue += f"Medication Name: {payment[0]}\n"
            if (payment[2]):
                prologue += f"Insurance Plan: {payment[2]}\n"
            prologue += f"Pharmacy Name: {payment[3]}\n"
            prologue += f"Payment ammount: {payment[5]}\n"
            prologue += f"Paid Date: {payment[4]}\n"
            prologue += "------------------\n"
    menu = ConsoleMenu("Payment History", prologue_text=prologue, exit_menu_char='q')
    menu.show()
    menu.exit()
    global context
    context = 'patient_display'