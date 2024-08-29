def read_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def write_to_file(file_path, content):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def create_file(file_path):
    with open(file_path, "w", encoding="utf-8"):
        pass