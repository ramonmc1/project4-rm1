#Import dependencies into juputer notebook
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error , r2_score


def data_info():
    pd.options.mode.chained_assignment = None
    df = pd.read_csv("Resources/RealEstate_Georgia.csv")
    df_gdp = pd.read_csv("Resources/GAgdpbycounty2020.csv")
    df_income = pd.read_csv("Resources/ACSST5Y2020.S1901_data_with_overlays_2022-05-17T173521.csv")
    df_gdp2 = df_gdp.drop('CAGDP2 Gross domestic product (GDP) by county and metropolitan area 1/', axis=1, inplace=False)
    df_gdp2= df_gdp2.rename(columns={'Unnamed: 1': 'county', 'Unnamed: 2': 'GDP (thousands)'}).dropna()
    gdp_county_column = df_gdp2["county"].str.split(",", n =1, expand = True) 
    df_gdp2["county"]= gdp_county_column[0]
    df_gdp_clean = df_gdp2[2:].reset_index(drop=True)
    
    cleandata= df_income[['NAME', 'S1901_C03_012E','S1901_C04_012E']]
    #Renaming the columns
    cleandata_transformed = cleandata.rename(columns={"NAME": "name",
                                                            "S1901_C03_012E": "Married Family Income",
                                                            "S1901_C04_012E": "Nonfamily Income"})
    cleandata_transformed["county"] = cleandata_transformed["name"].str.replace(' County, Georgia', '')
    census_clean = cleandata_transformed.dropna().reset_index().drop(columns = ['name','index'])
    census_clean = census_clean[1:160].reset_index(drop=True)
    census_clean["Married Family Income"] = census_clean["Married Family Income"].astype('int')
    census_clean["Nonfamily Income"] = census_clean["Nonfamily Income"].astype('int')

    df_mergefiles1 = pd.merge(census_clean, df_gdp_clean, on="county", how="outer")
    
    #Cleaning Data
    df.drop_duplicates()
    df_cln = df.loc[(df.is_bankOwned == False) & (df.is_forAuction == False)& (df.homeType != 'LOT')]
    df_cln.loc[:,'Month'] = df_cln.loc[:,'datePostedString'].str[0].astype(int)
    #df_cln['Month'] = df_cln['datePostedString'].str[0].astype('int')
    df_cln = df_cln.loc[(df_cln.yearBuilt < 2022) & (df_cln.yearBuilt > 1800) ]
    drop_columns = ['Unnamed: 0', 'id', 'stateId', 'countyId', 'cityId', 'country',
        'is_bankOwned', 'is_forAuction', 'event', 'time','state',
        'streetAddress', 'hasBadGeocode',#'homeType',
        'description', 'currency', 'livingAreaValue',
        'lotAreaUnits', 'buildingArea', 
        'garageSpaces', 'hasPetsAllowed','datePostedString']
    df_ready = df_cln.drop(columns=drop_columns).dropna()
    df_ready["county"] = df_ready["county"].str.replace(' County', '')
    df_ready["county"] = df_ready["county"].str.replace('Dekalb', 'DeKalb')

    df_merge = pd.merge(df_ready, df_mergefiles1, on="county", how="left")
    
    return df_merge

def cluster_info(df_merge):    
    #deleting additional columns for clustering analysis
    drop_columns2 = ['city','Month','county', 'zipcode', 'homeType', 'levels', 'pricePerSquareFoot', 'parking', 'longitude', 'latitude']
    df_cluster = df_merge.drop(columns=drop_columns2)
    df_cluster.reset_index(drop=True, inplace=True)
    
    df_filtered = df_cluster
    df_filtered = df_filtered.loc[(df_filtered.price < 1000000) & (df_filtered.livingArea < 15000) & (df_filtered.livingArea > 400) & (df_filtered.bathrooms < 8) &( df_filtered.bedrooms < 9) & (df_filtered.bedrooms > 0)]

    df_num = pd.get_dummies(df_filtered)

    scaler = StandardScaler().fit(df_num)
    data_cluster = scaler.transform(df_num)
    
    pca = PCA(n_components=0.90)
    data_pca = pca.fit_transform(data_cluster)
    tsne = TSNE(learning_rate=100)
    tsne_data = tsne.fit_transform(data_pca)

    inertia = []
    k = list(range(1, 11))

    # Calculate the inertia for the range of k values
    for i in k:
        km = KMeans(n_clusters=i, random_state=0)
        km.fit(data_cluster)
        inertia.append(km.inertia_)

    # Create the Elbow Curve using hvPlot
    elbow_data = {"k": k, "inertia": inertia}
    df_elbow = pd.DataFrame(elbow_data)
    
    def get_clusters(k, data, column):
        # Initialize the K-Means model
        model = KMeans(n_clusters=k, random_state=42)
        # Train the model
        model.fit(data)
        # Predict clusters
        predictions = model.predict(data)
        # Create return DataFrame with predicted clusters
        data[column] = model.labels_
        return data

    cluster_name = ["class2", "class3", "class4", "class6"]
    ki = [2, 3, 4, 6]
    for k in ki:
        get_clusters(k, df_num, cluster_name[ki.index(k)])
   
    #create dictionary
    x_l = tsne_data[:,0].tolist()
    y_l = tsne_data[:,1].tolist()
    c_2 = df_num["class2"].tolist()
    c_3 = df_num["class3"].tolist()
    c_4 = df_num["class4"].tolist()
    c_6 = df_num["class6"].tolist()
    price = df_num["price"].tolist()
    livingArea = df_num["livingArea"].tolist()

    cluster_dict = {
    "x": x_l,
    "y": y_l,
    "c2": c_2,
    "c3": c_3,
    "c4": c_4,
    "c6": c_6,
    "price": price,
    "livingArea":livingArea
    }

    data1 = pd.DataFrame(cluster_dict)

    return data1, df_elbow

def line_info(df_merge): 
    df_merge.rename(columns = {'Married Family Income':'family_income', 'GDP (thousands)':'GDP'}, inplace = True)
    df_line = df_merge
    df_line = df_line.loc[(df_line.price < 2000000) & (df_line.price > 10000) & (df_line.livingArea < 12000) & (df_line.livingArea > 200) &(df_line.pricePerSquareFoot < 700) & (df_line.bathrooms < 8) & (df_line.bathrooms > 0) &( df_line.bedrooms < 9) & (df_line.bedrooms > 0) & (df_line.yearBuilt < 2022) & (df_line.yearBuilt > 1900)]

    y = df_line['price']
    colums_to_drop = ['pricePerSquareFoot','price', 'city', 'zipcode',
    'parking', 'hasGarage', 'levels', 'pool', 'spa',
    'homeType', 'county', 'Month','Nonfamily Income']
    feature_cols = df_line.drop(columns = colums_to_drop)

    X = feature_cols

    data3 = df_merge[['price', 'pricePerSquareFoot', 'yearBuilt',
    'longitude', 'latitude', 'livingArea', 'bathrooms', 'bedrooms',
    'parking', 'hasGarage', 'pool', 'spa', 'isNewConstruction',
    'family_income', 
    'GDP']]
    data3.reset_index(drop=True, inplace=True)

    # split data into train and test
    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=2)
    # the test set will be 20% of the whole data set

    reg = LinearRegression()
    reg.fit(x_train,y_train)

    # Use our model to make predictions
    predicted = reg.predict(x_test)

    # Score the predictions with mse and r2
    mse = mean_squared_error(y_test, predicted)
    r2 = r2_score(y_test, predicted)



    x_la = X["livingArea"]

    xl = np.array(x_la).reshape((-1,1))
    yl = np.array(y)
    regl = LinearRegression().fit(xl, yl)
    m = regl.coef_[0]
    la_int = regl.intercept_
    fit_la = m*x_la + la_int


    x_yb = X["bathrooms"]

    xb = np.array(x_yb).reshape((-1,1))
    yb = np.array(y)
    regb = LinearRegression().fit(xb, yb)
    m = regb.coef_[0]
    yb_int = regb.intercept_
    fit_yb = m*x_yb + yb_int



    data = {"livingArea": x_la, "bathrooms": x_yb, "price": y, "pred_la_price":fit_la, "pred_bath_price":fit_yb}

    data5 = pd.DataFrame(data)# columns = "livingArea", "bathrooms", "price", "pred_la_price", "pred_bath_price")
    data5.reset_index(drop=True, inplace=True)
    
    return data3, data5



