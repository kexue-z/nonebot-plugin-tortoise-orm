# 通用 ORM 数据库连接插件

> 施工中。。。

- 参考 [example_bot](example_bot) 来创建一个 _聊天记录_ 插件吧~！

## `.env` 设置

参考配置：

```ini
# db_url=postgres://postgres@localhost:5432/postgres
db_url=sqlite://db.sqlite3
db_generate_schemas=false
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
db_url=mysql://myuser:mypass:pass@db.host:3306/somedb
```

跟上面的差不多

### `db_generate_schemas`

- 填入 `true` 或 `false`
- 默认 `false`
- 如为 `true` 则会在每次启动时，在空的数据库上初始化数据表
  - 请在**第一次启动**或**有新数据表**时设置为 `true` 来初始化表，随后设置为`false` 关闭该功能

## 数据库类型

- [x] postgres
- [x] sqlite
- [x] MySQL/MariaDB

其他待补充
