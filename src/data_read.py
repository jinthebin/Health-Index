import pandas as pd
import os

#changing directory to parent directory
os.chdir("..")
print(os.getcwd())
#Loading all data
health_ind = pd.read_excel("dat/healthindex.xlsx", sheet_name='data')
#removing unwanted columns
health_ind.drop(columns=["Numerator","Denominator"], axis=1, inplace=True)

glossary = pd.read_excel("dat/healthindex.xlsx", 
                             sheet_name='Table_1_Indicator_details', 
                             header=2,
                             usecols="A:J"
                             )
#Health index england import:
exc4 = "dat/healthindexscoresengland.xlsx" #defining path
df4 = pd.read_excel(exc4, sheet_name="Table_2_Index_scores", header=2 )
df4 = (df4.rename(columns={"Area Type [Note 3]": "Area Type"})) #tranforming dataframe - renaming columns

#changing directory back to src folder
os.chdir("src")