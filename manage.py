from app import create_app, init_db

app = create_app("default")

if __name__ == "__main__":
    init_db()
    app.run()
else:
    init_db()