# manage.py
from server import app,db

if __name__ == "__main__":
    app.run(port=8000, debug=True)