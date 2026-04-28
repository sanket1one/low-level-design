"""
Singleton:
class with only one object

example -> Thread pool, caches, loggers etc..

[.] Single instance + Global Access


             ---
[singleton]     |
              <--
"""

import threading


class LazySingleton:
    _instace = None

    def __init__(self):
        if LazySingleton._instance is not None:
            raise Exception("user get_instace() instead")
    
    @staticmethod
    def get_instace():

        if LazySingleton._instace is None:
            LazySingleton._instace = LazySingleton()
        
        return LazySingleton._instace
    
# Thread-Safe Singleton
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()


    def __init__(self):
        if ThreadSafeSingleton._instance is not None:
            raise Exception("use get instance instead")
    
    @staticmethod
    def get_instance():
        with ThreadSafeSingleton._lock:
            if ThreadSafeSingleton._instance is None:
                ThreadSafeSingleton._instance = ThreadSafeSingleton()
        return ThreadSafeSingleton._instance

class DoubleCheckedSingleton:
    # Holds the single shared instance
    _instance = None
    # Lock used only during first-time creation
    _lock = threading.Lock()

    # Constructor prevents accidental direct creation
    def __init__(self):
        if DoubleCheckedSingleton._instance is not None:
            raise Exception("Use get_instance() instead.")

    # Global access point to get the Singleton instance
    @staticmethod
    def get_instance():
        
		# Fast path: first check without locking
        if DoubleCheckedSingleton._instance is None:
            # Lock only when the instance might need to be created
            with DoubleCheckedSingleton._lock:
                # Second check inside the lock (prevents double creation)
                if DoubleCheckedSingleton._instance is None:
                    DoubleCheckedSingleton._instance = DoubleCheckedSingleton()

        # Return the shared instance
        return DoubleCheckedSingleton._instance
    


# module - level singelton

# config_manager.py

class _ConfigManager:
    def __init__(self):
        self._settings = {}

    def set(self, key, value):
        self._settings[key] = value

    def get(self, key, default=None):
        return self._settings.get(key, default)


# Created once when module is first imported
config = _ConfigManager()


# Usage (from other files):
# from config_manager import config
# config.set("debug", True)

#  The interpreter caches modules in sys.modules after the first impor

class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

s1 = Singleton()
s2 = Singleton()
assert s1 is s2