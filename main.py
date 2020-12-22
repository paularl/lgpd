# coding: utf-8

import os
from fnmatch import fnmatch
from Readers import FileReader
import Searchers
import csv
import sys
import datetime

if __name__ == '__main__':

    root = sys.argv[1]
    # pattern = "*.pdf"

    output = []

    start = datetime.datetime.now()

    f = open("log.txt", "w")
    f.write("starting scan...........{}".format(start))
    f.close()




    for path, subdirs, files in os.walk(root):

        for name in files:
            print(name)
            classification_dict = None
            reader = None
            is_excel = None

            try:
                reader = FileReader(os.path.join(path, name))


            except Exception as e:
                print(e)
                if name.split('.')[-1] in ("doc", "docx", "pdf", "txt", "ppt", "pptx", "xls", "xlsx"):

                    classification_dict = {key: '' for key in Searchers.patterns.keys()}
                    classification_dict['path'] = path
                    classification_dict['name'] = name
                    classification_dict['extension'] = name.split('.')[-1]
                    classification_dict['error'] = 1
                    classification_dict['sensitive'] = ''
                    classification_dict['error_msg'] = 'Could not read the file.'

                pass

            if reader is not None:
                if reader.text is not None:
                    if reader.extension in ["xls", "xlsx"]:
                        is_excel=True
                    patterns_matches = Searchers.SearchData(reader.text, is_excel=is_excel)
                    classification_dict = Searchers.ClassifyData(patterns_matches, reader.text, is_excel=is_excel)
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

            if classification_dict is not None:

                desired_order_list = ['path', 'name', 'extension', 'error', 'sensitive', 'cpf', 'rg', 'cep', 'nascimento', 'nome',
                                      'telefone','email', 'error_msg']
                output_dict = {o: classification_dict[o] for o in desired_order_list}
                output.append(output_dict)

    end = datetime.datetime.now()
    lag = end-start

    with open("scan_{}.csv".format(end.strftime("%d-%m-%y_%H-%M")), "w", newline='', encoding="utf-8") as outfile:
        end.strftime("%d-%m-%y_%H-%M")
        keys = output[0].keys()
        writer = csv.writer(outfile, delimiter=';')
        writer.writerow(keys)
        for line in output:
            try:
                writer.writerow(list(line.values()))
            except:
                pass

    f = open("log.txt", "a", newline='')
    f.write('scan ended at {} and took {}'.format(end, lag))
    f.close()

