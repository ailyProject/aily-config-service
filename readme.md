# aily-config-service
运行在Linux上的配置服务


## 环境参数配置
> 需要手动配置下aliy服务的相关信息, 复制 `.env.sample`文件为 `.env`

- AILY_PATH: aily服务所在的文件夹
- AILY_ENV_PATH: aily服务环境配置文件的位置
- AILY_SUPERVISOR_NAME: 在supervisor中配置的aily服务名

```
cp .env.sample .env
```

## 部署
### 自动部署
```
chmod +x deploy.sh
deploy.sh
```

### 手动部署
#### 拉取与配置
- 拉取服务
```shell
git clone -b py https://github.com/ailyProject/aily-config-service.git
```

- 安装环境
```shell
python3 -m venv venv
venv/bin/pip install -r requirements.pip
```

#### supervisor方式
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

#### systemd方式
- 配置`systemd/ailyconf.service`中的`ExecStart`字段为自己的程序启动路径
- 执行以下操作:
```shell
sudo cp ailyconf.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable ailyconf.service
sudo systemctl start ailyconf.service
...
```