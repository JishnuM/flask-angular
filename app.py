from flask import Flask, render_template
from api import api

app = Flask(__name__)
app.config.from_object('default-config')
app.config.from_envvar('FLASK_ANGULAR_SETTINGS')

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def render_app():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
