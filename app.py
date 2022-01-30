from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send
from qkd_simulation import qkd

app = Flask (__name__)
app.config['SECRET_KEY'] = 'secret'


socketio = SocketIO(app)


@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')


@socketio.on('message')
def handle_message(msg):
  print(msg)
  send(qkd(msg), broadcast = True)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    #socketio.run(app)