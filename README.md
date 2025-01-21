# LiveChatFaceAuth

**LiveChatFaceAuth** is chat application that uses **facial recognition** for secure, password-free user authentication. It ensures privacy with **end-to-end encryption** and offers real-time communication through **WebSockets**. The application is built using **Django** for the backend and **MySQL** (or PostgreSQL) for the database. 

**Note**: While this app uses traditional **Web2** components, it is designed with an eye towards integrating **Web3** features in the future.

## Features:
- **Password-Free Authentication**: Secure login via facial recognition.
- **End-to-End Encryption**: All messages are encrypted, ensuring privacy.
- **Real-Time Messaging**: Powered by WebSocket for instant communication.
- **Open-Source**: Free for everyone to use, contribute, and customize.

---

## Project Setup

### Prerequisites

Ensure you have the following installed on your local machine:

1. **Python 3.x** (Preferably the latest stable version)
2. **Django 4.x** (or the version compatible with the app)
4. **MySQL** or **PostgreSQL** (Database for Django)

### 1. Clone the Repository

Clone the repository to your local machine:

``` bash
git clone https://github.com/zkzkGamal/LiveChatFaceAuth.git
cd LiveChatFaceAuth
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Usage
#### Authentication
Users will register their face via a webcam or image file.
The system then stores their facial embeddings for future authentication.
The app uses face_recognition to compare the facial features with the stored ones for secure login.

#### Real-Time Messaging
The app uses WebSockets for real-time chat between users. Messages will be sent instantly as they are typed, with no need to refresh the page.
