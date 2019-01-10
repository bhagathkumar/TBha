#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_quickstart():
    # [START datastore_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import datastore

    # Instantiates a client
    datastore_client = datastore.Client('lustrous-strand-225410')

    # The kind for the new entity
    kind = 'Task1'
    # The name/ID for the new entity
    name = 'sampletask3'
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind, name)

    # Prepares the new entity
    task = datastore.Entity(key=task_key)
#    task['description'] = 'Buy milk'
 #   task['amount']='1'

    task.update({
      'category': 'Personal',
      'done': False,
      'priority': 4,
      'description': 'Learn Cloud Datastore',
      'label': 5
    })

    # Saves the entity
    datastore_client.put(task)

    print('Saved {}: {}'.format(task.key.name, task['description']))
    # [END datastore_quickstart]


def get_data():
    # [START datastore_quickstart]
    # Imports the Google Cloud client library
    from google.cloud import datastore

    # Instantiates a client
    datastore_client = datastore.Client('lustrous-strand-225410')
 # The kind for the new entity
    kind = 'Task1'
    # The name/ID for the new entity
    name = 'sampletask3'
    # The Cloud Datastore key for the new entity
    task_key = datastore_client.key(kind,name)
    task = datastore_client.get(key=task_key)
    print(task)

    query = datastore_client.query(kind='Task1')
    results = list(query.fetch())
    print(results)

if __name__ == '__main__':
   # run_quickstart()
   get_data()
