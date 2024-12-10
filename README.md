

## SharBus Project Documentation  

### Overview  
SharBus is a web application designed to provide bus transportation information in Sharjah and the UAE. It allows users to explore bus routes, stops, schedules, and fares with an interactive and user-friendly interface.  

### Features  
- **Route Selection**: Users can select two locations, and the map displays the route between them.  
- **Comprehensive Bus Stops**: Shows all bus stops and pickup points in the UAE on the map.  
- **Bus Schedules**: Displays bus timings, bus numbers, fares, and destinations.  
- **Lightweight Design**: Does not include bookings, logins, or real-time updates for simplicity.  

---

### Tech Stack  
- **Backend**: Django  
- **Frontend**: Bootstrap  
- **Database**: SQLite3 (for development)  
- **Map Services**: Integrated with public map APIs  

---

### Installation  

Follow these steps to set up the SharBus project locally:  

1. **Clone the Repository**:  
   ```bash  
   git clone https://github.com/mohammednazir710/SHARJAH-MOWASALAT.git  
   cd SHARJAH-MOWASALAT  
   ```  

2. **Set Up a Virtual Environment**:  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # For Windows: venv\Scripts\activate  
   ```  

3. **Install Dependencies**:  
   ```bash  
   pip install -r requirements.txt  
   ```  

4. **Configure Database**:  
   SQLite3 is used as the default database. Run migrations to set it up:  
   ```bash  
   python manage.py migrate  
   ```  

5. **Start the Development Server**:  
   ```bash  
   python manage.py runserver  
   ```  
   Access the application at `http://127.0.0.1:8000/`.  

---

### Project Structure  

```plaintext  
sharbus/  
├── bus_schedule/            # Schadule data   
├── env/                     # Virtual environment directory (excluded in `.gitignore`)  
├── SHARJAH_MOWASALAT/       # Core Django project directory  
│   ├── __init__.py          # Marks the directory as a Python package  
│   ├── asgi.py              # ASGI configuration for deployment  
│   ├── settings.py          # Project settings file  
│   ├── urls.py              # Project-level URL configuration  
│   └── wsgi.py              # WSGI configuration for deployment  
├── templates/               # Global HTML templates  
├── address_with_code.csv    # CSV file containing bus stop data  
├── build.sh                 # Shell script for building the project  
├── db.sqlite3               # SQLite3 database file  
├── load_data.py             # Script to load data into the database  
└── location_data.csv        # Additional location data CSV file  
 
```  

---

### Database Models  

#### `BusStop`  
Stores details of all bus stops.  
- **Fields**:  
  - `name`: Name of the stop  
  - `code`: Unique code for the stop  
  - `latitude`: Latitude coordinate  
  - `longitude`: Longitude coordinate  
  - `is_start`: Flag indicating whether it is a starting point  

#### `EndStop`  
Defines routes between two stops.  
- **Fields**:  
  - `start`: Foreign key to `BusStop` (starting point)  
  - `end`: Foreign key to `BusStop` (ending point)  

#### `BusSchadule`  
Manages bus schedules for specific routes.  
- **Fields**:  
  - `route`: Foreign key to `EndStop`  
  - `dispatch_time`: Scheduled departure time  
  - `arrival_time`: Scheduled arrival time  

---

### Planned Features  
- Enhanced map visualization for bus stops and routes.  
- Conversion to Android app using Django APIs.  
- Improved accessibility and performance.  

---
