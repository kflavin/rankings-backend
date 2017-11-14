import os
from app import create_app, init_db

app = create_app("default")

if __name__ == "__main__":
    print("INITIALIZE DATABASE AND START APP")
    init_db()
    app.run()
else:
    if os.environ.get('WERKZEUG_RUN_MAIN') == "true":
        print("INIITALIZE DATABASE")
        init_db()