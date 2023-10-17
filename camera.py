import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

model = tf.keras.Sequential([
    hub.KerasLayer(
        name='inception_v1',
        handle='https://tfhub.dev/google/imagenet/inception_v1/classification/4',
        trainable=False),
])
model.build([None, 224, 224, 3])
model.summary()


def load_imagenet_labels(file_path):
  labels_file = tf.keras.utils.get_file('ImageNetLabels.txt', file_path)
  with open(labels_file) as reader:
    f = reader.read()
    labels = f.splitlines()
  return np.array(labels)

def read_image(file_name):
  image = tf.io.read_file(file_name)
  image = tf.io.decode_jpeg(image, channels=3)
  image = tf.image.convert_image_dtype(image, tf.float32)
  image = tf.image.resize_with_pad(image, target_height=224, target_width=224)
  return image

def top_k_predictions(img, k=1):
  imagenet_labels = load_imagenet_labels('https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
  image_batch = tf.expand_dims(img, 0)
  predictions = model(image_batch)
  probs = tf.nn.softmax(predictions, axis=-1)
  top_probs, top_idxs = tf.math.top_k(input=probs, k=k)
  top_labels = imagenet_labels[tuple(top_idxs)]
  return top_labels, top_probs[0]

import requests
import json
import tempfile
query = 'hp 6550'
res = requests.get(f"https://api.search.brave.com/res/v1/images/search?q={'+'.join(query.split(' '))}&safesearch=strict&count=1&search_lang=en&country=us&spellcheck=1", headers={
    'Accept':'application/json',
    'Accept-Encoding': 'gzip',
    'X-Subscription-Token':'BSArCBHslQs8k4GSeCIT_GgG7hVOQIY'
})
res = json.loads(res.text)
img_url = res['results'][0]['thumbnail']['src']
img_path = tf.keras.utils.get_file(tempfile.mktemp(), img_url)
img = read_image(img_path)


plt.imshow(img)
plt.title(img_path, fontweight='bold')
plt.axis('off')
plt.show()

pred_label, pred_prob = top_k_predictions(img)

if 'camera' in pred_label[0]:
  print(f'it is a camera ({pred_label[0]}: {pred_prob[0]:0.1%})')
else:
  print(f'it is NOT a camera ({pred_label[0]}: {pred_prob[0]:0.1%})')


import pyodbc
server_name = 'sql-dev-captureonebi02.database.windows.net'
user = "aasdevcaptureonebi02"
pw = "LM0xHJ!jMj4pLvCD!N3x"
db = "EDW"
connection_string = f"Driver={{ODBC Driver 18 for SQL Server}};Server={server_name};Database={db};UID={user};PWD={pw}"
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

sql_query = "SELECT CameraBrand, Series  FROM [edw].[DimAppCameras];"
cursor.execute(sql_query)
for row in cursor.fetchall():
  print(row)

cursor.close()
conn.close()


