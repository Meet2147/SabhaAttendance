import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Parsing the provided attendance data
data = {
    "Nirav Chauhan": ["A", "A", "P"],
    "Mayur Rajgor": ["P", "P", "P", "P"],
    "Meet Jethwa": ["P", "P", "P", "P"],
    "Manan Thakkar": ["P", "P", "P", "P"],
    "Smit Kotak": ["P", "P", "P", "P"],
    "Vatsal Patel": ["A", "A", "A"],
    "Devansh Jethva": ["P", "A", "P"],
    "Sanjay Mange": ["P", "A", "A"],
    "Harikrishna Padhiyar": ["A", "P", "P", "P"],
    "Jay Chauhan": ["A", "A", "P"],
    "Jaimin Chauhan": ["A", "A", "P", "P"],
    "Hari Mehta": ["A", "A", "A"],
    "Rushi Mehta": ["A", "A", "A"],
    "Jagdish Rajgor": ["P", "P", "A"],
    "Rushi Rajgor": ["P", "P", "P", "P"],
    "Abhi Vakharia": ["A", "A", "A"],
    "Manish Thakkar": ["A", "A", "A"],
    "Vedant Nanda": ["A", "A", "A"],
    "Mann Gori": ["P", "P", "P", "P"],
    "Sarvesh Padhiyar": ["P", "P", "P", "P"],
    "Dev Wadkar": ["P", "A", "A"],
    "Viraj Patel": ["A", "A", "A"],
    "Darshan Kataria": ["A", "A", "A"],
    "Rahul Gavli": ["A", "A", "A"],
    "Dhruv Patel": ["A", "A", "A"],
    "Preet Ravariya": ["A", "A", "A"],
    "Khushal Senghani": ["A", "P", "A"],
    "Akshay Padhiyar": ["A", "A", "A"],
    "Rohit Shinde": ["A", "A", "A"],
    "Harshit Makwana": ["A", "A", "A"],
    "Darshan Parmar": ["A", "A", "A"],
    "Kavya Dama": ["A", "A", "A"],
    "Yash Chawda": ["A", "A", "A"],
    "Krishna Bhanushali": ["A", "A", "A"],
    "Ankit Wadhvana": ["A", "P", "A"],
    "Mann Mange": ["A", "P", "P", "P"],
    "Vansh Bhanushali": ["A", "A", "A"],
    "Chintan Pujara": ["A", "A", "A"],
    "Darsh Solanki": ["A", "A", "A"]
}

# Function to generate dates for all Tuesdays in the current year starting from July
def get_all_tuesdays(year):
    d = datetime(year, 7, 1)
    d += timedelta(days=(1 - d.weekday() + 7) % 7)  # Move to the first Tuesday of July
    while d.year == year:
        yield d
        d += timedelta(days=7)

# Get current year
current_year = datetime.now().year

# Generate all Tuesdays for the current year starting from July
tuesdays = list(get_all_tuesdays(current_year))

# Initialize DataFrame
attendance_df = pd.DataFrame(index=data.keys(), columns=tuesdays)

# Populate the DataFrame with initial data
for idx, date in enumerate(tuesdays[:3]):  # First three dates in July
    for name, attendance in data.items():
        if idx < len(attendance):
            attendance_df.at[name, date] = attendance[idx]

# Function to get summary
def get_summary(attendance_df, period):
    summary = attendance_df.apply(lambda row: (row == "P").sum() + (row == "Present in White and White").sum(), axis=1)
    return summary

# Streamlit app with sidebar navigation
st.sidebar.title("Attendance App Navigation")
pages = ["Mark Attendance", "Week Attendance", "Month Attendance", "Quarter Attendance", "Half Year Attendance", "Yearly Attendance"]
page = st.sidebar.radio("Go to", pages)

if page == "Mark Attendance":
    st.title("Mark Attendance")
    selected_date = st.date_input("Select a Tuesday", value=tuesdays[0], min_value=tuesdays[0], max_value=tuesdays[-1])
    selected_date = pd.to_datetime(selected_date)

    if selected_date not in tuesdays:
        st.error("Please select a valid Tuesday.")
    else:
        st.write(f"## Mark Attendance for {selected_date.date()}")
        for name in data.keys():
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(name)
            with col2:
                attendance = st.radio(
                    f"Attendance for {name}",
                    ["Present", "Present in White and White", "Absent"],
                    index=0 if attendance_df.at[name, selected_date] == "P" else 1 if attendance_df.at[name, selected_date] == "Present in White and White" else 2,
                    key=f"attendance_{name}_{selected_date}",
                    label_visibility="collapsed"
                )
                attendance_df.at[name, selected_date] = attendance

elif page == "Week Attendance":
    st.title("Weekly Attendance Summary")
    st.dataframe(get_summary(attendance_df, "weekly"))

elif page == "Month Attendance":
    st.title("Monthly Attendance Summary")
    st.dataframe(get_summary(attendance_df, "monthly"))

elif page == "Quarter Attendance":
    st.title("Quarterly Attendance Summary")
    st.dataframe(get_summary(attendance_df, "quarterly"))

elif page == "Half Year Attendance":
    st.title("Half-Yearly Attendance Summary")
    st.dataframe(get_summary(attendance_df, "half-yearly"))

elif page == "Yearly Attendance":
    st.title("Yearly Attendance Summary")
    st.dataframe(get_summary(attendance_df, "yearly"))

# Provide a download link for the attendance data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(attendance_df)

st.download_button(
    label="Download attendance data as CSV",
    data=csv,
    file_name='attendance.csv',
    mime='text/csv',
)
