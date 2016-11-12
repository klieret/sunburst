#!/bin/bash

echo "Run this to test the examples without having to install the package"
echo "i.e. to update the path"
echo "run with 'source set_path.sh'"

add_to_pypath ()
{
    if [[ "$PYTHONPATH" =~ (^|:)"${1}"(:|$) ]]
    then
        return 0
    fi
    export PYTHONPATH=${1}:$PYTHONPATH
}

this_dir=$(dirname $0)
lib=${this_dir}/../

echo "old PYTHONPATH: $PYTHONPATH"
add_to_pypath $lib
echo "new PYTHONPATH: $PYTHONPATH"
