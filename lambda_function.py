import numpy as np
import rawpy
from libtiff import TIFF
import boto3

pathToTmpFile = '/tmp/file.cr2'

def SaveBinaryImageToFile(i, p):
    tif = TIFF.open(p, mode='w')
    wi = np.array(i*255, dtype=np.uint8)
    tif.write_image(wi)
    tif.close()

def OpenCr2FileIntoRGBNumpyArray(p):
    with rawpy.imread(p) as raw:
        print 'Image %s read!' % p
        rgb = raw.postprocess()
        print 'original type = %s' % rgb.dtype
        print 'dimensions of rgb %s' % str(rgb.shape)
    return rgb

def MainThing():
    rgb = OpenCr2FileIntoRGBNumpyArray(pathToTmpFile)
    b = rgb[:,:,0]
    b = b > np.mean(b)
    b.astype(np.uint8)
    print 'Saving blue channel thresholded to global mean'
    SaveBinaryImageToFile(b, 'blue.tif')
    #rgb32 = np.array(rgb, dtype=np.uint32)
    #print 'converted type = %s' % rgb32.dtype
    #print 'Postprocessing raw file done!'
    #tif = TIFF.open('filename.tif', mode='w')
    #tif.write_image(rgb32, write_rgb=True)
    #print 'Tiff file saved!'
    #tif.close()


def lambda_handler(event, context):
    print 'Numpy version is %s' % np.version.version
    # import cr2 file from s3 into pathToTmpFile
    MainThing()
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
