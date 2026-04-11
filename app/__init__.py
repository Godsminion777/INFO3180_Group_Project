import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

origins = os.getenv("CORS_ORIGINS").split(",")

CORS(app,
     resources={r"/api/*": {"origins": origins}},
     supports_credentials=True)