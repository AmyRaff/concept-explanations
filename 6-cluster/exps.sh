#!/bin/sh
#SBATCH -N 1
#SBATCH -n 1
#SBATCH --partition=PGR-Standard
#SBATCH --gres=gpu:1
#SBATCH --mem=90000
#SBATCH -o outfile_again
#SBATCH -t 120:00:00

export CUDA_HOME=/opt/cuda-10.0.130/
export CUDNN_HOME=/opt/cuDNN-7.6.5/
export STUDENT_ID=$(whoami)

export LD_LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH
export LIBRARY_PATH=${CUDNN_HOME}/lib64:$LIBRARY_PATH
export CPATH=${CUDNN_HOME}/include:$CPATH

export PATH=${CUDA_HOME}/bin:${PATH}
export PYTHON_PATH=$PATH

export TMPDIR=/disk/scratch/${STUDENT_ID}
export TMP=/disk/scratch/${STUDENT_ID}

source /home/${STUDENT_ID}/miniconda3/bin/activate lung


#python generate_new_data.py ExtractConcepts --model_path models/ConceptModelSmallLR/outputs/best_model_1.pth --data_dir processed_small_6 --out_dir ConceptModel1__PredConcepts

#python posfix_exps.py lung Concept_XtoC --seed 1 -ckpt 1 -log_dir models/Lung_Model_Posfix/outputs/ -e 1000 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir a_posfix/baby_posfix -normalize_loss -b 10 -weight_decay 0.00004 -lr 0.01 -scheduler_step 50 -bottleneck
#python lung_exps.py lung Concept_XtoC --seed 2 -ckpt 1 -log_dir models/Lung_Model_Seed2/outputs/ -e 50 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -normalize_loss -b 64 -weight_decay 0.00004 -lr 0.005 -scheduler_step 50 -bottleneck
#python lung_exps.py lung Concept_XtoC --seed 3 -ckpt 1 -log_dir models/Lung_Model_Seed3/outputs/ -e 50 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -normalize_loss -b 64 -weight_decay 0.00004 -lr 0.005 -scheduler_step 50 -bottleneck

# NOTE: did not run
#python LUNG/generate_new_data.py ExtractConcepts --model_path Lung_Model_Seed1/outputs/best_model_1.pth --data_dir LUNG/mimic_processed --out_dir Lung_ConceptModel1_PredConcepts
#python LUNG/generate_new_data.py ExtractConcepts --model_path Lung_Model_Seed2/outputs/best_model_2.pth --data_dir LUNG/mimic_processed --out_dir Lung_ConceptModel2_PredConcepts
#python LUNG/generate_new_data.py ExtractConcepts --model_path Lung_Model_Seed3/outputs/best_model_3.pth --data_dir LUNG/mimic_processed --out_dir Lung_ConceptModel3_PredConcepts

### Independent Model
python exps.py lung Concept_XtoC --seed 1 -ckpt 1 -log_dir ConceptModelAgain/outputs/ -e 1000 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir ../processed/original_6 -normalize_loss -b 16 -weight_decay 0.00004 -lr 0.0001 -scheduler_step 1000 -bottleneck

#python exps.py lung Independent_CtoY --seed 1 -log_dir IndependentSmall/outputs/ -e 500 -optimizer sgd -use_attr -data_dir processed_small_6 -no_img -b 32 -weight_decay 0.00005 -lr 0.001 -scheduler_step 100
#python lung_exps.py lung Independent_CtoY --seed 2 -log_dir models/Lung_IndependentModel_WithVal_Seed2/outputs/ -e 25 -optimizer sgd -use_attr -data_dir LUNG/mimic_processed -no_img -b 64 -weight_decay 0.00005 -lr 0.001 -scheduler_step 25
#python lung_exps.py lung Independent_CtoY --seed 3 -log_dir models/Lung_IndependentModel_WithVal_Seed3/outputs/ -e 25 -optimizer sgd -use_attr -data_dir LUNG/mimic_processed -no_img -b 64 -weight_decay 0.00005 -lr 0.001 -scheduler_step 25

#python LUNG/inference.py -model_dirs models/Lung_Model_Seed1/outputs/best_model_1.pth -model_dirs2 models/Lung_IndependentModel_WithVal_Seed1/outputs/best_model_1.pth -eval_data test -use_attr -data_dir LUNG/mimic_processed -bottleneck -use_sigmoid -log_dir inference/Lung_IndependentModel_WithValSigmoid/outputs

### Sequentialpython LUNG/inference.py -model_dirs Lung_Model_Seed1/outputs/best_model_1.pth Lung_Model_Seed2/outputs/best_model_2.pth Lung_Model_Seed3/outputs/best_model_3.pth -model_dirs2 Lung_SequentialModel_WithVal_Seed1/outputs/best_model_1.pth Lung_SequentialModel_WithVal_Seed2/outputs/best_model_2.pth Lung_SequentialModel_WithVal_Seed3/outputs/best_model_3.pth -eval_data test -use_attr -n_attributes 38 -data_dir LUNG/mimic_processed -bottleneck -feature_group_results -log_dir Lung_SequentialModel_WithVal/outputs

### Joint Model
#python exps.py lung Joint --seed 1 -ckpt 1 -log_dir Joint/outputs/ -e 1000 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir processed_small_6 -attr_loss_weight 0.01 -normalize_loss -b 16 -weight_decay 0.0004 -lr 0.001 -scheduler_step 25 -end2end
# NOTE: attrlossweight was 0.01
#python lung_exps.py lung Joint --seed 2 -ckpt 1 -log_dir models/Joint0.01Model_Seed2/outputs/ -e 25 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -attr_loss_weight 0.01 -normalize_loss -b 64 -weight_decay 0.0004 -lr 0.001 -scheduler_step 25 -end2end
#python lung_exps.py lung Joint --seed 3 -ckpt 1 -log_dir models/Joint0.01Model_Seed3/outputs/ -e 25 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -attr_loss_weight 0.01 -normalize_loss -b 64 -weight_decay 0.0004 -lr 0.001 -scheduler_step 25 -end2end

### Joint Sig Model
#python lung_exps.py lung Joint --seed 1 -ckpt 1 -log_dir models/Joint0.01SigmoidModel_Seed1/outputs/ -e 50 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -attr_loss_weight 0.01 -normalize_loss -b 64 -weight_decay 0.0004 -lr 0.001 -scheduler_step 1000 -end2end -use_sigmoid

### Standard Model
#python lung_exps.py lung Joint --seed 1 -ckpt 1 -log_dir models/StandardModel_Seed1/outputs/ -e 50 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -attr_loss_weight 0 -normalize_loss -b 64 -weight_decay 0.00004 -lr 0.01 -scheduler_step 20 -end2end

### Standard No Bottleneck Model
#python exps.py lung Standard --seed 1 -ckpt 1 -log_dir Standard/outputs/ -e 1000 -optimizer sgd -pretrained -use_aux -data_dir processed_small_6 -b 16 -weight_decay 0.0004 -lr 0.001 -scheduler_step 1000

### Multitask Model
#python lung_exps.py lung Multitask --seed 1 -ckpt 1 -log_dir models/MultitaskModel_Seed1/outputs/ -e 50 -optimizer sgd -pretrained -use_aux -use_attr -weighted_loss multiple -data_dir LUNG/mimic_processed -attr_loss_weight 0.01 -normalize_loss -b 64 -weight_decay 0.00004 -lr 0.01 -scheduler_step 20

### Generate Data
#python LUNG/generate_new_data.py ExtractConcepts --model_path models/Lung_Model_Seed1/outputs/best_model_1.pth --data_dir LUNG/mimic_processed --out_dir models/ConceptModel1__PredConcepts

### Sequential Model
#python lung_exps.py lung Sequential_CtoY --seed 1 -log_dir models/SequentialModel_WithVal__Seed1/outputs/ -e 50 -optimizer sgd -pretrained -use_aux -use_attr -data_dir models/ConceptModel1__PredConcepts -no_img -b 64 -weight_decay 0.00004 -lr 0.001 -scheduler_step 1000

#
