for image in `ls /Users/robertsonwang/desktop/bb_images/raw_input/* | grep jpg`
do
python boundingBox.py -i $image
done