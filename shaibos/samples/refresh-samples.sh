#!/bin/bash

for dir in $(find . -mindepth 1 -maxdepth 1 -type d)
do
    pushd $dir
    rm -r invoices
    ../../../bin/shaibos-invoice --format=html
    ../../../bin/shaibos-invoice --format=pdf
    ../../../bin/shaibos-journal --format=html --year=2015 --print_totals
    ../../../bin/shaibos-journal --format=pdf --year=2015 --print_totals
    popd
done
