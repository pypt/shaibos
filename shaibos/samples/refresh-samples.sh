#!/bin/bash

for dir in $(find . -mindepth 1 -maxdepth 1 -type d)
do
    pushd $dir
    rm -r invoices
    ../../../bin/shaibos-pdf
    ../../../bin/shaibos-html
    popd
done
