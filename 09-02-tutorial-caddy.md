# Caddy:一键进入 HTTPS 时代

人人都喜欢使用 Apache/Nginx 来作为自己的 Proxy Web Server。然而，悄悄打开 wireshark，对同一个局域网下的舍友们抓抓包，找到他们的登陆密码并不是一件困难的事情——他们都忘记给自己的项目加上 [HTTPS](https://www.howtogeek.com/181767/htg-explains-what-is-https-and-why-should-i-care/) 了。

HTTPS 的重要性无需多言：在 HTTP 的时代，网络上的数据包就如同裸奔，任何有心人都可以看到你和网页交换的数据包，以明文的形式；而 HTTPS 的出现彻底终结了这个裸奔的时代，我们的数据都被服务器提供的公钥/私钥给加密了。

然而，Apache/Nginx 在默认配置中并不提供 HTTPS 支持，Web Server 用户（或者说运维们），要么劳心费神地申请一个 Cloudflare 的共享证书，要么自己“编造”（自签）一个不受浏览器认可的证书。花时间去完成这些操作，对于我们宝贵的开发开发时间来说简直就是暴殄天物。

所以，Caddy出现了。它能在 28 秒内自动完成一个 HTTPS 网页的部署，如果你可以访问 Utube 的话，你可以在[这里](https://www.youtube.com/watch?v=nk4EWHvvZtI)看到这个操作。除此之外，它还是一个 Go 语言写的 Web Server，性能强劲，安装便捷，新特性加入的速度也远超同辈。

如果你的时间宝贵，不想亲自搞到一个证书；如果你觉得你的网站用户的信息安全需要保障；如果你想尝试一个全新的 Web Server，请继续。

## 安装

Caddy 的安装是简单的，它在官方提供了一键安装脚本，你只需

```
curl https://getcaddy.com | bash -s personal
```

即可安装成功。或者，你也可以直接下载二进制文件，然后把它扔去 `$PATH`

```
wget https://caddyserver.com/download/windows/amd64?license=personal&telemetry=off
tar -xzf caddy*.tar.gz caddy
sudo mv ./caddy /usr/local/bin
```

## 使用

Caddy 的使用也是简单的，只需要一个 

```
caddy
``` 

命令，它就会在当前目录下运行一个 demo。访问 `localhost:2015`，你就能看到一个网页了。

> 如果你看到的是 404 not found，不用担心，Caddy运行的好好的，只是因为你这个运行 caddy 的目录下面没有 `index.html` 而已。

但是等等，说好的 HTTPS 呢？为什么它还是 HTTP？稍安勿躁。

## 进入 HTTPS

Caddy 获取 HTTPS 也是简单的，因为它内置了 [Let’s Encrypt](https://letsencrypt.org/) 的证书脚本。你所需要的一切只是新建一个caddy配置文件，往里面写入你的网址就好。

```
echo yourdomainname.com > Caddyfile
sudo caddy
```

在接下来的提示中输入自己的邮箱（如果是第一次使用的话），然后，caddy会出现这样的显示

```
Activating privacy features... done.
https://yourdomainname.com
http://yourdomainname.com
```

现在，一切工作已经完成了，访问 `yourdomainname.com`，这就是你的网站，这就是带有绿色 HTTPS 标志的网站。

## 一个运维的忠告

或许你还沉浸在不费吹灰之力获得了 HTTPS 的快乐之中，但是我不得不提醒你（作为一个被 Caddy 多次坑害的运维），上面简洁的操作了充满了安全隐患。

### 忘掉 sudo

一个运维是不需要 `sudo` 的。但是，我在最后一次执行 `caddy` 命令时却使用了它，这是因为 `caddy` 需要开启 `80/443` 端口的权限。`sudo` 固然简单，但是依赖它会带来永恒的梦魇。我推荐 [setcap](https://linux.die.net/man/8/setcap)，它在能为你带来一个更安全的 `sudo` 使用方法。

简而言之，

```
sudo setcap cap_net_bind_service=+ep $(which caddy)
```

然后就可以 `caddy without sudo` 了。

### 持久化服务

没有人想在半夜停电之后被老板（PM）叫起来重启 caddy 服务，我们需要一个自动重启的配置。在这里，我用 [systemd](http://www.ruanyifeng.com/blog/2016/03/systemd-tutorial-commands.html).

```
sudo curl -s https://raw.githubusercontent.com/mholt/caddy/master/dist/init/linux-systemd/caddy.service -o /etc/systemd/system/caddy.service
sudo systemctl daemon-reload
sudo systemctl enable caddy.service # 设置 caddy 服务自启动
sudo systemctl status caddy.service # 查看 caddy 状态
```

### 与 Flask 在一起

我们的项目使用的是 Flask，它并不太 ❤ Caddy，我们需要再装一个 [Unicorn](http://gunicorn.org/).

```
pip install gunicorn
gunicorn -b "127.0.0.1:8000" project.wsgi
```

然后在 Caddyfile 里面对 unicorn 的端口进行透明代理

```
yourdomainname.com {
    root /path/to/project/folder
    proxy / localhost:8000 {
        transparent
    }
}
```