"""
UniPath Ghana - Backend Entry Point

Run with:
    python run.py

Or in production, use gunicorn:
    gunicorn -w 4 -b 0.0.0.0:5000 run:app
"""

import os
from app import create_app

config_name = os.getenv("FLASK_ENV", "development")
app = create_app(config_name)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=app.config.get("DEBUG", True),
    )
