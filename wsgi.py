from service_rest import app

if __name__ == "__main__":
    app.config['JSON_SORT_KEYS'] = False
    app.run()
