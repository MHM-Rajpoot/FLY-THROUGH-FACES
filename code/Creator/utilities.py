from common import *

class Utilities:

    def __init__(self) -> None:
        pass

    def check_cnic(self, cnic: str) -> bool:
        """
        Check if the provided CNIC (Computerized National Identity Card) is valid.

        Args:
            cnic (str): The CNIC to be checked.

        Returns:
            bool: True if the CNIC is valid, False otherwise.
        """
        numbers = '1234567890'
        
        if len(cnic) < 1 or len(cnic) > 13:
            return False
        
        for i in cnic:
            if i in numbers:
                continue
            else:
                return False

        return True
    
    def train_test_split(self):
        """
        Split the dataset into train and test sets for model training and evaluation.
        """
        base_dir = '...'
        os.makedirs(base_dir, exist_ok=True)

        train_dir = os.path.join(base_dir, 'train')
        test_dir = os.path.join(base_dir, 'test')

        # Create the train and test directories
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(test_dir, exist_ok=True)

        # Create the positive and negative subdirectories inside train and test
        for directory in [train_dir, test_dir]:
            os.makedirs(os.path.join(directory, 'positive'), exist_ok=True)
            os.makedirs(os.path.join(directory, 'negative'), exist_ok=True)

        source_positive_dir = '...'
        source_negative_dir = '...'

        train_positive_dir = os.path.join(train_dir, 'positive')
        test_positive_dir = os.path.join(test_dir, 'positive')

        train_negative_dir = os.path.join(train_dir, 'negative')
        test_negative_dir = os.path.join(test_dir, 'negative')

        # List all positive and negative image files
        positive_images = os.listdir(source_positive_dir)
        negative_images = os.listdir(source_negative_dir)

        # Shuffle the lists of images randomly
        random.shuffle(positive_images)
        random.shuffle(negative_images)

        # Calculate the split index for positive images
        split_index_positive = int(0.8 * len(positive_images))

        # Calculate the split index for negative images
        split_index_negative = int(0.8 * len(negative_images))

        # Copy 80% of the positive images to train/positive
        for image in positive_images[:split_index_positive]:
            src_path = os.path.join(source_positive_dir, image)
            dest_path = os.path.join(train_positive_dir, image)
            shutil.copy(src_path, dest_path)

        # Copy 20% of the positive images to test/positive
        for image in positive_images[split_index_positive:]:
            src_path = os.path.join(source_positive_dir, image)
            dest_path = os.path.join(test_positive_dir, image)
            shutil.copy(src_path, dest_path)

        # Copy 80% of the negative images to train/negative
        for image in negative_images[:split_index_negative]:
            src_path = os.path.join(source_negative_dir, image)
            dest_path = os.path.join(train_negative_dir, image)
            shutil.copy(src_path, dest_path)

        # Copy 20% of the negative images to test/negative
        for image in negative_images[split_index_negative:]:
            src_path = os.path.join(source_negative_dir, image)
            dest_path = os.path.join(test_negative_dir, image)
            shutil.copy(src_path, dest_path)

    def usb_passport(self, fcnic: str):
        """
        Write the provided CNIC to a file on the USB drive.

        Args:
            fcnic (str): The CNIC to be written to the file.
        """
        with open('...', 'w') as file:
            file.write(fcnic)
