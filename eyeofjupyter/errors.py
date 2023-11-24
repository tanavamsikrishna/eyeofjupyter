class NoProject(BaseException):
    pass


class NoSnapShotFile(BaseException):
    def __init__(self, folder) -> None:
        super().__init__()
        self.folder = folder

    def __str__(self) -> str:
        return self.__repr__()