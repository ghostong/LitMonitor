**1. 安装**

    1) 下载 litmonitor 源代码
    2) 源代码解压至 /opt/litmonitor 目录
    3) 指定命令: ln -s /opt/litmonitor/litmonitor /usr/bin/litmonitor

**2. 配置**

    1) 配置文件保存位置 /opt/litmonitor/litmonitor.conf
    2) 配置文件详解
        1. SSH2配置 [SSH2_CONFIG]
            SSH2_USER 系统使用的用户名 需要通过密码可以登录到[HOST_LIST]中的所有机器
        2. 数据节点配置 [DATA_SERVER]
            请保持默认配置
        3. Agent配置 [AGENT_CONFIG]
            请保持默认配置
        4. 主机列表 [HOST_LIST]
            主机名=主机IP 可自行添加要监控的机器
        5. 命令行ui配置 [CMDUI_CONFIG]
            请保持默认配置
**3. 初始化**

    1) 运行 litmonitor init 进行初始化配置
    2) 执行过程中会需要输入配置[SSH2_USER]用户的密码
    3) 请注意[SSH2_USER]是各节点都存在的一个用户,密码也是统一的密码
    
**4. 启动服务**

    litmonitor start      启动服务
    litmonitor stop       停止服务
    litmonitor restart    重启服务
    
**5.CmdUi**

    litmonitor cmdui  启动cmdui客户端