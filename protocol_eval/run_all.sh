#!/bin/sh

REPETITIONS=10

sizes=$(python -c "print(' '.join(map(str,(range(1024, 2**14 + 1, 1024)))))")

gen_name(){
    echo "data-${1}.json"
}

for size in $sizes; do
    file=$(gen_name $size)
    if [ ! -f $file ]; then
        echo "Generating $file"
        ./generate.py $size $file
    fi
done

for size in $sizes; do
    file=$(gen_name $size)
    for lang in py js; do
        for serialization in json bson cbor; do
            echo "Testing under load $serialization in $lang for $size entries"
            ./benchmark.$lang $serialization $REPETITIONS "$(gen_name $size)" > "$lang-$serialization-$size"
        done
    done
done
