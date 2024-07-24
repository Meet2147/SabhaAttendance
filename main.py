import streamlit as st
import pandas as pd
from datetime import datetime

# Names extracted from the PDF
names = [
    "Nirav Chauhan", "Mayur Rajgor", "Meet Jethwa", "Manan Thakkar", "Smit Kotak", 
    "Vatsal Patel", "Devansh Jethva", "Sanjay Mange", "Harikrishna Padhiyar", 
    "Jay Chauhan", "Jaimin Chauhan", "Hari Mehta", "Rushi Mehta", "Jagdish Rajgor", 
    "Rushi Rajgor", "Abhi Vakharia", "Manish Thakkar", "Vedant Nanda", "Mann Gori", 
    "Sarvesh Padhiyar", "Dev Wadkar", "Viraj Patel", "Darshan Kataria", "Rahul Gavli", 
    "Dhruv Patel", "Preet Ravariya", "Khushal Senghani", "Akshay Padhiyar", "Rohit Shinde", 
    "Harshit Makwana", "Darshan Parmar", "Kavya Dama", "Yash Chawda", "Krishna Bhanushali", 
    "Ankit Wadhvana", "Mann Mange", "Vansh Bhanushali", "Chintan Pujara", "Darsh Solanki", 
    "Kush Thakkar"
]

# Create a DataFrame
df = pd.DataFrame(names, columns=["Names"])

# Initialize attendance DataFrame
def initialize_attendance(df):
    today = datetime.now()
    if today.weekday() == 1:  # If today is Tuesday
        date_col = today.strftime("%d|%m|%y")
        if date_col not in df.columns:
            df[date_col] = "A"
    return df

# Mark attendance
def mark_attendance(df):
    today = datetime.now()
    if today.weekday() == 1:  # If today is Tuesday
        date_col = today.strftime("%d|%m|%y")
        for index, row in df.iterrows():
            if st.checkbox(row['Names'], key=row['Names']):
                df.loc[index, date_col] = "P"
    return df

# Calculate attendance
def calculate_attendance(df):
    today = datetime.now()
    monthly = (df.iloc[:, 1:] == "P").sum(axis=1)
    quarterly = monthly  # Simplified for demo purposes
    halfyearly = monthly  # Simplified for demo purposes
    yearly = monthly  # Simplified for demo purposes
    df["Monthly"] = monthly
    df["Quarterly"] = quarterly
    df["Half-Yearly"] = halfyearly
    df["Yearly"] = yearly
    return df

# Streamlit app
def main():
    st.title('Attendance App')

    global df  # Ensure df is recognized as a global variable
    df = initialize_attendance(df)

    # Mark attendance
    df = mark_attendance(df)

    st.write("Attendance Data:")
    st.write(df)

    # Calculate and display attendance
    if st.button('Calculate Attendance'):
        df = calculate_attendance(df)
        st.write(df)

if __name__ == "__main__":
    main()
