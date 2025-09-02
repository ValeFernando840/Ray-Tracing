import pandas as pd

df = pd.read_excel('NuevoExcelCompleto_para_ver.xlsx')

R0 = 6.371E6 # radio tierra en mts. 
latitudes_columns = [f'lat_{i}' for i in range(1,101)]
longitudes_columns = [f'long_{i}' for i in range(1,101)]
alturas_columns = [f'elev_{i}' for i in range(1,101)]

new_df = df[latitudes_columns + longitudes_columns + alturas_columns]


print(new_df)