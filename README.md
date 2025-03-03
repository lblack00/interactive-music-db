# Pass the Aux

Here’s what to download and stuff:

So first you’ll need Python3, pip, postgres and nodejs/npm

If you have a Mac, you can use homebrew to install via CLI:

`brew install python3` (pip3 comes with Python3, and if you already have python3 - no need to install)
`brew install postgresql@13`
`brew install libpq`
`brew install openssl@3` (requirement for Postgres that worked for me)
`brew install node`

Note: in order for any Postgres database to run (at least on Mac) you have to have the PostgreSQL service running. You can do this by running: `brew services start postgresql@13` and it’ll start a background process that allows the backend to communicate with Postgres databases

If you use Windows, I’m not sure how installation goes but Linux should be fairly similar just with `sudo apt-get install` instead.

You can use `git clone https://github.com/lblack00/interactive-music-db.git` to download the repository via CLI

After downloading the project repository, change the directory of wherever you downloaded it in a terminal.

I recommend creating a virtual environment in the root folder of the project directory with Python3.
Like `python3 -m venv .env` and then activate the virtual environment by doing `source .env/bin/activate` (it keeps the pip packages installed local to the virtual environment when active)

Then download the required python packages using: `pip3 install -r requirements.txt` and that should be it for the backend dependencies

To install the frontend dependencies:
`cd client`
`npm install`

For running the project files, you’ll need two terminal tabs or windows.

How to run the backend:
`cd <path-to-project-directory>/server`
`source ../.env/bin/activate` (activate virtual environment if you made one)
`python3 app.py`

How to run the frontend:
`cd <path-to-project-directory>/client`
`npm run dev`

Open “http://localhost:5173/release/367084” and you should see a release page for Nirvana - Nevermind
