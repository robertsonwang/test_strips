import json
import os

def make_json_bboxes(file_path = '/Users/robertsonwang/Desktop/Python/test_strips/'):
	output_path = os.path.join(file_path, 'train')
	labels = ['4.0-6.0', '6.5-7.5', '8.0-9.0']
	dict_key = []
	dict_list = []

	for label in labels:
	    filename = 'boundingBoxes'+label+'.txt'
	    
	    with open(file_path + filename, 'r') as read_file:
	        bboxes = read_file.read()
	        
	    label_path = '/Users/robertsonwang/Desktop/Python/test_strips/raw_input/'+ label + "/"
	    image_files = os.listdir(label_path)
	    bboxes = bboxes.replace(':'+label, '')
	    clean_list = [x + ')]' for x in bboxes.split(')]') if x != '']
	    
	    for item in clean_list:
	        tup = item.split(':')
	        if tup[0].replace("\n", "") in image_files:
	            dict_key.append(label_path + tup[0].replace("\n", ""))
	            dict_list.append(eval(tup[1]))
	            
	final_dict = {k:v for k,v in zip(dict_key, dict_list)}

	with open(output_path + 'boundingboxes.json', 'w') as outfile:
	    json.dump(final_dict, outfile)

def make_label_map(output_path):
	files = [x for x in os.listdir(file_path) if 'jpg' in x]

	out_file_str = ''
	index = [1,2,3]
	label = ['4.0-6.0', '6.5-7.5', '8.0-9.0']
	for (i,l) in zip(index, label):
	    out_file_str += """
	    item{
	    id: %s
	    name: \"test_strip_ + %s\"
	    }
	    """% (str(i), l)

	with open(output_path + 'ts_labels_train.txt', 'w') as out_file:
	    out_file.write(out_file_str)