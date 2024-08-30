import pandas as pd

import sys

import os



# Paths to csv files

docking_score = sys.argv[1]

qikprop_output = sys.argv[2]



prot_name = docking_score.split('/')[-1].split('_')[0]



# Read csv/tsv as dataframe

df_score = pd.read_csv(docking_score)

df_qikprop = pd.read_csv(qikprop_output,sep='\t')



df_merge = df_qikprop.merge(df_score, how='inner', left_on='molecule', right_on='s_m_title')



df_merge.drop('s_m_title',inplace=True,axis=1)



output_path = os.sep.join(os.path.normpath(docking_score).split(os.sep)[:4]) + '/' + prot_name + '_merge.csv'



df_merge.to_csv(output_path,index=False,sep=',')
