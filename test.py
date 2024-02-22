import streamlit as st
import sqlite3
from hashlib import sha256
import pandas as pd
import random 
import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

##PosGreSQL
params = {
    "host": "localhost",
    "user": "postgres",
    "port": 5432,
    "password": "Mkw@naz1" 
}
connection = psycopg2.connect(**params, dbname= "ICP_db")
    

CURSOR=connection.cursor()

# # Function to create a SQLite database connection
# def create_connection():
#     conn = sqlite3.connect("issues20240202.db")
#     return conn


# function to view current issues
def view_all_issues():
    CURSOR.execute('SELECT * FROM  issues2024')
    data = CURSOR.fetchall()
    return data


# function to view current issues status
def view_all_issues_status():
    CURSOR.execute('SELECT issue_status FROM  issues2024')
    data = CURSOR.fetchall()
    return data

df_status=pd.DataFrame(view_all_issues_status(),columns=['Issue_Status'])
# Function to create a table for  new user
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Function to sign up a new user
def signup(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = password
    cursor.execute("INSERT INTO  users  (username, password) VALUES (?,?)", (username, hashed_password))

    conn.commit()
    conn.close()

#
# Function to execute SQL queries
def execute_query(query):
    CURSOR.execute(query)
    connection.commit()
# Function to log in a user
def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = password
    cursor.execute("SELECT * FROM  users  WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()
    return user

#Custom Streamlit theme
def set_custom_theme():
    st.markdown(
        """
        <style>
            body {
                background-color: red; /* Change theme background color to red */
                color: #f0f2f6; /* Set text color to a light shade for readability */
            }
            .element-container img {
                max-width: 80%; /* Resize logo image to appear smaller */
            }
            .title-centered {
                text-align: center; /* Align title to the center */
            }
        </style>
        """,
        unsafe_allow_html=True
    )

# Streamlit app layout with custom theme
set_custom_theme()
# st.title("Issue Tracker App")
st.image("absa1502.jpg", use_column_width=True)  # Add company logo


# # Function to create the issues table
# def create_table():
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS issues (
#             id Serial PRIMARY KEY,
#             issue_code VARCHAR(255) UNIQUE,
#             issue_name VARCHAR(255),
#             description TEXT,
#             issue_status VARCHAR(50),
#             risk_type VARCHAR(50),
#             subrisk_type VARCHAR(50),
#             entities VARCHAR(255),
#             bu_rating VARCHAR(50),
#             agl_rating VARCHAR(50),
#             assurance_provider VARCHAR(255),
#             due_date DATE,
#             financially_implicated BOOLEAN,
#             risk_event_type VARCHAR(255),
#             additional_evidence TEXT,
#             file_contents VARCHAR(255),
#             issuer_name VARCHAR(255),
#             issuer_surname VARCHAR(255),
#             issuer_email VARCHAR(255),
#             usernam Varchar(255)      
#         )
#     ''')

#     conn.commit()
#     conn.close()
# Functions to fetch issue code and generate new code from the database start here
def generate_unique_code():
    while True:
        # Generate a random four-digit code
        code = str(random.randint(1000, 9999))

        # Check if the code is unique in the database
        if not is_code_exists(code):
            return code
 
def is_code_exists(code):
    #Check if the code exists in the 'issues' table
    CURSOR.execute("SELECT COUNT(*) FROM issues2024 WHERE issue_code = %s", (code,))
    count = CURSOR.fetchone()[0]
    return count > 0
    

#Function end here :)
    
# Streamlit UI
def main():
    
    st.title("Issue Tracker App")

    # Sidebar
    page = st.sidebar.radio("Navigation", ["Login", "View Current Issues", "Log Issue", "Update Issue"])
    if page=='View Current Issues':
       
        # Retrieve column names
        CURSOR.execute("select * from issues2024 LIMIT 1") 
        row=CURSOR.fetchone()
        # Extract column names from cursor description
        columns = [description[0] for description in CURSOR.description]
        
        df=pd.DataFrame(view_all_issues(),columns=columns)#['ID','issue_code','review_name', 'issue_name', 'description', 'issue_status','risk_type','entities','subrisk_type', 'bu_rating','agl_rating', 'due_date','assurance_provider','financially_implicated','view_option','fraud_element','amount_zar','issue_owner_name','issue_owner_surname', 'issue_owner_email','username'])
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.table(df_fil)
        else:
            st.table(df.tail(5))
            csv_data = df.to_csv(index=False).encode()
            st.download_button(label="Download CSV", data=csv_data, file_name='Issues.csv', mime='text/csv')


        #st.write(view_all_issues())
    # if page == "Signup":s
    #     st.header("Signup")
    #     username = st.text_input("Username")
    #     password = st.text_input("Password", type="password")
    #     if st.button("Signup"):
    #         signup(username, password)
    #         st.success("Signup successful! Now you can log in.")

    if page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.username = username  # Store username in session state
                st.success(f"Welcome, {user[1]}!")
            else:
                st.error("Invalid username or password.")

    elif page == "Log Issue":
        st.header("Log Issue")
        if st.session_state.get('username'):
            # Generate 4 random numbers
            random_numbers = [random.randint(1, 100) for _ in range(4)]
            issue_code = random.randint(1000, 9999) #st.text_input("Issue Code (4 characters)")
            review_name = st.text_area("Review Name")
            issue_name = st.text_input("Issue Name")
            description = st.text_area("Description")
            issue_status =st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
            risk_type = st.selectbox("Risk Type", ["Operational & Resilience Risk", "Insurance risk type", "Compliance Risk", "Model Risk", "Conduct Risk"])
            subrisk_type = st.selectbox("Subrisk Type", ["Model Uncertainty Risk", "Process Management Risk", "Supplier Risk", "Technology Risk", "Transaction Processing and Management Risk", "Underwriting Risk", "Anti-Money Laundering", "Business Continuity Risk", "Change Risk", "Conduct Risk", "Customer Engagement Risk", "Data and Records Management Risk", "Fraud Risk", "Information Security and Cyber Risk", "Insurance Exposure Risk"])
            entities = st.selectbox("Entity Name", ["FAK", "ALAK", "LIFE SA", "ALB", "ALZ", "NBFS: SPM", "NBFS: WILLS TRUST AND ESTATES", "NBFS: AIFA", "AIC", "GAM"])
            bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate", "Critical"])
            agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate", "Critical"])
            assurance_provider = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit", "Internal Audit", "GSA"])
            due_date = st.date_input("Due Date")
            financially_implicated_help = "Select 'Yes' if the issue has a financial implication, otherwise select 'No'."
            financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])

            if financially_implicated == "Yes":
                view_option = st.radio("View Financial Statements:", ["Balance Sheet", "Income Statement"])
                if view_option == "Balance Sheet" or view_option == "Income Statement":
                    fraud_element = st.radio("Does this have elements of fraud?", ["Yes", "No"])
                    amount_zar = st.number_input("Enter the amount in ZAR")
            else:
                st.write("No financial implications.")
            issue_owner_name = st.text_input("issue_owner_name")
            issue_owner_surname = st.text_input("issue_owner_surname")
            issue_owner_email = st.text_input("issue_owner_email")    
            # e... Add other input fields for the remaining columns
            # File attachment option for various types
            uploaded_file = st.file_uploader("Attach a File (if applicable)", type=["pdf", "jpg", "png", "txt", "csv", "xlsx"])
    
            # Check if a file is uploaded
            if uploaded_file is not None:
                file_type = uploaded_file.name.split(".")[-1].lower()
    
                # Your logic for handling CSV data goes here
                if file_type == "csv":
                    # Handle CSV file
                    df = pd.read_csv(uploaded_file)
                    st.write("CSV file content:")
                    st.dataframe(df)
    
                # Your logic for handling Excel data goes here
                elif file_type in ["xlsx", "xls"]:
                    # Handle Excel file
                    df = pd.read_excel(uploaded_file)
                    st.write("Excel file content:")
                    st.dataframe(df)
    
                else:
                    # Handle other file types
                    file_contents = uploaded_file.read()
                    st.text(f"Content of the uploaded file ({file_type}):")
                    st.text(file_contents.decode("utf-8"))

            if st.button("Log Issue"):
                            if issue_status != "Open":
                                st.warning("The issue status must be 'Open' to log a new issue. Please correct the issue status.")
            else:
                log_issue(issue_code, issue_name,description, issue_status, risk_type,subrisk_type, entities, bu_rating, agl_rating,assurance_provider, due_date, financially_implicated,review_name, view_option, fraud_element, amount_zar, issue_owner_name, issue_owner_surname, issue_owner_email,st.session_state.username)
                # try:
                #     log_issue(issue_code, issue_name, description, issue_status,risk_type,subrisk_type,entities, bu_rating,agl_rating, due_date,financially_implicated,view_option,fraud_element,amount_zar,issue_owner_name,issue_owner_surname, issue_owner_email,review_name)
                # except:
                #     st.warning(f"Error Logging the issue,please try again!{log_issue}")
                # Function to send email
                def send_email(subject, message):
                    sender_email = "your_email@gmail.com"  # Add your sender email address
                    receiver_email = "recipient_email@example.com"  # Add recipient email address
                    password = "your_password"  # Add your email password
                
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(message, 'plain'))
                
                    with smtplib.SMTP('smtp.gmail.com', 587) as server:
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                        st.success("Issue logged successfully!")
        else:
            st.warning("Please login to log an issue.")

    elif page == "Update Issue":
        st.header("Update Issue")
        st.subheader("Main Table")
        # df=pd.DataFrame(view_all_issues(),columns=['issue_code','issue_name',' description','issue_status','risk_type','subrisk_type','entities','bu_rating','agl_rating','assurance_provider','due_date','financially_implicated','risk_event_type',' additional_evidence',' file_contents','issuer_name','issuer_surname','issuer_email','username'])
        # dffiltered=st.text_input("...")
        # df_fil=df[df['issue_code']==dffiltered]
        # src_btn=st.button("Search")
        # if src_btn==True:
        #     st.data_editor(df_fil)
        # else:
        #     #st.table(df.tail(5))
        #     st.data_editor(df)
        df=pd.DataFrame(view_all_issues(),columns=['ID', 'issue_code', 'issue_name','description', 'issue_status', 'risk_type','subrisk_type', 'entities', 'bu_rating', 'agl_rating','assurance_provider', 'due_date', 'financially_implicated','review_name', 'view_option', 'fraud_element', 'amount_zar', 'issue_owner_name', 'issue_owner_surname', 'issue_owner_email','username'])
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.table(df_fil)
        else:
            st.table(df.tail(5))
        # Example: Update a row in a table
        st.header('Update a Row')
        #table_name = st.text_input('Enter the table name:')
        column_to_update = st.text_input('Enter the column name to update:')
        new_value = st.text_input('Enter the new value:')
        condition_column = st.text_input('Enter the column name for the condition:')
        condition_value = st.text_input('Enter the value for the condition:')
        
        if st.button('Update Row'):
            query = f"UPDATE issues2024 SET {column_to_update} = '{new_value}' WHERE {condition_column} = '{condition_value}';"
            execute_query(query)
            st.success(f'Row updated successfully in table Issues.')
      
            
        

# # Function to log an issue
# def log_issue(issue_code, issue_name,description, issue_status, risk_type,subrisk_type, entities, bu_rating, agl_rating,assurance_provider, due_date, financially_implicated,review_name, view_option, fraud_element, amount_zar, issue_owner_name, issue_owner_surname, issue_owner_email,username):

#     CURSOR.execute('''
#         INSERT INTO issues2024 (
#             'issue_code', 'issue_name','description', 'issue_status', 'risk_type','subrisk_type', 'entities', 'bu_rating', 'agl_rating','assurance_provider', 'due_date', 'financially_implicated','review_name', 'view_option', 'fraud_element', 'amount_zar', 'issue_owner_name', 'issue_owner_surname', 'issue_owner_email','username') 
#             VALUES (%s, %s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
#     ''',(issue_code, issue_name,description, issue_status, risk_type,subrisk_type, entities, bu_rating, agl_rating,assurance_provider, due_date, financially_implicated,review_name, view_option, fraud_element, amount_zar, issue_owner_name, issue_owner_surname, issue_owner_email,username))

#     connection.commit()
#     #connection.close()
# Function to log an issue
def log_issue(issue_code, issue_name, description, issue_status, risk_type, subrisk_type, entities, bu_rating, agl_rating, assurance_provider, due_date, financially_implicated, review_name, view_option, fraud_element, amount_zar, issue_owner_name, issue_owner_surname, issue_owner_email, username):
    CURSOR.execute('''
        INSERT INTO issues2024 (
            "issue_code", "issue_name", "description", "issue_status", "risk_type", "subrisk_type", "entities", "bu_rating", "agl_rating", "assurance_provider", "due_date", "financially_implicated", "review_name", "view_option", "fraud_element", "amount_zar", "issue_owner_name", "issue_owner_surname", "issue_owner_email", "username"
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (issue_code, issue_name, description, issue_status, risk_type, subrisk_type, entities, bu_rating, agl_rating, assurance_provider, due_date, financially_implicated, review_name, view_option, fraud_element, amount_zar, issue_owner_name, issue_owner_surname, issue_owner_email, username))

    connection.commit()


# def log_issue(issue_code, name, description, issue_status,risk_type ,subrisk_type,entities,bu_rating,agl_rating, risk_event_type, assurance_provider,due_date,financially_implicated,issuer_surname,issuer_email,username):
#     conn = create_connection()
#     cursor = conn.cursor()

#     cursor.execute('''
#         INSERT INTO issues (
#            issue_code, name, description, issue_status,risk_type ,subrisk_type,entities,bu_rating,agl_rating, risk_event_type, username,assurance_provider,due_date,financially_implicated,issuer_surname,issuer_email
#         ) VALUES (?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?)
#     ''', (issue_code, name, description, issue_status,risk_type ,subrisk_type,entities,bu_rating,agl_rating, risk_event_type, assurance_provider,due_date,financially_implicated,issuer_surname,issuer_email,username))

#     conn.commit()
#     conn.close()

# Function to update an issue Discription
def update_issue(issue_id, new_issue):

    CURSOR.execute("UPDATE issues SET description=%s WHERE id=%s, (new_issue, issue_id)")

    connection.commit()
    connection.close()

# Function to update an issue Status
def update_issue_status(issue_id, new_issue):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE issues SET issue_status=%s WHERE id=%s", (new_issue, issue_id))

    conn.commit()
    conn.close()
# ... (Other functions remain unchanged)

if __name__ == '__main__':
    main()
