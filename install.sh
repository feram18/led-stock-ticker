#!/usr/bin/bash
#
# Description: Install LED-Stock-Ticker software (github.com/feram18/led-stock-ticker)
#

echo "___________________________________________________________________"
echo "   __   _______    ______           __     _______     __          "
echo "  / /  / __/ _ \  / __/ /____  ____/ /__  /_  __(_)___/ /_____ ____"
echo " / /__/ _// // / _\ \/ __/ _ \/ __/  '_/   / / / / __/  '_/ -_) __/"
echo "/____/___/____/ /___/\__/\___/\__/_/\_\   /_/ /_/\__/_/\_\\__/_/   "
echo "___________________________________________________________________"

echo -e "\n"

# Update Raspberry Pi & Install Python 3
sudo apt-get update && sudo apt install python3 idle3

# Install dependencies
echo "Installing dependencies..."
sudo pip install -r requirements.txt

# Install rpi-rgb-led-matrix library
echo "Installing rpi-rgb-led-matrix library..."

cd rpi-rgb-led-matrix/bindings/python || exit
make build-python
sudo make install-python
sudo pip install -e python/

# Clean up & update repository
cd ../../
git reset --hard
git checkout master
git fetch origin --prune
git pull

# Create config.json file from config.json.example
echo -e "\nTo customize your preferences, a config.json file is required. "
echo "If this is your first time installing, select Y. If you are updating, "
echo "and you would like to keep your existing config.json, select N"
read -r -p "Would you like to continue? [Y/n]: " choice
choice=${choice,,} # tolower
if [[ $choice =~ ^(yes|y| ) ]] || [[ -z $choice ]]; then
    echo "Creating new config.json file..."
    rm config/config.json
    cp config/config.json.example config/config.json
    chown pi:pi config/config.json
fi

echo -e  "\nIf there are no errors shown above, installation was successful."

echo -e "\nEdit the config.json file located in the config directory to customize your settings."
echo -e "\nIf the file is missing, you can create one by copying the config.json.example to config.json."
echo -e "\nMake sure your matrix is properly working with the samples located in rpi-rgb-led-matrix/bindings/python/samples\n"