DROP DATABASE IF EXISTS MedicalMinds;
CREATE DATABASE MedicalMinds;
USE MedicalMinds;

CREATE TABLE Doctor (
	DoctorID INT AUTO_INCREMENT PRIMARY KEY,
    DFirstName TEXT,
    DLastName TEXT,
    DType TEXT
);

CREATE TABLE Patient (
	SSN INT(9) PRIMARY KEY,
    FirstName TEXT,
    LastName TEXT,
    Gender TEXT,
    Age INT(3),
    Height INT,
    Weight DECIMAL(5, 2),
    PCare_doctorid INT,
    CONSTRAINT patient_pcare_fk FOREIGN KEY (PCare_doctorid) REFERENCES Doctor (DoctorID)
);

CREATE TABLE Workplace (
	Address VARCHAR(255) PRIMARY KEY,
    WName TEXT,
    WType TEXT
);

CREATE TABLE Insurance (
	IName VARCHAR(255) PRIMARY KEY,
    InitialDeductible DECIMAL,
    Copay DECIMAL,
    Coinsurance DECIMAL(1,2)
);

CREATE TABLE Pharmacy (
	PName VARCHAR(255) PRIMARY KEY,
    PAddress TEXT
);

CREATE TABLE Medication (
	Generic_Name VARCHAR(255) PRIMARY KEY,
    Side_effects TEXT,
    Classification TEXT,
    Uses TEXT,
    Applications TEXT
);

CREATE TABLE Prescribes (
	SSN INT,
    DoctorID INT,
    Generic_Name VARCHAR(255),
    Date_Prescribed DATETIME,
    Reason TEXT,
    Dosage DECIMAL,
    Expiry DATETIME,
    PRIMARY KEY (SSN, DoctorID, Generic_Name, Date_Prescribed),
    CONSTRAINT prescribes_patient_fk FOREIGN KEY (SSN) REFERENCES Patient (SSN),
    CONSTRAINT prescribes_doctor_fk FOREIGN KEY (DoctorID) REFERENCES Doctor (DoctorID),
    CONSTRAINT prescribes_medication_fk FOREIGN KEY (Generic_Name) REFERENCES Medication (Generic_Name)
);

CREATE TABLE Works_at (
	DoctorID INT,
    Address VARCHAR(255),
    PRIMARY KEY (DoctorID, Address),
    CONSTRAINT works_at_doctor_fk FOREIGN KEY (DoctorID) REFERENCES Doctor (DoctorID),
    CONSTRAINT works_at_workplace_fk FOREIGN KEY (Address) REFERENCES Workplace (Address)
);

CREATE TABLE Covered_by (
	SSN INT,
    IName VARCHAR(255),
    DeductibleLeft DECIMAL,
    PRIMARY KEY (SSN, IName),
    CONSTRAINT covered_by_patient_fk FOREIGN KEY (SSN) REFERENCES Patient (SSN),
    CONSTRAINT covered_by_insurance_fk FOREIGN KEY (IName) REFERENCES Insurance (IName)
);

CREATE TABLE Covers (
	Generic_Name VARCHAR(255),
    IName VARCHAR(255),
    PRIMARY KEY (Generic_Name, IName),
    CONSTRAINT covers_medication_fk FOREIGN KEY (Generic_Name) REFERENCES Medication (Generic_Name),
    CONSTRAINT covers_insurance_fk FOREIGN KEY (IName) REFERENCES Insurance (IName)
);

CREATE TABLE Has (
	Generic_Name VARCHAR(255),
    PName VARCHAR(255),
    Retail_price DECIMAL,
    PRIMARY KEY (Generic_Name, PName),
    CONSTRAINT has_medication_pk FOREIGN KEY (Generic_Name) REFERENCES Medication (Generic_Name),
    CONSTRAINT has_pharmacy_pk FOREIGN KEY (PName) REFERENCES Pharmacy (PName)
);

CREATE TABLE Pays_for (
	Generic_Name VARCHAR(255),
    SSN INT,
    IName VARCHAR(255),
    PName VARCHAR(255),
    Paid_Date DATETIME,
    Payment DECIMAL,
    PRIMARY KEY (Generic_Name, SSN, IName, PName, Paid_Date),
    CONSTRAINT pays_for_medication_fk FOREIGN KEY (Generic_Name) REFERENCES Medication (Generic_Name),
    CONSTRAINT pays_for_patient_fk FOREIGN KEY (SSN) REFERENCES Patient (SSN),
    CONSTRAINT pays_for_insurance_fk FOREIGN KEY (IName) REFERENCES Insurance (IName),
    CONSTRAINT pays_for_pharmacy_fk FOREIGN KEY (PName) REFERENCES Pharmacy (PName)
);


