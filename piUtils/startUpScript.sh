#!/bin/bash

python downloadConfigAndApp.py

if [ $? -eq 0 ]; then
    unzip -o -q app.zip
    rm app.zip
    python app/main.py
fi
