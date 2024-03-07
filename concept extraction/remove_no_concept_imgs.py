import pandas as pd
from tqdm import tqdm
import os

# attr_data =  pd.read_csv('full_dataset/image_attribute_labels.txt', sep=' ', header=None)
# attr_data.columns=['Im_ID', 'Attr', 'Presence']
# relevant_ids = attr_data['Im_ID'].unique()

# print(len(relevant_ids))

# remove from: images directory, images.txt, image_class_labels.txt

# images.txt
# image_ids = pd.read_csv('full_dataset/images.txt', sep=' ', header=None)
# image_ids.columns=['Im_ID', 'Im_Name']

# print(len(image_ids))
# a = image_ids.drop(image_ids[~image_ids.Im_ID.isin(relevant_ids)].index)
# print(len(a))

# a.to_csv('images.txt', header=None, index=False)

# image_class_labels.txt
class_ids = pd.read_csv('full_dataset/image_class_labels.txt', sep=' ', header=None)
print(class_ids)
class_ids.columns=['Im_ID', 'Label']

# print(len(class_ids))
# b = class_ids.drop(class_ids[~class_ids.Im_ID.isin(relevant_ids)].index)
# print(len(b))

#b.to_csv('image_class_labels.txt', header=None, index=False)


# image directory

# all_imgs = os.listdir('full_dataset/imgs/')
# for img in all_imgs:
#     id = image_ids[image_ids['Im_Name'] == img]['Im_ID'].values[0]
#     if id not in relevant_ids:
#         os.remove('full_dataset/imgs/' + img)
