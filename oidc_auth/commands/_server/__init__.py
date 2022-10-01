from http import HTTPStatus
from http.server import HTTPServer, SimpleHTTPRequestHandler
from multiprocessing import Semaphore
import os

pipe = None
semaphore = None
state = None


class AuthorizationCodeHandler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, directory=os.path.dirname(__file__))

    def do_GET(self):
        if '?' not in self.path:
            self.send_error(HTTPStatus.BAD_REQUEST, 'Bad Request', 'The authorization server returned an invalid response.')
        else:
            query_args = self.path.split('?')[-1].split('&')
            query = {
                arg.split('=')[0]: arg.split('=')[1]
                for arg in query_args
            }
            if 'code' not in query or 'state' not in query:
                self.send_error(HTTPStatus.BAD_REQUEST, 'Bad Request', 'The authorization server returned an invalid response.')
            else:
                if query['state'] != state:
                    self.send_error(HTTPStatus.BAD_REQUEST, 'Bad Request', 'The authorization server returned an invalid response.')
                else:
                    self.path = '/success.html'
                    pipe.send(query['code'])
                    semaphore.release()
        super().do_GET()


def callback(cpipe, tstate):
    global pipe, semaphore, state
    pipe = cpipe
    semaphore = Semaphore(0)
    state = tstate
    with HTTPServer(('', 9527), AuthorizationCodeHandler) as server:
        while True:
            if semaphore.acquire(block=False):
                break
            server.handle_request()
