import global_options
import pandas as pd
from pathlib import Path

### Group firms by averaging document TFIDF scores

print("Calculating mean values of TFIDF while grouping by firms (in case of multiple document scores).")

# Read in data
tfidf = pd.read_csv(str(Path(global_options.OUTPUT_FOLDER, "scores", "firm_scores_TFIDF.csv")))

# Calculate mean values while group by firm
tfidf = tfidf.groupby(['firm_id'])[['diversity', 'inclusion', 'equity']].mean()

print(tfidf.head())

# Save output
tfidf.to_csv(Path(global_options.OUTPUT_FOLDER,"scores","mean_firm_scores_TFIDF.csv"))

print("Done.")