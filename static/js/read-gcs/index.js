window.onload=function(){
  async function listFiles() {
    var gallery = document.getElementById('simple-gallery');
    let output = "";

    let resp = await fetch('https://storage.googleapis.com/storage/v1/b/images.mccurdyc.dev/o?prefix=images/photography/2022-02-09-yoga');
    if (resp.ok) {
      let json = await resp.json();

      json.items.forEach(file => {
        output += `
        <a href="https://storage.googleapis.com/images.mccurdyc.dev/${file.name}" target="_blank">
          <div class="box fancy-figure caption-position-bottom caption-effect-fade">
            <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
              <div class="img">
                <img src="https://www.mccurdyc.dev/${file.name}?quality=30&pad=100&bg-color=ffffff"/>
              </div>
              <figcaption>
                <p>${file.name}</p>
              </figcaption>
            </figure>
          </div>
        </a>`;
      });
    }
    gallery.innerHTML = output;
  }

  listFiles().catch(console.error);
};
