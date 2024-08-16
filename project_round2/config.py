import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/your_database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY') or 'your_sendgrid_api_key'
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL') or 'noreply@yourdomain.com'

