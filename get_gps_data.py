#Import functions and modules
import os
import sys
import PIL.ExifTags
import PIL.Image
import json

try:
	current_dir = sys.argv[1]
except:
	current_dir = os.getcwd()

def convert_to_degrees(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

image_types = ['.ras', '.xwd', '.bmp', '.jpe', '.jpg', '.jpeg', '.xpm', '.ief', '.pbm', '.tif', 
'.gif', '.ppm', '.xbm', '.tiff', '.rgb', '.pgm', '.png', '.pnm']
image_types.extend([x.upper() for x in image_types])

#Get image files
image_files = [file_name + file_extension for (file_name, file_extension) in [os.path.splitext(x) for x in os.listdir(current_dir)]
if file_extension in image_types]

#Get exif data from image files then print to a dictionary, store as a JSON object
gps_dict = {}
for image in image_files:
    img = PIL.Image.open(image)
    exif_data = img._getexif()
    exif = {
        PIL.ExifTags.TAGS[k]: v
        for k, v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
    }
    
    gpsinfo = {}

    try:
        for key in exif['GPSInfo'].keys():
            decode = PIL.ExifTags.GPSTAGS.get(key,key)
            gpsinfo[decode] = exif['GPSInfo'][key]
        lat_value = gpsinfo['GPSLatitude']
        long_value = gpsinfo['GPSLongitude']
        gps_dict[image] = (str(convert_to_degrees(lat_value)) + " " + gpsinfo['GPSLatitudeRef'], str(convert_to_degrees(long_value)) + " " + gpsinfo['GPSLongitudeRef'])
    
    except KeyError:
        print("No GPS data was found in the exif metadata")

with open(current_dir + "/exif_data.json", 'wb') as out_file:
	json.dump(gps_dict, out_file)
