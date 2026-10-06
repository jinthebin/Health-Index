import pandas as pd
import geopandas
import os
import requests
import contextlib

# tst_data = pd.read_excel('/tstdat/healthindex.xlsx', sheet_name='data') #test data load


with contextlib.chdir('dat/'): #using block-local directory switching 
    #Loading all data:
    health_ind = pd.read_excel('healthindex.xlsx', sheet_name='data')

    #Health index england import:
    hlth_ind_eng_pth = "healthindexscoresengland.xlsx" #defining path
    hlth_ind_eng = pd.read_excel(hlth_ind_eng_pth, sheet_name="Table_2_Index_scores", header=2 )
    
    #Health index england import:
    exc4 = "healthindexscoresengland.xlsx" #defining path
    df4 = pd.read_excel(exc4, sheet_name="Table_2_Index_scores", header=2 )

    region_dat = pd.read_csv("Regions_December_2020_EN_BFC_2022.csv", usecols=['RGN20CD','RGN20NM','BNG_E','BNG_N','LONG','LAT'])

    #Reading LTLA point data:
    LTLA_dat = pd.read_excel("Local_Authority_Districts_December_2021_UK_BFC_2022.xlsx",
                             sheet_name="LAD_DEC_2021_UK_BFC_0",
                            usecols=['LAD21CD','BNG_E','BNG_N','LONG','LAT'])

    #Glossary import:
    glossary = pd.read_excel("healthindex.xlsx", 
                             sheet_name='Table_1_Indicator_details', 
                             header=2,
                             usecols="A:J"
                             )

'''

Transforming data below:

'''


#renaming columns
df4 = (df4.rename(columns={"Area Type [Note 3]": "Area Type"}))

#changing directory to parent directory
# os.chdir("..")
# print(os.getcwd())
# #Loading all data
# health_ind = pd.read_excel("dat/healthindex.xlsx", sheet_name='data')
#removing unwanted columns
health_ind.drop(columns=["Numerator","Denominator"], 
                # axis=1, 
                inplace=True)



hlth_ind_eng = (hlth_ind_eng.rename(columns={"Area Type [Note 3]": "Area Type"})) #tranforming dataframe - renaming columns


region_dat = (region_dat.rename(columns={"RGN20CD": "Area Code"})) #renaming columns
region_dat.drop(columns=["RGN20NM"], 
                # axis=1, 
                inplace=True) #dropping name region

#merging with health_index_england data:
hlth_ind_eng_mrg = pd.merge(
    left=hlth_ind_eng,
    right=region_dat,
    left_on='Area Code',
    right_on='Area Code',
    how="left"
)

'''
New function to create Geopandas df 
with validation steps to exclude NULLs
This is due to error in plotting GeoPandas with NULLs &
other non-numeric values in the geometry column.
'''

def create_point_gdf(data: pd.DataFrame) -> geopandas.GeoDataFrame:
    data = data.copy()

    for column in ("LONG", "LAT"):
        data[column] = pd.to_numeric(data[column], errors="coerce")

    valid = data["LONG"].notna() & data["LAT"].notna()
    data = data.loc[valid].copy()

    if data.empty:
        raise ValueError("No valid LONG/LAT coordinates were found")

    return geopandas.GeoDataFrame(
        data,
        geometry=geopandas.points_from_xy(
            data["LONG"],
            data["LAT"],
        ),
        crs="EPSG:4326",
    )

#converitng to geopandas dataframe
hlth_ind_eng_gdf = create_point_gdf(hlth_ind_eng_mrg)


'''
hlth_ind_eng_gdf = geopandas.GeoDataFrame(
    hlth_ind_eng_mrg, # Our pandas dataframe
    geometry = geopandas.points_from_xy(
        hlth_ind_eng_mrg['LONG'], # Our 'x' column (horizontal position of points)
        hlth_ind_eng_mrg['LAT'] # Our 'y' column (vertical position of points)
        ),
    crs = 'EPSG:4326' # the coordinate reference system of the data - use EPSG:4326 if you are unsure
    )
'''


LTLA_dat = (LTLA_dat.rename(columns={"LAD21CD": "Area Code"})) #renaming columns

#merging with health_index_england data:
hlth_ind_eng_LTLA_mrg = pd.merge(
    left=hlth_ind_eng,
    right=LTLA_dat,
    left_on='Area Code',
    right_on='Area Code',
    how="inner"
)

#converitng to geopandas dataframe
hlth_ind_eng_LTLA_gdf = create_point_gdf(hlth_ind_eng_LTLA_mrg)
'''
hlth_ind_eng_LTLA_gdf = geopandas.GeoDataFrame(
    hlth_ind_eng_LTLA_mrg, # Our pandas dataframe
    geometry = geopandas.points_from_xy(
        hlth_ind_eng_LTLA_mrg['LONG'], # Our 'x' column (horizontal position of points)
        hlth_ind_eng_LTLA_mrg['LAT'] # Our 'y' column (vertical position of points)
        ),
    crs = 'EPSG:4326' # the coordinate reference system of the data - use EPSG:4326 if you are unsure
    )
'''

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

'''
api_url = "https://nihr.opendatasoft.com/api/explore/v2.1/catalog/datasets/nihr-infrastructure-supported-projects/exports/json" 
nihr = fetch_json_from_api(api_url)
nihr_data = pd.json_normalize(nihr)

'''
#changing directory back to src folder
# os.chdir("src")
