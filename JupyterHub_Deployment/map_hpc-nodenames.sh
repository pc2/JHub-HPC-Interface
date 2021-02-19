#!/bin/bash

# This script appends the IP mapping of the HPC node names to the hosts file.

if grep -q "node01-001" /etc/hosts
then
    echo "nodes already mapped"
    echo "DONE"
    exit 0
fi

# map nodes:
for i in {01..12}
do
    for j in {001..048}
    do
        # echo 127.0.0.1 node$i-$j >> /etc/hosts
        echo 127.0.0.1 node$i-$j | sudo tee --append /etc/hosts
    done
done

# map gpus:
for i in {001..035}
do
    # echo 127.0.0.1 gpu$i >> /etc/hosts
    echo 127.0.0.1 gpu$i | sudo tee --append /etc/hosts
done

echo "DONE"

exit 0
