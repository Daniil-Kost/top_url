from application import app, create_api


if __name__ == "__main__":
    create_api()
    app.run(host="localhost", port="8000")
