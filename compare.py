import argparse
import ast


class CompareTexts:

    """Reading files and transforming them to string to apply the Levenshtein algorithm.
    Cleaning the code  from docstrings with ast tools.
    Implementation of the Levenshtein algorithm and its application to processed files.
    Output of the Levenshtein results to a file scorer.txt"""

    def __init__(self):
        parser = argparse.ArgumentParser(description='Сomparison of python code to determine the degree of similarity')
        parser.add_argument('input', type=str, help='input for input.txt')
        parser.add_argument('scores', type=str, help='output for scores.txt')
        args = parser.parse_args()
        self.input_file, self.output_file = args.input, args.scores

    def calculate_results(self):
        with open(self.input_file, 'r') as f:
            list_to_compare = f.readlines()
        file_scores = open(self.output_file, 'w')
        for line in list_to_compare:
            orig_name, plgt_name = line.split()
            orig = self.read_transform(orig_name)
            plgt = self.read_transform(plgt_name)
            file_scores.write(str(round((self.levenshtein(orig, plgt) / max(len(orig), len(plgt))), 3)) + "\n")
            print('The files are compared. The result is written in score.txt')

    def read_transform(self, to_transform):
        code = []
        with open(to_transform, 'r', encoding='utf8') as pyfile:
            pyfile = self.normalization(to_transform)
        for line in pyfile.split('\n'):
            if not line.strip():
                continue
            code.append(line.strip())
        return ''.join(code)

    def normalization(self, to_normalize):
        with open(to_normalize, 'r', encoding='utf8') as code:
            ast_tree = ast.parse(code.read())
        for node in ast.walk(ast_tree):
            if not isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                continue
            if not len(node.body):
                continue
            if not isinstance(node.body[0], ast.Expr):
                continue
            if not hasattr(node.body[0], 'value') or not isinstance(node.body[0].value, ast.Str):
                continue
            node.body = node.body[1:]
        normalised_file = ast.unparse(ast_tree)
        return normalised_file

    def levenshtein(self, str1: str, str2: str) -> int:
        n, m = len(str1), len(str2)
        if n > m:
            str1, str2 = str2, str1
            n, m = m, n
        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str1[j - 1] != str2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]


if __name__ == "__main__":
    results = CompareTexts()
    results.calculate_results()



