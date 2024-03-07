import os
import pandas as pd
from tqdm import tqdm

data = pd.read_csv('mimic-cxr-2.0.0-chexpert.csv') # from dataset

filtered = pd.DataFrame(columns = ['subject_id', 'study_id', 'label'])

num_cancerous = 0
num_healthy = 0

for row in tqdm(range(len(data))):
    lesion = data.iloc[row]['Lung Lesion']
    healthy = data.iloc[row]['No Finding']
    
    if lesion == 1.0:
        new_row = {'subject_id': int(data.iloc[row]['subject_id']), 'study_id': int(data.iloc[row]['study_id']), 'label': 'cancer'}
        filtered.loc[len(filtered)] = new_row
        num_cancerous +=1
    elif healthy == 1.0:
        new_row = {'subject_id': int(data.iloc[row]['subject_id']), 'study_id': int(data.iloc[row]['study_id']), 'label': 'healthy'}
        filtered.loc[len(filtered)] = new_row
        num_healthy +=1

print(num_healthy)
print(num_cancerous)
print(len(filtered))

filtered.to_csv('filtered.csv', index=False)
data = pd.read_csv('filtered.csv')
counts = data['label'].value_counts()
print(counts)
