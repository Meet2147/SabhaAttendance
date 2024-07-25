import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Parsing the provided attendance data
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

if "attendance_df" not in st.session_state:
    st.session_state.attendance_df = pd.DataFrame(index=names, columns=saturdays)

# Initialize DataFrame
attendance_df = st.session_state.attendance_df

# Function to get summary
def get_summary(attendance_df, period):
    summary = attendance_df.apply(lambda row: (row == "P").sum(), axis=1)
    return summary

# Function to filter attendance data based on period
def filter_attendance(attendance_df, period):
    if period == "weekly":
        return attendance_df.iloc[:, :4]
    elif period == "monthly":
        return attendance_df.iloc[:, :4]  # Assuming 4 Saturdays in a month
    elif period == "quarterly":
        return attendance_df.iloc[:, :13]  # Assuming 13 Saturdays in a quarter
    elif period == "half-yearly":
        return attendance_df.iloc[:, :26]  # Assuming 26 Saturdays in a half-year
    elif period == "yearly":
        return attendance_df  # All data for the year

# Streamlit app with sidebar navigation
st.sidebar.title("Attendance App Navigation")
pages = ["Mark Attendance", "Week Attendance", "Month Attendance", "Quarter Attendance", "Half Year Attendance", "Yearly Attendance"]
page = st.sidebar.radio("Go to", pages)

if page == "Mark Attendance":
    st.title("Mark Attendance")
    selected_date = st.date_input("Select a Saturday", value=saturdays[0], min_value=saturdays[0], max_value=saturdays[-1])
    selected_date = pd.to_datetime(selected_date)

    if selected_date not in saturdays:
        st.error("Please select a valid Saturday.")
    else:
        st.write(f"## Mark Attendance for {selected_date.date()}")

        search_name = st.text_input("Search for a name:")
        filtered_names = [name for name in names if search_name.lower() in name.lower()]

        if search_name and filtered_names:
            name = filtered_names[0]  # Get the first matching name
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write(name)
            with col2:
                attendance = st.radio(
                    f"Attendance for {name}",
                    ["Present", "W&W", "Absent", "Absent with reason"],
                    index=0 if attendance_df.at[name, selected_date] == "P" else 1 if attendance_df.at[name, selected_date] == "W&W" else 2 if attendance_df.at[name, selected_date] == "A" else 3,
                    key=f"attendance_{name}_{selected_date}",
                    horizontal=True
                )

                reason = ""
                if attendance == "Absent with reason":
                    reason = st.text_input(f"Reason for {name}", key=f"reason_{name}_{selected_date}")

            if st.button("Submit"):
                if attendance == "Absent with reason":
                    attendance_df.at[name, selected_date] = f"AR: {reason}"
                elif attendance == "Present":
                    attendance_df.at[name, selected_date] = "P"
                elif attendance == "W&W":
                    attendance_df.at[name, selected_date] = "W&W"
                elif attendance == "Absent":
                    attendance_df.at[name, selected_date] = "A"
                st.success(f"Attendance marked for {name}")
                st.experimental_rerun()  # Refresh the page to update the data

elif page == "Week Attendance":
    st.title("Weekly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "weekly"))

elif page == "Month Attendance":
    st.title("Monthly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "monthly"))

elif page == "Quarter Attendance":
    st.title("Quarterly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "quarterly"))

elif page == "Half Year Attendance":
    st.title("Half-Yearly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "half-yearly"))

elif page == "Yearly Attendance":
    st.title("Yearly Attendance Summary")
    st.dataframe(filter_attendance(attendance_df, "yearly"))

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
