# aily-config-service
运行在Linux上的配置服务

## 拉取与配置
- 拉取服务
```shell
git clone -b py https://github.com/ailyProject/aily-config-service.git
```

- 安装环境
```shell
python3 -m venv venv
venv/bin/pip install -r requirements.pip
```

- 运行
```shell
venv/bin/python main.py
```

## 部署
### supervisor方式
- 配置`supervisor/ailyconf.conf`中的`command`字段为自己的程序启动路径
- 执行以下操作:
```shell
// 安装supervisor
sudo apt-get update
sudo apt-get install supervisor

// 复制ailyconf配置文件
sudo cp ailyconf.conf /etc/supervisor/conf.d/

sudo supervisorctl reload
...
```

### systemd方式
- 配置`systemd/ailyconf.service`中的`ExecStart`字段为自己的程序启动路径
- 执行以下操作:
```shell
sudo cp ailyconf.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable ailyconf.service
sudo systemctl start ailyconf.service
...
```