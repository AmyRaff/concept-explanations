# Concept-Based Explanations for Lung Cancer Detection in Chest X-rays

This repo does not contain the data used in experiments. Data can be downloaded from https://physionet.org/content/mimic-cxr-jpg/2.0.0/ after signing Physionet's data use agreement.

Scripts for the original 28-concept experiment can be found in the 28-concept directory. Scripts for the fully clustered experiment can be found in the 6-cluster directory.

Data must be in the following format:

- data
    - attributes.txt (attribute id, attribute name)
    - classes.txt (class id, class name)
    - image_attribute_labels.txt (img id, attribute id, is_present)
    - image_class_labels.txt (img id, class id)
    - images.txt (img id, filename)
    - train_test_split.txt (img id, is_training)
    - images
        - (JPG IMAGE FILES - NOT INCLUDED)

Concept extraction scripts can be found in the concept extraction directory.