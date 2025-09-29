import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect('MovieTicketSystem.db')
cursor = conn.cursor()
print("Database opened successfully")

# Drop tables if they exist to avoid errors when re-running
tables = ['Movie', 'Theatre', 'Seats', 'Admin', 'Customer', 'Show', 'Tickets', 'Discount']
for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Create Movie table
cursor.execute('''
CREATE TABLE Movie (
    m_id INTEGER PRIMARY KEY,
    m_name TEXT NOT NULL,
    release_date TEXT,
    director TEXT,
    actors TEXT
)
''')

# Create Theatre table
cursor.execute('''
CREATE TABLE Theatre (
    tid INTEGER PRIMARY KEY,
    tname TEXT NOT NULL,
    location TEXT
)
''')

# Create Admin table
cursor.execute('''
CREATE TABLE Admin (
    admin_id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
)
''')

# Create Seats table
cursor.execute('''
CREATE TABLE Seats (
    seat_id INTEGER PRIMARY KEY,
    seat_name TEXT NOT NULL,
    no_of_seats INTEGER,
    theatre_id INTEGER,
    FOREIGN KEY (theatre_id) REFERENCES Theatre(tid)
)
''')

# Create Show table
cursor.execute('''
CREATE TABLE Show (
    show_id INTEGER PRIMARY KEY,
    st_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    language TEXT,
    movie_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES Movie(m_id)
)
''')

# Create Customer table
cursor.execute('''
CREATE TABLE Customer (
    cid INTEGER PRIMARY KEY,
    c_name TEXT NOT NULL,
    password TEXT NOT NULL,
    email_id TEXT UNIQUE,
    phone_no TEXT
)
''')

# Create Discount table
cursor.execute('''
CREATE TABLE Discount (
    offer_id INTEGER PRIMARY KEY,
    m_name TEXT NOT NULL,
    price REAL NOT NULL
)
''')

# Create Tickets table
cursor.execute('''
CREATE TABLE Tickets (
    ticket_no INTEGER PRIMARY KEY,
    show_id INTEGER,
    show_date TEXT,
    seat_no TEXT,
    price REAL,
    hall_no INTEGER,
    tid INTEGER,
    admin_id INTEGER,
    booking_date TEXT,
    customer_id INTEGER,
    FOREIGN KEY (show_id) REFERENCES Show(show_id),
    FOREIGN KEY (tid) REFERENCES Theatre(tid),
    FOREIGN KEY (admin_id) REFERENCES Admin(admin_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(cid)
)
''')

print("Tables created successfully")

# Let's insert some sample data

# Insert sample movie data
movies = [
    (1, 'Inception', '2010-07-16', 'Christopher Nolan', 'Leonardo DiCaprio, Ellen Page'),
    (2, 'The Godfather', '1972-03-24', 'Francis Ford Coppola', 'Marlon Brando, Al Pacino'),
    (3, 'Parasite', '2019-10-11', 'Bong Joon-ho', 'Song Kang-ho, Lee Sun-kyun')
]

cursor.executemany("INSERT INTO Movie VALUES (?, ?, ?, ?, ?)", movies)

# Insert sample theatre data
theatres = [
    (1, 'Cinema Paradise', 'Downtown'),
    (2, 'Royal Screens', 'West Avenue'),
    (3, 'Star Cineplex', 'East Mall')
]

cursor.executemany("INSERT INTO Theatre VALUES (?, ?, ?)", theatres)

# Insert admin data
admins = [
    (101, 'admin123'),
    (102, 'secure456')
]

cursor.executemany("INSERT INTO Admin VALUES (?, ?)", admins)

# Insert seats data
seats = [
    (1, 'Regular', 100, 1),
    (2, 'Premium', 50, 1),
    (3, 'Regular', 120, 2),
    (4, 'VIP', 30, 3)
]

cursor.executemany("INSERT INTO Seats VALUES (?, ?, ?, ?)", seats)

# Insert show data
shows = [
    (1, '18:00', '20:30', 'English', 1),
    (2, '15:30', '18:00', 'English', 2),
    (3, '20:00', '22:30', 'Korean', 3)
]

cursor.executemany("INSERT INTO Show VALUES (?, ?, ?, ?, ?)", shows)

# Insert customer data
customers = [
    (201, 'John Smith', 'pass123', 'john@example.com', '555-1234'),
    (202, 'Sarah Jones', 'secure789', 'sarah@example.com', '555-5678'),
    (203, 'Mike Brown', 'pwdmike', 'mike@example.com', '555-9012')
]

cursor.executemany("INSERT INTO Customer VALUES (?, ?, ?, ?, ?)", customers)

# Insert discount data
discounts = [
    (301, 'Tuesday Special', 5.00),
    (302, 'Student Discount', 3.50)
]

cursor.executemany("INSERT INTO Discount VALUES (?, ?, ?)", discounts)

# Insert tickets data
tickets = [
    (401, 1, '2025-04-15', 'A1,A2', 20.00, 1, 1, 101, '2025-04-14', 201),
    (402, 2, '2025-04-16', 'B5', 15.00, 2, 2, 101, '2025-04-14', 202),
    (403, 3, '2025-04-15', 'C3,C4,C5', 45.00, 3, 3, 102, '2025-04-13', 203)
]

cursor.executemany("INSERT INTO Tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", tickets)

conn.commit()
print("Sample data inserted successfully")

# Display sample data from each table
print("\nMovies:")
cursor.execute("SELECT * FROM Movie")
for row in cursor.fetchall():
    print(row)

print("\nTheatres:")
cursor.execute("SELECT * FROM Theatre")
for row in cursor.fetchall():
    print(row)

print("\nTickets:")
cursor.execute("SELECT * FROM Tickets")
for row in cursor.fetchall():
    print(row)

print("\nCustomers:")
cursor.execute("SELECT * FROM Customer")
for row in cursor.fetchall():
    print(row)

# Example query: Get all tickets booked by a specific customer
print("\nTickets booked by Customer 201:")
cursor.execute("""
SELECT t.ticket_no, m.m_name, t.show_date, t.seat_no, th.tname
FROM Tickets t
JOIN Show s ON t.show_id = s.show_id
JOIN Movie m ON s.movie_id = m.m_id
JOIN Theatre th ON t.tid = th.tid
WHERE t.customer_id = 201
""")
for row in cursor.fetchall():
    print(row)

conn.close()
print("\nDatabase operations completed and connection closed.")