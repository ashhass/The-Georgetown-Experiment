import ast
from load_data import load_data
from program import Rules

data = load_data('data.csv')
glossary = {}
for i in range(1, len(data)):
    word, equivalent, codes = map(str.strip, data[i].split('|'))
    glossary[word] = [equivalent.strip('[]').split(','), ast.literal_eval(codes)]

sentences = load_data('test.csv')
for idx, sentence in enumerate(sentences):
    _, rus_sentence, _ = sentence.split(',')
    rules = Rules(rus_sentence, glossary)
    
    output = list(filter(lambda x: x != '', rules.translate()))
    print(f'{idx, rus_sentence} -> {" ".join(output)}')