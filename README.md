# BoxOfficePrediction
The project aims to predict the box office and score of an upcoming movie

## Group Members: 
[Quan Yuan](https://github.com/libou), [Yuheng Liu](https://github.com/DearBean), [Wenlong Wu](https://github.com/wn248211)

## Instruction:

### data
This directory stores all the data set used and generated in the project.  
1. "boxoffice_dataset.csv": the raw dataset  
2. "prediction.csv": the final result predicted by the model  
3. "trainset.csv": training dataset  
4. "testset.csv": testing dataset

### data_processing
This directory stores the codes used for data cleaning and integration.  
"boxoffice_dataset.csv" in the 'data' folder has already been cleaned and integrated.  

### visualization
This directory stores the codes used for data analysis. They presents the relationship between
some features and the movie box office.

### WebScraping
This directory stores the codes used for scraping raw dataset from multiple websites. We also built
a proxy program to avoid Anti-Spider.

## How to run:
**feature_engineering.py**: This file contains all functions used for processing each column in 
the raw dataset.

**feature_selection.py**: This file generates a new dataset which is fully prepared and divides the
dataset into training set and testing set. By commenting some rows, the program can generate 
different combinations of features.  
Run this file and the generated dataset will be saved under the "data" folder.

**modeling.ipynb**: This notebook builds the final model and has all the material used for model
tuning. Running this notebook will generate a .pkl file under the root folder.

**model_testing.py**: This file runs the testing using the generated model and prints the r2_socre on
the console. The result is saved under the "data" folder.
