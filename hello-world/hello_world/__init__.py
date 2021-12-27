print("Initializing hello world module")
from .some_funcs import say_hello, repeat_string

__all__ = ["say_hello", "repeat_string"]
