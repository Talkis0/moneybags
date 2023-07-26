import sys
import pandas as pd
filenames = sys.argv[1:-1]
outfilename = sys.argv[-1]
big_df = pd.DataFrame()
for f in filenames:
    df_temp = pd.read_csv( f )
    big_df = pd.concat( [big_df, df_temp], ignore_index=True  )
big_df.to_csv( outfilename, index=False )