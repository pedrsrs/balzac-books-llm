import torch
import torch.nn as nn
from torch.nn import functional as F

BATCH_SIZE = 32
BLOCK_SIZE = 8
MAX_ITERS = 3000
EVAL_INTERVAL = 300
LEARNING_RATE = 1e-2
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
EVAl_ITERS = 200

with open('../scraper/balzac_full_books.txt', 'r', encoding='utf-8') as f:
        text = f.read()

chars = sorted(list(set(text)))
vocab_size = len(chars)

stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for ch,i in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join([itos[i] for i in l])

data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9*len(data))
train_data = data[:n]
val_data = data[:n]

print(''.join(chars))
print(vocab_size)

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.radint(len(data) - BLOCK_SIZE, (BATCH_SIZE))
    x = torch.stack([data[i:i+BLOCK_SIZE] for i in ix])
    y = torch.stack([data[i+1:i+BLOCK_SIZE] for i in ix])
    x, y = x.to(DEVICE), y.to(DEVICE)
    return x, y 
