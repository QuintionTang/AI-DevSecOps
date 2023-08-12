__author__ = "Quintion Tang <QuintionTang@gmail.com>"
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
