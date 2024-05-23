class Logger:

    def __init__(self, printed:bool=False):
        self._printed = printed
        self._cache = ""

    def log(self, text:str="") -> None:
        self._cache += f"{text}\n"
        if self._printed:
            print(text)

    def get_log(self) -> str:
        return self._cache