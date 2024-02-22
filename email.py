import sqlite3
import pandas as pd
import win32com.client as win32
from datetime import datetime, timedelta

def exceptions_input():
    # Database connection
    dbase = "C:\sqlite\gui\SQLiteStudio\ARO_Identified_Impairments"
    conn = sqlite3.connect(dbase)
    
    # Reading data and exporting to Excel
    ex1_df = pd.read_sql_query("SELECT * FROM NML_ECL_Output", conn)
    ex1_df.to_excel("NML_ECL_Output.xlsx", index=False)
    ex2_df = pd.read_sql_query("SELECT * FROM EXCO_TRANSACTIONS", conn)
    ex2_df.to_excel("EXCO_TRANSACTIONS.xlsx", index=False)
    
    # Closing database connection
    conn.close()
    
    # Sending email for new issue logged
    send_new_issue_email()

    # Reminding the person who logged/opened the case three months before the due date
    remind_three_months_before_due_date()

    # Notifying management one month before the due date
    notify_management_one_month_before_due_date()

def send_new_issue_email():
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    
    mail.Subject = 'New Issue Logged'
    mail.HTMLBody = """
    Dear User,<br><br>
    A new issue has been logged. Please take necessary actions.<br><br>
    Regards,<br>
    Automated Calculator
    """
    
    mail.To = "name.surname@absa.africa"  # Replace with the appropriate email address
    mail.Send()

def remind_three_months_before_due_date():
    # Calculate the due date three months from now
    due_date = datetime.now() + timedelta(days=90)
    
    # TODO: Query database to get the person who logged/opened the case
    #       and send them a reminder email
    
    # Example:
    # person_email = query_person_email()  # Implement query_person_email() function
    # send_reminder_email(person_email, due_date)

def notify_management_one_month_before_due_date():
    # Calculate the due date one month from now
    due_date = datetime.now() + timedelta(days=30)
    
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    
    mail.Subject = 'Action Required: Approaching Due Date'
    mail.HTMLBody = """
    Dear Management,<br><br>
    This is a reminder that certain tasks are due soon. Please ensure they are completed on time.<br><br>
    Regards,<br>
    Automated Calculator
    """
    
    mail.To = "management@absa.africa"  # Replace with the appropriate email address
    mail.Send()

# Call the function
exceptions_input()
