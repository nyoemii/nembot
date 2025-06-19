## Source
~~most assets here (basically just the map shit) is sourced from https://developer.valvesoftware.com/wiki/Counter-Strike_2/Maps~~
dumped myself now </3 (panorama/images/map_icons for map icons, anything else is probably sourced from valve dev wiki now too)

`for f in map_icon_*.svg *.svg; do [ -f "$f" ] || continue; out="${f#map_icon_}"; out="${out%.svg}.png"; rsvg-convert -w 1024 -h 1024 "$f" -o "$out"; done` after dumping svgs with s2viewer