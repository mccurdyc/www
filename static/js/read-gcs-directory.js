// https://github.com/googleapis/nodejs-storage/blob/04791c7fa2602a3d8532d485b5265d759882596e/samples/listFilesByPrefix.js
// Copyright 2020 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * This application demonstrates how to perform basic operations on files with
 * the Google Cloud Storage API.
 *
 * For more information, see the README.md under /storage and the documentation
 * at https://cloud.google.com/storage/docs.
 */

  const {Storage} = require('@google-cloud/storage');
  const projectId = 'www-mccurdyc-dev'
  const storage = new Storage({projectId: projectId});
  const delimiter = '/';
  const options = {
    prefix: 'images/photography/',
  };

  if (delimiter) {
    options.delimiter = delimiter;
  }

async function listFiles() {
  const [files] = await storage.bucket('images.mccurdyc.dev').getFiles({});

  console.log('Files:');
  files.forEach(file => {
    console.log(file.name);
  });
}

listFiles().catch(console.error);
