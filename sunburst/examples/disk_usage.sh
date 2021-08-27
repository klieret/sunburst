#!/bin/bash

cd ..
du | sort -n -r > examples/data/file_sizes.txt
