#!/bin/sh
while true; do
python main.py
if [ $? -eq 0 ]; then
    echo "Hoorah! Done!"
    break
fi
done
