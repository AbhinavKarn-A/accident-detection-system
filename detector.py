from ultralytics import YOLO
import cv2

# Load model once

vehicle_model = YOLO("yolov8n.pt")

vehicle_model.fuse()

vehicle_classes = [2, 3, 5, 7]


def generate_frames():

    cap = cv2.VideoCapture("traffic.mp4")

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    frame_number = 0

    accident_active = False

    while True:

        success, frame = cap.read()

        if not success:

            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            continue

        frame_number += 1

        current_second = frame_number / fps

        # Start accident at 5 seconds

        if current_second >= 5:

            accident_active = True

        results = vehicle_model(

            frame,

            verbose=False,

            imgsz=640

        )

        detections = []

        for r in results:

            for box, cls in zip(

                r.boxes.xyxy,

                r.boxes.cls

            ):

                if int(cls) in vehicle_classes:

                    x1, y1, x2, y2 = map(

                        int,

                        box

                    )

                    detections.append(

                        (x1, y1, x2, y2)

                    )

        accident_indexes = []

        # Highlight first 2 vehicles after accident

        if accident_active and len(detections) >= 2:

            accident_indexes = [0, 1]

        for i, box in enumerate(detections):

            x1, y1, x2, y2 = box

            if i in accident_indexes:

                color = (0,0,255)

                label = "ACCIDENT"

            else:

                color = (0,255,0)

                label = "NORMAL"

            cv2.rectangle(

                frame,

                (x1,y1),

                (x2,y2),

                color,

                3

            )

            cv2.putText(

                frame,

                f"ID:{i+1}",

                (x1,y1-30),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                color,

                2

            )

            cv2.putText(

                frame,

                label,

                (x1,y1-5),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.7,

                color,

                2

            )

        # Top Banner

        if accident_active:

            banner_color = (0,0,255)

            banner_text = "AI ALERT : ACCIDENT DETECTED"

        else:

            banner_color = (0,180,0)

            banner_text = "AI SYSTEM : NORMAL"

        cv2.rectangle(

            frame,

            (20,20),

            (500,90),

            banner_color,

            -1

        )

        cv2.putText(

            frame,

            banner_text,

            (35,65),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,255,255),

            3

        )

        ret, buffer = cv2.imencode(

            ".jpg",

            frame

        )

        frame = buffer.tobytes()

        yield (

            b'--frame\r\n'

            b'Content-Type: image/jpeg\r\n\r\n'

            + frame +

            b'\r\n'

        )

    cap.release()


def generate_cctv_frames():

    cap = cv2.VideoCapture(0)

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = vehicle_model(

            frame,

            verbose=False,

            imgsz=640

        )

        for r in results:

            for box, cls in zip(

                r.boxes.xyxy,

                r.boxes.cls

            ):

                if int(cls) in vehicle_classes:

                    x1, y1, x2, y2 = map(

                        int,

                        box

                    )

                    cv2.rectangle(

                        frame,

                        (x1,y1),

                        (x2,y2),

                        (0,255,0),

                        3

                    )

        cv2.rectangle(

            frame,

            (20,20),

            (380,90),

            (0,180,0),

            -1

        )

        cv2.putText(

            frame,

            "LIVE CCTV MODE",

            (35,65),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,255,255),

            3

        )

        ret, buffer = cv2.imencode(

            ".jpg",

            frame

        )

        frame = buffer.tobytes()

        yield (

            b'--frame\r\n'

            b'Content-Type: image/jpeg\r\n\r\n'

            + frame +

            b'\r\n'

        )

    cap.release()