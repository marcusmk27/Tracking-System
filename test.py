__import__('pysqlite3')
import sys

sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import sqlite3
from hashlib import sha256
import pandas as pd
#from auth import sign
import random


# Function to create a SQLite database connection
def create_connection():
    conn = sqlite3.connect("issues20240202.db")
    return conn


# function to view current issues
def view_all_issues():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM  issues')
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    return data,column_names


# function to view current issues status
def view_all_issues_status():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT issue_status FROM  issues')
    data = cursor.fetchall()
    return data

df_status=pd.DataFrame(view_all_issues_status(),columns=['Issue_Status'])
# Function to create a table for  new user
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
    cursor.execute("INSERT INTO  users  (username, password) VALUES (?, ?)", (username, hashed_password))

    conn.commit()
    conn.close()

#
# Function to log in a user

 
def login(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_password = password
    cursor.execute("SELECT * FROM  users  WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()
    return user






# Function to create the issues table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_code VARCHAR(4) UNIQUE,
            name VARCHAR(255),
            description TEXT,
            issue_status VARCHAR(50),
            risk_type VARCHAR(50),
            subrisk_type VARCHAR(50),
            entities VARCHAR(255),
            bu_rating VARCHAR(50),
            agl_rating VARCHAR(50),
            assurance_provider VARCHAR(255),
            due_date DATE,
            financially_implicated BOOLEAN,
            risk_event_type VARCHAR(255),
            additional_evidence TEXT,
            file_contents VARCHAR(255),
            issue_owner_name VARCHAR(255),
            issuer_surname VARCHAR(255),
            issuer_email VARCHAR(255),
            username TEXT Varchar(255)      
        )
    ''')

    conn.commit()
    conn.close()
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
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM issues WHERE issue_code = ?", (code,))
    count = cursor.fetchone()[0]
    return count > 0
    

#Function end here :)
    
# Streamlit UI
def main():
    create_table()

    st.title("Issue Tracker App")
    # Display the image below the title
    image_path = "C:/Users/ab0295s/Desktop/ICP_System/Absa-rebrand-artboard-01-logo-e1532702773207.png"
    st.image(image_path, caption="Welcome to the Issue Tracker App!", use_column_width=True)

    # Sidebar
    page = st.sidebar.radio("Navigation", ["Login", "View Current Issues", "Log Issue", "Update Issue"])
    if page=='View Current Issues':
       
        data,columns=view_all_issues()
        df=pd.DataFrame(data,columns=columns)
        #df=pd.DataFrame(view_all_issues(),columns=['issue_code','name',' description','issue_status','risk_type','subrisk_type','entities','bu_rating','agl_rating','assurance_provider','due_date','financially_implicated','risk_event_type',' additional_evidence',' file_contents','issue_owner_name','issuer_surname','issuer_email','username'])
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.table(df_fil)
        else:
            st.table(df.head(5))
        #st.write(view_all_issues())
    # if page == "Signup":
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
            # Automatically generate the issue code
            issue_code = generate_unique_code()

            # Display the generated code
            st.text(f"Issue Code: {issue_code}")
            name = st.text_input("Name")
            description = st.text_area("Description")
            issue_status =st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
            risk_type = st.selectbox("Risk Type", ["Operational & Resilience Risk", "Insurance risk type", "Compliance Risk", "Model Risk", "Conduct Risk"])
            subrisk_type = st.selectbox("Subrisk Type", ["Model Uncertainty Risk", "Process Management Risk", "Supplier Risk", "Technology Risk", "Transaction Processing and Management Risk", "Underwriting Risk", "Anti-Money Laundering", "Business Continuity Risk", "Change Risk", "Conduct Risk", "Customer Engagement Risk", "Data and Records Management Risk", "Fraud Risk", "Information Security and Cyber Risk", "Insurance Exposure Risk"])
            bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate", "Critical"])
            agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate", "Critical"])
            assurance_provider_dropdown = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit", "Internal Audit", "GSA"])
            due_date = st.date_input("Due Date")
            financially_implicated = st.radio("Does the issue have a financial implication?", ["Yes", "No"])
            issue_owner_name = st.text_input("Issue Owner Name")
            issue_owner_surnam = st.text_input("Issue Owner surname")
            issue_owner_email = st.text_input("Issue Owner Email Address")
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
            
            btn=st.button('Log Issue')
            if btn==True:
                if issue_status!= "Open":
                  st.warning("The issue status must be 'Open' to log a new issue. Please correct the issue status.")
                else:
                    log_issue(issue_code, name, description,issue_status,risk_type,subrisk_type, bu_rating ,agl_rating,assurance_provider_dropdown, due_date,financially_implicated,issue_owner_name,issue_owner_surnam,issue_owner_email, st.session_state.username)
                    st.success("Issue logged successfully!")
            else:
             st.warning("Please login to log an issue.")

    elif page == "Update Issue":
        st.header("Update Issue")
        st.subheader("Mian Table")
        data,columns=view_all_issues()
        df=pd.DataFrame(data,columns=columns)
        #df=pd.DataFrame(view_all_issues(),columns=['issue_code','name',' description','issue_status','risk_type','subrisk_type','entities','bu_rating','agl_rating','assurance_provider','due_date','financially_implicated','risk_event_type',' additional_evidence',' file_contents','issue_owner_name','issuer_surname','issuer_email','username'])
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.data_editor(df_fil)
        else:
            #st.table(df.tail(5))
            st.data_editor(df)

        if st.checkbox("Updated Description"):
            if st.session_state.get('username'):
                issue_id = st.text_input("Enter Issue ID")
                new_issue = st.text_area("Describe the updated issue",key=30)
                if st.button("Update Issue"):
                    update_issue(issue_id, new_issue)
                    st.success("Issue updated successfully!")

            if st.checkbox("Updated Issue Status"):
                if st.session_state.get('username'):
                    issue_id = st.text_input("Enter Issue ID",key='id')
                    new_issue =st.selectbox("Status",options=["Open", "Closed", "Risk Accepted", "Overdue"]) #st.text_area("Describe the updated issue",key=20)
                    if st.button("Update Issue Status"):
                        update_issue_status(issue_id, new_issue)
                        st.success("Issue updated successfully!")
            else:
                st.warning("Please login to update an issue.")

# Function to log an issue
def log_issue(issue_code, name, description, issue_status,risk_type,subrisk_type, bu_rating,agl_rating,assurance_provider,due_date,financially_implicated,issuer_surname, issuer_email,username):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO issues (
            issue_code, name, description,issue_status,risk_type,subrisk_type,bu_rating,agl_rating ,assurance_provider, due_date,financially_implicated,issuer_surname, issuer_email,username
        ) VALUES (?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?)
    ''', (issue_code, name, description, issue_status,risk_type,subrisk_type, bu_rating,agl_rating,assurance_provider, due_date,financially_implicated,issuer_surname, issuer_email,username))

    conn.commit()
    conn.close()

# Function to update an issue Discription
def update_issue(issue_id, new_issue):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE issues SET description=? WHERE id=?", (new_issue, issue_id))

    conn.commit()
    conn.close()

# Function to update an issue Status
def update_issue_status(
    issue_id, issue_status, risk_type, subrisk_type, bu_rating, 
    agl_rating, assurance_provider, due_date, financially_implicated
):
    conn = create_connection()
    cursor = conn.cursor()

    query = """
        UPDATE issues 
        SET 
            issue_status = ?, 
            risk_type = ?, 
            subrisk_type = ?, 
            bu_rating = ?, 
            agl_rating = ?, 
            assurance_provider = ?, 
            due_date = ?, 
            financially_implicated = ?
        WHERE id = ?
    """

    cursor.execute(query, (
        issue_status, risk_type, subrisk_type, bu_rating, 
        agl_rating, assurance_provider, due_date, financially_implicated, 
        issue_id
    ))

    conn.commit()
    conn.close()

# ... (Other functions remain unchanged)

if __name__ == '__main__':
    main()
