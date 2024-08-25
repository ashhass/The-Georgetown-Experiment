import ast
from load_data import load_data
from program import Rules

data = load_data('data.csv')
glossary = {}
for i in range(1, len(data)):
    word, equivalent, codes = map(str.strip, data[i].split('|'))
    glossary[word] = [equivalent.strip('[]').split(','), ast.literal_eval(codes)]

sentences = load_data('test.csv')
def main(idx):
    sentence = sentences[idx]
    _, rus_sentence, _ = sentence.split(',')
    rules = Rules(rus_sentence, glossary)
    
    output = list(filter(lambda x: x != '', rules.translate()))
    return rus_sentence, output
    
choice = input("Choose a number betwen 1 to 48: ")
rus_sentence, eng_sentence = main(int(choice))
print(f"You chose this Russian sentence:{rus_sentence}")
print(f'English translation: {" ".join(eng_sentence)}')