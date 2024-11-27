import streamlit as st
import pandas as pd
import random
from hashlib import sha256
import os
import hashlib

# Paths to your CSV files
ISSUES_FILE = 'Tracking-System/blob/main/issues.csv'
USERS_FILE = 'Tracking-System/blob/main/users.csv'

# Helper function to read issues from CSV
def read_issues_from_csv():
    if os.path.exists(ISSUES_FILE):
        return pd.read_csv(ISSUES_FILE,delimiter=";")
    else:
        # If the file does not exist, return an empty DataFrame
        return pd.DataFrame()

# Helper function to save issues to CSV
def save_issues_to_csv(df):
    df.to_csv(ISSUES_FILE, index=False)

# Helper function to read users from CSV
def read_users_from_csv():
    if os.path.exists(USERS_FILE):
        return pd.read_csv(USERS_FILE,delimiter=";")
    else:
        return pd.DataFrame()

# Helper function to save users to CSV
def save_users_to_csv(df):
    df.to_csv(USERS_FILE, index=False)

# Function to sign up a new user
def signup(username, password):
    users_df = read_users_from_csv()

    # Hash the password before saving
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    
    # Append the new user data
    users_df = users_df.append({'username': username, 'password': hashed_password}, ignore_index=True)
    
    save_users_to_csv(users_df)
    return "Signup successful!"
# Function to hash passwords (SHA256)
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
# Function to log in a user
def login(username, password):
    users_df = read_users_from_csv()
    #hashed_password = hash_password() #sha256(password.encode('utf-8')).hexdigest()
    
    user = users_df[users_df['username'] == username]
    if not user.empty and user['password'].values[0] :#== hashed_password:
        return True
    return False

# Function to generate a unique code for an issue
def generate_unique_code():
    issues_df = read_issues_from_csv()
    
    # Ensure 'issue_code' column exists
    if 'issue_code' not in issues_df.columns:
        issues_df['issue_code'] = []  # Add empty column if missing
    
    while True:
        # Generate a random four-digit code
        code = str(random.randint(1000, 9999))
        
        # Check if the code is unique
        if code not in issues_df['issue_code'].astype(str).values:
            return code

# Function to log an issue
import pandas as pd

# Function to log an issue (fixing the append issue)
def log_issue(issue_code, name, description, issue_status, risk_type, subrisk_type, bu_rating,
              agl_rating, assurance_provider, due_date, financially_implicated, issuer_surname, 
              issuer_email, username):

    # Assuming 'issues.csv' is the file where you are saving your issues
    try:
        # Read the existing issues from the CSV
        issues_df = pd.read_csv('Tracking-System/blob/main/issues.csv')

        # Create a new DataFrame for the new issue
        new_issue = pd.DataFrame([{
            'issue_code': issue_code,
            'name': name,
            'description': description,
            'issue_status': issue_status,
            'risk_type': risk_type,
            'subrisk_type': subrisk_type,
            'bu_rating': bu_rating,
            'agl_rating': agl_rating,
            'assurance_provider': assurance_provider,
            'due_date': due_date,
            'financially_implicated': financially_implicated,
            'issuer_surname': issuer_surname,
            'issuer_email': issuer_email,
            'username': username
        }])

        # Use pd.concat() to append the new issue to the existing DataFrame
        issues_df = pd.concat([issues_df, new_issue], ignore_index=True)

        # Write the updated DataFrame back to the CSV
        issues_df.to_csv('issues.csv', index=False)

        print("Issue logged successfully!")
    except Exception as e:
        print(f"Error logging the issue: {e}")



# Function to view all issues
def view_all_issues():
    issues_df = pd.read_csv( 'https://github.com/marcusmk27/Tracking-System/blob/main/issues.csv', delimiter=';',  error_bad_lines=False, es
        ,bad_lines=True,    # Warn about problematic lines
        engine='python'     )#read_issues_from_csv()
    return issues_df.head()

# Function to update an issue description
def update_issue(issue_id, new_description):
    issues_df = read_issues_from_csv()
    
    # Update the issue where the 'id' matches
    issues_df.loc[issues_df['id'] == issue_id, 'description'] = new_description
    
    save_issues_to_csv(issues_df)
    return "Issue description updated successfully!"

# Function to update an issue status
def update_issue_status(issue_id, issue_status, risk_type, subrisk_type, bu_rating, agl_rating,
                        assurance_provider, due_date, financially_implicated):
    issues_df = read_issues_from_csv()
    
    # Update the issue where the 'id' matches
    issues_df.loc[issues_df['id'] == issue_id, ['issue_status', 'risk_type', 'subrisk_type', 
                                                 'bu_rating', 'agl_rating', 'assurance_provider', 
                                                 'due_date', 'financially_implicated']] = \
        [issue_status, risk_type, subrisk_type, bu_rating, agl_rating, assurance_provider, due_date, financially_implicated]
    
    save_issues_to_csv(issues_df)
    return "Issue status updated successfully!"
# Function to hash passwords (SHA256)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
# Streamlit UI
def main():
    st.title("Issue Tracker App")

    # Sidebar Navigation
    page = st.sidebar.radio("Navigation", ["Login", "View Current Issues", "Log Issue", "Update Issue"])
    
    if page == "View Current Issues":
        st.header("Current Issues")
        issues_df = view_all_issues()
        st.write(issues_df.head(15))

    if page == "Login":
        st.header("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username=='ab0001' and password=='testing':#login(username, password):
                st.session_state.username = username  # Store username in session state
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
        # Function to log in a user
        # Capture the username and password
        
        
      
   
        st.header("Log Issue")
        if 'username' in st.session_state:
            issue_code = generate_unique_code()
            st.text(f"Generated Issue Code: {issue_code}")
            
            name = st.text_input("Name")
            description = st.text_area("Description")
            issue_status = st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
            risk_type = st.selectbox("Risk Type", ["Operational", "Insurance", "Compliance", "Model Risk"])
            subrisk_type = st.selectbox("Subrisk Type", ["Technology", "Compliance", "Financial", "Operational"])
            bu_rating = st.selectbox("BU Rating", ["Limited", "Moderate", "Critical"])
            agl_rating = st.selectbox("AGL Rating", ["Limited", "Moderate", "Critical"])
            assurance_provider = st.selectbox("Assurance Provider", ["Internal Audit", "External Audit", "GSA"])
            due_date = st.date_input("Due Date")
            financially_implicated = st.radio("Financial Implication?", ["Yes", "No"])
            issuer_surname = st.text_input("Issuer Surname")
            issuer_email = st.text_input("Issuer Email")
            
            if st.button("Log Issue"):
                log_issue(issue_code, name, description, issue_status, risk_type, subrisk_type, bu_rating,
                          agl_rating, assurance_provider, due_date, financially_implicated, issuer_surname,
                          issuer_email, st.session_state.username)
                st.success("Issue logged successfully!")
                df= pd.read_csv('C:/Users/AB033NI/Downloads/New folder 1/New folder/issues.csv')
                st.write(df.tail(20))
        else:
            st.warning("Please login to log an issue.")

    elif page == "Update Issue":
        st.header("Update Issue")
        issues_df = view_all_issues()
        issue_id = st.number_input("Enter Issue ID to Update", min_value=1, max_value=len(issues_df))
        
        if issue_id:
            new_description = st.text_area("New Description")
            if st.button("Update Description"):
                update_issue(issue_id, new_description)
                st.success("Issue description updated successfully!")
            
            new_status = st.selectbox("Update Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
            new_risk_type = st.selectbox("Risk Type", ["Operational", "Insurance", "Compliance", "Model Risk"])
            new_subrisk_type = st.selectbox("Subrisk Type", ["Technology", "Compliance", "Financial", "Operational"])
            new_bu_rating = st.selectbox("BU Rating", ["Limited", "Moderate", "Critical"])
            new_agl_rating = st.selectbox("AGL Rating", ["Limited", "Moderate", "Critical"])
            new_assurance_provider = st.selectbox("Assurance Provider", ["Internal Audit", "External Audit", "GSA"])
            new_due_date = st.date_input("Due Date")
            new_financially_implicated = st.radio("Financial Implication?", ["Yes", "No"])

            if st.button("Update Status"):
                update_issue_status(issue_id, new_status, new_risk_type, new_subrisk_type, new_bu_rating,
                                    new_agl_rating, new_assurance_provider, new_due_date, new_financially_implicated)
                st.success("Issue status updated successfully!")

if __name__ == "__main__":
    main()
