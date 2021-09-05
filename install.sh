#!/usr/bin/bash
# Description: Install LED-Stock-Ticker software (github.com/feram18/led-stock-ticker)

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Installs rpi-rgb-led-matrix library
installMatrixLibrary() {
  printf "\nInstalling rpi-rgb-led-matrix library...\n"
  cd "${ROOT_DIR}/rpi-rgb-led-matrix/" || exit
  make build-python PYTHON="$(which python3)"
  sudo make install-python PYTHON="$(which python3)"
  cd bindings || exit
  pip3 install -e python/
  cd "${ROOT_DIR}" || exit # Back to repo's root directory
}

main() {
  # Print welcome banner
  echo "$(tput setaf 5)___________________________________________________________________"
  echo "$(tput setaf 5)   __   _______    ______           __     _______     __          "
  echo "$(tput setaf 5)  / /  / __/ _ \  / __/ /____  ____/ /__  /_  __(_)___/ /_____ ____"
  echo "$(tput setaf 5) / /__/ _// // / _\ \/ __/ _ \/ __/  '_/   / / / / __/  '_/ -_) __/"
  echo "$(tput setaf 5)/____/___/____/ /___/\__/\___/\__/_/\_\   /_/ /_/\__/_/\_\\__/_/   "
  echo "$(tput setaf 5)___________________________________________________________________"

  # Update Raspberry Pi & Install Python 3
  echo -e "$(tput setaf 7)\nUpdating system & installing Python 3"
  sudo apt-get update && sudo apt install python3 idle3

  installMatrixLibrary

  chmod +x update.sh
  ./update.sh

  make

  echo -e "\n$(tput setaf 2)If there are no errors shown above, installation was successful."
  echo "$(tput setaf 7)To make sure your matrix is working properly, execute the samples located in ./rpi-rgb-led-matrix/bindings/python/samples"

  exit
}

# Execute script
main