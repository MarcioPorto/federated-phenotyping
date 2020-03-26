### Instructions to generate csv from i2b2 Obesity Challenge xml files

First gain access to dataset. Once you have the access, you need to download the following xml files mentioned below:
1. Download Training Data: Obesity Training Records (XML).
2. Download Training Data: The second set of Obesity Training Records (XML).
3. Download Training Data: Intuitive Annotations for Training Records (XML).
4. Download Training Data: Annotations for the second set of Obesity Training Records (XML).
5. Download Training Data: Addendum to the Intuitive Annotations for Training Records (XML).
6. Download Test Data: Test Records (XML).
7. Download Test Data: Ground Truth for Intuitive Judgments on Test Data (XML).

Move all the files inside the `downloads` folder at the root of the project.

Install the dependencies using `pip install -r requirments.txt`

Run `python gen_csv.py` to generate `train.csv` and `test.csv`. 
They will be in the `data` folder at the root of the project.