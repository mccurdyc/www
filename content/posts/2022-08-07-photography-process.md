---
title: "2022.08.07 Photography Process"
description: ""
author: ""
date: 2022-08-07T13:49:57-04:00
subtitle: ""
image: ""
post-tags: ["photography"]
posts: ["Photography Process"]
draft: false
hide: false
---

1. Take photos
1. (Optional) "Star" a photo on the camera
1. Import to Lightroom/Capture One on iPad via an SD-card dongle
1. "Star" photos
1. Filter and delete unstarred photos
1. Apply minor edits (I hate editing, so I try to shoot so I don't have to edit)
    - Fix exposure
    - Usually white balance of 5700 kelvin.
    - Minor cropping

1. Export from Lightroom/Capture One on iPad to external SSD
    - **(Critical step) should be stored as `YYYY/MM/DD-something`**

1. Mount the external SSD to my Linux box (Intel NUC)
1. `gsutil -m rsync -r /mnt/photos/YYYY/MM/ gs://images.mccurdyc.dev/images/YYYY/MM/`
1. `hugo new photos YYYY-MM-DD-something.md`
1. `make deploy`
