from Module import app
import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = os.environ['FLASK_PORT'], debug=True, use_reloader=False)