def predict_image(image):
    # Perform prediction using your ML model
    # ...
    # Your prediction logic here
    # ...

    prediction_result = "image proccessed to mml models"

    return prediction_result




import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def trainPlantPredictionModel(dataset_path):
    # Load the dataset
    dataset = pd.read_csv(dataset_path)

    # Split the dataset into input features (X) and target variable (y)
    X = dataset[['temperature', 'elevation', 'precipitation']]
    y = dataset['plant_type']

    # Create and train the model
    model = DecisionTreeClassifier()
    model.fit(X, y)

    # Return the trained model
    return model


#modeltrainPlantPredictionModel = trainPlantPredictionModel('./plantprdecitiondataset.csv')