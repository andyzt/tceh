from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    # debug_value = app
    return 'hello world!'

if __name__ == '__main__':
    app.run()
