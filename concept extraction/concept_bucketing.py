
### buckets 

# Nodule = nodular_density, nodular_densities, nodular_opacity, 
# nodular_opacities, nodular_opacification, nodule
## Nodule = 2 - 7

# Mass = mass, lump, cavitary_lesion, carcinoma, neoplasm, tumor, rounded_opacity, 
# lung_cancer, triangular_opacity, apical_opacity 
## Mass = 1, 8 - 15, 19

# Irregular Hilum = hilar_adenopathy, hilus_enlarged, hilus_bulbous, hilus_fullness, 
# hilar_lymphadenopathy, hilar_mass, hilar_opacity 
## Hilum = 24-27, 20, 16, 17

# Irregular Lung Parenchyma = Carcinomatosis, pulmonary_metastasis, metastatic_disease 
## Lung Parenchyma = 23, 22, 18
# The lung parenchyma comprises a large number of thin-walled alveoli, forming an enormous 
# surface area, which serves to maintain proper gas exchange. 

# Irregular Mediastinum = lymphadenopathy 
## Mediastinum = 21
# space in your chest that holds your heart and other important structures. It's the middle 
# compartment within your thoracic cavity, nestled between your lungs.

## Healthy concepts
# unremarkable = normal / unremarkable / lungs_clear / no_evidence / normal_hilar_contours
# unremarkab;e = 28 - 31, 35
# no_change = no_new_nodule, no_new_mass, no_interval_change
# no_change = 32-34


import pandas as pd
import numpy as np
from tqdm import tqdm

orig = pd.read_csv('full_dataset_5/orig_attr_labels.txt', sep=' ', header=None)
orig.columns=['Im_ID', 'Attr_ID', 'Present']
im_ids = orig['Im_ID'].unique()
print(len(im_ids))

# bucketed concept IDs

c1 = [1, 8, 9, 10, 11, 12, 13, 14, 15, 19]
c2 = [2, 3, 4, 5, 6, 7]
c3 = [16, 17, 20, 24, 25, 26, 27]
c4 = [18, 22, 23]
c5 = [21]
c6 = [28, 29, 30, 31, 35]
c7 = [32, 33, 34]

totals = [0] * 7
def get_new_attrs(id):
    attrs = [0] * 7
    present = orig[(orig['Im_ID'] == id) & (orig['Present'] == 1)]['Attr_ID'].tolist()
    for a in present:
        if a in c1: attrs[0] = 1; totals[0] +=1; break
        elif a in c2: attrs[1] = 1; totals[1] +=1;break
        elif a in c3: attrs[2] = 1; totals[2] +=1;break
        elif a in c4: attrs[3] = 1; totals[3] +=1;break
        elif a in c5: attrs[4] = 1; totals[4] +=1;break
        elif a in c6: attrs[5] = 1; totals[5] +=1;break
        elif a in c7: attrs[6] = 1; totals[6] +=1;break
    return attrs

for id in tqdm(im_ids):
    get_new_attrs(id)
print(totals)

# with open('full_dataset_5/image_attribute_labels.txt', 'w') as f:
#     for id in tqdm(im_ids):
#         occurences = get_new_attrs(id)
#         if occurences != None:
#             for o in range(len(occurences)):
#                 f.write('{} {} {}\n'.format(id, o + 1, occurences[o]))