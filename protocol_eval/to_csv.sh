#!/bin/sh
set -e
if [ $# -lt 1 ]; then
    echo "Uso: $0 <lang>-<format>-<entries> [<lang>-<format>-<entries> ...]"
    echo "donde lang y format son los mismos para todas las entradas"
    exit 1
fi

files=$(echo "$*" | sed -r 's/ /\n/g' | sort -V)

# El archivo de salida va a tener nombre <lang>-<format>.csv
# Las entradas serán
# entries, serialized_size, dump_time, load_time

rm -i *.csv || true

for f in $files; do
    lang=$(echo "$f" | cut -d- -f1)
    format=$(echo "$f" | cut -d- -f2)
    entries=$(echo "$f" | cut -d- -f3)

    dump_time=$(cat $f  | grep Promedio | grep dump | cut -d: -f2 | cut -d' ' -f2)
    load_time=$(cat $f  | grep Promedio | grep load | cut -d: -f2 | cut -d' ' -f2)
    serialized_size=$(cat $f  | grep Tam | cut -d: -f2 | cut -d' ' -f2)

    output="${lang}-${format}.csv"
    if [ ! -f "$output" ]; then
        echo 'entries, serialized_size, dump_time, load_time' > "$output"
    fi

    echo "$entries, $serialized_size, $dump_time, $load_time" >> "$output"
done
