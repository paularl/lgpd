# coding: utf-8

import os
from fnmatch import fnmatch
from Readers import FileReader
import Searchers
import csv
import sys
import datetime

# root = sys.argv[1]
# print(root)
root = 'C:/'
# pattern = "*.pdf"

output = []

start = datetime.datetime.now()

f = open("log.txt", "w")
f.write("starting scan...........{}".format(start))
f.close()

for path, subdirs, files in os.walk(root):

    for name in files:

        try:
            reader = FileReader(os.path.join(path, name))

        except:

            reader = None
            classification_dict = {key: '' for key in Searchers.patterns.keys()}
            classification_dict['path'] = path
            classification_dict['name'] = name
            classification_dict['extension'] = name.split('.')[-1]
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
                classification_dict['extension'] = reader.extension
                classification_dict['error'] = 0
                classification_dict['error_msg'] = ''
            else:
                classification_dict = {key: '' for key in Searchers.patterns.keys()}
                classification_dict['path'] = path
                classification_dict['name'] = name
                classification_dict['extension'] = reader.extension
                classification_dict['error'] = 1
                classification_dict['sensitive'] = ''
                classification_dict['error_msg'] = 'No text found in file'


        desired_order_list = ['path', 'name', 'error', 'sensitive', 'cpf', 'rg', 'cep', 'nascimento', 'nome',
                              'telefone','email', 'error_msg']
        output_dict = {o: classification_dict[o] for o in desired_order_list}

        output.append(output_dict)


with open("output.csv", "w", newline='', encoding="utf-8") as outfile:

    keys = output[0].keys()
    writer = csv.writer(outfile, delimiter=';')
    writer.writerow(keys)
    for line in output:
        try:
            writer.writerow(list(line.values()))
        except:
            pass
    # dict_writer = csv.DictWriter(outfile, keys)
    # dict_writer.writeheader()
    # dict_writer.writerows(output)

end = datetime.datetime.now()
lag = end-start
f = open("log.txt", "a")
f.write('scan ended at {} and took {}'.format(end, lag))
f.close()


