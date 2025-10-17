from data_dirs_manager import get_app_data_dir, get_encodings_file_path
import datetime
import pandas as pd
import os

# App data dir setup
data_dir = get_app_data_dir()
attendance_file = os.path.join(data_dir, "attendance.csv")
encodigns_file = get_encodings_file_path()


if not os.path.exists(attendance_file):
    known_names = []
    df = pd.DataFrame(index=known_names)
    df.index.name = "Name/ID"
    df.to_csv(attendance_file)


def add_to_attendance(name):
    """
    Adds a new entry to the attendance file with the current date and time.

    :param name: The name or ID of the person.
    """
    # Read existing attendance data
    df = pd.read_csv(attendance_file, index_col=0)

    # Create a new entry
    if name not in df.index:
        df.loc[name] = [0] * len(df.columns)  # Initialize with empty values

    # Save back to the CSV file
    df.to_csv(attendance_file)


def remove_from_attendance(name):
    """
    Removes a person from the attendance file.

    :param name: The name or ID of the person to remove.
    """
    df = pd.read_csv(attendance_file, index_col=0)

    if name in df.index:
        df.drop(name, inplace=True)
        df.to_csv(attendance_file)
    else:
        print(f"{name} not found in attendance records.")


def mark_attendance(name: str) -> str:
    """
    Marks attendance for a person by updating the current date and time.

    :param name: The name or ID of the person.
    """
    df = pd.read_csv(attendance_file, index_col=0)

    # Get today's date
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Update today's date column
    if today not in df.columns:
        df[today] = 0  # Initialize with 0 if the column doesn't exist

    df.at[name, today] = 1  # Increment attendance count for today

    # Save back to the CSV file
    df.to_csv(attendance_file)
    return name
