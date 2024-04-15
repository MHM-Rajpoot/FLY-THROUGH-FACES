from common import *

class ModelA():

    def __init__(self) -> None:
        """
        Initialize the ModelA class.
        """
        pass

    def model_a_verification(self,cnic:str) -> bool:
        """
        Verify the model based on the provided CNIC number.

        Args:
            cnic (str): The CNIC number to identify the model.

        Returns:
            Tuple[float, float]: Average probabilities for class 0 and class 1.
        """
        # Load the model architecture from a JSON file
        with open(f'...', "r") as json_file:
            loaded_model_json = json_file.read()

        self.loaded_model = model_from_json(loaded_model_json)

        # Load the model weights
        self.loaded_model.load_weights(f'...')
        
        images = []

        # Load and preprocess images for verification
        for i in range(1,21):
            temp = cv2.imread('...'.format(i))
            temp = cv2.resize(temp, (150, 200), interpolation=cv2.INTER_CUBIC)
            temp = temp.astype('float32')  # Convert to float32
            temp = np.expand_dims(temp, axis=0)  # Add batch dimension
            images.append(temp)
    
        # Initialize variables to accumulate probabilities for each class
        count_class_0 = 0
        count_class_1 = 0

        # Predict probabilities for each image
        for img in images:
            prediction = self.loaded_model.predict(img)
            print('\r',end='')

            threshold = 0.5  # Adjust this threshold as needed
            predicted_class = 1 if prediction > threshold else 0

            if(predicted_class == 0):
                count_class_0 += 1
            else:
                count_class_1 += 1

        # Calculate average probabilities for class 0 and class 1
        avg_prob_class_0 = float(count_class_0 / 20.0)
        avg_prob_class_1 = float(count_class_1 / 20.0)

        return avg_prob_class_0, avg_prob_class_1
