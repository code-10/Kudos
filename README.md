# Kudos
Kudos application

## Setup Instructions

### 1. Create a virtual environment and activate it
```Command Prompt
virtualenv venv
venv\Scripts\activate
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Change directory to access manage.py
```bash
cd project_kudos
```

### 4. Apply migrations
```bash
python manage.py makemigrations app_kudos
python manage.py makemigrations
python manage.py migrate
```

### 5. Load fixture
```bash
python manage.py loaddata fixtures/demo_data.json
```

### 5. Run the application
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser
