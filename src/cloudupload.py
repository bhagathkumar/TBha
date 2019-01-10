# Imports the Google Cloud client library
from google.cloud import storage
import glob
import time
import os

dpath = "/work/work1/out2"


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


while True:
    a = glob.glob(dpath + "/*.jpg")
    for fn in a:
        print(fn)
        p, f = os.path.split(fn)
        upload_blob("bha-cc-camfiles1",fn,f)
        os.rename(fn,"/work/work1/out3/"+f)
    print("sleeping")
    time.sleep(2)

#upload_blob("bha-cc-camfiles1", "/work/work1/out/img15.jpg", "img15.jpg")
