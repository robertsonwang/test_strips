import json
import os

def make_json_bboxes(filename, file_path, label = '8.0-9.0', output_path = ''):
	with open(file_path + filename, 'r') as read_file:
	    bboxes = read_file.read()
	bboxes = bboxes.replace(':'+label, '')
	clean_list = [x + ')]' for x in bboxes.split(')]') if x != '']

	dict_key = []
	dict_list = []

	for item in test_list:
	    tup = item.split(':')
	    dict_key.append(tup[0])
	    dict_list.append(eval(tup[1]))
	final_dict = {k:v for k,v in zip(dict_key, dict_list)}

	with open(output_path + filename.split('.')[0] + '.json', 'w') as outfile:
	    json.dump(final_dict, outfile)

def make_label_map(file_path = '/Users/robertsonwang/Desktop/bb_images/'):
	files = [x for x in os.listdir(file_path) if 'jpg' in x]

	out_file_str = ''
	for i in range(len(files)):
	    out_file_str += """
	    {
	    id: %s
	    name: 'test_strip'
	    }
	    """% str(i+1)
	with open(file_path + 'ts_labels_train.txt', 'w') as out_file:
	    out_file.write(out_file_str)