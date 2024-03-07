import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tqdm import tqdm

image_ids = pd.read_csv('full_dataset/images.txt', sep=' ', header=None)
image_ids.columns=['Im_ID', 'Im_Name']

label_data = pd.read_csv('full_dataset/image_class_labels.txt', sep=' ', header=None)
label_data.columns = ['X', 'y']
X = np.array(label_data['X'].tolist())
y = np.array(label_data['y'].tolist())

print(len(y)) # 22238
print(list(y).count(0)) # 21051
print(list(y).count(1)) # 1187

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.1)
print(len(X_train)) # 20014
print(len(X_test)) # 2224

print(list(y_train).count(0)) # 18946
print(list(y_train).count(1)) # 1068
print(list(y_test).count(0)) # 2105
print(list(y_test).count(1)) # 119

with open('full_dataset/train_test_split.txt', 'w') as f:
    for i in tqdm(image_ids.index):
        image_id = image_ids['Im_ID'].iloc[i]
        is_training = 0
        if image_id in X_train:
            is_training = 1
        f.write('{} {}\n'.format(image_id, is_training))