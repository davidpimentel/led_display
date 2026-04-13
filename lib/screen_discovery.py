import os

SCREENS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screens")


def discover_screens():
    screen_names = []
    for entry in os.listdir(SCREENS_DIR):
        entry_path = os.path.join(SCREENS_DIR, entry)
        if (
            os.path.isdir(entry_path)
            and entry != "__pycache__"
            and os.path.isfile(os.path.join(entry_path, "__init__.py"))
        ):
            screen_names.append(entry)
    return sorted(screen_names)
