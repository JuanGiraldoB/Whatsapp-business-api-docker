from flask import Flask
from dotenv import load_dotenv
import os
from routes import routes_bp

app = Flask(__name__)

load_dotenv()

config = {
    "APP_ID": os.getenv("APP_ID"),
    "APP_SECRET": os.getenv("APP_SECRET"),
    "RECIPIENT_WAID": os.getenv("RECIPIENT_WAID"),
    "VERSION": os.getenv("VERSION"),
    "PHONE_NUMBER_ID": os.getenv("PHONE_NUMBER_ID"),
    "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
    "VERIFY_TOKEN": os.getenv("VERIFY_TOKEN"),
    "SERVICE_ACCOUNT_PATH": os.getenv("SERVICE_ACCOUNT_PATH"),
    "SPREADSHEET": os.getenv("SPREADSHEET"),
    "WORKSHEET": os.getenv("WORKSHEET"),
}

app.config.update(config)
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(debug=True)
