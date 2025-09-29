from datetime import datetime

class Informs:
    def __init__(self, log_file="logs.txt"):
        self.log_file = log_file

    def log_access_attempt(self, model, user, file, action, result, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = (
            f"[{timestamp}] | "
            f"Model: {model} | "
            f"User: {user.username} (Role: {user.role}) | "
            f"File: {file.name} (Level: {file.resource_level}) | "
            f"Action: {action} | "
            f"Result: {'Success' if result == 1 else 'Failure'} | "
            f"Message: {message}"
        )

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")

    def get_all_logs(self):
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []  

    def clear_logs(self):
        open(self.log_file, "w").close()  # Limpia el archivo
