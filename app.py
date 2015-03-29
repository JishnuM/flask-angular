from flask import Flask
from api import api

app = Flask(__name__)
app.config.from_object('default-config')

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
