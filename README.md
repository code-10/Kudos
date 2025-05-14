# Kudos
Kudos application

## Setup Instructions for Frontend - Angular

### 1. Change directory for npm install
```bash
cd frontend-kudos
```

### 2. npm install
```bash
npm install
```

### 3. Run the application
```bash
ng serve or ng s
```

Note: Make sure to have latest version of nodejs and Angular CLI installed


## Setup Instructions for Backend - Django

### 1. Create a virtual environment and activate it
```bash
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
python manage.py migrate app_kudos
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

![register](https://github.com/user-attachments/assets/de9d73a4-e2cd-44cb-9b2d-a6816234a141)

![login](https://github.com/user-attachments/assets/66a57ac3-4e2d-4ea7-897f-9098ce7d8f2c)

![image](https://github.com/user-attachments/assets/480c6662-e423-40ec-83c8-3fd468bad15e)

![give_kudos](https://github.com/user-attachments/assets/ef8d3d2c-3a55-404f-8a95-5ceb6675c0e4)

![available_kudos](https://github.com/user-attachments/assets/a50a26b4-45b3-4ca8-8f24-591be4b64a8b)

![given_kudos](https://github.com/user-attachments/assets/1505f376-6339-48e8-a274-a074f7aabaf2)

![received_kudos](https://github.com/user-attachments/assets/7841e867-c952-4ff8-84f3-df1bde78e379)

![users_belonging_to_same_organization](https://github.com/user-attachments/assets/54b1b88e-4b30-478a-aaab-427d29eaf860)
