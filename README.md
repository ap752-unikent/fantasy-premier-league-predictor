# fantasy-premier-league-predictor

- Data Collection/TrainingDataCollection is used to collect the training data from the Fantasy Premier League api
	- It collects all possibly useful information however some columns may be excluded during model training
	- Uses pandas, numpy 
	
- Model/EvaluateClassifier evaluates the trained classifier using 10 fold cross validation. 
	- It returns the correlation coefficient and the mean absolute error
	- It uses the WEKA Java Library to generate the model

- Model/TestClassifier allows a user to input player information (unlabeledPlayerData.csv) to predict the performance of the player for the next X (currently 3) weeks. 
