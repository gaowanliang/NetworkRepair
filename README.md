这个是一个修复网络的小工具，可以让你轻松的浏览P站（是哪个P站呢？？？）

核心代码来自：https://github.com/bypass-GFW-SNI/main

可能会出现的问题
1.网站提示 xxxx.xxxx.xxxx accessed with http
需要使用https登录网站，比如baidu就是https://www.baidu.com ，其他网站自行举一反三

2.网站提示 建立安全连接失败 
你证书安装了吗，如果在运行过程中没有出现一个让你安装一个证书的提示框，请自行打开 ca 文件夹，双击 ca.crt 点击 安装证书 。如果已经安装了，但是还是连不上，重启一下试试。

3.有一些本来能上的网站上不去了/关闭软件之后有一些本来能上的网站上不去了
因为某些原因，如果出现这个情况需要你改回hosts，请将data文件夹里的host.bak改名为hosts，替换C:/WINDOWS/system32/drivers/etc/里的hosts，并在命令提示符里输入ipconfig /flushdns,回车即可恢复正常。如果是关闭软件之后有一些本来能上的网站上不去了，下一次用的时候记得把这个目录下的HOSTS.txt删除，会让你重新配置hosts

4.提示listen tcp [::1]:443: bind: An attempt was made to access a socket in a way forbidden by its access permissions.等类似内容

这是端口被占用了，需要自行百度解决，比如上面的报错就是443端口被占用，你就应该搜索“端口被占用怎么办”，找到占用443端口的进程，杀掉就行了。
