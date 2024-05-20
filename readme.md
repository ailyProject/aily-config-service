# aily-config-service
运行在Linux上的配置服务

## 自动部署

```
git clone https://github.com/ailyProject/aily-config-service-deploy.git
cd aily-config-service-deploy
chmod +x deploy.sh
./deploy.sh
```

## 手动部署

### 环境配置
#### 安装bluez(树莓派上默认安装了)
- 安装教程：https://learn.adafruit.com/install-bluez-on-the-raspberry-pi/installation

#### 安装bluez-tools(https://github.com/khvzak/bluez-tools)
- 安装：
    ```
    sudo apt-get update && sudo apt-get install autoconf automake libtool

    git clone https://github.com/khvzak/bluez-tools
    cd bluez-tools
    ./autogen.sh
    ./configure
    make
    sudo make install
    ```
- 服务配置:
    ```
    sudo cp systemd/bluetools.service /etc/systemd/system/bluetools.service
    sudo systemctl start bluetools.service
    sudo systemctl enable bluetools.service
    ```


### 参数配置
> 需要手动配置下aliy服务的相关信息, 复制 `.env.sample`文件为 `.env`

```
cp .env.sample .env
nano .env
```

#### 参数说明
- AILY_PATH: aily服务所在的文件夹
- AILY_ENV_PATH: aily服务环境配置文件的位置
- AILY_SUPERVISOR_NAME: 在supervisor中配置的aily服务名

### 运行

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.pip
.venv/bin/python main.py
```

### 部署
> 采用supervisor方式

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
