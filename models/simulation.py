import csv
import os
from models.informs import Informs
from models.user import User
from models.file import File


class Simulation:

    def __init__(self, users_file: str = "users.csv", files_file: str = "files.csv"):
        self.users = []
        self.files = []
        self.informs = Informs()
        self.users_file = users_file
        self.files_file = files_file

        # Cargar datos desde CSV
        self._load_users_from_csv()
        self._load_files_from_csv()

    # Users

    def add_user(self, user: User):
        """Agrega un usuario en memoria y actualiza el CSV"""
        self.users.append(user)
        self._save_all_users_to_csv()

    def edit_user(self, user_id: int, updated_user: User):
        """Edita un usuario existente y actualiza el CSV"""
        for idx, user in enumerate(self.users):
            if user.id == user_id:
                updated_user.id = user_id  # mantener ID
                self.users[idx] = updated_user
                self._save_all_users_to_csv()
                return True
        return False

    def get_all_users(self):
        return self.users

    def _save_all_users_to_csv(self):
        """Reescribe el CSV de usuarios"""
        with open(self.users_file, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "username", "role"])
            for user in self.users:
                writer.writerow([user.id, user.username, user.role])

    def _load_users_from_csv(self):
        """Carga todos los usuarios desde el CSV"""
        if not os.path.isfile(self.users_file):
            return
        with open(self.users_file, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user = User(
                    id=int(row["id"]),
                    username=row["username"],
                    role=row["role"]
                )
                self.users.append(user)

    # Files

    def add_file(self, file: File):
        """Agrega un archivo en memoria y actualiza el CSV"""
        self.files.append(file)
        self._save_all_files_to_csv()

    def edit_file(self, file_id: int, updated_file: File):
        """Edita un archivo existente y actualiza el CSV"""
        for idx, file in enumerate(self.files):
            if file.id == file_id:
                updated_file.id = file_id  # mantener ID
                self.files[idx] = updated_file
                self._save_all_files_to_csv()
                return True
        return False

    def get_all_files(self):
        return self.files

    def _save_all_files_to_csv(self):
        """Reescribe el CSV de archivos"""
        with open(self.files_file, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["id", "name", "resource_level"])
            for file in self.files:
                writer.writerow([file.id, file.name, file.resource_level])

    def _load_files_from_csv(self):
        """Carga todos los archivos desde el CSV"""
        if not os.path.isfile(self.files_file):
            return
        with open(self.files_file, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                file = File(
                    id=int(row["id"]),
                    name=row["name"],
                    resource_level=int(row["resource_level"])
                )
                self.files.append(file)


    # Simulation

    def run_simulation(self):
        self.informs.clear_logs()
