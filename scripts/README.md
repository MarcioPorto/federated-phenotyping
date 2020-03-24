### Instructions to generate csv from i2b2 Obesity Challenge xml files

First gain access to dataset. Once you have the access, you need to download the following xml files and rename exactly as below:
1. Download Training Data: Obesity Training Records (XML) as rename as `text1.xml`
2. Download Training Data: The second set of Obesity Training Records (XML) as rename as `text2.xml`
3. Download Training Data: Intuitive Annotations for Training Records (XML) as rename as `label1.xml`
4. Download Training Data: Annotations for the second set of Obesity Training Records (XML) as rename as `label2.xml`
5. Download Training Data: Addendum to the Intuitive Annotations for Training Records (XML) as rename as `label3.xml`
6. Download Test Data: Test Records (XML) as rename as `test_text.xml`
7. Download Test Data: Ground Truth for Intuitive Judgments on Test Data (XML) as rename as `test_label.xml`

Move all the files inside the `scripts` folder.

Run `python gen_csv.py` to generate `train.csv` and `test.csv` and move them to the `data` folder.