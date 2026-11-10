## Combining the data from the Pristine Surveys XXVII and XVII 

import pandas as pd
import numpy as np

# reading the data in
pristine = pd.read_csv("Cleaned Data/pristine_c19_confirmed.csv")
gaia_pristine = pd.read_csv("Cleaned Data/gaia_pristine_c19_stars.csv")

# losing the duplicates 
combined = pd.concat([pristine, gaia_pristine], ignore_index=True)
combined = combined.drop_duplicates(subset="source_id", keep="first")

# losing the leftover index columns
combined = combined.loc[:, ~combined.columns.str.startswith("Unnamed")]

# combining all feh values into one column, prioritising the feh over feh_pr column **look into best choise here
combined["feh_combined"] = combined["feh"].fillna(combined["feh_pr"])

# saving to file
combined.to_csv("Cleaned Data/the_one_c19_to_rule_them_all.csv", index=False)