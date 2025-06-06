# rpyc-ws

[![CI](https://github.com/magoocas/rpyc-ws/actions/workflows/ci.yaml/badge.svg)](https://github.com/magoocas/rpyc-ws/actions/workflows/ci.yaml)
[![PyPI version](https://img.shields.io/pypi/v/rpyc-ws)](https://pypi.org/project/rpyc-ws/)
[![License](https://img.shields.io/github/license/magoocas/rpyc-ws)](LICENSE)

`rpyc-ws` allows running an RPyC classic server over WebSocket connections. It provides a FastAPI application for the server and a helper for connecting via WebSockets from the client side.

## Installation

```bash
pip install rpyc-ws
```

## Usage

### Server

```python
from rpyc_ws import create_rpyc_fastapi_app

app = create_rpyc_fastapi_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Client

```python
from rpyc_ws import connect_ws

with connect_ws("ws://localhost:8000/rpyc-ws/") as conn:
    print(conn.modules.os.getcwd())

# or

conn = connect_ws("ws://localhost:8000/rpyc-ws/")
print(conn.modules.os.getcwd())
conn.close()
```

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for more information.
