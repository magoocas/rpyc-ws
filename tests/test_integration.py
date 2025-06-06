import socket
import threading
import time

import pytest
import uvicorn

from rpyc_ws import connect_ws, create_rpyc_fastapi_app


def _run_server(app, host, port):
    config = uvicorn.Config(app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.01)
    return server, thread


def test_client_server_roundtrip():
    app = create_rpyc_fastapi_app()
    host = "127.0.0.1"
    sock = socket.socket()
    sock.bind((host, 0))
    port = sock.getsockname()[1]
    sock.close()
    server, thread = _run_server(app, host, port)
    try:
        conn = connect_ws(f"ws://{host}:{port}/rpyc-ws/")
        try:
            assert conn.modules.builtins.sum([1, 2, 3]) == 6
        finally:
            conn.close()
    finally:
        server.should_exit = True
        thread.join()
