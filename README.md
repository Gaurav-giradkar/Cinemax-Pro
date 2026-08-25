# 🎬 CINEMAX PRO

<p align="center">
  <strong>A full-stack movie ticket booking system built with Flask and MySQL.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5">
  <img src="https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
</p>

---

## 🍿 Overview

**Cinemax Pro** is a web-based movie ticket booking platform that simulates the complete cinema booking workflow.

Users can:

* Create an account and log in
* Browse available movies
* Select a movie show
* Choose a date
* Select available seats
* View dynamically calculated pricing
* Confirm a booking
* Receive a booking confirmation/receipt

The application uses **Flask** for the backend, **MySQL** for persistent data storage, and a modular Blueprint-based architecture to separate authentication, movies, shows, seats, and bookings.

---

## ✨ Features

### 🔐 User Authentication

Users can create accounts and securely log in.

* Signup with username, email, mobile number, and password
* Password hashing using Werkzeug
* Session-based authentication
* Protected booking routes
* Logout functionality
* Automatic logged-in-user loading

Passwords are stored using Werkzeug's password hashing utilities rather than plain text.

---

### 🎥 Movie Discovery

The home page retrieves movies directly from MySQL.

Each movie contains:

* Title
* Genre
* Rating
* Poster

The project includes sample movies such as:

* Dune: Part Two
* Oppenheimer
* The Batman
* Inception
* Interstellar

---

### 🕐 Show Selection

After selecting a movie, users can browse available cinema shows.

The system organizes shows by:

* Theatre
* Showtime
* Selected date

Supported sample theatres include:

* PVR Cinemas
* INOX
* Cinepolis

---

### 📅 Date-Based Booking

Users can select the booking date before choosing their seats.

The application is designed around date-specific seat availability, meaning a seat booked for one show/date combination does not automatically become unavailable for another date.

---

### 💺 Interactive Seat Selection

The booking flow provides seat-level selection.

Each show has:

```text
10 rows × 10 seats
```

for a total of:

```text
100 seats per show
```

Seat pricing varies by row.

| Rows | Price |
| ---- | ----: |
| A–D  |  ₹150 |
| E–H  |  ₹200 |
| I–J  |  ₹250 |

Users can select up to **10 seats per booking**.

---

### 🚫 Double-Booking Prevention

Before creating a booking, Cinemax Pro checks whether selected seats have already been booked for the requested show and date.

```text
User selects seats
       ↓
Check existing bookings
       ↓
Already booked?
   ↙          ↘
 YES           NO
  ↓             ↓
Reject       Calculate
booking       price
                ↓
          Create booking
                ↓
          Reserve seats
```

This prevents the application from accepting seats that are already associated with an existing booking for that show/date.

---

### 💰 Automatic Price Calculation

The backend retrieves the prices of selected seats from MySQL and calculates the total automatically.

```text
Seat A1  → ₹150
Seat A2  → ₹150
Seat I1  → ₹250
             ─────
Total    → ₹550
```

The calculated amount is stored with the booking.

---

### 🎟️ Booking Confirmation

After a successful booking, the system generates a unique booking identifier and displays a confirmation page containing:

* Movie
* Theatre
* Showtime
* Booking ID
* Selected seats
* Total price

---

## 🏗️ Architecture

Cinemax Pro follows a modular Flask application structure.

```text
                    ┌─────────────────────┐
                    │       Browser       │
                    │  HTML / CSS / JS    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Flask App      │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
       Authentication       Movies / Shows    Bookings
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     MySQL Database  │
                    └─────────────────────┘
```

### Application Modules

| Module        | Responsibility                        |
| ------------- | ------------------------------------- |
| `auth.py`     | Signup, login, logout, authentication |
| `movies.py`   | Movie listing                         |
| `shows.py`    | Show and theatre selection            |
| `seats.py`    | Seat availability and selection       |
| `bookings.py` | Booking creation and confirmation     |
| `db.py`       | MySQL connection management           |

---

## 🧩 Tech Stack

### Backend

* Python
* Flask 3.0.3
* Werkzeug 3.0.3
* MySQL Connector/Python

### Frontend

* HTML5
* CSS3
* Vanilla JavaScript
* Jinja2 templates

### Database

* MySQL

### Configuration

* `python-dotenv`

---

## 📁 Project Structure

```text
Cinemax-Pro/
│
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── bookings.py
│   ├── db.py
│   ├── movies.py
│   ├── seats.py
│   ├── shows.py
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │       └── main.js
│   │
│   └── templates/
│       ├── base.html
│       │
│       ├── auth/
│       │   ├── login.html
│       │   └── signup.html
│       │
│       ├── bookings/
│       │   └── confirmation.html
│       │
│       ├── movies/
│       │   └── index.html
│       │
│       ├── seats/
│       │   └── selection.html
│       │
│       └── shows/
│           └── selection.html
│
├── requirements.txt
├── run.py
├── setup_db.py
├── schema.sql
├── .gitignore
└── README.md
```

---

## 🗄️ Database Design

The application uses MySQL as its primary persistence layer.

The core entities are:

```text
Users
  │
  │
  ▼
Bookings ──────── Shows ──────── Movies
  │                │
  │                │
  ▼                ▼
Booking Seats    Theatres
  │
  ▼
Seats
```

### Main Tables

| Table           | Purpose                        |
| --------------- | ------------------------------ |
| `users`         | Registered users               |
| `movies`        | Movie information              |
| `theatres`      | Cinema/theatre information     |
| `shows`         | Movie showtimes                |
| `seats`         | Seats assigned to shows        |
| `bookings`      | Booking records                |
| `booking_seats` | Seats associated with bookings |

---

## ⚙️ Requirements

Before running the project, install:

* Python 3.x
* MySQL Server
* pip

Verify Python:

```bash
python --version
```

Verify pip:

```bash
pip --version
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Cinemax-Pro
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Setup

Cinemax Pro requires a local MySQL database.

The default configuration currently expects:

```text
Host:     127.0.0.1
User:     root
Password: root123
Database: cinemax_pro
```

> **Do not use these hardcoded credentials in a production deployment.** Move database credentials into environment variables.

### Initialize the database

Run:

```bash
python setup_db.py
```

The setup script creates and populates the database with:

* Sample movies
* Theatres
* Shows
* Seats

---

## ▶️ Run the Application

Start the Flask development server:

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000
```

---

## 🔄 Booking Flow

The complete user journey is:

```text
        HOME
          │
          ▼
   Select a Movie
          │
          ▼
   Select a Show
          │
          ▼
    Select a Date
          │
          ▼
    Select Seats
          │
          ▼
  Validate Availability
          │
          ▼
   Calculate Total
          │
          ▼
   Create Booking
          │
          ▼
 Booking Confirmation
```

---

## 🔐 Authentication Flow

```text
Signup
  ↓
Password Hashing
  ↓
MySQL User Record
  ↓
Login
  ↓
Password Verification
  ↓
Session Created
  ↓
Protected Booking Routes
```

Unauthenticated users are redirected to the login page when attempting to access protected routes.

---

## 🌐 Application Routes

### Authentication

| Method     | Endpoint       | Purpose                 |
| ---------- | -------------- | ----------------------- |
| `GET/POST` | `/auth/signup` | Register a user         |
| `GET/POST` | `/auth/login`  | Authenticate a user     |
| `GET`      | `/auth/logout` | End the current session |

### Movies

| Method | Endpoint | Purpose       |
| ------ | -------- | ------------- |
| `GET`  | `/`      | Browse movies |

### Shows

| Method | Endpoint            | Purpose              |
| ------ | ------------------- | -------------------- |
| `GET`  | `/shows/<movie_id>` | Select show and date |

### Seats

| Method | Endpoint           | Purpose                     |
| ------ | ------------------ | --------------------------- |
| `GET`  | `/seats/<show_id>` | View/select available seats |

### Bookings

| Method | Endpoint                           | Purpose                   |
| ------ | ---------------------------------- | ------------------------- |
| `POST` | `/bookings/confirm`                | Create booking            |
| `GET`  | `/bookings/receipt/<booking_uuid>` | View booking confirmation |

---

## 🧠 Key Engineering Concepts

### Flask Blueprints

The application separates functionality into independent Flask Blueprints:

```python
auth
movies
shows
seats
bookings
```

This avoids putting the entire application inside a single Flask file and makes individual modules easier to maintain.

---

### Password Security

Passwords are never stored directly.

The application uses:

```python
generate_password_hash()
check_password_hash()
```

from Werkzeug for password hashing and verification.

---

### Session Authentication

After successful login:

```python
session['user_id'] = user['id']
```

The application uses this session to identify the current user and restrict booking-related functionality.

---

### Transaction Handling

Booking operations use database transactions.

If an error occurs:

```python
db.rollback()
```

If the operation succeeds:

```python
db.commit()
```

This prevents partially completed bookings from being persisted.

---

## ⚠️ Current Limitations

This is a functional project implementation, not a production cinema platform.

Current limitations include:

* Database credentials are currently hardcoded in `app/db.py`.
* Flask's secret key is hardcoded.
* Payment processing is not implemented.
* There is no admin dashboard.
* Movie/show management is not available through the UI.
* Booking cancellation is not implemented.
* Seat availability relies on application-level validation.
* No production-grade connection pooling is configured.
* No automated test suite is currently included.
* The application runs using Flask's development server by default.

---

## 🔮 Future Improvements

### User Features

* [ ] Booking history
* [ ] Ticket cancellation
* [ ] Email confirmation
* [ ] Digital ticket / QR code
* [ ] User profile
* [ ] Multiple payment methods

### Cinema Management

* [ ] Admin dashboard
* [ ] Add/edit/delete movies
* [ ] Manage theatres
* [ ] Create and modify shows
* [ ] Seat layout management
* [ ] Revenue analytics

### Backend

* [ ] Environment-based configuration
* [ ] Database connection pooling
* [ ] Production WSGI deployment
* [ ] API layer
* [ ] Automated testing
* [ ] Improved transaction-level seat locking

---

## 📸 Screenshots

Add screenshots from the actual application here:

```text
docs/
└── screenshots/
    ├── home.png
    ├── login.png
    ├── movies.png
    ├── show-selection.png
    ├── seat-selection.png
    └── booking-confirmation.png
```

Example:

```markdown
![Movie Selection](docs/screenshots/movies.png)

![Seat Selection](docs/screenshots/seat-selection.png)

![Booking Confirmation](docs/screenshots/booking-confirmation.png)
```

---

## 🎯 Project Objective

Cinemax Pro was built to demonstrate the implementation of a complete transactional web application using:

**Flask + MySQL + Authentication + Database Relationships + Seat Allocation + Booking Logic**

The project focuses on understanding how a real-world booking workflow can be modeled and implemented from the frontend through the backend and database.

---

## 👨‍💻 Author

**Gaurav Giradkar**

Full-Stack Development · Python · Flask · Database Systems

---

<p align="center">

### 🎬 CINEMAX PRO

**Choose a movie. Pick your seats. Book your experience.**

</p>
