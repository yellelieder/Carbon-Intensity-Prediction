# import config
# from app.helpers import common
# import os
# import pandas as pd

# type=0
# file_index=1 if type==config.p_id else 0
# file=config.merged_data_folder+sorted(os.listdir(config.merged_data_folder))[file_index]
# try:
#     df=pd.read_csv(file, sep=",", index_col=0, dtype=object)
# except FileNotFoundError as exception:
#     common.print_fnf(file, exception)
# df=df.replace("-",0)
# #formatting datetime
# df["Datum"]= df[['Datum', 'Uhrzeit']].agg(' '.join, axis=1)
# print(df["Datum"])#


for i in range(1,3):
    i=str(i)
    print(i)