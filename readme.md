# Django Google Drive & WebSocket Project



This project is a Django backend application that integrates:
- **Google OAuth 2.0 Authentication**: Users sign in with Google.
- **Google Drive Integration**: Upload and download files from Google Drive.
- **WebSocket Chat**: Real-time communication using Django Channels.

The project is built with Django 5.1.6, Django REST Framework, Channels, and integrates with Google APIs.

---

## Features

- **Google OAuth Flow**:  
  - **/auth/google/**: Redirects users to the Google OAuth consent screen.  
  - **/auth/google/callback/**: Exchanges the authorization code for tokens.

- **Google Drive API**:  
  - **/drive/upload/**: Accepts file uploads via POST (using form-data) and uploads them to Google Drive.
  - **/drive/download/**: Downloads a file from Google Drive and returns it as a file response.

- **WebSocket Chat**:  
  - **/ws/chat/**: Provides real-time chat functionality using WebSocket connections.

---

## Prerequisites

- Python 3.8+
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo



1. Log in to Google Cloud Console
Go to Google Cloud Console and sign in with your Google account.
2. Create or Select a Project
In the top navigation bar, click on the project dropdown and either select an existing project or click "NEW PROJECT" to create a new one.
If you create a new project, give it a name (e.g., "Django Google Drive Project") and click "Create".
3. Configure the OAuth Consent Screen
Before creating credentials, you need to configure the OAuth consent screen:

Navigate to the OAuth Consent Screen:

In the left-hand menu, go to "APIs & Services" and click "OAuth consent screen".
Select User Type:

Choose "External" if your app will be used by users outside your organization, or "Internal" if it's only for users within your Google Workspace domain.
Click "Create".
Fill in App Information:

App name: Provide a name for your app (e.g., "Django Google Drive").
User support email: Choose an email where users can contact you.
App logo: (Optional) Upload a logo.
Click "Next" after filling in these details.
Scopes:

You can add scopes now or later. For basic user info and Google Drive access, add the following scopes:
https://www.googleapis.com/auth/userinfo.email
https://www.googleapis.com/auth/userinfo.profile
https://www.googleapis.com/auth/drive.file
Click "Next".
Test Users:

If your app is in testing mode, add the email addresses of the users allowed to test the app.
Click "Save and Continue".
Review and Back to Dashboard:

Your OAuth consent screen is now set up. You can always come back to modify it if needed.
4. Create OAuth 2.0 Credentials (Client ID and Client Secret)
Navigate to Credentials:

In the left-hand menu, go to "APIs & Services" and then click "Credentials".
Create Credentials:

Click the "Create Credentials" button at the top.
Select "OAuth client ID".
Configure the OAuth Client ID:

Application Type: Choose "Web application".
Name: Give your client a name (e.g., "Django Web Client").
Authorized JavaScript origins: For local development, add:
arduino
Copy
Edit
http://localhost:8000
Authorized redirect URIs: Add the redirect URI that your app will use. For example, for local development:
bash
Copy
Edit
http://localhost:8000/auth/google/callback/
Make sure this exactly matches the URI in your Django settings.
Create and Retrieve Your Credentials:

Click "Create".
A dialog will appear showing your Client ID and Client Secret. Copy these values; you'll use them in your Django project's settings (ideally via environment variables).
5. Update Your Project Settings
Save your credentials in a secure manner. For example, using a .env file and python-dotenv:
env
Copy
Edit
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback/
Load these variables in your settings.py as described earlier.



after cloning and setting up the details in .env file then install the requirements and run the server

pip install -r requirements.txt && python manage.py migrate


daphne -b 127.0.0.1 -p 8000 myproject.asgi:application





all the endpoints
for the websocket   wss://nine0north-r9id.onrender.com/ws/chat/

for the authentication  https://nine0north-r9id.onrender.com/auth/google

for the upload after getting the token -  https://nine0north-r9id.onrender.com/drive/upoad/
in the body send the token and file as form data

for the download  https://nine0north-r9id.onrender.com/drive/download/
in the body send the token and file id as form data

