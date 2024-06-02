import streamlit as st
from datetime import datetime
import pyodbc
import pandas as pd


def get_connection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-O16J5JA;"
        "DATABASE=Airport_Management_System;"
        "Trusted_Connection=yes;"  # Assuming Windows authentication
    )
    return conn

# Function to fetch flights
def fetch_flights():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT flight_id, flight_number FROM flight")
    flights = c.fetchall()
    c.close()
    conn.close()
    return flights

def generate_seat_numbers(capacity):
    seat_letters = ["A", "B", "C", "D", "E", "F"]
    rows = (capacity + len(seat_letters) - 1) // len(seat_letters)  # Calculate the number of rows needed
    seats = [f"{row + 1}{letter}" for row in range(rows) for letter in seat_letters]
    return seats[:capacity]  # Ensure only the number of seats up to capacity is returned

# Function to fetch available seats for a flight
def fetch_available_seats(airplane_id):
    conn = get_connection()
    c = conn.cursor()
    # Your logic to fetch available seats for a given flight_id
    # Example:
    c.execute("SELECT capacity FROM airplane WHERE airplane_id = ?", (airplane_id,))
    capacity = c.fetchone()[0]
    c.close()
    conn.close()
    
    # Generate seats based on capacity
    seats = generate_seat_numbers(capacity)
    return seats
    # available_seats = c.fetchall()
    # return available_seats
    # c.close()
    # conn.close()
    # return [("1A",), ("1B",), ("1C",), ("1D",), ("1E",)]  # Example data


# Function to insert booking into seat_booking table
def insert_booking(new_booking_id, seat_number, booking_date, passenger_id, flight_id):
    booking_date = datetime.strptime(booking_date, "%Y-%m-%d")
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO seat_booking (booking_id, seat_number, booking_date, passenger_id, flight_id) VALUES (?, ?, ?, ?, ?)",
        (new_booking_id, seat_number, booking_date, passenger_id, flight_id),
    )
    conn.commit()
    c.close()
    conn.close()


def insert_passenger(passenger_name, surname, email):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        # Get the maximum passenger ID
        cursor.execute("SELECT MAX(passenger_id) FROM passenger")
        max_passenger_id = cursor.fetchone()[0]
        
        # If the table is empty, set the max_passenger_id to 0
        if max_passenger_id is None:
            max_passenger_id = 0
        
        # Increment the max_passenger_id by 1
        new_passenger_id = max_passenger_id + 1
        
        # Insert the new passenger
        cursor.execute("INSERT INTO passenger (passenger_id, passenger_name, surname, email) VALUES (?,?,?,?)",
                       (new_passenger_id, passenger_name, surname, email))
        conn.commit()
        
        return new_passenger_id
    except Exception as e:
        st.error(f"Error inserting passenger: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
        
        
def fetch_passengers():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT passenger_id, passenger_name, surname FROM passenger")
    passengers = c.fetchall()
    c.close()
    conn.close()
    return passengers

def fetch_data_as_df(table_name):
    conn = get_connection()
    c = conn.cursor()
    # c.execute(f"SELECT * FROM {table_name}")
    if table_name == "flight":
        c.execute("""
            SELECT f.flight_id, f.flight_number, a1.airport_name AS departure_airport, 
                       a2.airport_name AS destination_airport, f.departure_date_time, 
                       f.arrival_date_time
            FROM flight f
            INNER JOIN airport a1 ON f.departure_airport_id = a1.airport_id
            INNER JOIN airport a2 ON f.destination_airport_id = a2.airport_id
        """)
    else:
        c.execute(f"SELECT * FROM {table_name}")
    data = c.fetchall()
    columns = [description[0] for description in c.description]
    df = pd.DataFrame([list(row) for row in data], columns=columns)
    c.close()
    conn.close()
    return df

# Fetch existing passengers
# passengers = fetch_passengers()
# passenger_options = {f"{passenger[1]} {passenger[2]} ({passenger[0]})": passenger[0] for passenger in passengers}

# Display select box for passengers
# selected_passenger = st.selectbox('Select Passenger', list(passenger_options.keys()))

# if selected_passenger:
#     passenger_id = passenger_options[selected_passenger]

# Fetch flights
flight_df = fetch_data_as_df("flight")
st.write("### Flight Data")
st.dataframe(flight_df)
flights = fetch_flights()
flight_options = {flight[1]: flight[0] for flight in flights}
selected_flight = st.selectbox("Select Flight", list(flight_options.keys()))


if selected_flight:
    # Fetch available seats for the selected flight
    airplane_id = flight_options[selected_flight]  # This should be updated based on your data schema
    available_seats = fetch_available_seats(airplane_id)
    selected_seat = st.selectbox("Select Seat", available_seats)
    # available_seats = fetch_available_seats(flight_options[selected_flight])
    # seat_options = [seat[0] for seat in available_seats]
    # selected_seat = st.selectbox("Select Seat", seat_options)

    # Option to create new passenger
    st.subheader("Passenger Information")
    create_new_passenger = st.checkbox("Create New Passenger")

    if create_new_passenger:
        # Form to create new passenger
        st.subheader("Create New Passenger")
        # passenger_id = st.number_input("Passenger ID", min_value=1, step=1, value=1)
        passenger_name = st.text_input("Passenger Name")
        surname = st.text_input("Surname")
        email = st.text_input("Email")

        if passenger_name and surname and email:
            passenger_id = insert_passenger(passenger_name, surname, email)
            if passenger_id:
                st.success(f"Passenger {passenger_name} created with ID: {passenger_id}")
            else:
                st.warning("Failed to create passenger.")
        else:
            st.warning("Please fill in all fields to create the passenger.")
    else:
        st.subheader("Select Existing Passenger")
        passengers = fetch_passengers()
        passenger_options = {
            f"{passenger[1]} {passenger[2]} ({passenger[0]})": passenger[0]
            for passenger in passengers
        }
        selected_passenger = st.selectbox(
            "Select Passenger", list(passenger_options.keys())
        )
        # Select existing passenger
        if selected_passenger:
            passenger_id = passenger_options[selected_passenger]
            st.info(f"Selected Passenger ID: {passenger_id}")

        # passenger_id = st.number_input('Passenger ID', min_value=1, max_value=20, step=1)

    # Display passenger selection (optional, you can also input new passenger details)
    # passenger_id = st.number_input('Passenger ID', min_value=1, max_value=20, step=1)

    # Booking date input
    booking_date = st.date_input("Booking Date")

    # Submit button
    if st.button("Book Seat"):
        conn = get_connection()
        c = conn.cursor()
                # Get the maximum passenger ID
        c.execute("SELECT MAX(booking_id) FROM seat_booking")
        max_booking_id = c.fetchone()[0]
        
        # If the table is empty, set the max_passenger_id to 0
        if max_booking_id is None:
            max_booking_id = 0
        
        # Increment the max_passenger_id by 1
        new_booking_id = max_booking_id + 1

        insert_booking(
            new_booking_id,
            selected_seat,
            booking_date.strftime("%Y-%m-%d"),
            passenger_id,
            flight_options[selected_flight],
        )
        st.success("Booking successful!")

# Close database connectionconn.close()
