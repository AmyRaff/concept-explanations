# Concept-Based Explanations for Lung Cancer Detection in Chest X-rays

This repo does not contain the data used in experiments. Data can be downloaded from https://physionet.org/content/mimic-cxr-jpg/2.0.0/ after signing Physionet's data use agreement.

This repo contains the original source code for building and refining the original ClinicXAI / XpertXAI pipeline. Code is for the binary classification task of lung cancer detection (ClinicXAI) but can easily be expanded to the multiclass domain (XpertXAI) by editing data text files and changing the N_ATTRIBUTES and N_CLASSES values in the Python scripts.

We present our original work as proof of concept, using report phrases as direct clinical concepts (28 concepts directory), as well as the refinement step of clustering these phrases into consolidated clinical concepts under radiologist guidance (6 concepts directory), which is the approach presented in both our ClinicXAI and XpertXAI publications.

Phrases associated with clinical concepts for six target pathologies (Lung Cancer, Healthy, Pneumonia, Pneumothorax, Pleural Effusion, Cardiomegaly) are provided in **concepts_to_phrases.png**.

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
