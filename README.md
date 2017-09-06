# BrowserStack CLI

A CLI wrapper for the BrowserStack API, written in Python.

It is inspired by [dbrans/browserstack-cli](https://github.com/dbrans/browserstack-cli), which has not been updated in awhile, and is dependent on other libraries which are also outdated. This project has no dependancies besides Python.  

At the moment there are only a few actions, which were the ones I needed at the creation of this project. I will continue to add more over time and welcome PRs for more usability. 

It works with Python 3. 

## Install

```
git clone https://github.com/jsakas/browserstack-cli
cd browserstack-cli
pip3 install .
```

## Authentication

Requests must be signed with a username and password. These are stored in environment variabes:

```
export BROWSERSTACK_API_USERNAME=<username>
export BROWSERSTACK_API_KEY=<key>
```


## Usage

```
usage: browserstack [-h] [-o OS] [-ov OS_VERSION] [-b BROWSER]
                    [-bv BROWSER_VERSION] [-d DEVICE] [-u URL] [-t TIMEOUT]
                    [-p PID] [-a]
                    action

A CLI wrapper for the BrowserStack API

positional arguments:
  action                Which action should be taken? 
                        
                        Available commands:
                        
                        launch
                        kill
                        worker
                        browsers

optional arguments:
  -h, --help            Show this menu and quit
                                              
  -o OS, --os OS        Operating system
                                              
  -ov OS_VERSION, --os_version OS_VERSION
                        Operating system version
                                              
  -b BROWSER, --browser BROWSER
                        Browser
                                              
  -bv BROWSER_VERSION, --browser_version BROWSER_VERSION
                        Browser version
                                              
  -d DEVICE, --device DEVICE
                        Device name
                                              
  -u URL, --url URL     URL to request once browser is launched
                                              
  -t TIMEOUT, --timeout TIMEOUT
                        Timeout
                                              
  -p PID, --pid PID     Process or worker id
                                              
  -a, --attach          If given, the program will wait after launching a browser before 
                        exiting the program. This is useful when working with test runners 
                        such as Testem.
                        
```
