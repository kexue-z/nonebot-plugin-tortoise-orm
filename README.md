<p align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://user-images.githubusercontent.com/44545625/209862575-acdc9feb-3c76-471d-ad89-cc78927e5875.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
</p>

<div align="center">

# nonebot-plugin-tortoise-orm

_✨ 通用 ORM 数据库连接插件 ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/kexue-z/nonebot-plugin-tortoise-orm/master/LICENSE">
    <img src="https://img.shields.io/github/license/kexue-z/nonebot-plugin-tortoise-orm.svg" alt="license">
  </a>
  <a href="https://pypi.org/project/nonebot-plugin-tortoise-orm/">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-tortoise-orm" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>


- 参考 [example_bot](example_bot) 来创建一个 _聊天记录_ 插件吧~！

## 快速上手

### 新建 `models.py`

```python
from tortoise import fields
from tortoise.models import Model

# 导入插件方法
from nonebot_plugin_tortoise_orm import add_model


add_model("src.plugins.models")
# 如果以包/插件的方式，例如 nonebot_plugin_word_bank3
# add_model("nonebot_plugin_word_bank3.models")
# 或
# add_model("__name__")
class TestTable(Model):
    message_id = fields.BigIntField(pk=True)
    text = fields.TextField()


    class Meta:
        table = "test_table"
        table_description = "测试标题" # 可选
```

### 在 `__init__.py` 中加入引用

```python
from nonebot import require

require("nonebot_plugin_tortoise_orm")

# 插件存放结构
# src/plugins/__init__.py
# src/plugins/models.py

from .models import TestTable
```

### 直接使用

参考 [tortoise models](https://tortoise.github.io/models.html)

```python
# 创建
await TestTable.create(message_id=114514)
await TestTable.update_or_create(message_id=114514)
await TestTable.get_or_create(message_id=114514)

# 获取
await TestTable.get(message_id=114514)
await TestTable.get_or_none(message_id=114514)

# 更改
if record := await TestTable.get_or_none(message_id=114514):
    record.text = "1919810"
    await record.save()

# 删除
if record := await TestTable.get_or_none(message_id=114514):
    await record.delete()
    await record.save()
```

以上就是最简用法

### 多个数据库

在某些特殊情况下，可以不使用默认数据库，`add_model` 的参数即可实现

- `db_name` 自行确认
- `db_url` 地址同下数据库URL


```py
add_model(
    __name__,
    db_name="chatrecorder",
    db_url="sqlite://data/chatrecorder.db",
)
```

## `.env` 设置

参考配置：

[db-url](https://tortoise.github.io/databases.html#db-url)

```ini
# db_url=postgres://postgres@localhost:5432/postgres
db_url=sqlite://db.sqlite3
```

### `db_url`

#### 使用 `sqlite`

直接使用相对路径来建立

```ini
db_url=sqlite://db.sqlite3
```

如果时指定路径，则应该是

```ini
db_url=sqlite:///data/db.sqlite
```

使用绝对路径 注意有三个 `/`

#### 使用 `PostgreSQL`

```ini
db_url=postgres://postgres:pass@db.host:5432/somedb
```

- 说明： `postgres://` 表示协议
- `postgres:pass@` 表示登入账号和密码 如果没有密码则用 `postgres@`
- `db.host:5432` 表示数据库的地址 和 端口 如果是本机 则为 `localhost:5432`
- `/somedb` 表示数据库名

#### 使用 `MySQL/MariaDB`

```ini
db_url=mysql://myuser:mypass@db.host:3306/somedb
```

跟上面的差不多

## 数据库类型

- [x] postgres
- [x] sqlite
- [x] MySQL/MariaDB

其他待补充
