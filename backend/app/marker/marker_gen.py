import cv2
from cv2 import aruco
import numpy as np
import io
from fastapi.responses import StreamingResponse

def generate_aruco_marker(marker_id: int, size: int = 200, border_size: int = 15) -> StreamingResponse:
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)

    marker_img = aruco.generateImageMarker(aruco_dict, marker_id, size)

    marker_with_border = cv2.copyMakeBorder(
        marker_img,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv2.BORDER_CONSTANT,
        value=255
    )

    _, buffer = cv2.imencode(".png", marker_with_border)

    return StreamingResponse(
        io.BytesIO(buffer.tobytes()),
        media_type="image/png"
    )
