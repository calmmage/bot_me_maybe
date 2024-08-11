class WebServer:
    def __init__(self):
        self._server = None

    def start(self):
        # Start the web server
        self._server = Server()

    def stop(self):
        # Stop the web server
        self._server.stop()

def start_web_server():
    """Start the web server.

    """
    # Start the web server
    web_server = WebServer()
    web_server.start()


def tmux_decorator(func):
    """
    Decorator to run a function in a tmux session.

    func: function to run in a tmux session
    """
    def wrapper(*args, **kwargs):
        print('tmux_decorator')
        # q: will this run my func in a tmux session?
        # a: no, it will just run the func
        # q: how do I run the func in a tmux session?
        # a: I need to use the subprocess module
        return func(*args, **kwargs)
    return wrapper