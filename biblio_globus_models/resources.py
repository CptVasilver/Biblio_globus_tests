
from pathlib import Path

def file_path(file_name):
    return str(Path(__file__).parent.joinpath(f'files/{file_name}'))