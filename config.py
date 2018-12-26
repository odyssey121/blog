from os import getenv
from os.path import dirname, join
from dotenv import load_dotenv

root_dir = dirname(__file__)
dotenv_path = join(root_dir, '.env')
load_dotenv(dotenv_path)

class Config:
	FLASK_APP = getenv('FLASK_APP')
	SECRET_KEY = getenv('SECRET_KEY')
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(root_dir,'db.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = 1
	MAIL_USERNAME = getenv('HZ1')
	MAIL_PASSWORD = getenv('HZ')
	ADMINS = ['gfgfujhbv@gmail.com']


