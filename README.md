# fantasy-premier-league-predictor

- Data Collection/TrainingDataCollection is used to collect the dataset from the Fantasy Premier League api
	- It collects all possibly relevant information however some columns may be excluded during model training
	- PlayerData.csv is the generated csv file after TrainingDataCollection is run
	
- Model/EvaluateClassifier evaluates the trained classifier using 10 fold cross validation. 
	- EvaluateClassifier returns the correlation coefficient and the mean absolute error

- Model/TestClassifier allows a user to input player information (unlabeledPlayerData.csv) to predict the performance of the player for the next X (currently 3) weeks. 
