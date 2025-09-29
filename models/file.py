class File:
    def __init__(self, id, name, resource_level):
        self.id = id
        self.name = name
        self.resource_level = resource_level

    def __repr__(self):
        return f"File(id={self.id}, name={self.name}, resource_level={self.resource_level})"