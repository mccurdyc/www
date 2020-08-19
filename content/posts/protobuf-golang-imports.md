---
title: "Protobuf Golang Imports"
author: ""
type: ""
date: 2020-08-19T06:26:29-04:00
subtitle: ""
image: ""
post-tags: []
posts: []
---

`source_relative`
https://github.com/golang/protobuf/issues/39#issuecomment-486920945


```
protoc -I=. --go_out=plugins=grpc,paths=source_relative:. **/*.proto
```

break the above down

`-I` where to look for `proto` files

`--go_out=plugins=paths=source_relative` - you can avoid having `package ".;foo"` in your proto file (I think).
