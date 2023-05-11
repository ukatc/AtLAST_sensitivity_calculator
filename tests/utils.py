from contextlib import contextmanager

@contextmanager
def does_not_raise():
    # Utility for checking that an exception is NOT raised
    yield
