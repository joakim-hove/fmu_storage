#!/bin/bash
set -e
git clone https://github.com/Statoil/libecl
mkdir libecl/build
cd libecl/build
cmake .. -DBUILD_PYTHON=ON -DCMAKE_INSTALL_PREFIX=${TRAVIS_BUILD_DIR}/install
make
make install

