import cv2
import numpy as np

aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)

async def detect(inputImage):
    file_bytes = await inputImage.read()
    np_array = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Cannot read: " + inputImage.filename)
    parameters = aruco.DetectorParameters()
    detector = aruco.ArucoDetector(dictionary, parameters)

    corners, ids, rejected = detector.detectMarkers(image)

    if ids is not None:
        print("Detected IDs:", ids.flatten())
        return ids.flatten().tolist()
    else:
        print("No markers detected")
        return []