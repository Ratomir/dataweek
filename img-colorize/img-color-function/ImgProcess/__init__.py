import logging
import os
import azure.functions as func
import numpy as np
import cv2
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(os.environ["BlobStorage"])
container_name = 'no-color-image'

base_path = os.path.abspath(os.path.join(__file__, "../../../../..")) + "/mnt/data/data/"
local_path = base_path + "no-image"

prototxt = base_path + "colorization_deploy_v2.prototxt"
model = base_path + "colorization_release_v2.caffemodel"
points = base_path + "pts_in_hull.npy"

net = cv2.dnn.readNetFromCaffe(prototxt, model)
pts = np.load(points)

class8 = net.getLayerId("class8_ab")
conv8 = net.getLayerId("conv8_313_rh")
pts = pts.transpose().reshape(2, 313, 1, 1)
net.getLayer(class8).blobs = [pts.astype("float32")]
net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

def main(myblob: func.InputStream):
    
    IMAGE = myblob.name.split('/')[-1]
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=IMAGE)
    download_file_path = os.path.join(local_path, IMAGE)
    print("\nDownloading blob to \n\t" + download_file_path)

    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    image = cv2.imread(download_file_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    scaled = image.astype("float32") / 255.0
    lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2LAB)
    resized = cv2.resize(lab, (224, 224))
    L = cv2.split(resized)[0]
    L -= 50

    net.setInput(cv2.dnn.blobFromImage(L))
    ab = net.forward()[0, :, :, :].transpose((1, 2, 0))
    ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

    L = cv2.split(lab)[0]
    colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

    colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
    colorized = np.clip(colorized, 0, 1)
    colorized = (255 * colorized).astype("uint8")

    cv2.imwrite(base_path + 'color-image/' + IMAGE, cv2.cvtColor(colorized, cv2.COLOR_RGB2BGR))

    logging.info(f"Python blob trigger function processed blob \n"
             f"Name: {myblob.name}\n"
             f"Blob Size: {myblob.length} bytes")
