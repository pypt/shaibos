#!/bin/bash

for dir in $(find . -mindepth 1 -maxdepth 1 -type d)
do
    pushd $dir
    rm -r invoices
    ../../../bin/shaibos-invoice --format=html
    ../../../bin/shaibos-invoice --format=pdf
    popd
done
