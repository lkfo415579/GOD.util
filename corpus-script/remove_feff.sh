grep -I -r -l $'\xEF\xBB\xBF' Bi-uy-zh.filter.zh | xargs sed -i 's/\xEF\xBB\xBF//'
