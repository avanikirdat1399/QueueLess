# QueueLess – Smart Queue Management System

**Your Time Matters. Skip The Wait.**

QueueLess is a student-focused smart queue management system designed to reduce waiting time at college service counters. Students can register, log in, generate digital tokens, track their queue position, and cancel active tokens through a simple web application.

## Features

- **Student Registration and Login:** Create an account and securely log in.
- **Digital Token Generation:** Generate a token for the required college service.
- **Queue Tracking:** View your token number, number of people ahead, and estimated waiting time.
- **Token Cancellation:** Cancel an active token when it is no longer required.
- **Multiple Services:** Supports three college services:
  - Administrative Office
  - Fees Counter
  - Student Section

## Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, Tailwind CSS, JavaScript |
| Backend | Python, FastAPI |
| Database | PostgreSQL (Supabase) |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Password Security | PBKDF2 Hashing |

## Project Structure

```text
QueueLess/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── auth_utils.py
│   │   ├── init_db.py
│   │   └── seed_data.py
│   ├── requirements.txt
│   └── test_db.py
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── app.js
│   │   ├── auth.js
│   │   └── dashboard.js
│   ├── index.html
│   ├── auth.html
│   └── dashboard.html
│
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/avanikirdat1399/QueueLess.git
```

### 2. Open the Project Folder

```bash
cd QueueLess
```

### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file inside the `backend` folder.

Add your PostgreSQL database connection URL and JWT secret using the environment variable names expected by the backend configuration.

**Important:** Never upload your `.env` file or expose database credentials and secret keys on GitHub.

### 6. Initialize the Database

Configure your Supabase PostgreSQL database and run the database initialization and seed scripts as required.

### 7. Run the Application

From the main project folder, execute:

```bash
uvicorn backend.app.main:app --reload
```

Open the application in your browser:

```text
http://127.0.0.1:8000
```

## How It Works

1. A student opens the QueueLess website.
2. The student registers or logs in.
3. The student selects a college service.
4. A digital queue token is generated.
5. The dashboard displays the token number, people ahead, and estimated waiting time.
6. The student can cancel the active token if needed.

## Current Project Scope

QueueLess is a student-side prototype. Queue position and estimated waiting time are simulated using generated tokens. The estimated waiting time is calculated using five minutes per person ahead.

The current version does not include staff-side token calling, service completion, or a live counter-management system.

## Future Scope

- Staff-side queue management.
- Real-time token calling and service updates.
- Improved waiting-time estimation.
- Notifications when a student's turn approaches.
- Support for additional college services.

## Author

**Avani Kirdat**

Second Year – Computer Engineering

SIES Graduate School of Technology

---

*QueueLess – Making college queues simpler and more convenient.*
