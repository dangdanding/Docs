### 前言

在中小规模团队中，经常会在多台Linux服务器上编写和调试代码，涉及到在众多服务器上设立账户，团队成员的权限和密码同步管理也很繁琐，成员用户的数据同步和安全保障也很比较困难。本文为中小团队的服务器端开发使用提供了一种相对便捷的解决方案。具有如下若干优点。

- 统一的用户创建，权限和密码管理，用户密码的自主修改
- 用户 HOME 数据的漫游功能
- NAS 存储用户数据，提高安全性。



### 平台的选择

首先是平台的选择，国内的各种教程用 CentOS 居多，这方面的文档和支持也多一些，但是考虑 CentOS8 快要 EOL 了，所以放弃了 CentOS

Ubuntu 版本更新和迭代都比较顺畅，在全世界的 Linux 发行版使用统计中占比还更高。遇到问题 Google 一下或者到 Stack Overflow 上搜搜大概率能找到解决方案。遂就选择了 Ubuntu20.04 版本



### 技术路线的选择

大体的技术路线的选择是: SSSD + LDAP + AUTOFS + NFS ，我们先就逐个概念和技术做个简单的介绍，后边的章节会详细介绍配置细节。

LDAP：用来统一存储用户的密码身份权限等信息。Linux 上有 OpenLDAP，Windows 上有 AD 活动目录，均可以提供类似的功能。

SSSD：Linux 的一个守护进程，该进程用来访问多种验证服务器，如 LDAP，Kerberos 等，并提供授权。 SSSD 是介于本地用户和数据存储之间的进程，本地客户端首先连接 SSSD，再由 SSSD 联系外部资源提供者(一台远程服务器)

AUTOFS 自动挂载服务是一种 Linux 系统守护进程，当检测到用户试图访问一个尚未挂载的文件系统时，会自动挂载该文件系统。简单来说将挂载信息写入 /etc/fstab 文件中，系统在每次开机时都会自动挂载，而 AUTOFS 服务则是在用户需要使用该文件系统时才去动态挂载，从而节约了网络资源和服务器硬件资源的开销。

NFS（网络文件系统，Network File System）是一个分布式的文件系统，可以用于在局域网中共享文件。对于 Linux 服务器之间的文件共享来说，对于应用程序来说 NFS 也是透明的，性能还可以接受。

一个用户登录的流程大概是这样的，登录的请求先传达给 SSSD 守护进程， SSSD 守护进程先查询配置去 LDAP Server 上查询用户的权限和密码等信息，如果用户登录成功，因为配置了 auto create home directory选项，AUTOFS 服务会自动根据配置文件中用户对应的条目，挂载局域网中 NAS 服务器上提供的 NFS 目录。这样整个整个登录自动挂载目录的过程就完成了。

下文涉及具体的环境部署和命令执行

### LDAP Server 的搭建

首先忠告大家，千万不要去看网上搭建 LDAP 的各种文档，都是特别老和过时的，我走了很多的弯路。就跟 着Ubuntu 走，省事儿，好使。

#### OpenLDAP Server

The Lightweight Directory Access Protocol, or LDAP, is a protocol for querying and modifying a X.500-based directory service running over TCP/IP. The current LDAP version is LDAPv3, as defined in [RFC4510](http://tools.ietf.org/html/rfc4510), and the implementation used in Ubuntu is OpenLDAP.”

slapd 的安装会创建一个顶层级别的实例的最小化配置，一个管理员 DN ，同时会创建一个数据库去存储数据。

> **Note**
>
> This guide will use a database suffix of *dc=example,dc=com*.
>
> 这里有个Note，后续的dc都以example为例，但是，但是，但是，如果你不修改example，这个LDAP不能用。修改一个好玩或者好记的名字**，例如`xxxxx`,后文中的example均需要用这个名字替换。**

执行如下代码安装 slapd 和 ldap-utiils ，要输入根密码（牢记这个密码后续可能有用），有个类似图形界面的东西蹦出来，有条件的同学帮忙截个图，我没这个条件:

```shell
sudo apt install slapd ldap-utils
```

如果你想改变你的 DIT（信息树）后缀，执行下面这行语句，改变 DIT 的后缀。

```shell
sudo dpkg-reconfigure slapd
```

切换你的 DIT 后缀 to *dc=example,dc=com*, 举例说明，有个交互菜单问你 DNS domain 那么填入 `example.com`  我们可以直接配置 OpenLDAP 配置文件 `/etc/ldap/ldap.conf`:

```
BASE dc=example,dc=com
URI ldap://ldap01.example.com
TLS_CACERT /etc/ssl/certs/ca-certificates.crt
```

> **Note**
>
> Adjust for your server name and directory suffix，记得修改server那么和目录后缀

文本格式的额LDIF配置文件存放在 `/etc/ldap/slapd.d`, 但是永远不要直接改写它.

This is what the *dc=example,dc=com* DIT looks like:

```
$ ldapsearch -x -LLL -H ldap:/// -b dc=example,dc=com dn

dn: dc=example,dc=com

dn: cn=admin,dc=example,dc=com
```

验证是否安装成功用下面的命令。

```
$ ldapwhoami -x
anonymous

$ ldapwhoami -x -D cn=admin,dc=example,dc=com -W
Enter LDAP Password:
dn:cn=admin,dc=example,dc=com
```

基本的数据库已经安装成功，如有遗漏检查这个帮助文档

https://Ubuntu.com/server/docs/service-ldap



#### User and Group Management - ldapscripts

虽说可以通过LDIF文件来添加用户和组，但是我们有更便利的武器，**ldapscripts**

安装下面的包：

```
sudo apt install ldapscripts
```

接着编辑配置文件 `/etc/ldapscripts/ldapscripts.conf`:

```
SERVER=ldap://ldap01.example.com
LDAPBINOPTS="-ZZ"
BINDDN='cn=admin,dc=example,dc=com'
BINDPWDFILE="/etc/ldapscripts/ldapscripts.passwd"
SUFFIX='dc=example,dc=com'
GSUFFIX='ou=Groups'
USUFFIX='ou=People'
MSUFFIX='ou=Computers'
```


> **Note**
>
> - 调整SERVER和后缀名去适配你的目录结构。
> - 我们强制是能了START_TLS* usage here (*-ZZ* parameter),后续的章节会介绍使能 [LDAP with TLS](https://Ubuntu.com/server/docs/service-ldap-with-tls) ，SSSD要默认用到TLS。

存储 cn=admin* password in the `/etc/ldapscripts/ldapscripts.passwd` 并且保证他的属性是400

保证只有 root 用户可读。这个密码就是你安装 openLDAP 时配置的根密码，明文保存即可。

```
$ sudo chmod 400 /etc/ldapscripts/ldapscripts.passwd
```

下面是一些常用的命令:

- Create a new user: 添加一个新用户，添加之前，组必须存在

  ```
  sudo ldapaddgroup george
  sudo ldapadduser george george
  ```

  This will create a group and user with name *george* and set the user’s primary group (gid) to *george*

- Change a user’s password: 更改用户的密码

  ```
  $ sudo ldapsetpasswd george
  Changing password for user uid=george,ou=People,dc=example,dc=com
  New Password:
  Retype New Password:
  Successfully set password for user uid=george,ou=People,dc=example,dc=com
  ```

- Delete a user: 删除一个用户

  ```
  sudo ldapdeleteuser george

  > **Note**
  >
  > This won't delete the user's primary group, but will remove the user from supplementary ones.
  ```

- Add a group: 添加一个组

  ```
  sudo ldapaddgroup qa
  ```

- Delete a group: 删除一个组

  ```
  sudo ldapdeletegroup qa
  ```

- Add a user to a group: 添加一个用户到组

  ```
  sudo ldapaddusertogroup george qa
  ```

  You should now see a *memberUid* attribute for the *qa* group with a value of *george*.

- Remove a user from a group: 讲一个用户从组里删除。

  ```
  sudo ldapdeleteuserfromgroup george qa
  ```

可以编写一些脚本 sh，python 来批量的添加删除用户，重置密码等操作，很是方便，不用去记忆反人类的 LDIF 文件了。并且添加的用户可以自己通过 passwd 命令自助修改密码，无需管理员介入。当然管理员可以通过 ldapresetpasswd 直接重置密码。

#### LDAP & TLS

当与一个 OpenLDAP server 认证的时候最好采用加密会话，可以用TLS技术来实现。

这里我们的 LDAP Server 作为 CA 服务器， certtool 工具套件可以完成一系列签名的工作，为了简单起见在 OpenLDAP Server 上完成这些工作，你也可以在任意的其他 CA 上完成相应的工作

安装两个包 *gnutls-bin* and *ssl-cert* ：

```
sudo apt install gnutls-bin ssl-cert
```

创建CA服务器的私钥，

```
sudo certtool --generate-privkey --bits 4096 --outfile /etc/ssl/private/mycakey.pem
```

创建一个临时文件去定义这个 CA，`/etc/ssl/ca.info`:

```shell
cn = Example Company
ca
cert_signing_key
expiration_days = 3650
```

创建自签名 CA 证书:

```
sudo certtool --generate-self-signed \
--load-privkey /etc/ssl/private/mycakey.pem \
--template /etc/ssl/ca.info \
--outfile /usr/local/share/ca-certificates/mycacert.crt
```

执行 `update-ca-certificates` 将刚才新建的 CA 加入可信 CA 中。注意一个 CA 被加入:

```shell
$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
1 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```

这个时候也会创建一个符号链接指向真实的 CA 证书。 `/etc/ssl/certs/mycacert.pem` >>>>>>>>>>>>>>>>>in `/usr/local/share/ca-certificates`.

生成 Server 的私钥：

```
sudo certtool --generate-privkey \
--bits 2048 \
--outfile /etc/ldap/ldap01_slapd_key.pem
```

创建一个 info 文件，包含如下内容 `/etc/ssl/ldap01.info` :

```
organization = Example Company
cn = ldap01.example.com
tls_www_server
encryption_key
signing_key
expiration_days = 365
```

上面的参数可以保证这个 server 一年期内有效，可以相应的修改这个数字，并且仅仅对 **ldap01.example.com** 有效，请做相应的修改.

生成 Server 的证书:

```
sudo certtool --generate-certificate \
--load-privkey /etc/ldap/ldap01_slapd_key.pem \
--load-ca-certificate /etc/ssl/certs/mycacert.pem \
--load-ca-privkey /etc/ssl/private/mycakey.pem \
--template /etc/ssl/ldap01.info \
--outfile /etc/ldap/ldap01_slapd_cert.pem
```

调整合适的权限和归属:

```
sudo chgrp openldap /etc/ldap/ldap01_slapd_key.pem
sudo chmod 0640 /etc/ldap/ldap01_slapd_key.pem
```

到这一步，你的 server 就已经可以接收 TLS 配置了。

创建 `certinfo.ldif` 包含如下的内容 following contents ：

```
dn: cn=config
add: olcTLSCACertificateFile
olcTLSCACertificateFile: /etc/ssl/certs/mycacert.pem
-
add: olcTLSCertificateFile
olcTLSCertificateFile: /etc/ldap/ldap01_slapd_cert.pem
-
add: olcTLSCertificateKeyFile
olcTLSCertificateKeyFile: /etc/ldap/ldap01_slapd_key.pem
```

使用 ldapmodify 命令去告诉 slapd TLS 通过 slapd-config 数据库工作:

```
sudo ldapmodify -Y EXTERNAL -H ldapi:/// -f certinfo.ldif
```

本章参考文章，如有错误和遗漏请到下面的官方文档查阅。

https://Ubuntu.com/server/docs/service-ldap-with-tls



### SSSD 协议的配置

SSSD 可以使用 LDAP 协议做认证，用户，组信息的查询。

使能 SSSD 协议的前提和假定是：

- 一个已经搭建好的 OpenLDAP 服务器，并且使能了 SSL。

- 一个客户端服务器，安装了必须的软件和私有 LDAP Server 上的用户信息，进行用户的认证和登录。

安装如下软件包

```
sudo apt install sssd-ldap ldap-utils
```

#### SSSD Configuration

在如下位置创建 SSSD 配置文件 `/etc/sssd/sssd.conf` ，并且确保权限是 *0600*， 归属 *root:root*, 内容如下表:

基于上下文的内容，替换 example.com 的内容。

```
[sssd]
config_file_version = 2
domains = example.com

[domain/example.com]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://ldap01.example.com
cache_credentials = True
ldap_search_base = dc=example,dc=com
```

确保重启 *sssd* 服务，如果重启失败，大概率是配置文件属性不对。

```
sudo systemctl start sssd.service
```

#### 使能自动创建 HOME 目录

执行下列命令：

```
sudo pam-auth-update --enable mk HOME dir
```

#### 在客户端（shell服务器）检查 SSL 的配置

客户端与 LDAP 相连时必须使用 TLS :

- 客户端知晓并且信任CA服务器签署的LDAP Server证书。
- CA服务器认证了正确的主机 (`ldap01.example.com` )
- 进行TLS联接时，保证client和server的时间是同步的，一般用配置NTP服务器来保证，并且配置在相同的时区。
- CA证书和CA服务器都在有效期内（实际部署时，可以把有效期设置为3650，一般足够支持到下一次技术重构）

如果你使用自己搭建的 CA，最简单的方法是把 '.crt' 结尾的 CA 证书放到 `/usr/local/share/ca-certificates/`，

然后执行 `sudo update-ca-certificates`

同时，编辑 ldap 配置文件，TLS 证书指向正确的位置: `/etc/ldap/ldap.conf`
`TLS_CACERT` to the CA public key file. 配置文件大概如下所示

```
#
# LDAP Defaults
#

BASE   dc=xxxxx,dc=com
URI ldap://ldap01.xxxxx.com

TLS_CACERT  /usr/local/share/ca-certificates/mycacert.crt
```

> **Note**
>
> 做完所有操作后，重启sssd服务: `sudo systemctl restart sssd`

所有的都完成后，运行如下命令检查客户端到 LDAP 服务器的 SSL 联接是否成功：

```
$ ldapwhoami -x -ZZ -h ldap01.example.com
anonymous
```

#### 配置HOSTS文件

因为在局域网里配置，没有 DNS 解析域名，所以要手动配置 HOST 文件

```
vi /etc/hosts
127.0.0.1  localhost
127.0.0.1  engshell01
10.208.168.168  ldap01.xxxxx.com
```

所有的都完成后，运行如下命令检查客户端到 LDAP 服务器的 SSL 联接是否成功：

```
$ ldapwhoami -x -ZZ -h ldap01.example.com
anonymous
```



### 使能 AUTOFS

安装 autofs，执行如下命令：

```
sudo apt-get install autofs
```

修改 `/etc/auto.master` 文件，添加如下内容

```
+auto.master
/ HOME  /etc/auto. HOME
```

编辑 `/etc/auto`. HOME 文件，为每个用户添加一行配置。

登录时自动创建 HOME 目录，并且自动 mount nfs 服务的一个目录

```
vi /etc/auto. HOME

xiaoming -filetype=nfs.rw 10.208.168.166:/mnt/ NAS pool/xiaoming
laowang -filetype=nfs.rw 10.208.168.166:/mnt/ NAS pool/laowang
xiaoli -filetype=nfs.rw 10.208.168.166:/mnt/ NAS pool/xiaoli
```

如果你希望提供 engshell 集群，/etc/auto. HOME 文件需要在每个server上同步，具体实现方法不在本文中赘述。

10.208.168.166为 NAS 服务器地址，并且使能了 NFS 服务



### 搭建 NAS ，提供 NFS 服务

搭建 NAS 的目的是为了给数据一个安全便于管理的家。

开源的可以使用 FreeNAS ，或者 TrueNAS ，或者其他商用的产品，这个选择基于预算来选择。没有预算也可以用虚拟机来模拟实现。

NFS 的实现不在本文中赘述，看到这里的人应该不难配置 NFS。

FreeNAS 和 TrueNAS 都支持 LDAP 客户端，可以从 LDAPServer 同步用户数据，我们新建用户的时候给创建对应的目录，并且配置对应的权限，并用NFS把上一级目录发布出去就完成了本次的部署。可以手工完成，也可以编写 bash 脚本来完成文件夹创建，权限配置的问题。

配置 idmapd 服务，使能 NFSv4 ID Mapping 功能

如果遇到文件和目录的 owner 42949697294 的问题

```
vi /etc/idmapd.conf, 添加Domain=xxxxx.com"
然后重启idmapd服务即可。
```
