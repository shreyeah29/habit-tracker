import os
import sys

# Ensure 'app' package can be imported regardless of how Flask runs
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5011, debug=True)
