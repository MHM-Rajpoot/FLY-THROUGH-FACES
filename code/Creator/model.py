from common import *

class ModelA:

    def __init__(self) -> None:
        """
        Initialize ModelA class.
        """

        # Load the model structure from the JSON file
        with open('...', 'r') as json_file:
            model_structure = json_file.read()

        # Recreate the model from the saved structure
        base_model = model_from_json(model_structure)

        # Load the model weights from the H5 file
        base_model.load_weights('...')

        # Freeze layers in the base model
        for layer in base_model.layers:
            layer.trainable = False

        # Add custom classification layers
        x = Flatten()(base_model.output)
        x = Dense(4096, activation='relu')(x)
        x = Dense(4096, activation='relu')(x)
        x = Dense(1024, activation='relu')(x)
        predictions = Dense(1, activation='sigmoid')(x)

        # Create the model
        self.model = Model(inputs=base_model.input, outputs=predictions)

        # Compile the model
        self.model.compile(optimizer=Adam(lr=0.0001), loss='binary_crossentropy', metrics=['accuracy'])

    def model_a_training(self) -> bool:
        """
        Train the model using the prepared datasets.

        Returns:
            bool: True if training is successful, False otherwise.
        """

        # Set batch size and number of epochs
        batch_size = 15
        epochs = 3

        # Directory paths for your new dataset directories
        train_data_dir = '...'  # Adjust this to your training data directory
        validation_data_dir = '...'  # Adjust this to your validation data directory

        # Define data generators without data augmentation
        train_datagen = ImageDataGenerator(rescale=1.0/255.0)
        validation_datagen = ImageDataGenerator(rescale=1.0/255.0)

        # Prepare data generators
        train_generator = train_datagen.flow_from_directory(
            train_data_dir,
            target_size=(200, 150),  # Updated target size without channels
            batch_size=batch_size,
            class_mode='binary')

        validation_generator = validation_datagen.flow_from_directory(
            validation_data_dir,
            target_size=(200, 150),  # Updated target size without channels
            batch_size=batch_size,
            class_mode='binary')

        # Train the model
        self.model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size)

        return True

    def model_a_save(self, fcnic: str) -> bool:
        """
        Save the trained model architecture and weights to files.

        Args:
            fcnic (str): The CNIC used as the model identifier.

        Returns:
            bool: True if the model is successfully saved, False otherwise.
        """
        os.makedirs(f'...', exist_ok=True)

        # Save the model architecture to a JSON file
        model_json = self.model.to_json()
        with open(f"...", "w") as json_file:
            json_file.write(model_json)

        # Save the model weights to an HDF5 file
        self.model.save_weights(f"...")

        print("Model architecture and weights have been saved.")

        del self.model

        return True

    def train_and_save(self, fcnic: str) -> bool:
        """
        Train the model and save the trained model.

        Args:
            fcnic (str): The CNIC used as the model identifier.

        Returns:
            bool: True if training and saving are successful, False otherwise.
        """
        if self.model_a_training():
            if self.model_a_save(fcnic):
                return True
        return False
