import random
import string
import time

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class VerifyCodeGenerator(metaclass=SingletonMeta):
    def __init__(self, length=6):
        print('code generator initialized')
        self.length = length
        self.code = self.generate()
        self.expiry = 60
        self.created_at = time.time()

    def generate(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=self.length))
    
    def is_expired(self):
        return time.time() - self.created_at > self.expiry

    def validate(self, code):
        return code == self.code and not self.is_expired()