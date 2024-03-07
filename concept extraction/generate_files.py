import os
import pandas as pd 
import numpy as np
from tqdm import tqdm
import shutil

label_data = pd.read_csv('mimic-cxr-2.0.0-chexpert.csv')
metadata = pd.read_csv('mimic-cxr-2.0.0-metadata.csv')

# # NOTE: not all data labelled, use images in dataset that are also in chexpert file

# class_info = pd.DataFrame(columns=['filename', 'label'])

# print('Generating class info...')
# for row in tqdm(label_data.index):
#     lesion = label_data['Lung Lesion'].iloc[row]
#     healthy = label_data['No Finding'].iloc[row]
#     study = label_data['study_id'].iloc[row]
#     subject = label_data['subject_id'].iloc[row]
#     # NOTE: Only want cancerous and healthy scans in dataset.
#     if healthy == 1.0:
#         label = 0
#     elif lesion == 1.0:
#         label = 1
#     else:
#         label = None
#     if label != None:
#         filename = metadata[(metadata['study_id'] == study) & (metadata['subject_id'] == subject)]['dicom_id'].values[0]
#         new_row = {'filename': filename, 'label': label}
#         class_info.loc[len(class_info)] = new_row

# print(len(class_info))
# class_info.to_csv('label_info.csv', header=None, index=False)
# print('Done.')
# exit()

## GENERATE IMAGES.TXT AND IMAGE DATASET ##########################################

class_info = pd.read_csv('label_info.csv')
# print(len(class_info))
# # NOTE: Only want PA images
# image_path = 'PA/'
# dataset = os.listdir(image_path)
# count = 0
# print('Generating images.txt and image directory....')
# with open('full_dataset/images.txt', 'w') as f:
#     for i in tqdm(range(len(dataset))):
#         filename = dataset[i].split('.')[0]
#         # NOTE: Only want PA images that are cancerous or healthy
#         if filename in class_info['filename'].unique():
#             f.write('{} {}.jpg\n'.format(i + 1, filename))
#             shutil.copy('PA/' + filename + '.jpg', 'full_dataset/imgs/' + filename + '.jpg')
#             count +=1
# print('Done.')
# print(count)


## GENERATE IMAGE_CLASS_LABELS.TXT ############################################

# image_ids = pd.read_csv('full_dataset/images.txt', sep=' ', header=None)
# image_ids.columns=['ID', 'Name']

# print('Generating class file...')
# with open('full_dataset/image_class_labels.txt', 'w') as f:
#     for row in tqdm(image_ids.index):
#         image_id = image_ids['ID'].iloc[row]
#         filename = image_ids['Name'].iloc[row][:-4] # remove .jpg
#         #if filename in class_info['filename'].unique():
#         label = class_info[class_info['filename'] == filename]['label'].values[0]
#         f.write('{} {}\n'.format(image_id, label))
# print('Done.')
    
# print(class_info)


# NOTE: metadata file unreliable for LATERAL or PA view information !!
