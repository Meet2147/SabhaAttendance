import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

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

# Function to get all Tuesdays of the current month
def get_all_tuesdays():
    today = datetime.now()
    first_day = today.replace(day=1)
    first_tuesday = first_day + timedelta(days=(1 - first_day.weekday() + 7) % 7)
    tuesdays = [first_tuesday]
    while True:
        next_tuesday = tuesdays[-1] + timedelta(days=7)
        if next_tuesday.month != today.month:
            break
        tuesdays.append(next_tuesday)
    return [tuesday.strftime("%d|%m|%y") for tuesday in tuesdays]

# Initialize attendance DataFrame
def initialize_attendance(df):
    tuesdays = get_all_tuesdays()
    for date_col in tuesdays:
        if date_col not in df.columns:
            df[date_col] = "A"
    df["Total Attendance"] = 0
    return df

# Mark attendance
def mark_attendance(df):
    today = datetime.now().strftime("%d|%m|%y")
    if today in df.columns:
        st.write(f"Mark attendance for {today}:")
        for index, row in df.iterrows():
            if st.checkbox(row['Names'], key=row['Names']):
                df.loc[index, today] = "P"
    return df

# Calculate total attendance
def calculate_attendance(df):
    attendance_columns = [col for col in df.columns if col not in ["Names", "Total Attendance"]]
    df["Total Attendance"] = (df[attendance_columns] == "P").sum(axis=1)
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
