#!/bin/sh

set -e

jupyter nbextension install src/jupyter/y_extension --user
jupyter nbextension enable y_extension/main 

mkdir -p ~/.jupyter/custom/
cp src/jupyter/custom.css ~/.jupyter/custom/custom.css

jupyter notebook --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.allow_origin='*' &>/dev/null

uvicorn src.main:app --host 0.0.0.0
