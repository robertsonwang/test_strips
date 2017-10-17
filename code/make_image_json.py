import os
import json

bound_results_dict = {}

def get_image_dict(folder_path = '/Users/robertsonwang/Desktop/Python/test_strips/', text_file = 'boundingBoxes4.0-6.0.txt'):
	
	end_string = text_file[-11:-1] + text_file[-1]
	data_path = '/Users/robertsonwang/Desktop/Python/test_strips/raw_input/' + end_string[0:7] + "/"
	#Open file with form image_str:[(bounding box)]
	with open(folder_path + text_file, 'rb') as box_file:
	    box_str = box_file.read()

	#Create image dictionary from file contents    
	box_list = box_str.replace(end_string, '').split('\n')
	box_list = [x.split(':') for x in box_list]
	image_dict = {k:v for (k, v) in zip([data_path + x[0] for x in box_list if x[0] != ''], 
	           [eval(x[1]) for x in box_list if x[0] != ''])}
	return image_dict


def make_label_txt(image_dict, file_path = '/Users/robertsonwang/Desktop/Python/test_strips/data/'):

	out_file_str = ''
	for i in range(len(image_dict.keys())):
	    out_file_str += """
	    item {
	    id: %s
	    name: 'test_strip'
	    }
	    """% str(i+1)
	with open(file_path + 'ts_labels_train.txt', 'w') as out_file:
	    out_file.write(out_file_str)


if __name__ == '__main__':
	text_file_list = ['boundingBoxes' + x + '.txt' for x in ['4.0-6.0', '8.0-9.0', '6.5-7.5']]
	bound_results_dict = {}
	for text_file in text_file_list:
		if not bound_results_dict:
			bound_results_dict = get_image_dict(text_file = text_file)
		else:
			bound_results_dict.update(get_image_dict(text_file = text_file))
		
	with open('/Users/robertsonwang/Desktop/Python/test_strips/data/' + 'bound_results_train.json', 'w') as out_file:
		json.dump(bound_results_dict, out_file)