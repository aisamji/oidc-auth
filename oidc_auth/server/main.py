import requests
import sys
from flask import Flask, request

app = Flask(__name__)

alias = None
token_endpoint = None


@app.route('/')
def code():
    request.args['code']
    requests.get(token_endpoint)
    return 'success'


def main():
    global alias, token_endpoint
    alias, token_endpoint = sys.argv[1:]
    app.run(host='0.0.0.0', port=9527)
