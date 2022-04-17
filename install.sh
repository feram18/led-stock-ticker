#!/usr/bin/bash
# Description: Install LED-Stock-Ticker (github.com/feram18/led-stock-ticker)

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

function installMatrixLibrary() {
  printf "\nInstalling rpi-rgb-led-matrix library...\n"
  cd "${ROOT_DIR}/rpi-rgb-led-matrix/" || exit
  make build-python PYTHON="$(command -v python3)"
  sudo make install-python PYTHON="$(command -v python3)"
  cd "${ROOT_DIR}" || exit
}

function main() {
  echo "$(tput setaf 5)___________________________________________________________________"
  echo "$(tput setaf 5)   __   _______    ______           __     _______     __          "
  echo "$(tput setaf 5)  / /  / __/ _ \  / __/ /____  ____/ /__  /_  __(_)___/ /_____ ____"
  echo "$(tput setaf 5) / /__/ _// // / _\ \/ __/ _ \/ __/  '_/   / / / / __/  '_/ -_) __/"
  echo "$(tput setaf 5)/____/___/____/ /___/\__/\___/\__/_/\_\   /_/ /_/\__/_/\_\\__/_/   "
  echo "$(tput setaf 5)___________________________________________________________________"

  echo -e "$(tput setaf 7)\nUpdating system & installing Python 3"
  sudo apt-get update && sudo apt install python3-dev

  installMatrixLibrary

  chmod +x update.sh
  ./update.sh

  echo -e "\n$(tput setaf 2)If there are no errors shown above, installation was successful."
  echo "$(tput setaf 7)To make sure your matrix is working properly, execute the samples located in ./rpi-rgb-led-matrix/bindings/python/samples"

  exit
}

main