import json
import os

origins = ["http://localhost:3000/*", "https://basketball-v0-906cb.web.app/*", "https://basketball-v0-906cb.firebaseapp.com/*"]

firebase_credentials = json.loads(
    os.environ.get("FIREBASE_SERVICE_ACCOUNT_CONFIG_JSON", "")
)
