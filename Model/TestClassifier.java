import java.io.BufferedWriter;
import java.io.FileWriter;

import weka.classifiers.AbstractClassifier;
import weka.classifiers.Classifier;
import weka.core.Attribute;
import weka.core.Instances;
import weka.core.converters.ConverterUtils.DataSource;

public class TestClassifier 
{
	
	public static void main(String[] args) 
	{
		try 
		{
			DataSource source = new DataSource("PlayerData.csv");
			Instances data = source.getDataSet();
			
			//removes irrelevant attributes
			data.deleteAttributeAt(0);
			data.deleteAttributeAt(5);
			
			if (data.classIndex() == -1)
				   data.setClassIndex(data.numAttributes() - 1);
			
			DataSource sourceNew = new DataSource("UnlabelledPlayerData.csv");
			Instances unlabeled = sourceNew.getDataSet();

			Classifier classifier = generateModel(data);
			
			ClassifyNewInstances(classifier, unlabeled);
			
		}catch(Exception e) 
		{
			e.printStackTrace();
		}
	}
	
	public static Classifier generateModel(Instances data) 
	{
		try 
		{
			 Classifier classifier = AbstractClassifier.forName("weka.classifiers.meta.Bagging", new String[]{"-P", "74", "-I", "16", "-S", "1", "-W", "weka.classifiers.trees.RandomTree", "--", "-M", "7", "-K", "14", "-depth", "9", "-N", "0", "-U"});
			 classifier.buildClassifier(data);

			 return classifier;
			 
		}catch(Exception e) 
		{
			e.printStackTrace();
			return null;
		}
	
	}
	
	public static void ClassifyNewInstances(Classifier classifier, Instances unlabeled) 
	{
		try 
		{
			 String[] names = new String[unlabeled.numInstances()];
			 
			 //store names
			 for(int i = 0; i < names.length; i++) 
			 {
				 names[i] = unlabeled.instance(i).stringValue(0);
			 }
			
			 unlabeled.deleteAttributeAt(0);
			 unlabeled.setClassIndex(unlabeled.numAttributes() - 1);
			 
			 // create copy
			 Instances labeled = new Instances(unlabeled);

			 // label instances
			 for (int i = 0; i < unlabeled.numInstances(); i++) 
			 {
			   double clsLabel = classifier.classifyInstance(unlabeled.instance(i));
			   labeled.instance(i).setClassValue(clsLabel);
			 }
			 
			 Attribute attribute = new Attribute("Names", true);
			 labeled.insertAttributeAt(attribute, 0);
			 
			 for (int i = 0; i < unlabeled.numInstances(); i++) 
			 {
			   labeled.instance(i).setValue(0, names[i]);
			 }
			 
			 
			 BufferedWriter writer = new BufferedWriter(
                     new FileWriter("labelledPlayerData.csv"));
			 writer.write(labeled.toString());
			 writer.newLine();
			 writer.flush();
			 writer.close();
			 
			 System.out.println("done");
			 
		}catch(Exception e) 
		{
			e.printStackTrace();
		}
		
	}
	
}
