# TODO:
source /pah/to/your/virtualenv/bin/activate
#/home/guest0/program_self_guest/LLM/UUproject/scrip/VisProcess.sh
## print a  long linr
echo "=====================================================================================================" >>  path/to/manage.log
date >> path/to/manage.log
python SQLtest.py >> path/to/manage.log
nohup python  /path/to/demo.py 600 50  2 > /dev/null 2>&1 &


watch -n 1 ./VisLog.sh 5
