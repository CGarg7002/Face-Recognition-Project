import face_recognition
import cv2

from attendance import mark_attendance


def process_frame_for_attendance(frame, known_names, known_encodings):
    """
    Takes an OpenCV frame, performs simulated face recognition, and annotates the frame.

    Args:
        frame (np.array): The BGR frame captured from the camera.
        known_names (list): List of known names.
        known_encodings (list): List of known face encodings.

    Returns:
        tuple: (annotated_frame, status_message)
    """
    status_message = ""

    # Convert the frame from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all face locations and encodings in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Compare the face encoding with known encodings
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        # If a match is found, get the corresponding name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

            # Mark attendance for the recognized person
            temp = mark_attendance(name)
            status_message = status_message + temp + ", "

        # Draw a rectangle around the face
        top, right, bottom, left = face_location
        if name != "Unknown":
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(
                frame, (left, bottom + 35), (right, bottom), (0, 255, 0), cv2.FILLED
            )
        else:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)
            cv2.rectangle(
                frame, (left, bottom + 35), (right, bottom), (0, 0, 0), cv2.FILLED
            )

        # Annotate the name on the frame
        cv2.putText(
            frame,
            name,
            (left + 6, bottom + 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    status_message = status_message.rstrip(", ")
    status_message = status_message + " marked present."

    # Return the modified frame and the status message
    return frame, status_message
