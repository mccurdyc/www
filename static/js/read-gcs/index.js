window.onload=function(){
  async function listFiles() {
    let bucket = $('#readgcs').attr("bucket");
    let prefix = $('#readgcs').attr("prefix");

    var gallery = document.getElementById('simple-gallery');
    let output = "";

    let resp = await fetch(`https://storage.googleapis.com/storage/v1/b/${bucket}/o?prefix=${prefix}`);
    if (resp.ok) {
      let json = await resp.json();

      json.items.forEach(file => {
        output += `
        <a href="https://storage.googleapis.com/${bucket}/${file.name}" target="_blank">
          <div class="box fancy-figure caption-position-bottom caption-effect-fade">
            <figure itemprop="associatedMedia" itemscope itemtype="http://schema.org/ImageObject">
              <div class="img">
                <img src="https://www.mccurdyc.dev/${file.name}?quality=15&pad=100&bg-color=ffffff"/>
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
