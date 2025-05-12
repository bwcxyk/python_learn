# Oracle 数据库批量获取 AWR 和 ASH 报告

获取 Oracle 的 AWR 和 ASH 报告，要求多节点，多份，批量，手动 sql 比较麻烦，特开通此项目做个批量化脚本实现。

## 食用方法

1. 准备好 python 环境，开发环境为 python3.8.2，要求 python3.6+。
2. 安装依赖环境 `pip install -r requirements.txt`。
3. 修改配置，将 `run_config_template.py` 模板文件按照自己的情况进行修改，并将文件名修改为 `run_config.py` 以生效。
4. 运行脚本测试是否没问题 `python oracle_get_awr_ash.py`。

## 更新日志

v1.2 20210416：

1. 优化 ASH 报告获取的部分，需要支持登录对应节点才能获取对应节点的 ASH 报告配置。
2. 优化报错文字提示，更加精准。

v1.1 20210414：

1. 补充支持同步导出 ASH 报告的部分。
2. 所有自定义函数新增类型提示。

v1.0 20201203：

1. 更新初始版本，实现 AWR 报告的批量可配置化快速获取。
