def load_data(file):
    with open(file, 'r') as f:
        data = f.readlines()
    
    return data