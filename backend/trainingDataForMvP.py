import os
import pandas as pd
base_dir = os.path.dirname(os.path.abspath(__file__))
dataset_path=os.path.join(base_dir, 'data', 'data.csv')
df = pd.read_csv(dataset_path)
with open(os.path.join(base_dir, 'data', 'mvp_train.txt'), 'w', encoding='utf-8') as f:
    for idx, row in df.iterrows():
        line = f"{row['text']}####[['{row['A']}','{row['C']}','{row['S']}','{row['O']}']]"
        f.write(line + '\n')
