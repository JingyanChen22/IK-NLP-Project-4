import os

parent_path = 'Experiments/cross_validation/orth'
for folder in sorted(os.listdir(parent_path)):
    deeper_path = parent_path+'/'+folder
    for validation in sorted(os.listdir(deeper_path)):
        final_path = f'{deeper_path}/{validation}'
        yaml_dir = f'{final_path}'+f'/{folder}.yaml'
        src_train = f'{final_path}/src_train.txt'
        src_valid = f'{final_path}/src_valid.txt'
        tgt_train = f'{final_path}/tgt_train.txt'
        tgt_valid = f'{final_path}/tgt_valid.txt'

        with open (src_train, 'r') as train:
            sample_size = len(train.readlines())

        with open(yaml_dir, 'w') as yaml:
            yaml.write(f'''save_data: {final_path[12:]}/example\n
## Where the vocab(s) will be written
src_vocab: {final_path[12:]}/example.vocab.src
tgt_vocab: {final_path[12:]}/example.vocab.tgt
# Prevent overwriting existing files in the folder
overwrite: False

# Corpus opts:
data:
    corpus_1:
        path_src: {src_train[12:]}
        path_tgt: {tgt_train[12:]}
    valid:
        path_src: {src_valid[12:]}
        path_tgt: {tgt_valid[12:]}

# Vocabulary files that were just created
src_vocab: {final_path[12:]}/example.vocab.src
tgt_vocab: {final_path[12:]}/example.vocab.tgt


seed: 123
encoder_type: brnn
dropout: 0.3
decoder_type: rnn
rnn_type: LSTM
batch_size: 20
learning_rate: 1.0
train_steps: 24440
enc_layers: 2
feat_merge: concat
dec_layers: 2
enc_rnn_size: 100
dec_rnn_size: 100
feat_vec_size: 300
beam_size: 12
optim: adadelta
verbose: True
learning_rate_decay: 1.0
tensorboard: True
tensorboard_log_dir: logs
report_every: 244
log_file: '{final_path[12:]}/log_file_orth.txt'
log_file_level: 20

# Where to save the checkpoints
save_model: {final_path[12:]}/model
save_checkpoint_steps: {str(int(sample_size/20*10))}
train_steps: {str(int(sample_size/20*100))}
''')
