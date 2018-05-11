#!/bin/bash
#------------------------------------------------------
# Automation Builder (for Docker Compose)
#------------------------------------------------------
CYAN='\e[1;36m'
NC='\e[0m'
ARTIFACTS=artifacts

TAG_BUILD=$1
echo -e "${CYAN}Set Build Number(${TAG_BUILD})${NC}"
echo "[egg_info]" >> src/main/python/setup.cfg
echo "tag_build=${TAG_BUILD}" >> src/main/python/setup.cfg

echo -e "${CYAN}Install Dependencies${NC}"
python -m pip install enum34
python -m pip install paramiko
python -m pip install PyYAML
python -m pip install requests
#python -m pip install selenium
python -m pip install Appium-Python-Client

python -m pip install pybuilder

echo -e "${CYAN}Build uiXautomation(PyXTaf*.whl file) project & Run tests${NC}"
pyb -v clean publish

# ARGS=${@:2}
# echo -e "${CYAN}Run tests according to arguments(${ARGS})${NC}"
# python -m pip install dist/dist/PyXTaf*.whl
# python -m PyXTaf ${ARGS}

# echo -e "${CYAN}Save artifacts and run BDD tests${NC}"
mkdir -p ${ARTIFACTS}
mv build/reports/*.xml ${ARTIFACTS}/

pushd .
python -m pip install allure-behave
python -m pip install dist/dist/PyXTaf*.whl
cd ./src/test/python
python -m bpt.bdd -f allure_behave.formatter:AllureFormatter -o ../../../${ARTIFACTS}/allure -t ~@wip -D browser="chrome" -D is_remote="True"
popd

mv dist/dist/PyXTaf*.whl ${ARTIFACTS}/
chmod a+w -R ${ARTIFACTS}/
