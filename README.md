# technical_assesment5

# Create vitual environment
python -m venv venv_name

# Activate virtual environmemnt
# Mac OS
source venv_name/bin/activate
# Windows
venv_name\Scripts\activate.bat

# Install required packages
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations <br>
python manage.py migrate

# Runserver
python manage.py runserver


swagger link:
swagger doc: 
