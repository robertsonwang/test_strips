import tensorflow as tf

from object_detection.utils import dataset_util


flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

def create_tf_example(encoded_ts, filename, xmin, xmax, ymin, ymax):
   """Creates a tf proto from sample test_strip image.

  Args:
    encoded_ts: The jpg encoded data of the test_strip image.

  Returns:
    example: The created tf.Example.
  """

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