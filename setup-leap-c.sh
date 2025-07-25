#!/bin/bash

echo "Activating tdmpc2 conda environment..."
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
else
    echo "Conda not found."
    exit 1
fi
conda activate tdmpc2

echo "Cloning leap-c..."
git submodule add -b main git@github.com:MazenAmria/leap-c.git ./tdmpc2/leap-c
git submodule update --init --recursive
cd ./tdmpc2/leap-c

echo "Installing CasADi..."
pip install casadi

echo "Installing acados..."
cd ./external/acados

mkdir -p build
cd build
cmake -DACADOS_WITH_QPOASES=ON -DACADOS_WITH_OPENMP=ON -DACADOS_PYTHON=ON -DACADOS_NUM_THREADS=1 ..
make install -j4

cd ../

conda env config vars set ACADOS_SOURCE_DIR=$PWD LD_LIBRARY_PATH=$LD_LIBRARY_PATH:"$PWD/lib"
conda deactivate
conda activate tdmpc2

cd ../../

echo "Installing leap-c dependencies..."
pip install -e $ACADOS_SOURCE_DIR/interfaces/acados_template
pip install torch
pip install -e .[rendering]

exit 0
