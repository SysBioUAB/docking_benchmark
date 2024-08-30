import pandas as pd
import sys

# Import the CSV tables from Schrodinger
first_prot=sys.argv[1]
second_prot=sys.argv[2]
output_path=sys.argv[3]

# Names of the proteins
prot1=first_prot.split('/')[-1].split('.')[0]
prot2=second_prot.split('/')[-1].split('.')[0]

# Read CSV files
df1=pd.read_csv(first_prot)
df2=pd.read_csv(second_prot)

# Select the title and glide_score columns, only entries with a score <=- 4.5
df1_score = df1[["s_m_title","r_i_glide_gscore"]].loc[df1["r_i_glide_gscore"] <= -4.5]
df2_score = df2[["s_m_title","r_i_glide_gscore"]].loc[df2["r_i_glide_gscore"] <= -4.5]

# Inner merge to select the compounds that are shared in both proteins
scores= df1_score.merge(df2_score,left_on="s_m_title",right_on="s_m_title",how='inner')

# Rename columns
scores=scores.rename(columns={'s_m_title': 'Pubchem_ID', 'r_i_glide_gscore_x': 'Glide_score_'+prot1, 'r_i_glide_gscore_y': 'Glide_score_'+prot2})

# Export output CSV
scores.to_csv(output_path,index=False)
