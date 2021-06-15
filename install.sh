#!/usr/bin/bash
#
# Description: Install LED-Stock-Ticker software (github.com/feram18/LED-stock-ticker)
#

echo "___________________________________________________________________"
echo "   __   _______    ______           __     _______     __          "
echo "  / /  / __/ _ \  / __/ /____  ____/ /__  /_  __(_)___/ /_____ ____"
echo " / /__/ _// // / _\ \/ __/ _ \/ __/  '_/   / / / / __/  '_/ -_) __/"
echo "/____/___/____/ /___/\__/\___/\__/_/\_\   /_/ /_/\__/_/\_\\__/_/   "
echo "___________________________________________________________________"

echo -e "\n"

# Update Raspberry Pi & Install Python 2.7-dev
sudo apt-get update && sudo apt-get install python2.7-dev -y

# Install rpi-rgb-led-matrix library
cd rpi-rgb-led-matrix || exit
echo "Installing rpi-rgb-led-matrix library..."
cd bindings || exit
sudo pip install -e python/

# Clean up & update repository
cd ../../
git reset --hard
git checkout master
git fetch origin --prune
git pull

# Install dependencies
echo "Installing dependencies..."
sudo pip install requests pytz

# Create config.json file from config.json.example
cp config.json.example config.json
chown pi:pi config.json

echo -e  "\nIf there are no errors shown above, installation was successful"

echo -e "\nEdit the config.json file to customize your settings"
echo -e "\nIf the file is missing, you can create one by copying the config.json.example to config.json"
echo -e "\nMake sure your matrix is properly working with the samples located in rpi-rgb-led-matrix/bindings/python/samples\n"