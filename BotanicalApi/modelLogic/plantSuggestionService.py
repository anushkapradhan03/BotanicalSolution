from django.conf import settings
import os

from sklearn.tree import DecisionTreeClassifier
import pandas as pd

from BotanicalApi.constant.BotanicalConstant import BotanicalConstant
import warnings



basePath = settings.BASE_DIR
datasetRelativePath = 'BotanicalApi/plantprdecitiondataset.csv'
datasetPath = os.path.join(basePath, datasetRelativePath)


def suggestPlant(temperature, precipitation, elevation):
    
    # Load the dataset  
    dataset = pd.read_csv(datasetPath)

    # Split the dataset into input features (X) and target variable (y)
    X = dataset[[BotanicalConstant.temperature, BotanicalConstant.elevation, BotanicalConstant.precipitation]]
    y = dataset[BotanicalConstant.plant_type]

    # Create and train the model
    model = DecisionTreeClassifier()
    
    warnings.filterwarnings("ignore", category=UserWarning)
    model.fit(X, y)

    # Perform the prediction based on the given values
    predicted_plant = model.predict([[temperature, elevation, precipitation]])


    # predicted_plant = ["abc", "def"]
    predicted_plant = predicted_plant.tolist() 

    return predicted_plant


if __name__ == '__main__':
    print("importing plantSuggestionService")