#!/usr/bin/bash
#
# Description: Install LED-Stock-Ticker software (github.com/feram18/led-stock-ticker)
#

echo "$(tput setaf 5)___________________________________________________________________"
echo "$(tput setaf 5)   __   _______    ______           __     _______     __          "
echo "$(tput setaf 5)  / /  / __/ _ \  / __/ /____  ____/ /__  /_  __(_)___/ /_____ ____"
echo "$(tput setaf 5) / /__/ _// // / _\ \/ __/ _ \/ __/  '_/   / / / / __/  '_/ -_) __/"
echo "$(tput setaf 5)/____/___/____/ /___/\__/\___/\__/_/\_\   /_/ /_/\__/_/\_\\__/_/   "
echo "$(tput setaf 5)___________________________________________________________________"

echo -e "$(tput setaf 7)\n"

# Update Raspberry Pi & Install Python 3
sudo apt-get update && sudo apt install python3 idle3

# Install dependencies
echo -e "\nInstalling dependencies..."
sudo pip3 install -r requirements.txt

# Install rpi-rgb-led-matrix library
echo -e "\nInstalling rpi-rgb-led-matrix library..."

cd rpi-rgb-led-matrix || exit
make build-python
sudo make install-python
cd bindings || exit
sudo pip install -e python/

# Clean up & update repository
cd ../../
git reset --hard
git checkout master
git fetch origin --prune
git pull

# Configuration file
echo -e "\nTo customize your preferences, a config.json file is required."
read -r -p "Would you like to create this file now? (This will overwrite any existing config.json files) [Y/n]: " choice

if [ "$choice" != "${choice#[Yy]}" ] ;then
    echo "Creating new config.json file..."
    rm -f -v config/config.json
    cp config/config.json.example config/config.json
    chown pi:pi config/config.json
    echo "Edit the config.json file located in the config directory to set your preferences."
    echo "If the file is missing, you can create one by copying the config.json.example to config.json."
else
  echo -e "\nTo avoid issues, please check the config.json.example to make sure your config.json is still valid."
  echo "If you do not have a config.json file, you can manually copy the config.json.example file in the config directory."
fi

echo -e "\n$(tput setaf 2)If there are no errors shown above, installation was successful."
echo "$(tput setaf 7)Make sure your matrix is properly working with the samples located in rpi-rgb-led-matrix/bindings/python/samples"
exit