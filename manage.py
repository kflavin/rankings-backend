import os
from app import create_app, init_db

app = create_app("default")


@app.before_first_request
def before_first_request():
    init_db()

if __name__ == "__main__":
    print("INITIALIZE DATABASE AND START APP")
    # init_db()
    app.run()
else:
    print("STARTING")
