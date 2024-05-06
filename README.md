# meican-testing

# Introduction

We need to integrate Selenium automation testing into the SDX-Meican project to enhance its UI-level testing capabilities and ensure robustness in our software releases.

# Objective:

The primary goal of this task is to establish a Selenium-based automation framework tailored specifically for SDX-Meican. This framework will allow us to automate the testing of critical functionalities at the UI level, improve test coverage, and streamline our testing processes.

# Scope:

**Framework Setup**: Set up a Selenium automation framework compatible with the SDX-Meican project environment.<br>
**Test Script Development**: Develop test scripts to cover key features and user workflows of SDX-Meican.<br>
**Integration with CI/CD**: Integrate the automation tests with our continuous integration and continuous deployment pipelines to ensure tests run automatically with each build.<br>
**Reporting and Monitoring**: Implement comprehensive reporting and monitoring mechanisms to track test results and identify issues efficiently.<br>
**Maintenance and Scalability**: Ensure the automation framework is easily maintainable and scalable to accommodate future changes and additions to the SDX-Meican application.<br><br>
**Expected Deliverables**:

Fully functional Selenium automation framework integrated into the SDX-Meican project.
Test scripts covering essential functionalities and user scenarios.
Integration with CI/CD pipelines for automated testing.
Documentation detailing setup instructions, usage guidelines, and maintenance procedures.

Preparing the environment:
==========================

Please make sure you're using Debian and have Meican instance up and running

lsb_release -a


``Installing Python``

``Please make sure that you're using python3.9``

sudo rm -rf /var/lib/apt/lists/*; sudo apt-get purge -y --auto-remove; sudo apt-get autoremove; sudo apt-get clean;
sudo rm -rf /etc/apt/sources.list.d/*

sudo apt update && sudo apt upgrade

sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev -y

wget https://www.python.org/ftp/python/3.9.17/Python-3.9.17.tar.xz

tar -xf Python-3.9.17.tar.xz

sudo mv Python-3.9.17 /usr/local/share/python3.9

cd /usr/local/share/python3.9

./configure --enable-optimizations --enable-shared

make

make -j 5

sudo make altinstall

sudo ldconfig /usr/local/share/python3.9

sudo ln -s /usr/local/bin/python3.9 python3.9

pip3.9 install --upgrade pip

pip3.9 install pytest

pip3.9 install selenium

sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt install ./google-chrome-stable_current_amd64.deb 
