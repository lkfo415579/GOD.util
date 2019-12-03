git ls-tree -r -l master |sort -k4 -n
git filter-branch --index-filter git rm -rf --cached --ignore-unmatch jenkins_data/SERVER/bin/server_batch -- --all
git filter-branch --index-filter git rm -rf --cached --ignore-unmatch jenkins_data/SERVER/bin/server_batch HEAD
