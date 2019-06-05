import java.util.Random;

import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
import weka.classifiers.Evaluation;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class EvaluateClassifier 
{

	public static void main(String[] args) 
	{
		try 
		{
			DataSource source = new DataSource("PlayerData.csv");
			Instances data = source.getDataSet();
			
			data.deleteAttributeAt(0);
			data.deleteAttributeAt(5);
			
			 if (data.classIndex() == -1)
				   data.setClassIndex(data.numAttributes() - 1);
			
			EvaluateModel(data);
			
		}catch(Exception e) 
		{
			e.printStackTrace();
		}
		
	}
	
	public static void EvaluateModel(Instances data) 
	{
		try 
		{	
			Classifier classifier = AbstractClassifier.forName("weka.classifiers.meta.Bagging", new String[]{"-P", "74", "-I", "16", "-S", "1", "-W", "weka.classifiers.trees.RandomTree", "--", "-M", "7", "-K", "14", "-depth", "9", "-N", "0", "-U"});
			Evaluation eval = new Evaluation(data);
			eval.crossValidateModel(classifier, data, 10, new Random(1));
			
			System.out.println(eval.correlationCoefficient());
			System.out.println(eval.meanAbsoluteError());
		} catch (Exception e) 
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
}
