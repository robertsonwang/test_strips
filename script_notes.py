import PIL.Image
test_image = 'IMG_3272.JPG'

img = PIL.Image.open(test_image)
exif_data = img._getexif()

import PIL.ExifTags
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items()
    if k in PIL.ExifTags.TAGS
}

def convert_to_degress(value):
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


gpsinfo = {}
for key in exif['GPSInfo'].keys():
    decode = PIL.ExifTags.GPSTAGS.get(key,key)
    gpsinfo[decode] = exif['GPSInfo'][key]
gpsinfo

lat_value = gpsinfo['GPSLatitude']
long_value = gpsinfo['GPSLongitude']
print convert_to_degress(lat_value)
print convert_to_degress(long_value)