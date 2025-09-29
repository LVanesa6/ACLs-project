class Request:
    def __init__(self, model: str, user_id: int, file_id: int, action: str):
        self.model = model
        self.user_id = user_id
        self.file_id = file_id
        self.action = action