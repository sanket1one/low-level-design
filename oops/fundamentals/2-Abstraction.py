"""
2. ABSTRACTION

Hiding complexity + Showing essential.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from fileinput import filename


class Logger(ABC):

    def __init__(self, level: str):
        self._level = level

    @abstractmethod
    def log(self, message: str) -> None:
        pass

    def format_message(self, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] [{self._level}] {message}"

class ConsoleLogger(Logger):
    def __init__(self, level: str):
        super().__init__(level)
    
    def log(self, message: str) -> None:
        formatted_message = self.format_message(message)
        print(formatted_message)

class FileLogger(Logger):
    def __init__(self, level: str, file_path: str):
        super().__init__(level)
        self._filepath = file_path
    
    def log(self, message: str) -> None:
        print(f"Logging to file {self._filepath}")


## Public API as Abstraction.

class DatabaseClient:
    def __init__(self, max_connections: int, retry_attempts: int):
        self.__max_connections = max_connections
        self.__retry_attempts = retry_attempts

    def connect(self, host: str, port: int)-> None:
        self.__open_socket(host, port)
        self.__authenticate()
        self.__initialize_connection_pool()


    def query(self, sql: str) -> str:
        parsed_query = self.__parse_query(sql)
        return self.__execute_query(parsed_query)
    
    def __open_socket(self, host: str, port: int) -> None: pass
    def __authenticate(self) -> None: pass
    def __initialize_connection_pool(self) -> None: pass
    def __parse_query(self, sql: str) -> str: pass
    def __execute_query(self, parsed_query: str) -> str: pass
    def __execute_with_retry(self, query: str) -> str:
        for i in range(self.__retry_attempts):
            try:
                return self.__execute_query(query)
            except Exception:
                if i == self.__retry_attempts - 1:
                    raise
        return ""
    def __execute_query(self, query: str) -> str: return "result"



"""
 Practical Example: Media Player
"""

from abc import ABC, abstractmethod

class MediaPlayer(ABC):
    def __init__(self, player_name: str):
        self._player_name = player_name

    @abstractmethod
    def play(self) -> None:
        pass

    @abstractmethod
    def pause(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    def display_status(self) -> None:
        print(f"[{self._player_name}] Status: Ready")

    def log_action(self, action: str) -> None:
        print(f"[{self._player_name}] Action: {action}")


class AudioPlayer(MediaPlayer):
    def __init__(self, audio_file: str):
        super().__init__("AudioPlayer")
        self._audio_file = audio_file

    def play(self) -> None:
        self.log_action(f"Playing audio: {self._audio_file}")

    def pause(self) -> None:
        self.log_action(f"Paused audio: {self._audio_file}")

    def stop(self) -> None:
        self.log_action(f"Stopped audio: {self._audio_file}")


class VideoPlayer(MediaPlayer):
    def __init__(self, video_file: str, resolution: str):
        super().__init__("VideoPlayer")
        self._video_file = video_file
        self._resolution = resolution

    def play(self) -> None:
        self.log_action(f"Playing video: {self._video_file} at {self._resolution}")

    def pause(self) -> None:
        self.log_action(f"Paused video: {self._video_file}")

    def stop(self) -> None:
        self.log_action(f"Stopped video: {self._video_file}")


class StreamingPlayer(MediaPlayer):
    def __init__(self, stream_url: str, buffer_size: int):
        super().__init__("StreamingPlayer")
        self._stream_url = stream_url
        self._buffer_size = buffer_size

    def play(self) -> None:
        self.log_action(f"Streaming from: {self._stream_url} (buffer: {self._buffer_size}KB)")

    def pause(self) -> None:
        self.log_action(f"Paused stream: {self._stream_url}")

    def stop(self) -> None:
        self.log_action(f"Stopped stream: {self._stream_url}")


class PlayerController:
    def __init__(self, player: MediaPlayer):
        self._player = player

    def start_playback(self) -> None:
        self._player.display_status()
        self._player.play()

    def pause_playback(self) -> None:
        self._player.pause()

    def stop_playback(self) -> None:
        self._player.stop()

audio_ctrl = PlayerController(AudioPlayer("song.mp3"))
audio_ctrl.start_playback()
audio_ctrl.pause_playback()

print()

video_ctrl = PlayerController(VideoPlayer("movie.mp4", "1080p"))
video_ctrl.start_playback()
video_ctrl.stop_playback()

print()

stream_ctrl = PlayerController(
    StreamingPlayer("https://stream.example.com/live", 2048))
stream_ctrl.start_playback()
stream_ctrl.stop_playback()



"""
Example 2: Shape
"""

from abc import ABC, abstractmethod
import math

class Shape(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> None:
        print(f"Shape: {self._name}, Area: {self.area():.2f}, Perimeter: {self.perimeter():.2f}")

class Circle(Shape):
    def __init__(self, radius: float):
        super().__init__("Circle")
        self._radius = radius

    def area(self) -> float:
        return math.pi * self._radius * self._radius

    def perimeter(self) -> float:
        return 2 * math.pi * self._radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        super().__init__("Rectangle")
        self._width = width
        self._height = height

    def area(self) -> float:
        return self._width * self._height

    def perimeter(self) -> float:
        return 2 * (self._width + self._height)



circle = Circle(5.0)
circle.describe()

rectangle = Rectangle(4.0, 6.0)
rectangle.describe()