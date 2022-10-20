import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import csv
from tqdm import tqdm

def paraphrase(query):
    text = "paraphrase: " + str(query) + " </s>"
    encoding = tokenizer.encode_plus(text,pad_to_max_length=True, return_tensors="pt")
    input_ids, attention_masks = encoding["input_ids"], encoding["attention_mask"]
    outputs = model.generate(
    		input_ids=input_ids, attention_mask=attention_masks,
    		max_length=256,
    		do_sample=True,
    		top_k=120,
    		top_p=0.95,
    		early_stopping=True,
    		num_return_sequences=3
    )

    tmp_out = []
    for output in outputs:
        line = tokenizer.decode(output, skip_special_tokens=True,clean_up_tokenization_spaces=True)
        tmp_out.append(line)
    return tmp_out



## change input and output file names

input_file = './squall/squall_split_0.json'
output_file = 'squall_split_0_paraphrased.csv'

og_sentences = []
f = open(input_file,'r')

data = json.load(f)
for key,value in data.items():
    og_sentences = og_sentences + value[0]

print(len(og_sentences))

tokenizer = AutoTokenizer.from_pretrained("Vamsi/T5_Paraphrase_Paws")  
model = AutoModelForSeq2SeqLM.from_pretrained("Vamsi/T5_Paraphrase_Paws")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
print(device)
model = model.to(device)

tq = tqdm(og_sentences)
print(len(tq))

out_csv = open(output_file,'w')
writer = csv.writer(out_csv)
for og_sent, tq_sent in zip(og_sentences, tq):
  row = [og_sent]
  for ps in paraphrase(tq_sent): row.append(ps)
  writer.writerow(row)
