
## This is a ML project for MSc at the University of Europe for Applied Sciences, specifed to create a model, able to predict hotel room rates

### Overview

* The pre-processing phase, uses a compiler directive: omp, for faster processing of the files

* The target variable is the room-rate

* Feature engineering was implemented, in order to introduce two new features: hotel_location and number_of_star

* The github directory is at: ***https://github.com/Chukwunazaekpere/hotel-room-rate-prediction.git***, the master directory (not main)

### Instructions

1. Create a virtual environment

2. Do: **pip -r install requierments.txt**

3. The ***processor.py*** file, pre-processes the files, in the data folder and writes to ***processed_data.csv*** file

4. The ***predict.ipynb*** is where the model is trained.

### Cell Interpretations

* In cell 3 we're doing one-hot endcoding, by replacing string values with integer values.

* in cell 4, we're sharing our processed data into target and features

* in cell 5, we are splitting our data into training and validation data

* in cell 6, we are training our model and measurung our model score