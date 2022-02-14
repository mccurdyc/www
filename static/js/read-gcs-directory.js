$( document ).ready(function() {
  const {Storage} = require('@google-cloud/storage');

  const projectId = 'www-mccurdyc-dev'
  const storage = new Storage({projectId: projectId});
  const options = {
    prefix: 'images/photography/2022-02-09-yoga',
  };

  async function listFiles() {
    let output = "";

    const [files] = await storage.bucket('images.mccurdyc.dev').getFiles(options);
    var gallery = document.getElementById('image-gallery');

    files.forEach(file => {
      output += `
      <div class="box">
        <figure itemprop='associatedMedia' itemscope itemtype='http://schema.org/ImageObject'>
          <div class='img'>
            <img itemprop='thumbnail' src='https://storage.googleapis.com/images.mccurdyc.dev/${file.name}' alt='TODO HERE' />
          </div>
          <figcaption>
            <p>Caption HERE</p>
          </figcaption>
          <a href='https://storage.googleapis.com/images.mccurdyc.dev/${file.name}' itemprop='contentUrl'></a>
        </figure>
      </div>`;
    });

     gallery.innerHTML = output;
    console.log(output);
  }

  listFiles().catch(console.error);
});
