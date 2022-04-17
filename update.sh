#!/usr/bin/bash
# Description: Update LED-Stock-Ticker (github.com/feram18/led-stock-ticker)

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function clean() {
  rm -f "*.log*"
  sudo rm -rf "*/__pycache__"
  sudo rm -rf "__pycache__"
}

function updateRepository() {
  printf "Updating repository...\n"
  git reset --hard
  git checkout master
  git fetch --tags
  tag="$(git describe --abbrev-0)"
  git checkout tags/"$tag"
}

function installDependencies(){
  printf "\nInstalling dependencies...\n"
  sudo pip3 install -r requirements.txt
}

function createConfigFile() {
  echo "$(tput setaf 7)Creating new config.json file..."
  cp config.json.example config.json
  chown "$USER": config.json
  echo "Set your preferences using the command $(tput setaf 3)./config.py$(tput setaf 7)"
}

# Checks if configuration file exists/requires update
function checkConfigFile() {
  cd "${ROOT_DIR}/config/" || exit
  if [[ ! -e config.json ]]; then
    createConfigFile
  elif [[ -e config.json && config.json.example -nt config.json ]];then
    echo -e "\n$(tput setaf 1)Your config file is out of date"
    mv config.json old-config.json
    createConfigFile
  fi
  cd "${ROOT_DIR}" || exit
}

function main() {
  clean
  updateRepository
  installDependencies
  checkConfigFile

  # Allow scripts to be easily executed next time
  chmod +x install.sh update.sh config.py

  echo "$(tput setaf 2)Update completed$(tput setaf 7)"
}

main