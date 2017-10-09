import tensorflow as tf
import sys
sys.path.append('/Users/robertsonwang/Desktop/models/research/')
from object_detection.utils import dataset_util
import json
flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

with open('/Users/robertsonwang/Desktop/bb_images/data/bound_results_train.json') as data_file:    
    bboxes = json.load(data_file)

def importImage(fileName):
    imgText = open(fileName, 'rb')
    imgTextStr = imgText.read()
    imgText.close()
    return imgTextStr

def create_tf_example(encoded_ts, filename, xmin, xmax, ymin, ymax):
#   Creates a tf proto from sample test_strip image.
#   Args:
#     encoded_ts: The jpg encoded data of the test_strip image.
#   Returns:
#     example: The created tf.Example.

    height = 250
    width = 250
    image_format = b'jpg'

    xmins = [float(xmin)/float(width)]
    xmaxs = [float(xmax)/float(width)]
    ymins = [float(ymin)/float(height)]
    ymaxs = [float(ymax)/float(height)]

    classes_text = ['test_strip']
    classes = [1]

    tf_example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(filename),
      'image/source_id': dataset_util.bytes_feature(filename),
      'image/encoded': dataset_util.bytes_feature(encoded_ts),
      'image/format': dataset_util.bytes_feature(image_format),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
      'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
      'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    
    return tf_example

def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

    for image in bboxes.keys():
        image = str(image)
        image_jpg = importImage(image)
        xmin, xmax, ymin, ymax = float(bboxes[image][0][0]), float(bboxes[image][1][0]), \
                                float(bboxes[image][0][1]), float(bboxes[image][1][1])
        tf_example = create_tf_example(image_jpg, image, xmin, xmax, ymin, ymax)
        writer.write(tf_example.SerializeToString())

    writer.close()

if __name__ == '__main__':
	tf.app.run()