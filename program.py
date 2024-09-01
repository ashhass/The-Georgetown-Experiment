class Rules:
    '''
        Translates Russian sentence to English

        Args:
            sentence (str): the sentence to be translated
            glossary (dict[str, tuple[list[str], list[tuple[int, int, int]]]]): dictionary of russian words as keys and corresponding english words and their codes as values
        
        Returns:
            str: the translated sentence
    
    '''
    def __init__(self, sentence: str, glossary: dict[str, tuple[list[str], list[tuple[int, int, int]]]]) -> list:
        self.glossary = glossary
        self.output = []
        self.input = self._process_input(sentence)

    def _process_input(self, sentence: str) -> list[str]:
        """Processes the input sentence into tokens."""
        inputs = []
        for word in sentence.split():
            if word in self.glossary:
                inputs.append(word)
                continue

            for idx in range(len(word)):
                prefix = word[:idx] + '-'
                suffix = '-' + word[idx:]
                if prefix in self.glossary and suffix in self.glossary:
                    inputs.extend([prefix, suffix])

        return inputs

    def translate(self):
        """Translates the input sentence based on the glossary and rules."""
        for idx in range(len(self.input)):
            word, codes = self.find_word(idx)
            pid, _, _ = codes if len(codes) == 3 else codes[0]

            self.apply_rules(pid, idx)

        return self.output

    def find_word(self, idx):
        word = self.input[idx]
        return self.glossary.get(word)
        
    def apply_rules(self, pid, idx):
        switch = {
            110: self.rule1,
            121: self.rule2,
            131: self.rule3,
            141: self.rule4,
            151: self.rule5,
            '***': self.rule6
        }
        switch[pid](idx)

    def rule1(self, idx):
        if idx - 1 < 0: return self.rule6(idx)
        
        _, pre_codes = self.find_word(idx - 1)
        eng_word, _ = self.find_word(idx)

        if (pre_codes[2] if len(pre_codes) > 2 else pre_codes[0][2]) == 21:
            self.output.append(eng_word[0])
            self.output[idx], self.output[idx - 1] = self.output[idx - 1], self.output[idx]
        else:
            self.output.append(eng_word[0])

    def rule2(self, idx):
        if idx >= len(self.input): return self.rule6(idx)
        
        eng_word, codes = self.find_word(idx)
        for post_idx in range(idx + 1, len(self.input)):
            _, post_codes = self.find_word(post_idx)
            code = (post_codes[1] if len(post_codes) > 2 else post_codes[0][1])
            if code in {221, 222}:
                self.output.append(eng_word[code - 221])
                break
      
    def rule3(self, idx):
        if idx <= 0: return self.rule6(idx)

        eng_word, _ = self.find_word(idx)
        for i in range(1, 4):
            if idx - i < 0: break
            _, pre_code = self.find_word(idx - i)
            code = (pre_code[2] if len(pre_code) > 2 else pre_code[0][2])
            if code == 23:
                self.output.append(eng_word[1])
                return

        self.output.append(eng_word[0])
        self.output[idx], self.output[idx - 1] = self.output[idx - 1], self.output[idx]

    def rule4(self, idx):
        if idx <= 0: return self.rule6(idx)

        eng_word, _ = self.find_word(idx)
        for pre_idx in range(idx - 1, -1, -1):
            _, pre_codes = self.find_word(pre_idx)
            code = (pre_codes[1] if len(pre_codes) > 2 else pre_codes[0][1])
            if code in {241, 242}:
                self.output.append(eng_word[code - 241])
                break

    def rule5(self, idx):
        if idx + 1 > len(self.input): return self.rule6(idx)

        _, post_code = self.find_word(idx + 1)
        eng_word, _ = self.find_word(idx)

        if (post_code[2] if len(post_code) > 2 else post_code[0][2]) == 25:
            self.output.append(eng_word[1])
        else:
            self.output.append(eng_word[0])

    def rule6(self, idx):
        word, _ = self.find_word(idx)
        self.output.append(word[0])