import os
from flask import Flask, render_template, request, abort, redirect

app = Flask(__name__)

token_endpoint = None
state = None
queue = None


devnull = open(os.devnull, 'w')


@app.route('/code')
def convert_code():
    global authorization_code
    passed_state = request.args.get('state')
    if passed_state != state:
        abort(400, 'The state value is not correct.')
    code = request.args.get('code')
    queue.put(code)
    return render_template('code.html.j2', code=code)


@app.before_first_request
def end_me_please():
    print('Press Enter to continue.')
