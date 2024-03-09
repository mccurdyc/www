#!/usr/bin/env bash

cat <<EOF
{{< gallery >}}
EOF

gsutil ls "gs://images.mccurdyc.dev/images/$1" | sed -En 's/gs:\/\/images.mccurdyc.dev(.*)$/\t{{< figure src="\1" >}}/p'

cat <<EOF
{{< /gallery >}}
{{< load-photoswipe >}}

EOF

cat <<EOF
{{< rawhtml >}}
    <meta property="og:image:url" content="https://www.mccurdyc.dev/images/2024/03-SF/0035.jpg" />
{{< /rawhtml >}}
EOF
