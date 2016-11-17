#!/bin/bash

if [[ "$1" != "quiet" ]]
then
	echo "Run this to test the examples without having to install the package"
	echo "i.e. to update the path"
	echo "run with 'source set_path.sh'"
fi

add_to_pypath ()
{
    if [[ "$PYTHONPATH" =~ (^|:)"${1}"(:|$) ]]
    then
        return 0
    fi
    export PYTHONPATH=${1}:$PYTHONPATH
}

this_dir=$(dirname $0)
lib=$(realpath ${this_dir}/../)

if [[ "$1" != "quiet" ]]
then
	echo "old PYTHONPATH: $PYTHONPATH"
fi

add_to_pypath $lib

if [[ "$1" != "quiet" ]]
then
	echo "new PYTHONPATH: $PYTHONPATH"
fi
