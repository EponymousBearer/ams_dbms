import streamlit as st
import pyodbc
import pandas as pd


# Function to check database connection
def check_db_connection():
    try:
        # Establish a connection to the SQL Server database
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-O16J5JA;"  # Replace with your server name
            "DATABASE=Airport_Management_System;"  # Replace with your database name
        )
        c = conn.cursor()

        conn.close()
        return True
    except pyodbc.Error as e:
        st.error(f"Database connection failed: {e}")
        return False


# Title
st.title("Airport Management System")

# Check database connection
if check_db_connection():
    st.success("Database is connected!")

    # Select an airport
    st.header("Select Airport")
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-O16J5JA;"
        "DATABASE=Airport_Management_System;"
    )
    c = conn.cursor()

    def display_airline_fleets(selected_airport):
        st.header(f"Airline Fleets at {selected_airport}")

        # Fetch airport ID based on selected airport name
        c.execute(
            "SELECT airport_id FROM airport WHERE airport_name = ?", (selected_airport,)
        )
        airport_id = c.fetchone()[0]

        # Fetch airline fleets for the selected airport
        c.execute("SELECT * FROM airline_fleet WHERE airport_id = ?", (airport_id,))
        fleets = c.fetchall()

        # Check if there are any fleets to display
        if fleets:
            columns = [description[0] for description in c.description]
            df = pd.DataFrame([list(row) for row in fleets], columns=columns)
            st.table(df)
        else:
            st.write("No airline fleets found for the selected airport.")

    # Fetch all airport names for the dropdown selection
    c.execute("SELECT airport_name FROM airport")
    airports = c.fetchall()
    airport_options = [airport[0] for airport in airports]

    # Select an airport using Streamlit selectbox
    selected_airport = st.selectbox("Choose an airport", airport_options)

    if selected_airport:
        display_airline_fleets(selected_airport)

    st.header("Select Airline Fleet")
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-O16J5JA;"
        "DATABASE=Airport_Management_System;"
    )
    c = conn.cursor()

    def display_airplanes(selected_airline_fleet):
        st.header(f"Airplanes at {selected_airline_fleet}")

        # Fetch airport ID based on selected airport name
        c.execute(
            "SELECT airline_fleet_id FROM airline_fleet WHERE airline_name = ?",
            (selected_airline_fleet,),
        )
        airline_fleet_id = c.fetchone()[0]

        # Fetch airline fleets for the selected airport
        c.execute(
            "SELECT * FROM airplane WHERE airline_fleet_id = ?", (airline_fleet_id,)
        )
        fleets = c.fetchall()

        # Check if there are any fleets to display
        if fleets:
            columns = [description[0] for description in c.description]
            df = pd.DataFrame([list(row) for row in fleets], columns=columns)
            st.table(df)
        else:
            st.write("No airplane found for the selected airline fleet.")

    # Fetch all airport names for the dropdown selection
    c.execute("SELECT airline_name FROM airline_fleet")
    airline_fleets = c.fetchall()
    airline_fleet_options = [airline_fleet[0] for airline_fleet in airline_fleets]

    # Select an airport using Streamlit selectbox
    selected_airline_fleet = st.selectbox(
        "Choose an airline fleet", airline_fleet_options
    )

    if selected_airline_fleet:
        display_airplanes(selected_airline_fleet)

    st.header("Select Passenger")
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-O16J5JA;"
        "DATABASE=Airport_Management_System;"
    )
    c = conn.cursor()

    def display_booking(selected_passenger):
        st.header(
            f"Seat Bookings for Passenger {selected_passenger['passenger_name']} (ID: {selected_passenger['passenger_id']})"
        )

        # Create a cursor object
        c = conn.cursor()

        # Fetch passenger ID based on selected passenger ID
        c.execute(
            "SELECT * FROM seat_booking WHERE passenger_id = ?",
            (selected_passenger["passenger_id"],),
        )
        bookings = c.fetchall()

        # Check if there are any bookings to display
        if bookings:
            columns = [description[0] for description in c.description]
            df = pd.DataFrame([list(row) for row in bookings], columns=columns)
            st.table(df)
        else:
            st.write("No bookings found for the selected passenger.")

    # Fetch all airport names for the dropdown selection
    c.execute("SELECT passenger_id, passenger_name FROM passenger")
    passengers = c.fetchall()
    passenger_options = [
        {"passenger_id": passenger[0], "passenger_name": passenger[1]}
        for passenger in passengers
    ]

    # Select a passenger using Streamlit selectbox
    selected_passenger = st.selectbox(
        "Choose a passenger",
        passenger_options,
        format_func=lambda passenger: f"{passenger['passenger_id']} - {passenger['passenger_name']}",
    )

    if selected_passenger:
        display_booking(selected_passenger)

    # Select an airplane
    st.header("Select Flight")

    c.execute("SELECT flight_id FROM flight")
    flights = c.fetchall()
    flight_options = [flight[0] for flight in flights]
    selected_flight = st.selectbox("Choose an flight", flight_options)

    def fetch_data_as_df(table_name):
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-O16J5JA;"  # Replace with your server name
            "DATABASE=Airport_Management_System;"  # Replace with your database name
        )
        c = conn.cursor()
        c.execute(f"SELECT * FROM {table_name}")
        data = c.fetchall()
        columns = [description[0] for description in c.description]
        df = pd.DataFrame([list(row) for row in data], columns=columns)
        conn.close()
        return df

    flight_df = fetch_data_as_df("flight")

    # Display dataframes
    st.write("### Flight Data")
    st.dataframe(flight_df)

    # Function to fetch booking data for a specific passenger
    def fetch_booking_data(passenger_id):
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=DESKTOP-O16J5JA;"  # Replace with your server name
            "DATABASE=Airport_Management_System;"  # Replace with your database name
        )
        c = conn.cursor()
        c.execute("SELECT * FROM seat_booking WHERE passenger_id = ?", (passenger_id,))
        booking_data = c.fetchall()
        conn.close()
        columns = [description[0] for description in c.description]
        df = pd.DataFrame([list(row) for row in booking_data], columns=columns)
        return df

    # Fetch data from tables
    flight_df = fetch_data_as_df("flight")
    passenger_df = fetch_data_as_df("passenger")
    booking_df = fetch_data_as_df("seat_booking")
    staff_df = fetch_data_as_df("staff")

    # Display dataframes
    st.write("### Flight Data")
    st.dataframe(flight_df)

    st.write("### Passenger Data")
    st.dataframe(passenger_df)

    st.write("### Booking Data")
    st.dataframe(booking_df)

    st.write("### Staff Data")
    st.dataframe(staff_df)

    # Adding interactivity
    st.sidebar.title("Filter Data")

    # Filter flight data based on departure airport
    departure_airports = st.sidebar.multiselect(
        "Filter by Departure Airport", flight_df["departure_airport_id"].unique()
    )
    filtered_flights = flight_df[
        flight_df["departure_airport_id"].isin(departure_airports)
    ]
    st.write("### Filtered Flight Data")
    st.dataframe(filtered_flights)

    # Search for a specific passenger
    search_query = st.sidebar.text_input("Search for Passenger", "")
    search_result = passenger_df[
        passenger_df.apply(
            lambda row: search_query.lower() in row.astype(str).str.lower().values,
            axis=1,
        )
    ]
    st.write("### Search Results for Passenger")
    st.dataframe(search_result)

    # Select an Passenger
    st.header("Select Passenger")
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-O16J5JA;"  # Replace with your server name
        "DATABASE=Airport_Management_System;"  # Replace with your database name
    )
    c = conn.cursor()
    c.execute("SELECT passenger_id FROM passenger")
    passengers = c.fetchall()
    passenger_options = [passenger[0] for passenger in passengers]
    selected_passenger = st.selectbox("Choose a passenger", passenger_options)

    # Fetch and display passenger data
    passenger_df = fetch_data_as_df("passenger")
    st.write("### Passenger Data")
    st.dataframe(passenger_df)

    # Fetch and display booking data for the selected passenger
    if selected_passenger:
        st.header(f"Booking Data for Passenger ID: {selected_passenger}")
        booking_df = fetch_booking_data(selected_passenger)
        st.dataframe(booking_df)

    conn.close()
else:
    st.error("Failed to connect to the database.")
