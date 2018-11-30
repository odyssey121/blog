from os import getenv
from os.path import dirname, join
from dotenv import load_dotenv

root_dir = dirname(__file__)
dotenv_path = join(root_dir, '.env')
load_dotenv(dotenv_path)

class Config:
	FLASK_APP = getenv('FLASK_APP')
	SECRET_KEY = getenv('SECRET_KEY')
