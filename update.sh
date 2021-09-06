#!/usr/bin/bash
# Description: Update LED-Stock-Ticker software (github.com/feram18/led-stock-ticker)

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Cleans up & updates repository
updateRepository() {
  printf "Updating repository...\n"
  git reset --hard
  git checkout master
  git fetch origin --prune
  git pull
}

# Installs dependencies
installDependencies(){
  printf "\nInstalling dependencies...\n"
  python3 -m pip install -r requirements.txt
}

# Creates configuration file (config.json)
createConfigFile() {
  echo "$(tput setaf 7)Creating new config.json file..."
  cp config.json.example config.json
  chown "$USER": config.json
  echo "Configure the default preferences by running the command $(tput setaf 3)./config$(tput setaf 7)"
}

# Checks if configuration file exists/requires update
checkConfigFile() {
  cd "${ROOT_DIR}/config/" || exit
  if [[ ! -e config.json ]]; then # config.json file does not exist
    createConfigFile
  elif [[ -e config.json && config.json.example -nt config.json ]];then
    # config.json file exists, but format has changed
    echo -e "\n$(tput setaf 1)Your config file is out of date. Removing current config file..."
    rm -f config.json
    createConfigFile
  fi
  cd "${ROOT_DIR}" || exit # Back to repo's root directory
}

main() {
  updateRepository
  installDependencies
  checkConfigFile

  # Allow scripts to be easily executed next time
  chmod +x install.sh update.sh config.py

  echo "$(tput setaf 2)Update completed$(tput setaf 7)"
}

# Execute script
main