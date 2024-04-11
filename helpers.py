import random
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

def random_expiry_and_dosage():
    current_date = datetime.datetime.now()
    year_or_month = random.randint(0,1)
    match (year_or_month):
        case 0:
            expiry_date = current_date + relativedelta(years=1)
        case 1:
            expiry_date = current_date + relativedelta(months=6)
    date_prescribed = current_date.strftime("%Y-%m-%d %H:%M:%S")
    expiry = expiry_date.strftime("%Y-%m-%d %H:%M:%S")  # Corrected format     
    dosage = random.choice(np.arange(0.1, 10.05, 0.05)) # Random decimal dosage between 0.1 and 10.0
    return (date_prescribed, expiry, dosage)
