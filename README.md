# uiXautomation

### Overview
Extensible Test Automation Framework

### Architecture Diagram
![PyXTaf Diagram](diagram.png?raw=true "PyXTaf Architecture Diagram")

#### Plugins:
* WEB - Based on _**[Selenium WebDriver](http://www.seleniumhq.org/projects/webdriver/)**_  
[//]: # (* Mobile - Based on _**[appium](http://github.com/appium/appium)**_)
* CLI - Based on _**[paramiko](https://github.com/paramiko/paramiko)**_
* REST - Based on _**[requests](https://github.com/requests/requests)**_

#### Dependencies:
* paramiko (1.16.0+)
* PyYAML (3.11+)
* requests (2.9.1+)
* Selenium (2.48.0+)

#### Build
PyBuilder (pyb) is used to build wheel file in the project
```bash
# install pybuilder
pip install pybuilder

# build wheel file without executing tests
pyb -v -o clean publish
```

#### Build & Run Tests in Container
We are coming up with a solution of leveraging Docker container to run tests while building wheel file

```bash
# start services, run tests and build wheel file
docker-compose run --rm pyXTaf build#
```

#### License:
* Apache License V2.0

#### Others:
Please help support this project with a donation:

[![paypal donate][paypal-image]][paypal-url]

[paypal-image]: https://www.paypal.com/en_US/i/btn/btn_donateCC_LG.gif
[paypal-url]: https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=pengwei_v@hotmail.com&currency_code=USD&item_name=uiXautomation&return=https://github.com/wesleypeng