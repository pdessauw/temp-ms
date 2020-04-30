#!/usr/bin/env bash
# Install script for the project
INSTALL_DIR="/usr/local/bin/monitor"
REPO_DIR=$(realpath $(dirname ${BASH_SOURCE[0]}))

check_errors() {
  if [[ $? -ne 0 ]]
  then
    echo "An error occured with the last command. Exiting..."
    exit 1
  fi
}

echo "Installing ${REPO_DIR} to ${INSTALL_DIR}..."

# Removing install dir if it already exists
if [[ -d ${INSTALL_DIR} ]]
then
  echo "Cleaning up existing install..."
  rm -rf ${INSTALL_DIR} &> /dev/null
  check_errors
fi

# Copying the repository and cleaning up
echo "Copying the repository..."
cp -r ${REPO_DIR} ${INSTALL_DIR} &> /dev/null
check_errors
echo "Cleaning up the installation..."
rm -rf ${INSTALL_DIR}/.git* ${INSTALL_DIR}/README.md ${INSTALL_DIR}/*.sh &> /dev/null
check_errors

echo "Installation success!"
