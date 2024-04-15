from common import *

class ImageProcessing:
    """
    Class for processing images, including face detection, visualization, and image manipulation.
    """

    def __init__(self):
        """
        Initialize the ImageProcessing instance.
        """
        self.margin = 10  # pixels
        self.row_size = 10  # pixels
        self.font_size = 1
        self.font_thickness = 1
        self.text_color = (255, 0, 0)  # red

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_color = (255, 255, 255)  # White color in BGR
        self.font_thickness = 2

        # OpenCV Video Capture
        self.video_capture = cv2.VideoCapture(0)  # 0 for the default camera
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set frame width to 1280
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set frame height to 960
        self.video_capture.set(cv2.CAP_PROP_FPS, 120)

        # Medipipe Config
        self.base_options = python.BaseOptions(model_asset_path='...')
        self.options = vision.FaceDetectorOptions(base_options=self.base_options)
        self.detector = vision.FaceDetector.create_from_options(self.options)

    def get_video_capture(self):
        """
        Get the video capture object.

        Returns:
            cv2.VideoCapture: The video capture object.
        """
        return self.video_capture

    def get_detector(self):
        """
        Get the face detector object.

        Returns:
            vision.FaceDetector: The face detector object.
        """
        return self.detector

    def preprocess(self, image) -> np.ndarray:
        """
        Preprocess the input image for face detection.

        Args:
            image (np.ndarray): The input image.

        Returns:
            Tuple[vision.Detection, np.ndarray]: The detection result and preprocessed image.
        """
        # Crop the center part to 640x480
        center_x = (image.shape[1] - 480) // 2
        center_y = (image.shape[0] - 640) // 2
        frame = image[center_y:center_y+640, center_x:center_x+480]
        
        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)
        
        # Load the input image.
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        # Detect faces in the input image.
        detection_result = self.detector.detect(image)

        return detection_result, frame

    def image_cpaturing(self):
        """
        Capture images of detected faces.

        Returns:
            bool: True if successful, False otherwise.
        """
        for i in range(1, 21):
            ret, frame = self.video_capture.read()
            detection_result, frame = self.preprocess(frame)

            if detection_result.detections[0].categories[0].score > 0.75:
                origin_x = detection_result.detections[0].bounding_box.origin_x
                origin_y = detection_result.detections[0].bounding_box.origin_y
                width = detection_result.detections[0].bounding_box.width
                height = detection_result.detections[0].bounding_box.height

                frame = frame[origin_y:origin_y + height, origin_x:origin_x + width, :]
                frame = cv2.resize(frame, (300, 300))
                cv2.imwrite('...'.format(i), frame)
        
            else:
                return False

        return True

    def _normalized_to_pixel_coordinates_(
        self, normalized_x: float, normalized_y: float, image_width: int,
        image_height: int
    ):
        """
        Convert normalized value pair to pixel coordinates.

        Args:
            normalized_x (float): Normalized x-coordinate.
            normalized_y (float): Normalized y-coordinate.
            image_width (int): Width of the image.
            image_height (int): Height of the image.

        Returns:
            Tuple[int, int]: Pixel coordinates.
        """
        # Checks if the float value is between 0 and 1.
        def is_valid_normalized_value(value: float) -> bool:
            return (value > 0 or m.isclose(0, value)) and (value < 1 or
                                                        m.isclose(1, value))

        if not (is_valid_normalized_value(normalized_x) and
                is_valid_normalized_value(normalized_y)):
            # TODO: Draw coordinates even if it's outside of the image bounds.
            return  # You can return None or any other special value here
        x_px = min(m.floor(normalized_x * image_width), image_width - 1)
        y_px = min(m.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px

    def visualize(self, image, detection_result) -> np.ndarray:
        """
        Draw bounding boxes and keypoints on the input image and return it.

        Args:
            image (np.ndarray): The input RGB image.
            detection_result (vision.Detection): The detection result.

        Returns:
            np.ndarray: Image with bounding boxes and keypoints.
        """
        annotated_image = image.copy()
        height, width, _ = image.shape

        for detection in detection_result.detections:
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(annotated_image, start_point, end_point, self.text_color, 3)

            # Draw keypoints
            for keypoint in detection.keypoints:
                keypoint_px = self._normalized_to_pixel_coordinates_(
                    keypoint.x, keypoint.y, width, height)
                color, thickness, radius = (0, 255, 0), 2, 2
                cv2.circle(annotated_image, keypoint_px, thickness, color, radius)

            # Draw label and score
            category = detection.categories[0]
            category_name = category.category_name
            category_name = '' if category_name is None else category_name
            probability = round(category.score, 2)
            result_text = category_name + ' (' + str(probability) + ')'
            text_location = (self.margin + bbox.origin_x,
                            self.margin + self.row_size + bbox.origin_y)
            cv2.putText(annotated_image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        self.font_size, self.text_color, self.font_thickness)

        return annotated_image

    def timer_on_image(self, image, current_digit) -> np.ndarray:
        """
        Write the current digit on the input image.

        Args:
            image (np.ndarray): The input image.
            current_digit (str): The current digit to be written.

        Returns:
            np.ndarray: Image with the current digit written on it.
        """
        # Write the current digit on the frame
        cv2.putText(image, current_digit, (10, image.shape[0] - 10),
                    self.font, self.font_scale, self.font_color, 
                    self.font_thickness, cv2.LINE_AA)
        return image

    def add_circle(self, image, color) -> np.ndarray:
        """
        Add a colored circle to the input image.

        Args:
            image (np.ndarray): The input image.
            color (int): Color of the circle. 1 for green, 0 for red.

        Returns:
            np.ndarray: Image with the circle added.
        """
        # Determine the color for the circle (green or red)
        if color:
            circle_color = (0, 255, 0)  # Green in BGR
        else:
            circle_color = (0, 0, 255)  # Red in BGR

        # Get the image dimensions
        height, width, _ = image.shape

        # Calculate the radius of the circle (20 pixels as an example)
        radius = 10

        # Calculate the position of the top right corner for the circle
        x_pos = width - radius - 10  # 10 pixels from the right edge
        y_pos = radius + 10         # 10 pixels from the top edge

        # Add the circle to the image
        cv2.circle(image, (x_pos, y_pos), radius, circle_color, -1)  # -1 for a filled circle

        return image
