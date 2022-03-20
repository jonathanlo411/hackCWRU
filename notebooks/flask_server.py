from flask import Flask
from test_script import on_message

app = Flask(__name__)


@app.route('/')
def hello():
    on_message()
    return
