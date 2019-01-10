from google.cloud import pubsub_v1
import json
from ast import literal_eval
import io
from google.cloud import vision
from google.cloud.vision import types
import os


def ann(ipath):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = ipath
    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')
    for label in labels:
        print(label.description)


def receive_messages(project_id, subscription_name):
    """Receives messages from a pull subscription."""
    # [START pubsub_subscriber_async_pull]
    # [START pubsub_quickstart_subscriber]
    import time

    from google.cloud import pubsub_v1

    # TODO project_id = "Your Google Cloud Project ID"
    # TODO subscription_name = "Your Pub/Sub subscription name"

    subscriber = pubsub_v1.SubscriberClient()
    # The `subscription_path` method creates a fully qualified identifier
    # in the form `projects/{project_id}/subscriptions/{subscription_name}`
    subscription_path = subscriber.subscription_path(
        project_id, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        print("---------")
        pd = literal_eval(message.data.decode())
        print(type(pd))
        filename = "gs://"+pd["bucket"]+"/"+pd["name"]
        print("File Name ", filename)
        ann(filename)
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking. We must keep the main thread from
    # exiting to allow it to process messages asynchronously in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
    # [END pubsub_subscriber_async_pull]
    # [END pubsub_quickstart_subscriber]


receive_messages("lustrous-strand-225410", "bha-cc-camfiles1")
