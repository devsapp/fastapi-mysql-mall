# 准备工作

## 1. 域名解析  CNAME

```plaintext
forrester-mall-bj.devsapp.net  ---> 1348378242694825.cn-beijing.fc.aliyuncs.com

forrester-mall-hz.devsapp.net  ---> 1348378242694825.cn-hangzhou.fc.aliyuncs.com
```

![img1](https://img.alicdn.com/imgextra/i2/O1CN01Ie7fVk1goc9cvYuSa_!!6000000004189-0-tps-1932-1052.jpg)

## 2. RDS 全球多活

[创建全球多活数据库实例组](https://help.aliyun.com/zh/rds/apsaradb-rds-for-mysql/create-or-delete-an-instance-group)

可能 TODO:  

1. 主角色数据库（北京）和从角色数据库（杭州），需要有IAC 脚本自动创建， 并完成 mall 数据库的创建以及账号和DB初始化

> FC 杭州可用区: "cn-hangzhou-h","cn-hangzhou-i", "cn-hangzhou-j","cn-hangzhou-k","cn-hangzhou-f","cn-hangzhou-g","cn-hangzhou-b"
>
> FC 北京可用区: "cn-beijing-i", "cn-beijing-h", "cn-beijing-k", "cn-beijing-j", "cn-beijing-l","cn-beijing-c",
 "cn-beijing-e", "cn-beijing-g","cn-beijing-f"

2. 白屏化操作， 完成全球多活数据库， DTS 自动创建初始化， 耗时较长，目前没有自动化能力，处于公测阶段

目前已经搭建好一个环境， 和全息账号那边的同学做了一个后台处理，数据库、kafka 等资源保持90天，先不做自动清理操作

![](https://img.alicdn.com/imgextra/i2/O1CN01R63q5z1aQtxB7jrtU_!!6000000003325-0-tps-2964-1462.jpg)

全息账号，目前在北京和杭州已经都完成了多 partion 配置以及最大实例数目的配置

- 杭州 RDS: vpc-bp1eb1yli5k3by36oytc0  vsw-bp1116atok15zp2n0bfo1  K 可用区,  4091 个IP 地址

- 北京 RDS: vpc-2zec8s2r1v1n3pphboy58  vsw-2zem23hhmc6fp65n4ncpr  L 可用区,  4096 个IP 地址

## 3. iDaas 账号准备

1. 登录 [iDaas 控制台](https://yundun.console.aliyun.com/?spm=5176.b65080072.console-base_product-drawer-right.didaas.68ff1b4cfw2DaS&p=idaas#/overview/new/cn-hangzhou)，选择`北京` region，选择 「CIAM 用户身份登录」，进入实例 `idaas_ciam_public_cn_-ux1457g9y01`

2. 点击左侧「账户管理」，新建两个不同的账号，必填项如图所示

> 注意：每个手机号只能注册一个，如果手机号已经注册过，则无法注册，需要换一个手机号

![](https://img.alicdn.com/imgextra/i1/O1CN01vREuR81nOh3KQje38_!!6000000005080-0-tps-1011-642.jpg)

![](https://img.alicdn.com/imgextra/i3/O1CN01xL1oFK1SvZYOV4O29_!!6000000002309-0-tps-1007-1063.jpg)

![](https://img.alicdn.com/imgextra/i2/O1CN01ObLKJP1JOkcz33pea_!!6000000001019-0-tps-592-355.jpg)

3. 点击左侧「组管理」，点击 修改 -> 成员(账户) -> 添加成员，将两个账户分别加入 user 和 manager 的账号组 (已经给 user 账号组分配了 mall 的权限，给 manager 账号组分配了 mall 和管理库存的权限)

## 4. 支付宝账号绑定

1. 给自己的支付宝账号设置一个昵称(Nickname)和头像，会显示在应用的个人信息中

![](https://img.alicdn.com/imgextra/i4/O1CN01xflhRL1mxfgVs6uKe_!!6000000005021-0-tps-539-472.jpg)

2. 访问应用函数的域名（http://forrester-mall.devsapp.net），进入应用登录界面，选择支付宝登录，扫完码之后再次自动跳转回登录界面，在选择账号密码登录或者手机号登录，登录成功后，完成支付宝对账号的绑定

> 注意：由于支付宝域名下会有 Cookie 的产生，涉及到跨域的问题，无法清除支付宝域名下的 Cookie，需要访问支付宝开放平台（https://auth.alipay.com/login/index.htm），打开开发者模式清一下 Cookies，下次登录的时候才能看到支付宝扫码界面（TODO: 待解决）

## 5. 支付宝沙箱环境准备

1. 用 Android 手机扫码下载支付宝沙箱环境

![](https://img.alicdn.com/imgextra/i3/O1CN01KeYgJf1DlkpOQ5jMO_!!6000000000257-0-tps-696-698.jpg)

2. 登录沙箱环境支付宝账号（买家账号，最后扫码支付的账号）

- 账号：wmyfgt0347@sandbox.com
- 密码：111111
- 支付密码：111111

![](https://img.alicdn.com/imgextra/i3/O1CN01eJJsHm24rrkRa6I0o_!!6000000007445-0-tps-1044-887.jpg)

# 本地开发

## 代码工程规范
1. python fastapi 框架开发
2. 安装 `pip install black`
3. 每次提交代码在根目录执行 `black ./` 完成代码风格统一格式化
4. `pip install -r requirements.txt` 完成依赖安装

## 本地运行

1. 开发数据库，如下图这个杭州实例， database 为 mall， 数据库信息配置见 .env 文件
![img2](https://img.alicdn.com/imgextra/i4/O1CN01XQOqCZ1DxCj4Du7kj_!!6000000000282-0-tps-3282-858.jpg)
公网加了白名单， 如果连接不上，比如在家办公， 可以临时把家里公网出口添加到数据库的 IP 白名单中， 不要设置 0.0.0.0/0, 会被安全找上来

2. 进入 mall 目录，执行 `uvicorn authorization:app  --host 0.0.0.0 --port 80  --reload` 进入开发热更模式

3. 进入 `http://127.0.0.1/docs#/`  进入 API 详情和调试模式

# 场景

![](https://img.alicdn.com/imgextra/i1/O1CN01vE3Ovf1qefiZwpP1w_!!6000000005521-0-tps-2146-1160.jpg)

## 场景1

1. [forrester-mall-bj](http://forrester-mall-bj.devsapp.net/docs)
2. [forrester-mall-hz](http://forrester-mall-hz.devsapp.net/docs)
3. [forrester-mall](http://forrester-mall.devsapp.net/docs)

`forrester-mall-bj.devsapp.net ---> 北京的函数`
`forrester-mall-hz.devsapp.net ---> 杭州的函数`

而对于 `forrester-mall.devsapp.net`,如果用户位于华北的话，则直接访问北京的函数， 如果用户位于华东的话，则直接访问杭州的函数

![img3](https://img.alicdn.com/imgextra/i2/O1CN01dCpFrv1ZiTX9sLlsc_!!6000000003228-0-tps-2368-1110.jpg)

![img4](https://img.alicdn.com/imgextra/i4/O1CN01tME7u61Vlu2LW7rqd_!!6000000002694-0-tps-1742-800.jpg)

展示查询:

- 查询指定 id 商品

    ![img5](https://img.alicdn.com/imgextra/i2/O1CN01ODhxHY1bHZV7C5TJ7_!!6000000003440-2-tps-2136-1806.png)

- 有过滤条件的查询

    ![img6](https://img.alicdn.com/imgextra/i3/O1CN01zkUBOQ1PcO74FxB8G_!!6000000001861-2-tps-2440-1798.png)

## 场景2

### 2.1. 事件触发【北京的 kafka】

![img7](https://img.alicdn.com/imgextra/i2/O1CN01HMkEe01q6mPB39hBg_!!6000000005447-0-tps-2756-1792.jpg
)

```json
{
  "product_id": 10,
  "delta": 1
}
```

通过 kafka 控制台和 fc 控制台日志查询：

消息发送时间: 18:38:53， 函数消费完毕时间 18:38:54

### 2.2. 全球库存最终一致性展示

比如测试 id 为 10 的库存变化

1. 使用 hz 和 bj 域名, 查询这个商品的库存
2. 使用 hz 域名， 执行某个商品库存 -1 操作
3. 使用 bj 域名， 查询这个商品的库存，看到库存也 -1 了

![img8](https://img.alicdn.com/imgextra/i3/O1CN016xuQVH26nrVwW5jsw_!!6000000007707-2-tps-2762-1402.png)

## 场景3

### 身份认证 和 role-based access 展示

1. 访问应用域名（http://forrester-mall.devsapp.net），有两种身份登录，第一次选择 manager，选择支付宝扫码登录

> 因为 user 的购买链路较长，所以建议第一次登录 manager

2. 演示完成之后，点击右上角 `logout`（一定要 logout，下次才能换身份登录），会返回应用的登录界面，再次选择 manager 身份登录，输入 user 的账号和密码（不要用支付宝扫码登录了），会提示账号密码错误，证明 user 没有访问库存管理界面的权限

3. 再次返回登录页面，选择 user 身份登录，输入账号和密码，登录成功，进入商城页面

> 这里可以说明一下，我们有 user 和 manager 两个角色组，可以直接给角色组分配不同应用的权限，角色组下的用户都拥有相同的权限

### PII 展示 & PCI 支付 & 风控

1. PII 展示：以 user 的权限登录之后，点击右上角用户头像，可以看到用户的身份信息，包含用户名，手机号，邮箱，身份证号，绑定的支付宝账号信息，可以看到手机号，邮箱，身份证号的中间几位是加密的（TODO：手机号和邮箱还没加密，待修复）

> 可以说明下，阿里云的身份认证产品 iDaas 和支付宝都可以管理和维护用户的 PII 数据

> PII（个人身份信息）合规：

> 支付宝:
> 1. 数据加密：使用强加密算法保护用户数据。对于用户的个人信息以及交易记录，支付宝都会对用户数据的一切敏感信息进行加密，以保护用户隐私。
> 2. 访问控制：实施严格的访问控制措施。
> 3. 数据最小化：仅收集必要的个人信息，例如手机号，身份证号等实名认真信息
> 4. 用户同意：获取用户明确同意后才收集和使用数据。demo 集成了支付宝，用户在绑定支付宝的时候，需要有一个授权流程（这个过程已经走完了，因此没办法展示，需要提一下）
> 5. 匿名化和去标识化：对不必要的身份信息进行处理。

> iDaas:
> 1. 多因素认证：提供多种身份验证方式。demo 集成了iDaas CIAM，采用 SSO 单点登录方式，例如手机验证码登录 或 用户名密码登录 方式，同时也支持第三方授权登录，例如支付宝授权登录
> 2. 数据加密：传输和存储过程中进行加密。用户注册信息的时候需要绑定手机号，邮箱和身份证号，此应用集成 iDaas，对用户信息做了加密处理
> 3. 访问控制：基于角色的访问控制（RBAC）。例如在 demo 中，有 user 和 manager 两种角色，注册的用户属于这两种角色中的某一种，给 user 和 manager 分配了不同的权限，例如 manager 可以访问库存管理界面和商城界面，但 user 只能访问商城界面，这两个角色中的用户分别和角色的权限保持一致
> 4. 审计日志：记录所有访问和操作行为。在 iDaas 平台上，可以看到每一个身份的访问和操作行为，可以展示一下（在 iDaas 控制台，左侧栏「审计」->「操作日志」）

2. PCI 支付：选择商城的一个商品购买，进入购买页面，点击 `pay` 之后会跳转到付款页面，展示支付二维码，用提前下载好的支付宝沙箱环境 APP 扫码支付，界面上会展示支付状态，支付完成后会自动跳转到购买成功的页面，点击 `back to homepage` 按钮会返回到商城的主界面，可以展示一下库存减少。在支付宝沙箱 APP 上，点击 「我的」-> 「账单」，可以看到刚刚的付款记录

> 需要说明：支付宝是默认了满足 PCI DSS 标准的支付渠道，应用部署在函数计算上，接入了支付宝支付渠道，所以不需要额外任何配置，即可满足 PCI DSS 标准以及防篡改 等安全机制

> 支付宝：

> 1. 数据加密：在支付宝输入信用卡信息时，这些数据会立即被加密
> 2. 交易通知：每次进行交易后，支付宝会立即发送交易通知到手机，这是实时监控和快速响应机制的一个体现。(可以展示一下支付宝的交易记录，在「我的」-> 「账单」)
> 3. 交易限额：支付宝对日常交易和提现都设有限额，大额转账的时候要再次进行身份认证，风控的体现。（由于我们 mock 的沙箱环境，所以没办法在 demo 中展示，解释一下就行）
> 4. 安全中心：支付宝App中有专门的"安全中心"，提供各种安全设置选项，让用户能够自主管理账户安全。

### 安全审计

1. 登录 [iDaas 控制台](https://yundun.console.aliyun.com/?spm=5176.b65080072.console-base_product-drawer-right.didaas.68ff1b4cfw2DaS&p=idaas#/overview/new/cn-hangzhou)，选择`北京` region，选择 「CIAM 用户身份登录」，进入实例 `idaas_ciam_public_cn_-ux1457g9y01`

2. 点击左边「审计」-> 「操作日志」，可以看到用户日志和报表分析
## 场景4

### 压测

[https://pts.console.aliyun.com/#/scene/list](https://pts.console.aliyun.com/#/scene/list)
![](https://img.alicdn.com/imgextra/i1/O1CN01WXQ2MS1xy5p0wmUkt_!!6000000006511-2-tps-3126-1204.png)

简单压测过, 4C8G rds 面对 1000 qps 写压测问题不大， 读 10000 qps 加 1s TTL 内存 cache 压力还好。

> 提前开了多 partion, 预热了 vpc 的冷启动和 partion 数目一样的实例
> 
> 函数规格1.5C1.5G, 单实例多并发设置了 32, 数据库连接池配置:  pool_size=10, max_overflow=20
> 
> 最大按量实例不到 60, 体验我们成本优越性， 就是有个问题， 不知道他们之前比较看重快速拉起 1000 个实例这种，我们需要另外构造 case， 比如使用 0.1C128M go runtime 单实例单并发（延迟100ms 以内）的函数（冷启动需要够快）

读测试: TPS 直接拉到 1W:

![img9](https://img.alicdn.com/imgextra/i4/O1CN01cvhr5J25KGIkdEw0t_!!6000000007507-0-tps-2692-1256.jpg)

写测试: TPS 直接拉到 1K:

![img10](https://img.alicdn.com/imgextra/i2/O1CN018wQnnN1aVTulMfBiA_!!6000000003335-0-tps-2704-1288.jpg)

### 推荐算法

**[详情](./rec/readme.md)**

```shell
curl -H "Content-Type: application/json" -d '{"user_id":1}' https://forrestecommend-wjrdknhghs.cn-hangzhou.fcapp.run
```

- dev url: https://forrestmend-dev-evaabrgxnp.cn-hangzhou.fcapp.run
- hz_url: https://forrestecommend-wjrdknhghs.cn-hangzhou.fcapp.run
- bj_url: https://forrestecommend-wjrdknhghs.cn-beijing.fcapp.run

**[基于 RAG 的 AI 对话导购](./ai_shopping_guide/readme.md)**

基于 CAP 模版部署 [https://cap.console.aliyun.com/template-detail?template=cap-rag-deepseekr1](https://cap.console.aliyun.com/template-detail?template=cap-rag-deepseekr1)

> [cap-rag-deepseekr1 社区地址](https://registry.serverless-devs.com/details/cap-rag-deepseekr1?type=Project)

大约 3-4 min 完成部署， DASHSCOPE API_KEY:  `sk-40bf3ce276d24a2ca3897d1fe4d2f104`

![](https://gw.alicdn.com/imgextra/i3/O1CN01y3cZaZ1pc5s5q6doN_!!6000000005380-2-tps-3278-1080.png)

使用这个 [products.csv](./test-data/product/products.csv) 上传到结构化数据，创建表
![](https://img.alicdn.com/imgextra/i2/O1CN01IjIKnN1Yv0lOZnCts_!!6000000003120-2-tps-3222-976.png)

基于上面的表，创建一个知识库
![](https://img.alicdn.com/imgextra/i2/O1CN01ZHML5r1mbEHC5GfHB_!!6000000004972-2-tps-3228-796.png)

> 注意，创建知识库是需要一点时间的， 回答 chat 页面， 可以多刷新几次，知道能下拉出新建的知识库

问这个: `Please introduce this phone to me: Stay Smart Phone.`

对应这个表的 190 这个商品: [products.csv](./test-data/product/products.csv#L191)

![](https://img.alicdn.com/imgextra/i4/O1CN01sv3Puk1TjUizdeAi3_!!6000000002418-0-tps-2870-1482.jpg)


## 场景 5

在登录 forrester 账号的基础上，打开这个仪表盘

[Real-time_Inventory_Information_Dashboard](https://dms.aliyun.com/#shared=88f29ea1-73d6-48ac-96aa-da933f070447)

![](https://img.alicdn.com/imgextra/i2/O1CN01HZ4dHR1r7z475dSqJ_!!6000000005585-2-tps-3420-1778.png)

会有一个函数定时持续对[ADB](https://ads.console.aliyun.com/adb/cn-hangzhou/instances/v5/amv-bp18ej01gjd6wi80/basic) 对应的 1000 个商品数据持续随机进行库存进行改动。
