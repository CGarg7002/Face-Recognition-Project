from appdirs import AppDirs
import os

APP_NAME = "Attendance System"


def get_app_data_dir():
    """
    Gets the OS-specific, user-private data directory for the application.
    This is the correct place to store user-generated files like .pkl files and images.
    It automatically creates the directory if it doesn't exist.

    - Windows: C:/Users/<User>/AppData/Roaming/<AppAuthor>/<AppName>
    - Linux:   /home/<User>/.local/share/<AppName>
    - macOS:   /Users/<User>/Library/Application Support/<AppName>
    """
    # Initialize AppDirs with your application's name
    dirs = AppDirs(APP_NAME)

    # Get the path for user-specific data
    data_dir = dirs.user_data_dir

    # Create the directory if it doesn't exist.
    # The `exist_ok=True` flag prevents an error if the directory is already there.
    os.makedirs(data_dir, exist_ok=True)

    return data_dir


def get_image_data_folder():
    """
    Returns the full path to the 'image_data' subfolder within the app data directory.
    This is where we will store the copied images.
    """
    # Get the base data directory
    base_data_dir = get_app_data_dir()

    # Create a path for the 'image_data' subfolder
    image_folder = os.path.join(base_data_dir, "image_data")

    # Ensure this subfolder also exists
    os.makedirs(image_folder, exist_ok=True)

    return image_folder


def get_encodings_file_path():
    """
    Returns the full path for the 'face_encodings.pkl' file.
    """
    base_data_dir = get_app_data_dir()

    # Create the full path by joining the directory and the filename
    return os.path.join(base_data_dir, "face_encodings.pkl")
