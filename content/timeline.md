# "TIMELINE"

{{< rawhtml >}}
  <div class="recent-posts section">
    <div class="posts">
      {{ $pages := where .Site.RegularPages "Type" "in" .Site.Params.listedContentTypes }}
      {{ $paginator := .Paginate (where $pages "Params.hidden" "ne" true) 50 }}
      {{ range $paginator.Pages }}
        {{ if (.Param "hide" | default false) }}
        {{ else }}
        <div class="post">
          <div class="post-header">
            <div class="meta">
              <div class="date">
                <span class="day">{{ dateFormat "2006.01.02" .Date }}</span>
              </div>
            </div>
            <div class="matter">
              <h3 class="title small">
                <a href="{{ .RelPermalink }}">"{{.Title | upper}}"</a>
              </h3>
              {{- if eq .Page.Type "photos" }}
                {{ $image := .Param "image" }}
                {{- if $image }}
                    <img src="{{ $image }}?crop=1:1&quality=40&height=0.5&width=0.5" class="photo"/>
                {{ end }}
              {{ else }}
                {{ $image := .Param "image" }}
                {{- if $image }}
                    <img src="{{ $image }}" class="book-cover"/>
                {{ end }}
              {{ end }}
              <span class="description">
                {{ if isset .Params "description" }}
                  {{ .Description }}
                {{ end }}
              </span>
            </div>
          </div>
        </div>
        {{ end }}
      {{ end }}
    </div>
  </div>

{{< /rawhtml >}}
