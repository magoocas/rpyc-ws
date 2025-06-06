import pytest
from rpyc_ws.stream import CallbackStream

def test_read_and_close():
    frames = [b"hello", b"world", b"", b"!"]
    def recv(timeout):
        return frames.pop(0)
    sent = []
    closed = []
    def send(data):
        sent.append(data)
    def close():
        closed.append(True)
    stream = CallbackStream(recv, send, close)
    assert stream.read(5) == b"hello"
    assert stream.read(5) == b"world"
    with pytest.raises(EOFError):
        stream.read(1)
    assert closed == [True]


def test_write_after_close_raises():
    def recv(timeout):
        return b""
    events = []
    def send(data):
        events.append(data)
    def close():
        events.append("closed")
    stream = CallbackStream(recv, send, close)
    with pytest.raises(EOFError):
        stream.read(1)
    assert stream.closed
    with pytest.raises(EOFError):
        stream.write(b"data")
    assert "closed" in events
