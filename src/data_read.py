import pandas as pd
import geopandas
import os
import requests

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
hlth_ind_eng_pth = "dat/healthindexscoresengland.xlsx" #defining path
hlth_ind_eng = pd.read_excel(hlth_ind_eng_pth, sheet_name="Table_2_Index_scores", header=2 )
hlth_ind_eng = (hlth_ind_eng.rename(columns={"Area Type [Note 3]": "Area Type"})) #tranforming dataframe - renaming columns

region_dat = pd.read_csv("dat/Regions_December_2020_EN_BFC_2022.csv", usecols=['RGN20CD','RGN20NM','BNG_E','BNG_N','LONG','LAT'])
region_dat = (region_dat.rename(columns={"RGN20CD": "Area Code"})) #renaming columns
region_dat.drop(columns=["RGN20NM"], axis=1, inplace=True) #dropping name region

#merging with health_index_england data:
hlth_ind_eng_mrg = pd.merge(
    left=hlth_ind_eng,
    right=region_dat,
    left_on='Area Code',
    right_on='Area Code',
    how="left"
)

#converitng to geopandas dataframe

hlth_ind_eng_gdf = geopandas.GeoDataFrame(
    hlth_ind_eng_mrg, # Our pandas dataframe
    geometry = geopandas.points_from_xy(
        hlth_ind_eng_mrg['LONG'], # Our 'x' column (horizontal position of points)
        hlth_ind_eng_mrg['LAT'] # Our 'y' column (vertical position of points)
        ),
    crs = 'EPSG:4326' # the coordinate reference system of the data - use EPSG:4326 if you are unsure
    )


#Reading LTLA point data:
LTLA_dat = pd.read_csv("dat/GLTLA_DEC_2022_EW_BFC.csv", usecols=['GLTLA22CD','BNG_E','BNG_N','LONG','LAT'])
LTLA_dat = (region_dat.rename(columns={"GLTLA22CD": "Area Code"})) #renaming columns

#merging with health_index_england data:
hlth_ind_eng_LTLA_mrg = pd.merge(
    left=hlth_ind_eng,
    right=LTLA_dat,
    left_on='Area Code',
    right_on='Area Code',
    how="left"
)

#converitng to geopandas dataframe
hlth_ind_eng_LTLA_gdf = geopandas.GeoDataFrame(
    hlth_ind_eng_LTLA_mrg, # Our pandas dataframe
    geometry = geopandas.points_from_xy(
        hlth_ind_eng_LTLA_mrg['LONG'], # Our 'x' column (horizontal position of points)
        hlth_ind_eng_LTLA_mrg['LAT'] # Our 'y' column (vertical position of points)
        ),
    crs = 'EPSG:4326' # the coordinate reference system of the data - use EPSG:4326 if you are unsure
    )


#Reading NIHR Awards Data from OpenSoft API: 
# define function to make API call:
def fetch_json_from_api(url):
    try:
        # Send a GET request to the API endpoint
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            return json_data
        else:
            print(f"Error: Unable to fetch data, Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Exception occurred: {e}")
        return None

api_url = "https://nihr.opendatasoft.com/api/explore/v2.1/catalog/datasets/nihr-infrastructure-supported-projects/exports/json" 
nihr = fetch_json_from_api(api_url)
nihr_data = pd.json_normalize(nihr)

#changing directory back to src folder
os.chdir("src")