// https://github.com/googleapis/nodejs-storage/blob/04791c7fa2602a3d8532d485b5265d759882596e/samples/listFilesByPrefix.js
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
    var div = document.createElement('div');
    div.setAttribute('class', 'box');
    div.innerHTML = ""
    document.body.appendChild(div);
  });
}

listFiles().catch(console.error);
