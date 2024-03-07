import os
import cv2
import pandas as pd 
import numpy as np
import re
import string
from tqdm import tqdm

label_data = pd.read_csv('mimic-cxr-2.0.0-chexpert.csv')
metadata = pd.read_csv('mimic-cxr-2.0.0-metadata.csv')

def get_out_pathology(filepath):
    info = open(filepath, "r")
    info = info.read()
    if 'FINAL REPORT' in info:
        info = info[info.index('FINAL REPORT'):]
    if 'FINDINGS:' in info:
        info = info[info.index('FINDINGS:'):]
    info = info.split('.')

    filtered = [a for a in info if a != " \n"]  # remove empty lines
    
    out = ""
    for line in filtered:
        line = re.sub(r"\b[A-Z]+\b", " ", line)  # remove title phrases (all uppercase)
        line = re.sub(r"_|:", " ", line)
        line = re.sub("\n", " ", line)
        line = line.replace("\t", " ")
        # line = line.strip()
        line = re.sub(r"\s+", " ", line)  # remove multiple spaces and tabs
        while line.startswith(" "):
            line = line[1:]
        line = line + '.'
        out = out + line
    
    out = out.split(".")
    out = [a for a in out if len(a) > 2]
    out = [a[1:] if a.startswith(" ") else a for a in out]
    out = [a.lower() for a in out]
    out = [a.translate(str.maketrans("", "", string.punctuation)) for a in out]
    out = [a for a in out if len(a.split()) > 1]
    out = [a for a in out if re.search(r'[a-zA-Z]+', a)]

    unwanted_words = [
        "dr",
        "am",
        "pm",
        "p",
        "minutes",
        "telephone",
        "telehpone", 'phone',
        'thank', 'thanks',
        'comment',
        "time",
        "views",
        "radiograph",
        "xray",
        "normal",
        "unremarkable",
        "year", 'yearold',
        "dashboard",
        "female",
        "male",
        "woman",
        "man",
        "comparison",
        'hospital',
        "devices",
        'scan',
        "tube",
        "clips",
        'recommend',
        "available",
        "nipple",
        "evaluate"
    ]
    out = [s for s in out if not any(w in unwanted_words for w in s.split())]
    relevant = [a for a in out if a.startswith("no relevant change")]
    out = [a for a in out if not a.startswith("no ")]
    for sent in relevant:
        out.append(sent)
    out = [a for a in out if not a.startswith("there is no ")]
    out = [a for a in out if not a.startswith("there are no ")]
    return out

def get_out_healthy(filepath):
    info = open(filepath, "r")
    info = info.read()
    if 'FINAL REPORT:' in info:
        info = info[info.index('FINAL REPORT:'):]
    if 'FINDINGS:' in info:
        info = info[info.index('FINDINGS:'):]
    info = info.split('.')

    filtered = [a for a in info if a != " \n"]  # remove empty lines

    out = ""
    for line in filtered:
        line = re.sub(r"\b[A-Z]+\b", " ", line)  # remove title phrases (all uppercase)
        line = re.sub(r"_|:", " ", line)
        line = re.sub("\n", " ", line)
        line = line.replace("\t", " ")
        # line = line.strip()
        line = re.sub(r"\s+", " ", line)  # remove multiple spaces and tabs
        while line.startswith(" "):
            line = line[1:]
        line = line + '.'
        out = out + line
    out = out.split(".")
    out = [a for a in out if len(a) > 2]
    out = [a[1:] if a.startswith(" ") else a for a in out]
    out = [a.lower() for a in out]
    out = [a.translate(str.maketrans("", "", string.punctuation)) for a in out]
    out = [a for a in out if len(a.split()) > 1]
    out = [a for a in out if re.search(r'[a-zA-Z]+', a)]
    return out

## GENERATE IMAGE_ATTRIBUTE_LABELS.TXT ##########################################

image_ids = pd.read_csv('full_dataset/images.txt', sep=' ', header=None)
image_ids.columns=['Im_ID', 'Im_Name']

attribute_ids = pd.read_csv('full_dataset/attributes.txt', sep=' ', header=None)
attribute_ids.columns=['Attr_ID', 'Attr_Name']
attributes = attribute_ids['Attr_Name'].unique()

class_info = pd.read_csv('full_dataset/image_class_labels.txt', sep=' ', header=None)
class_info.columns=['Im_ID', 'Label']

def get_attribute_occurences(filename):

    subject = metadata[metadata['dicom_id'] == filename[:-4]]['subject_id'].values[0]
    study = metadata[metadata['dicom_id'] == filename[:-4]]['study_id'].values[0]
    path_to_report = 'files/p{}/p{}/s{}.txt'.format(str(subject)[:2], subject, study)
    
    occurences = [0] * len(attributes)
    
    id = image_ids[image_ids['Im_Name'] == filename]['Im_ID'].values[0]
    label = class_info[class_info['Im_ID'] == id]['Label'].values[0]
    if label == 0:
        phrases = get_out_healthy(path_to_report)
    elif label == 1:
        phrases = get_out_pathology(path_to_report)
    else:
        print(label)
        exit()
    
    for phrase in phrases:
        if 'nipple shadow' in phrase:
            phrases.remove(phrase)

    # for each attribute 1 - 24, 28 - 29, 31-33, 36, 38 check whether the report contains the words as they appear
    full_phrase_indices = [a for a in range(1, 25)]
    for num in [28, 29, 31, 32, 33, 34, 35]:
        full_phrase_indices.append(num)
        
    for i in full_phrase_indices:
        attribute = attributes[i - 1].replace('_', ' ')
        for phrase in phrases:
            if attribute in phrase:
                if occurences[i - 1] == 0:
                    #print('{} found!'.format(attribute))
                    occurences[i - 1] = 1
                break
    

    # for each attribute 26 - 28, 32, 34 - 35, 37 check whether a sentence contains the words in any location
    word_indices = [25, 26, 27, 30]
    for i in word_indices:
        words = attributes[i - 1].split('_')
        for phrase in phrases:
            num_present = 0
            if 'hilus' in phrase:
                phrase += 'hilum'
                phrase += 'hilar'
            if 'hilum' in phrase:
                phrase += 'hilus'
                phrase += 'hilar'
            if 'hilar' in phrase:
                phrase += 'hilus'
                phrase += 'hilum'
            for word in words:
                if word in phrase:
                    num_present +=1
            if num_present == len(words):
                #print('{} found!'.format(words))
                occurences[i - 1] = 1
    
    #### filtering and formatting
    # if no new mass remove mass
    if occurences[32] == 1: occurences[0] = 0
    # if no new nodule remove nodule
    if occurences[31] == 1: occurences[6] = 0
    # presence of any positives removes negatives
    for i in range(28):
        if occurences[i-1] == 1:
            for i in range(28, len(occurences)):
                occurences[i-1] = 0
    
    # only want images with some concepts
    
    contains_concepts = False
    for i in range(len(occurences)):
        if occurences[i] == 1:
            contains_concepts = True
    
    if contains_concepts:
        return occurences, path_to_report
    else:
        return None, None

## debug code 
# out = get_attribute_occurences('00695866-dafbd1d0-a7527adb-3437bca5-8d68acd0')[0]
# report = get_attribute_occurences('00695866-dafbd1d0-a7527adb-3437bca5-8d68acd0')[1]
# print(out)
# print(report)

with open('full_dataset/image_attribute_labels.txt', 'w') as f:
    for i in tqdm(image_ids.index):
        image_id = image_ids['Im_ID'].iloc[i]
        filename = image_ids['Im_Name'].iloc[i]
        occurences = get_attribute_occurences(filename)[0]
        if occurences != None:
            for o in range(len(occurences)):
                f.write('{} {} {}\n'.format(image_id, o + 1, occurences[o]))
    
# TODO: if not in this file delete from everywhere else