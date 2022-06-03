Counter Narrative Generation
====================


## Training
We finetune GPT-2 on CONAN data paired with KN, use the implementation [run_language_modeling.py](https://github.com/huggingface/transformers/blob/main/examples/legacy/run_language_modeling.py) from Transformers library.
 

```
python run_language_modeling.py \
  --output_dir models/Qhscn_3E_run1 \
  --model_type gpt2 \
  --model_name_or_path gpt2_model \
  --do_train \
  --train_data_file data/hscnkp_train.txt \
  --do_eval \
  --eval_data_file data/hscnkp_valid.txt \
  --line_by_line \
  --learning_rate 5e-5 \
  --num_train_epochs 3 \
  --save_steps 1000 \
  --per_gpu_train_batch_size 2 \
  --per_gpu_eval_batch_size 2
```

## Inferencing
For inferencing, please run ```run_generation_test_file.py``` over your test set. This script is slightly modified based on the implementation [run_generation.py](https://github.com/huggingface/transformers/tree/v4.3.0.rc1/examples/text-generation).

```
python run_generation_test_file.py \
  --model_type gpt2 \
  --model_name_or_path models/Qhscn_3E_run1 \
  --test_file data/hscnkp_test.txt \
  --out_file_path generation/Qhscn_3E_run1.txt \
  --length 50 \
  --p 0.9 \
  --num_return_sequences 1  
```
