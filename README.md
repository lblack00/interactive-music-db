# Pass the Aux

## Features

- Users can search for favorite artists and songs, post and view user-generated reviews, and explore accurate details about songs and albums, such as title, duration, writing credits, label, and country of origin
- The platform features up-to-date album release countdowns and text-based forums, where forum content can be moderated through an admin dashboard
- Spotify playlists can be loaded and played via OAuth

## Dependencies

Before setting up the project, ensure you have the following installed:

- [Python 3.6+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [PostgreSQL 13](https://www.postgresql.org/download/)
- [Node.js and npm](https://nodejs.org/en/download/)

## macOS Users

If you're using macOS, you can install the prerequisites using Homebrew:
```
brew install python3
brew install postgresql@13
brew install libpq
brew install openssl@3
brew install node
```
Note: To start the PostgreSQL service:
```
brew services start postgresql@13
```

## Windows Users

For Windows users, it's recommended to use the [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install) and install the dependencies with the native package manager.

## Installation
### Backend Setup

1. Clone the repository:
```
git clone https://github.com/lblack00/interactive-music-db.git
cd interactive-music-db
```

2. Create and activate a virtual environment:
```
python3 -m venv .env
source .env/bin/activate
```

3. Install Python dependencies:
```
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the `client` directory:
```
cd client
```

2. Install Node.js dependencies:
```
npm install
```

## Running the Application

You'll need two terminal windows or tabs to run the backend and frontend concurrently.
### Start the Backend

1. Activate the virtual environment (if not already active):
```
source ../.env/bin/activate
```

Navigate to the server directory and run the Flask application:
```
cd ../server
python3 app.py
```

### Start the Frontend

2. Navigate to the client directory:
```
cd ../client
```

3. Start the React development server:
```
npm run dev
```

Once both servers are running, open your browser and navigate to [http://localhost:5173/release/367084](http://localhost:5173/release/367084) to view the release page for Nirvana's Nevermind album.

## Data Import

To populate the database with music data, you'll need to import data from Discogs using the [discogs-xml2db](https://github.com/philipmat/discogs-xml2db) tool.

Schemas to create the remaining tables can be found in `server/tests/init_dicogs.sql` and `server/tests/init_users.sql`
