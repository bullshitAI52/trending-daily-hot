# 热点信息聚合推送工具

一个多平台热点信息聚合工具，自动抓取各大平台热点内容并推送到微信。

## 功能特性

- **多平台支持**: 微博、抖音、小红书、Twitter、百度、知乎、B站、快手、西瓜视频、Linux.do、52破解、YouTube、雪球、Reddit、StackOverflow
- **智能推送**: 早晚定时推送热点报告
- **微信友好**: 生成适合微信公众号的HTML格式
- **灵活配置**: 可自由开启/关闭各平台，配置推送服务

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置环境变量
```bash
# 复制配置文件模板
cp .env.example .env

# 编辑 .env 文件，填写你的配置
# 需要配置推送服务token和平台cookie
```

### 3. 配置推送服务（三选一）

#### 微信测试号 (推荐，直接推送)
1. 访问 [微信测试号平台](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login)
2. 微信扫码登录
3. 获取以下信息填入 `.env` 文件：
   - `appID` → `WECHAT_APPID`
   - `appsecret` → `WECHAT_APPSECRET`
4. 在"模板消息接口"添加模板，获取模板ID填入 `WECHAT_TEMPLATE_ID`
5. 在"体验者列表"添加自己，获取openid填入 `WECHAT_USER_OPENID`

**推荐模板内容：**
```
{{first.DATA}}
时间：{{keyword1.DATA}}
平台数量：{{keyword2.DATA}}
热点摘要：{{keyword3.DATA}}
{{remark.DATA}}
```

#### PushPlus (第三方服务)
1. 访问 [http://www.pushplus.plus/](http://www.pushplus.plus/)
2. 微信扫码登录
3. 获取token并填入 `.env` 文件的 `PUSHPLUS_TOKEN`

#### ServerChan (第三方服务)
1. 访问 [https://sct.ftqq.com/](https://sct.ftqq.com/)
2. 微信扫码登录
3. 获取key并填入 `.env` 文件的 `SERVERCHAN_KEY`

### 4. 配置平台Cookie（可选）
对于需要登录的平台（小红书、知乎、快手等）：
1. 登录网页版平台
2. 按F12打开开发者工具
3. 进入Network标签页
4. 刷新页面
5. 找到任意请求，复制Request Headers中的`Cookie`值
6. 填入 `.env` 文件对应配置项

### 5. 运行程序
```bash
# 单次运行
python main.py

# 定时运行（使用cron）- 一天四次推送
# 早上7:00推送 (昨日热点回顾)
0 7 * * * cd /path/to/cadname && source venv/bin/activate && python3 main.py

# 中午12:00推送 (上午热点速递)
0 12 * * * cd /path/to/cadname && source venv/bin/activate && python3 main.py

# 傍晚17:00推送 (下午热点更新)
0 17 * * * cd /path/to/cadname && source venv/bin/activate && python3 main.py

# 晚上22:00推送 (全天热点盘点)
0 22 * * * cd /path/to/cadname && source venv/bin/activate && python3 main.py
```

## 配置文件说明

### config.py
- `ENABLE_*`: 平台开关，设为`False`可禁用该平台
- `USER_AGENT`: 请求头配置

### 平台开关说明
默认开启所有平台，如需禁用：
```python
# 在config.py中修改
ENABLE_TWITTER = False  # 禁用Twitter
ENABLE_YOUTUBE = False  # 禁用YouTube
```

## Docker部署

### 构建镜像
```bash
docker build -t hotspot-aggregator .
```

### 运行容器
```bash
docker run -d \
  --name hotspot \
  --env-file .env \
  hotspot-aggregator
```

### 定时运行
```bash
# 使用cron定时执行
docker exec hotspot python main.py
```

## 注意事项

1. **合规使用**: 请遵守各平台的使用条款，合理设置请求频率
2. **Cookie安全**: 不要将cookie提交到公开仓库
3. **请求限制**: 部分平台有反爬机制，建议合理配置请求间隔
4. **错误处理**: 程序包含错误处理和模拟数据回退机制

## 故障排除

### 推送失败
- **微信测试号**: 检查appid/appsecret是否正确，模板ID是否匹配，openid是否正确
- **PushPlus**: 检查token是否正确
- **ServerChan**: 检查key是否正确
- 确认网络连接正常
- 查看程序输出日志

### 微信测试号特定问题
- **模板不匹配**: 确保模板内容与代码中的字段名一致（first, keyword1, keyword2, keyword3, remark）
- **openid错误**: 在测试号平台"体验者列表"中确认openid
- **token过期**: 微信access_token每2小时过期，程序会自动获取新的

### 数据抓取失败
- 检查网络连接
- 确认cookie是否过期（需要重新获取）
- 查看平台是否有反爬限制

### SSL证书错误
- 确保系统时间正确
- 更新certifi证书包：`pip install --upgrade certifi`

## 项目结构
```
cadname/
├── main.py          # 主程序
├── scraper.py       # 数据抓取模块
├── notifier.py      # 消息推送模块
├── config.py        # 配置文件
├── requirements.txt # 依赖列表
├── Dockerfile       # Docker配置
├── .env.example     # 环境变量模板
└── README.md        # 说明文档
```

## 许可证
MIT License