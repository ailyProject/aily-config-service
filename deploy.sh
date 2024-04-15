#!/bin/bash

set -e

# 克隆代码库
cd ~
git clone -b py https://github.com/ailyProject/aily-config-service.git
cd aily-config-service

# 创建虚拟环境并安装依赖
python3 -m venv venv
venv/bin/pip install -r requirements.txt

# 安装 supervisor
sudo apt-get update && sudo apt-get install supervisor

# 配置 supervisor
SUPERVISOR_CONF_DIR="/etc/supervisor/conf.d"
SUPERVISOR_CONF_FILE="supervisor/ailyconf.conf"

echo "[program: ailyconf]" > $SUPERVISOR_CONF_FILE
echo "command = $HOME/aily-config-service/venv/bin/python main.py" >> $SUPERVISOR_CONF_FILE
echo "directory = $HOME/aily-config-service" >> $SUPERVISOR_CONF_FILE
echo "user = root" >> $SUPERVISOR_CONF_FILE
echo "autostart = true" >> $SUPERVISOR_CONF_FILE
echo "autorestart = true" >> $SUPERVISOR_CONF_FILE
echo "stdout_logfile = /tmp/ailyconf.log" >> $SUPERVISOR_CONF_FILE
echo "stdout_logfile_maxbytes = 1MB" >> $SUPERVISOR_CONF_FILE
echo "stderr_logfile = /tmp/ailyconf-error.log" >> $SUPERVISOR_CONF_FILE
echo "stderr_logfile_maxbytes = 1MB" >> $SUPERVISOR_CONF_FILE

sudo cp supervisor/$SUPERVISOR_CONF_FILE $SUPERVISOR_CONF_DIR
sudo supervisorctl reload

# 检查命令是否成功执行
if [ $? -eq 0 ]; then
    echo "部署成功"
else
    echo "部署失败"
fi
