# Ride Sharing RESTful API

## 📋 Description

This is a RESTful API built with Django REST Framework for managing Ride Sharing. It provides endpoints for user management and ride management.

## 🚀 Features

### Rider/Driver Management
- **User Creation**: Register new users.
- **Authentication**: Secure login using **JWT** (JSON Web Tokens).
- **Logout**: Secure logout functionality.

### Ride Management
- Rider can create a ride.
- Driver can view and accept from available rides.
- Rider/Driver can view their rides.
- Rider/Driver can change the ride status.
- Driver/Rider can track their ride.

## 🛠️ Technologies Used
- **Django REST Framework**
- **PostgreSQL**
- **Django Rest Framework SimpleJWT** for authentication.
- **LocationIQ** used for reverse geocoding and distance/time calculations.

## 🔧 Setup Instructions

### Prerequisites
- **Python 3.13+**
- **pip** (Python package installer)
- **venv** (for creating a virtual environment)
- **PostgreSQL** (For the database)
- **LocationIQ API key** (For using LocationIQ API)

### Installation Steps

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/arjunvjn/Ride-Sharing.git
    cd Ride-Sharing
    cd RideSharing
    ```

2. **Create and Activate a Virtual Environment:**

    ```bash
    # Create virtual environment
    python -m venv myenv

    # Activate virtual environment
    # On macOS/Linux:
    source myenv/bin/activate

    # On Windows (Command Prompt):
    myenv\Scripts\activate

    # On Windows (PowerShell):
    myenv\Scripts\Activate.ps1
    ```

3. **Install the Required Packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup the .env File:**

    Create a .env file in the root of your project (next to manage.py).

    ```bash
    # PostgreSQL settings
    DB_NAME=your-database-name
    DB_USER=your-database-user
    DB_PASSWORD=your-database-password
    DB_HOST=localhost
    DB_PORT=5432
	
    # LocationIQ API Key
    LOCATIONIQ_API_KEY=LOCATIONIQ-Access-Token
    ```

5. **Migrate the Database:**

    ```bash
    python manage.py migrate
    ```

6. **Run the Django Server:**

    ```bash
    python manage.py runserver
    ```

## 🧪 Running Tests

To run the tests, use:
 ```bash
    python manage.py test
```

## 📬 Postman Collection
Postman Documentation link - https://documenter.getpostman.com/view/20668961/2sB3BEmUzG
