#!/usr/bin/env nodejs
'use strict';

var docopt = require('docopt');
var fs     = require('fs');
var util   = require('util');
var bson   = require('bson');
var cbor   = require('cbor');

var doc = ['Benchmark',
'',
'Usage:',
'    benchmark (json|bson|cbor) <repeat> <input>',
'',
'Options:',
'    -h --help   Show this screen'].join('\n')

var args = docopt.docopt(doc);
/*
    print('-' * 78)
    for operation, elapsed in iteritems(avgs):
        print('Promedio {}: {:.4f} seconds'.
              format(operation, elapsed / repeat))

    fun = globals()['{}_dump'.format(serialization)]
    print(
        'Tamaño {}: {:.4f} MiB'.format(
            serialization,
            len(fun(data)) / float(1048576)
            )
    )

if __name__ == '__main__':
    main(**docopt(__doc__))

*/
var methods = {}

methods.json_load = function (raw){
    return JSON.parse(raw);
};

methods.json_dump = function (data){
    return JSON.stringify(data);
};

methods.bson_load = function (raw){
    return bson.BSONPure.BSON.deserialize(raw);
};

methods.bson_dump = function (data){
    return bson.BSONPure.BSON.serialize(data);
};

methods.cbor_load = function (raw){
    return cbor.CBOR.decode(raw);
};

methods.cbor_dump = function (data){
    return cbor.CBOR.encode(data);
};

var bytes = {
    'json': function (str) { return str.length; },
    'cbor': function (obj) { return obj.byteLength; },
    'bson': function (bfr) { return bfr.length; }
};


function elapsed(before, after){
    return ((after[0] - before[0]) + (after[1] - before[1]) / 1000000000)
        .toFixed(4);
}

function run(operation, data){
    var before, after, s, nano;
    var res;

    before = process.hrtime();
    res = methods[operation](data);
    after = process.hrtime();
    util.print(operation, ': ', elapsed(before, after), '\n');
    return res;
}

function main(args){
    var infile = args['<input>'];
    var repeat = Number(args['<repeat>']);
    var serialization;
    var raw;
    var data = JSON.parse(fs.readFileSync(infile));

    for (var key in args){
        if (args.hasOwnProperty(key) && args[key] === true &&
                (key === 'json' || key === 'bson' || key === 'cbor')){
            serialization = key;
            break;
        }
    }

    for (var i = 0; i < repeat; i++){
        raw = run(util.format('%s_dump', serialization), data);
    }
    for (var i = 0; i < repeat; i++){
        run(util.format('%s_load', serialization), raw);
    }

    var fun = methods[util.format('%s_dump', serialization)];
    util.print('Tamaño ', serialization, ': ',
               (bytes[serialization](fun(data)) / 1048576).toFixed(4),
               ' MiB\n')
}


if (require.main === module){
    main(args);
}
