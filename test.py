import streamlit as st
import pandas as pd
import random
from hashlib import sha256
import os
import hashlib

# Paths to your CSV files
ISSUES_FILE = 'https://raw.githubusercontent.com/marcusmk27/Tracking-System/main/issues.csv'
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
def log_issue(issue_code, name, description, issue_status, risk_type, subrisk_type, business_unit, bu_rating,
              agl_rating, assurance_provider, due_date, financially_implicated, review_name, issue_number_and_title, date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date, issuer_name, issuer_surname, 
              issuer_email, username):

    # Assuming 'issues.csv' is the file where you are saving your issues
    try:
        # Read the existing issues from the CSV
        issues_df = pd.read_csv('https://raw.githubusercontent.com/marcusmk27/Tracking-System/main/issues.csv')

        # Create a new DataFrame for the new issue
        new_issue = pd.DataFrame([{
            'issue_code': issue_code,
            'name': name,
            'description': description,
            'issue_status': issue_status,
            'principal_risk_type': principal_risk_type,
            'subrisk_type': subrisk_type,
            'business_Unit': Business_Unit,
            'bu_rating': bu_rating,
            'agl_rating': agl_rating,
            'assurance_provider': assurance_provider,
            'due_date': due_date,
            'financially_implicated': financially_implicated,
            'review_name': Review_Name,
            'issue_number_and_Title': Issue_Number_and_Title,
            'date_submitted_to_risk_assurance': Date_Submitted_to_Risk_Assurance,
            'ra_reviewers': RA_Reviewers,
            'closure_email_or_feedback_date': Closure_email_or_Feedback_date,
            'issuer_name': issuer_name,
            'issuer_surname': issuer_surname,
            'issuer_email': issuer_email,
            'username': username,
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
    issues_df =read_issues_from_csv()
    
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
                        assurance_provider, due_date, financially_implicated, 'review_name',
                        'issue_number_and_title', 'date_submitted_to_risk_assurance', 
                        'ra_reviewers', 'closure_email_or_feedback_date'):
    issues_df = read_issues_from_csv()
    
    # Update the issue where the 'id' matches
    issues_df.loc[issues_df['id'] == issue_id, ['issue_status', 'principal_risk_type', 'subrisk_type', 'business_unit',
                                                 'bu_rating', 'agl_rating', 'assurance_provider', 
                                                 'due_date', 'financially_implicated', 'review_name',
                                                'issue_number_and_title', 'date_submitted_to_risk_assurance', 
                                                'ra_reviewers', 'closure_email_or_feedback_date']] = \
        [issue_status, principal_risk_type, subrisk_type, business_unit, bu_rating, agl_rating, assurance_provider, due_date, financially_implicated, review_name, issue_number_and_title, date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date,]
    
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
    
    if page=='View Current Issues':
       
        data,columns=view_all_issues()
        df=pd.DataFrame(data,columns=columns)
        dffiltered=st.text_input("...")
        df_fil=df[df['issue_code']==dffiltered]
        src_btn=st.button("Search")
        if src_btn==True:
            st.table(df_fil)
        else:
            st.table(df.head(5))

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
            description = st.text_area("Issue Description", "")
            issue_status = st.selectbox("Issue Status", ["Open", "Closed", "Risk Accepted", "Overdue"])
            principal_risk_type = st.selectbox("Principal Risk Type", ["Operational & Rislience Risk","Insurance risk type","Compliance Risk","Model Risk","Conduct Risk"])
            subrisk_type = st.selectbox("Subrisk Type", ["Model Uncertainty Risk","Process Management Risk","Supplier Risk","Technology Risk","Transaction Processing and Management Risk","Underwriting Risk","Anti-Money Laundering","Business Continuity Risk","Change Risk","Conduct Risk","Customer Engagement Risk","Data and Records Management Risk","Fraud Risk","Information Security and Cyber Risk","Insurance Exposure Risk"])
            business_unit = st.selectbox("BU",["FAK","ALAK","LIFESA","ALB","ALZ","NBFS","AIC", "GAM","IDIRECT","INSTANT LIFE","AL"])
            bu_rating = st.selectbox("BU Rating", ["Limited", "Major", "Moderate", "Critical"])
            agl_rating = st.selectbox("AGL Rating", ["Limited", "Major", "Moderate", "Critical"])
            assurance_provider = st.selectbox("Assurance Provider", ["2LOD Risk", "External Audit", "Internal Audit", "GSA"])
            due_date = st.date_input("Due Date")
            financially_implicated = st.radio("Financial Implication?", ["Yes", "No"])
            review_name = st.text_input("Review Name", "")
            issue_number_and_title = st.text_input("Issue Number and Title", "")
            date_submitted_to_risk_assurance = st.date_input("Date Submitted to Risk Assurance")
            ra_reviewers = st.selectbox("RA Reviewers", ["Thejal Kusial", "Sibongile Lebeko"])
            closure_email_or_feedback_date = st.date_input("Closure Email/Feedback Date")
            issuer_name = st.text_input("Issuer Name")
            issuer_surname = st.text_input("Issuer Surname")
            issuer_email = st.text_input("Issuer Email")
            
            if st.button("Log Issue"):
                log_issue(issue_code, name, description, issue_status, principal_risk_type, subrisk_type, business_unit, bu_rating,
                          agl_rating, assurance_provider, due_date, financially_implicated,review_name, 
                          issue_number_and_title, date_submitted_to_risk_assurance, ra_reviewers, closure_email_or_feedback_date, issuer_name,
                          issuer_surname, issuer_email, st.session_state.username)
                st.success("Issue logged successfully!")
                df= pd.read_csv('https://raw.githubusercontent.com/marcusmk27/Tracking-System/main/issues.csv')
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
            new_principal_risk_type = st.selectbox("Risk Type", ["Operational", "Insurance", "Compliance", "Model Risk"])
            new_subrisk_type = st.selectbox("Subrisk Type", ["Technology", "Compliance", "Financial", "Operational"])
            new_business_unit = st.text_input("Business_Unit")
            new_bu_rating = st.selectbox("BU Rating", ["Limited", "Moderate", "Critical"])
            new_agl_rating = st.selectbox("AGL Rating", ["Limited", "Moderate", "Critical"])
            new_assurance_provider = st.selectbox("Assurance Provider", ["Internal Audit", "External Audit", "GSA"])
            new_due_date = st.date_input("Due Date")
            new_financially_implicated = st.radio("Financial Implication?", ["Yes", "No"])
            new_review_name = st.text_input("Review Name")
            new_issue_number_and_title = st.text_input("Issue Number and Title")
            new_date_submitted_to_risk_assurance = st.date_input("Date Submitted to Risk Assurance")
            new_ra_reviewers = st.selectbox("RA Reviewers", ["Thejal Kusial", "Sibongile Lebeko"])
            new_closure_email_or_feedback_date = st.date_input("Closure Email/Feedback Date")

            if st.button("Update Status"):
                update_issue_status(issue_id, new_status, new_principal_risk_type, new_subrisk_type, new_business_unit, new_bu_rating,
                                    new_agl_rating, new_assurance_provider, new_due_date, new_financially_implicated, new_review_name, 
                                    new_issue_number_and_title, new_date_submitted_to_risk_assurance, new_ra_reviewers, new_closure_email_or_feedback_date)
                st.success("Issue status updated successfully!")

if __name__ == "__main__":
    main()
