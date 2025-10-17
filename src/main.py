import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

import face_recognition
import numpy as np
import cv2
import pandas as pd

import os
import shutil
import csv

import pickle

from data_dirs_manager import get_image_data_folder, get_encodings_file_path
from attendance import attendance_file, add_to_attendance, remove_from_attendance
import recognitions


class Application:
    def update_names_and_encodings(self):
        """Updates the known names and encodings from the encodings file."""

        if not os.path.exists(self.encodings_path):
            print(f"Encodings file not found: {self.encodings_path}")
            return

        try:
            with open(self.encodings_path, "rb") as f:
                encodings_data = pickle.load(f)
            self.known_names = list(encodings_data.keys())
            self.known_encodings = list(encodings_data.values())
            print("Known names and encodings updated successfully.")
        except Exception as e:
            print(f"Error loading encodings: {e}")

    def save_face_encodings(self, encodings_data):
        """Saves the face encodings data to the correct location."""

        # Get the correct, cross-platform file path for the pickle file

        print(f"Saving encodings to: {self.encodings_path}")

        try:
            with open(self.encodings_path, "wb") as f:
                pickle.dump(encodings_data, f)
            print("Encodings saved successfully.")
        except Exception as e:
            print(f"Error saving encodings: {e}")

    def store_user_image(self, source_image_path, name):
        """Copies a user's image to the application's image_data folder."""

        # Check if the source file exists
        if not os.path.exists(source_image_path):
            print(f"Error: Source image not found at '{source_image_path}'")
            return

        # Get the correct, cross-platform destination folder
        image_data_folder = get_image_data_folder()

        # Get the base name of the source image (e.g., 'person_a.jpg')
        image_filename = name + ".jpg"  # Keep original extension

        # Construct the full destination path
        destination_path = os.path.join(image_data_folder, image_filename)

        print(f"Copying image from '{source_image_path}' to '{destination_path}'")

        try:
            shutil.copyfile(source_image_path, destination_path)
            print("Image copied successfully.")
        except Exception as e:
            print(f"Error copying image: {e}")

    def add_an_entity(self):
        """Adds a new entity (person) to the attendance system."""
        new_name = self.input_name_add.get()
        source_image_path = self.photo_path.get()

        self.store_user_image(source_image_path, new_name)

        # save the encodings in the face_encodings.pkl file
        img = face_recognition.load_image_file(source_image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)[0]

        if not os.path.exists(self.encodings_path):
            print(f"Encodings file not found: {self.encodings_path}")
            return

        try:
            with open(self.encodings_path, "rb") as f:
                encodings_data = pickle.load(f)
        except Exception as e:
            print(f"Error loading encodings: {e}")
            return
        encodings_data[new_name] = encodings
        print(f"Added the encoding to the encodings data for: {new_name}")
        print(f"Saving encodings to: {self.encodings_path}")
        self.save_face_encodings(encodings_data)

        self.update_names_and_encodings()  # Update known names and encodings

        # Add the new name to the attendance file
        add_to_attendance(new_name)

    def remove_image_file(self, name):
        """Removes the image file of a user from the image_data folder."""
        image_data_folder = get_image_data_folder()
        image_filename = name + ".jpg"
        image_path = os.path.join(image_data_folder, image_filename)

        if os.path.exists(image_path):
            try:
                os.remove(image_path)
                print(f"Removed image file: {image_path}")
            except Exception as e:
                print(f"Error removing image file: {e}")
        else:
            print(f"Image file not found: {image_path}")  # Debugging line

    def remove_face_encoding(self, name):
        """Removes a user's face encoding from the encodings pickle file."""

        if not os.path.exists(self.encodings_path):
            print(f"Encodings file not found: {self.encodings_path}")
            return

        try:
            with open(self.encodings_path, "rb") as f:
                encodings_data = pickle.load(f)
        except Exception as e:
            print(f"Error loading encodings: {e}")
            return

        if name in encodings_data:
            del encodings_data[name]
            print(f"Removed encoding for: {name}")

            # Save the updated encodings back to the file
            self.save_face_encodings(encodings_data)
        else:
            print(f"No encoding found for: {name}")  # Debugging line

    def remove_an_entity(self):
        """Removes an entity (person) from the attendance system."""
        name_to_remove = self.input_name_remove.get()

        self.remove_image_file(name_to_remove)

        self.remove_face_encoding(name_to_remove)

        self.update_names_and_encodings()  # Update known names and encodings

        # Remove the name from the attendance file
        remove_from_attendance(name_to_remove)

    def browse_photo(self):
        filepath = filedialog.askopenfilename(
            title="Select Photo",
            filetypes=(("Image files", "*.jpg *.jpeg "), ("All files", "*.*")),
        )
        if filepath:
            self.photo_path.set(filepath)

    def preview_sheet(self):
        # Create a new Toplevel window for the popup
        popup = tk.Toplevel()
        popup.title("Preview Attendance Sheet")
        popup.attributes("-fullscreen", True)  # Make the popup full screen

        # Create a Treeview widget
        tree = ttk.Treeview(popup)
        tree.pack(fill="both", expand=True)

        # Add scrollbars to the Treeview
        vsb = ttk.Scrollbar(popup, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")
        hsb = ttk.Scrollbar(popup, orient="horizontal", command=tree.xview)
        hsb.pack(side="bottom", fill="x")
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        with open(attendance_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader)  # Read header row

            # Configure Treeview columns
            tree["columns"] = header
            tree.heading("#0", text="Index")  # Default first column
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)  # Adjust column width as needed

            # Insert data into the Treeview
            for i, row in enumerate(reader):
                tree.insert("", "end", iid=i, text=str(i), values=row)

        # Add a button to close the full-screen window
        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def download_sheet(self):
        # Read CSV into a pandas DataFrame
        df = pd.read_csv(attendance_file, index_col=0)

        # Open file dialog to save as Excel
        excel_file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")],
            title="Save Attendance Sheet as Excel",
        )
        if not excel_file_path:
            return  # User cancelled

        # Write DataFrame to Excel
        df.to_excel(
            excel_file_path
        )  # index=False prevents writing DataFrame index to Excel

        print(f"Successfully converted {attendance_file} to {excel_file_path}")

    def __init__(self, master):
        self.master = master
        master.title("Attendance System")
        master.geometry("1024x500")

        # Resizeing Mechanism
        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)  # left panel for interface
        master.grid_rowconfigure(1, weight=1)  # right panel for camera feed
        master.grid_columnconfigure(1, weight=1)

        # Main Frame
        # Left Panel for controls
        controls_frame = ttk.Frame(master, padding="15")
        controls_frame.grid(row=0, column=0, sticky="nsew")

        # Right Panel for camera feed
        camera_frame = ttk.Frame(master, padding="10", relief="groove", borderwidth=2)
        camera_frame.grid(row=0, column=1, sticky="nsew")

        # resizablility for controls on the left frame
        controls_frame.grid_columnconfigure(0, weight=0)  # Labels column, fixed width
        controls_frame.grid_columnconfigure(1, weight=1)
        controls_frame.grid_columnconfigure(2, weight=1)
        controls_frame.grid_columnconfigure(
            3, weight=0
        )  # Last column for Browse button

        # Labels/Entry boxes
        # Add an entity: Name/ID:
        ttk.Label(controls_frame, text="Add an entity:").grid(
            row=1, column=0, columnspan=4, pady=(10, 5), sticky="w"
        )
        ttk.Label(controls_frame, text="Name/ID:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )

        self.input_name_add = tk.StringVar()  # input name
        ttk.Entry(controls_frame, textvariable=self.input_name_add).grid(
            row=2,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="ew",  # **FIXED** columnspan
        )

        # Add an entity: Photo:
        ttk.Label(controls_frame, text="Photo:").grid(
            row=3, column=0, padx=5, pady=5, sticky="w"
        )

        self.photo_path = tk.StringVar()
        ttk.Entry(controls_frame, textvariable=self.photo_path, state="readonly").grid(
            row=3,
            column=1,
            columnspan=2,
            padx=5,
            pady=5,
            sticky="ew",  # Spans 2 columns
        )
        ttk.Button(controls_frame, text="Browse", command=self.browse_photo).grid(
            row=3,
            column=3,
            sticky="ew",
            padx=5,
            pady=5,  # Sits in the last column
        )

        # Add Button
        ttk.Button(controls_frame, text="Add", command=self.add_an_entity).grid(
            row=4, column=0, padx=5, pady=(5, 20), sticky="w"
        )

        # --- Remove an entity: Name/ID ---
        ttk.Label(controls_frame, text="Remove an entity:").grid(
            row=5, column=0, columnspan=4, pady=(15, 5), sticky="w"
        )
        ttk.Label(controls_frame, text="Name/ID:").grid(
            row=6, column=0, padx=5, pady=5, sticky="w"
        )
        self.input_name_remove = tk.StringVar()
        ttk.Entry(controls_frame, textvariable=self.input_name_remove).grid(
            row=6,
            column=1,
            columnspan=3,
            padx=5,
            pady=5,
            sticky="ew",  # **FIXED** columnspan
        )

        # Remove Button
        ttk.Button(controls_frame, text="Remove", command=self.remove_an_entity).grid(
            row=7, column=0, padx=5, pady=(5, 20), sticky="w"
        )

        # Current status:
        ttk.Label(controls_frame, text="Current Status:`").grid(
            row=8, column=0, columnspan=4, pady=(10, 5), sticky="w"
        )
        # Current status message readonly for the user
        self.status_message = tk.StringVar(value="Started")
        ttk.Entry(
            controls_frame, textvariable=self.status_message, state="readonly"
        ).grid(
            row=9,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=5,
            pady=5,  # Spans all 4 columns
        )

        # Preview Button
        ttk.Button(controls_frame, text="Preview", command=self.preview_sheet).grid(
            row=10,
            column=0,
            columnspan=2,
            padx=(5, 5),
            pady=(30, 15),
            sticky="ew",  # **FIXED** columnspan
        )
        # Download Button
        ttk.Button(controls_frame, text="Download", command=self.download_sheet).grid(
            row=10,
            column=2,
            columnspan=2,
            padx=(5, 5),
            pady=(30, 15),
            sticky="ew",  # **FIXED** columnspan
        )

        # --- Camera Footage/Stream Placeholder ---
        self.camera_label = ttk.Label(
            camera_frame,
            text="Camera Footage / Live Stream",
            anchor="center",
            background="black",
            foreground="white",
            font=("Arial", 16),
        )
        # Make the camera label expand to fill the entire right frame
        self.camera_label.grid(row=0, column=0, sticky="nsew")
        camera_frame.grid_columnconfigure(0, weight=1)
        camera_frame.grid_rowconfigure(0, weight=1)

        # --- Video Capture Initialization ---
        # 0 typically refers to the default camera. Change this if needed.
        self.cap = cv2.VideoCapture(0)
        # We need a reference to the PhotoImage to prevent garbage collection
        self.current_frame_img = None

        # Known names and encodings
        self.known_names = []
        self.known_encodings = []
        self.encodings_path = get_encodings_file_path()
        if os.path.exists(self.encodings_path):
            self.update_names_and_encodings()

        # Final setup and loop start
        self.master.protocol(
            "WM_DELETE_WINDOW", self.on_close
        )  # Handle window closing gracefully
        self.video_loop()  # Start the video stream update loop

    def video_loop(self):
        """Captures a frame, processes it, and updates the Tkinter label."""
        try:
            # Read frame from the camera
            ret, frame = self.cap.read()

            if ret:
                temp_rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                temp_locs = face_recognition.face_locations(temp_rgb_frame)
                if len(temp_locs) > 0:
                    # If there are faces detected, process the frame
                    # 1. Process the frame using the recognition module
                    processed_frame, status = recognitions.process_frame_for_attendance(
                        frame,
                        known_names=self.known_names,
                        known_encodings=self.known_encodings,
                    )

                    # Update status message based on recognition result
                    if status:
                        self.status_message.set(f"Recognition: {status}")

                    # 2. Convert the OpenCV image (BGR) to RGB
                    processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGBA)

                    # 2. Convert the OpenCV image (BGR) to RGB
                    cv2image = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGBA)

                    # 3. Resize frame to fit the camera_label size dynamically
                    # Get the current size of the label's parent frame
                    frame_width = self.camera_label.winfo_width()
                    frame_height = self.camera_label.winfo_height()

                    # Only proceed if the frame size is valid (i.e., not 1 or 0)
                    if frame_width > 1 and frame_height > 1:
                        img = Image.fromarray(cv2image)
                        img = img.resize(
                            (frame_width, frame_height), Image.Resampling.LANCZOS
                        )

                        # Convert to PhotoImage for Tkinter
                        self.current_frame_img = ImageTk.PhotoImage(image=img)

                        # 4. Update the label with the new image
                        self.camera_label.configure(image=self.current_frame_img)
                        self.camera_label.image = self.current_frame_img

            # Schedule the next call to video_loop after 15 milliseconds (~66 FPS)
            self.master.after(15, self.video_loop)

        except Exception as e:
            # Handle error if camera fails to initialize or process
            self.status_message.set(f"Video Error: {str(e)}")
            # Stop the loop to prevent continuous errors
            self.cap.release()

    def on_close(self):
        """Releases the camera and destroys the window when the app is closed."""
        self.cap.release()
        self.master.destroy()


def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()


if __name__ == "__main__":
    main()
