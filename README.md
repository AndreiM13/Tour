
AllThingsSocotra is a web-based application designed to manage and display virtual tours. Built with Python for the backend and HTML/CSS and JavaScript for the frontend, it offers functionalities to add new tours,
rebuild the tour database, and run the application server.

📂 Project Structure
```
Tour/
├── app/                # Main application code
├── add_tour.py         # Script to add new tours
├── rebuilddb.py        # Script to rebuild or initialise the database
├── run.py              # Script to start the application server
├── countries.json      # JSON file containing country data
├── requirements.txt    # Python dependencies
|── render.yaml
└── .gitignore          # Git ignore file
```
🚀 Getting Started
Prerequisites
Python 3.x

pip (Python package installer)

Virtual environment tool 

Installation
Clone the repository:
```
git clone https://github.com/AndreiM13/Tour.git
cd Tour

```
Create and activate a virtual environment (optional):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
Install the required dependencies:
```
pip install -r requirements.txt
```
Running the Application

Initialise or rebuild the database:
```
python rebuilddb.py
```
Add information to the database:
```
python add_tour.py
```
Start the application server:

```
python run.py
```

Access the application:
Open your web browser and navigate to http://localhost:5000

🛠️ Features
Add New Tours: Use add_tour.py to add new tours to the database.

Database Management: Utilise rebuilddb.py to initialise or reset the tour database.

Country Association: countries.json contains country data associated with tours.

Web Interface: Run the application using run.py and interact through a web browser.
LinkedIn

📄 License
All rights reserved to AllThingsSocotra.
This project does not currently specify an open-source license. Please get in touch with the repository owner for more information regarding usage and distribution.

