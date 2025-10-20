class Error:
    """
    Base Error Class
    """

    def __init__(self) -> None:
        self.message: str = ""

    def __repr__(self) -> str:
        return str({"message": self.message})
