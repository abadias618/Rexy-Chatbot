"""
Rexy
@author: abd
"""
from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch
class BertTransferLearning():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("twmkn9/bert-base-uncased-squad2")
        self.model = AutoModelForQuestionAnswering.from_pretrained("twmkn9/bert-base-uncased-squad2")
        
        
    def predict_answer(self, question, text):
        input_text = "[CLS] " + question + " [SEP] " + text + " [SEP]"
        input_ids = self.tokenizer.encode(input_text, add_special_tokens=False)
        token_type_ids = [0 if i <= input_ids.index(102) else 1
            for i in range(len(input_ids))]
        start_scores, end_scores = self.model(torch.tensor([input_ids]), token_type_ids=torch.tensor([token_type_ids]), return_dict=False)
        all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)
        answer = all_tokens[answer_start]
        for i in range(answer_start + 1, answer_end + 1):
            # If it's a subword token, then recombine it with the previous token.
            if all_tokens[i][0:2] == '##':
                answer += all_tokens[i][2:]
            # Otherwise, add a space then the token.
            else:
                answer += ' ' + all_tokens[i]
        return answer
