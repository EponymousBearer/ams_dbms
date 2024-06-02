import streamlit as st
import pyodbc
import pandas as pd

# Connection parameters
server = 'DESKTOP-O16J5JA'  # e.g., 'localhost' or 'DESKTOP-XXXXXXX'
database = 'demo'
# Use the following lines for SQL Server Authentication
# username = 'your_username'
# password = 'your_password'

# Create the connection string
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=' + server + ';'
    'DATABASE=' + database + ';'
    'Trusted_Connection=yes;'  # Use this for Windows Authentication
    # 'UID=' + username + ';PWD=' + password  # Uncomment and use this for SQL Server Authentication
)

# Establish a connection to the database
conn = pyodbc.connect(conn_str)

# # Define a function to fetch data from the database
# def fetch_data(query):
#     with conn.cursor() as cursor:
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         columns = [column[0] for column in cursor.description]
#         return pd.DataFrame(rows, columns=columns)

# # Example query
# query = "SELECT * FROM course"
# data = fetch_data(query)

# # Streamlit app
# st.title('SQL Server Database Frontend')

# # Display the data
# st.write('Data from SQL Server:')
# st.dataframe(data)

import streamlit as st
import pyodbc

# Function to check database connection
def check_db_connection():
    try:
        # Establish a connection to the SQL Server database
        conn = pyodbc.connect(
            'DRIVER={SQL Server};'
            'SERVER=DESKTOP-O16J5JA;'  # Replace with your server name
            'DATABASE=demo;'  # Replace with your database name
        )
        c = conn.cursor()
        
        # Check if the Airline table exists
        c.execute('SELECT TOP 1 Name FROM Airline')
        
        conn.close()
        return True
    except pyodbc.Error as e:
        st.error(f"Database connection failed: {e}")
        return False

# Title
st.title('Airport Management System')

# Check database connection
if check_db_connection():
    st.success('Database is connected!')
    
    # Select an airline
    st.header('Select Airline')
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=your_server_name;'
        'DATABASE=airport_management;'
        'UID=your_username;'
        'PWD=your_password'
    )
    c = conn.cursor()
    c.execute('SELECT Name FROM Airline')
    airlines = c.fetchall()
    airline_options = [airline[0] for airline in airlines]
    selected_airline = st.selectbox('Choose an airline', airline_options)

    # Show flights for the selected airline
    if selected_airline:
        st.header('Flights')
        c.execute('SELECT AirlineID FROM Airline WHERE Name = ?', (selected_airline,))
        airline_id = c.fetchone()[0]
        c.execute('SELECT * FROM Flight WHERE AirplaneID IN (SELECT AirplaneID FROM Airplane WHERE AirlineID = ?)', (airline_id,))
        flights = c.fetchall()
        for flight in flights:
            st.write(f'Flight Number: {flight[1]}, From: {flight[2]}, To: {flight[3]}, Departure: {flight[4]}, Arrival: {flight[5]}')
    conn.close()
else:
    st.error('Failed to connect to the database.')
# import streamlit as st
# import sqlite3

# # Connect to SQLite database
# conn = sqlite3.connect('demo')
# c = conn.cursor()

# # Title
# st.title('Airport Management System')

# # Select an airline
# st.header('Select Airline')
# airlines = c.execute('SELECT Name FROM Airline').fetchall()
# airline_options = [airline[0] for airline in airlines]
# selected_airline = st.selectbox('Choose an airline', airline_options)

# # Show flights for the selected airline
# if selected_airline:
#     st.header('Flights')
#     airline_id = c.execute('SELECT AirlineID FROM Airline WHERE Name = ?', (selected_airline,)).fetchone()[0]
#     flights = c.execute('SELECT * FROM Flight WHERE AirplaneID IN (SELECT AirplaneID FROM Airplane WHERE AirlineID = ?)', (airline_id,)).fetchall()
#     for flight in flights:
#         st.write(f'Flight Number: {flight[1]}, From: {flight[2]}, To: {flight[3]}, Departure: {flight[4]}, Arrival: {flight[5]}')

# # Book a flight
# st.header('Book a Flight')
# passenger_email = st.text_input('Enter your email')
# flight_number = st.text_input('Enter flight number')
# booking_date = st.date_input('Booking date')

# if st.button('Book'):
#     # Check if passenger exists
#     passenger = c.execute('SELECT PassengerID FROM Passenger WHERE Email = ?', (passenger_email,)).fetchone()
#     if not passenger:
#         st.error('Passenger not found. Please register first.')
#     else:
#         passenger_id = passenger[0]
#         flight = c.execute('SELECT FlightID FROM Flight WHERE FlightNumber = ?', (flight_number,)).fetchone()
#         if not flight:
#             st.error('Flight not found.')
#         else:
#             flight_id = flight[0]
#             c.execute('INSERT INTO Booking (PassengerID, FlightID, BookingDate) VALUES (?, ?, ?)', (passenger_id, flight_id, booking_date))
#             conn.commit()
#             st.success('Booking successful!')

# conn.close()
