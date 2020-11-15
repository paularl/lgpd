import os
from fnmatch import fnmatch
from Readers import FileReader
import Searchers
import csv
import sys


root = sys.argv[1]
# print(root)
root = 'C:/Users/paula.romero.lopes/Documents'
# pattern = "*.pdf"

output = []

for path, subdirs, files in os.walk(root):

    print(path)

    for name in files:
        print(name)

        try:
            reader = FileReader(os.path.join(path, name))

        except:

            reader = None
            classification_dict = {key: '' for key in Searchers.patterns.keys()}
            classification_dict['path'] = path
            classification_dict['name'] = name
            classification_dict['error'] = 1
            classification_dict['sensitive'] = ''
            classification_dict['error_msg'] = 'Could not read the file.'
            pass

        if reader:
            if reader.text is not None:
                patterns_matches = Searchers.SearchData(reader.text)
                classification_dict = Searchers.ClassifyData(patterns_matches, reader.text)
                classification_dict['path'] = path
                classification_dict['name'] = name
                classification_dict['error'] = 0
                classification_dict['error_msg'] = ''
            else:
                classification_dict = {key: '' for key in Searchers.patterns.keys()}
                classification_dict['path'] = path
                classification_dict['name'] = name
                classification_dict['error'] = 1
                classification_dict['sensitive'] = ''
                classification_dict['error_msg'] = 'No text found in file'


        desired_order_list = ['path', 'name', 'error', 'sensitive', 'cpf', 'rg', 'cep', 'nascimento', 'nome',
                              'telefone','email', 'error_msg']
        output_dict = {o: classification_dict[o] for o in desired_order_list}

        output.append(output_dict)


with open("output.csv", "w", newline='') as outfile:

    keys = output[0].keys()
    dict_writer = csv.DictWriter(outfile, keys)
    dict_writer.writeheader()
    dict_writer.writerows(output)

