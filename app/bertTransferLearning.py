"""
Rexy
@author: abd
"""
from transformers import BertTokenizer, BertForQuestionAnswering
import torch
class BertTransferLearning():
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
        
        
    def predict_answer(self, question, text):
        input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=False)
        token_type_ids = [0 if i <= input_ids.index(102) else 1
            for i in range(len(input_ids))]
        start_scores, end_scores = self.model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]), return_dict=False)
        all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        return(' '.join(all_tokens[torch.argmax(start_scores) : torch.argmax(end_scores)+1]))
