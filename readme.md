
> 注：当前项目为 Serverless Devs 应用，由于应用中会存在需要初始化才可运行的变量（例如应用部署地区、函数名等等），所以**不推荐**直接 Clone 本仓库到本地进行部署或直接复制 s.yaml 使用，**强烈推荐**通过 `s init ${模版名称}` 的方法或应用中心进行初始化，详情可参考[部署 & 体验](#部署--体验) 。

# fastapi-mall 帮助文档

<description>

一键部署 FastAPI 仓库管理系统

</description>


## 前期准备

使用该项目，您需要有开通以下服务并拥有对应权限：

<service>



| 服务/业务 |  权限  | 相关文档 |
| --- |  --- | --- |
| 云数据库RDS |  AliyunRDSFullAccess | [帮助文档](undefined) [计费文档](undefined) |
| 函数计算 |  AliyunFCFullAccess | [帮助文档](https://help.aliyun.com/product/2508973.html) [计费文档](https://help.aliyun.com/document_detail/2512928.html) |
| 专有网络 |  AliyunFCServerlessDevsRolePolicy | [帮助文档](https://help.aliyun.com/zh/vpc) [计费文档](https://help.aliyun.com/zh/vpc/product-overview/billing) |
| 日志服务 |  AliyunFCServerlessDevsRolePolicy | [帮助文档](https://help.aliyun.com/zh/sls) [计费文档](https://help.aliyun.com/zh/sls/product-overview/billing) |

</service>

<remark>



</remark>

<disclaimers>



</disclaimers>

## 部署 & 体验

<appcenter>
   
- :fire: 通过 [云原生应用开发平台 CAP](https://devs.console.aliyun.com/applications/create?template=fastapi-mall) ，[![Deploy with Severless Devs](https://img.alicdn.com/imgextra/i1/O1CN01w5RFbX1v45s8TIXPz_!!6000000006118-55-tps-95-28.svg)](https://devs.console.aliyun.com/applications/create?template=fastapi-mall) 该应用。
   
</appcenter>
<deploy>
    
   
</deploy>

## 项目架构图

<framework id="flushContent">

![](https://img.alicdn.com/imgextra/i3/O1CN017k2Ave1juyVd8xZe8_!!6000000004609-0-tps-760-478.jpg)

</framework>

## 案例介绍

<appdetail id="flushContent">

本案例中，帮助用户一键部署基于 FastAPI 框架的电商场景中的仓库管理系统，能够操作 MySQL 数据库，实现对商品的添加、删除、商品信息的修改以及库存管理。同时支持用户对应用进行二次开发，可以构造适用于多种业务场景的集成 MySQL 数据库的 FastAPI 应用

</appdetail>

## 使用流程

<usedetail id="flushContent">

**步骤一**：点击页面左侧「立即部署」，进入项目部署页面

![](https://img.alicdn.com/imgextra/i4/O1CN01n11LRZ1EYlD4JXjNA_!!6000000000364-0-tps-1456-1248.jpg)

> 需要确认开通 专有网络VPC、函数计算 FC、日志服务 SLS、云数据库 RDS，如未开通，请先跳转相关产品控制台开通。确认开通后，点击「确认部署」
![](https://img.alicdn.com/imgextra/i4/O1CN01eI7cr51eAeMxRFe3h_!!6000000003831-0-tps-1583-553.jpg)

**步骤二**：等待部署完成后，选中页面左侧名为 `fastapi` 的服务，点击「访问地址」即可立即体验基于 FastAPI 的仓库管理系统

![](https://img.alicdn.com/imgextra/i1/O1CN016SWAnn1mt5j87vbRJ_!!6000000005011-0-tps-2276-589.jpg)

访问地址后面加上路由 `/docs` 即可查看 API 列表

![](https://img.alicdn.com/imgextra/i3/O1CN01eD3fhC23m58KDQsbR_!!6000000007297-0-tps-1670-1340.jpg)

</usedetail>

## 二次开发指南

<development id="flushContent">

**Q：如果想自行更改项目代码，应该怎么做?**

A：可以选择绑定代码仓库部署，访问绑定的代码仓库地址即可获取项目的源代码。如果希望更改前端，可以访问 `src/code/template` 目录，所有的前端代码都放在这个目录下面；如果希望更改后端代码，可在 `src/code/app.py` 中进行修改，或者在同级目录下增加后端代码文件；如果希望更改数据库配置和测试数据，需要更改 `src/code/models` 和 `src/code/testData` 目录下的代码。

**Q：怎么修改项目的依赖库?**

A：所有的项目依赖都在  `src/code/requirements.txt` 中

</development>

## 常见问题

<question id="flushContent">
</question>

## 注意事项

<matters id="flushContent">
</matters>
