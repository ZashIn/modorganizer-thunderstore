ref=${1:-HEAD}
output=${2:-thunderstore-$(poetry version -s).zip}
git archive $ref thunderstore \
    --prefix=thunderstore/protocol/ \
    --add-file thunderstore/protocol/*.exe \
    --prefix= \
    -o ${output}