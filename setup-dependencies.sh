#!/usr/bin/env bash

set -e
set -u

sudo apt update
sudo apt install -y libopencv-dev

sudo apt install -y apt-transport-https
sudo mkdir -p /etc/apt/keyrings
curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo `lsb_release -cs` main" | \
sudo tee /etc/apt/sources.list.d/librealsense.list

sudo apt update
sudo apt install -y librealsense2-dkms librealsense2-utils

