## 启动图形界面

```bash
sudo systemctl start graphical.target
```





## 安装图形界面

| Distro          | Desktop Environment            | Metapackage                              |
| --------------- | ------------------------------ | ---------------------------------------- |
| Ubuntu          | Budgie                         | `ubuntu-budgie-desktop` (非常不推荐使用) |
| GNOME           | `ubuntu-desktop`               |                                          |
| KDE             | `kubuntu-desktop`              |                                          |
| Kylin           | `ubuntukylin-desktop`          |                                          |
| LXDE            | `lubuntu-desktop`              |                                          |
| MATE            | `ubuntu-mate-desktop`          |                                          |
| Studio          | `ubuntustudio-desktop`         |                                          |
| Unity           | `ubuntu-unity-desktop`         |                                          |
| Xfce            | `xubuntu-desktop`              |                                          |
| Ubuntu/Debian   | Cinnamon                       | `task-cinnamon-desktop`                  |
| GNOME           | `task-gnome-desktop`           |                                          |
| GNOME Flashback | `task-gnome-flashback-desktop` |                                          |
| KDE Plasma      | `task-kde-desktop`             |                                          |
| LXDE            | `task-lxde-desktop`            |                                          |
| LXQt            | `task-lxqt-desktop`            |                                          |
| MATE            | `task-mate-desktop`            |                                          |
| Xfce            | `task-xfce-desktop`            |                                          |

### 安装图形界面包

1. 选择好元包后，开始安装。例如，如果你选择 `ubuntu-desktop`，命令如下：

```bash
sudo apt install ubuntu-desktop xwayland

# 如果使用 Ubuntu，你可能想安装 snap-store。
sudo snap install snap-store
```

### 创建和修改服务

​	1.现在所有组件都已安装，我们需要修复 `/tmp/.X11-unix/` 目录，因为它默认是只读挂载的。我们将创建一个新的 systemd 单元：

```bash
sudo systemctl edit --full --force wslg-fix.service
```

​	2.在编辑器中粘贴以下代码：

```text
[Service]
Type=oneshot
ExecStart=-/usr/bin/umount /tmp/.X11-unix
ExecStart=/usr/bin/rm -rf /tmp/.X11-unix
ExecStart=/usr/bin/mkdir /tmp/.X11-unix
ExecStart=/usr/bin/chmod 1777 /tmp/.X11-unix
ExecStart=/usr/bin/ln -s /mnt/wslg/.X11-unix/X0 /tmp/.X11-unix/X0
ExecStart=/usr/bin/chmod 0777 /mnt/wslg/runtime-dir
ExecStart=/usr/bin/chmod 0666 /mnt/wslg/runtime-dir/wayland-0.lock

[Install]
WantedBy=multi-user.target
```

​	3.保存并退出编辑器。

​	4.启用 `wslg-fix.service`：

```bash
sudo systemctl enable wslg-fix.service
```

​	5.我们还需要移除所有对 Wayland 的引用，否则某些应用程序（例如 `gnome-terminal`）可能在桌面环境外打开。编辑 `user-runtime-dir@.service` 服务：

```bash
sudo systemctl edit user-runtime-dir@.service
```

​	6.在编辑器中粘贴以下代码：

```bash
[Service]
ExecStartPost=-/usr/bin/rm -f /run/user/%i/wayland-0 /run/user/%i/wayland-0.lock
```

​	7/保存并退出编辑器。

​	8.现在更改默认启动目标，否则每次启动发行版时都会出现一个 shell 窗口（例如，在 Windows 中打开发行版的终端）：

```bash
sudo systemctl set-default multi-user.target
```

### 用 XWayland 替换默认 Xorg

默认情况下，显示管理器为每个用户会话（包括登录界面）调用多个 `Xorg` 实例（如果你使用 GDM 作为显示管理器）。我们将用调用 `Xwayland` 的新脚本替换 `Xorg` 脚本。这是我们试图实现的核心魔法。

1. 首先，备份原始 `Xorg` 脚本：

```bash
sudo mv /usr/bin/Xorg /usr/bin/Xorg.original
```

​	2.创建新的 `Xorg` 脚本：

```bash
sudo nano /usr/bin/Xorg.Xwayland
```

​	3,在编辑器中粘贴以下代码：

```bash
#!/bin/bash
for arg do
  shift
  case $arg in
    # Xwayland 不支持 vtxx 参数，因此转换为 ttyxx
    vt*)
      set -- "$@" "${arg//vt/tty}"
      ;;
    # Xwayland 完全不支持 -keeptty
    -keeptty)
      ;;
    # Xwayland 完全不支持 -novtswitch
    -novtswitch)
      ;;
    # 其他参数保持不变
    *)
      set -- "$@" "$arg"
      ;;
  esac
done

# 检查运行时目录是否存在，如果不存在则创建
if [ ! -d $HOME/runtime-dir ]
then
 mkdir $HOME/runtime-dir
 ln -s /mnt/wslg/runtime-dir/wayland-0 /mnt/wslg/runtime-dir/wayland-0.lock $HOME/runtime-dir/
fi

# 将 XDG_RUNTIME_DIR 变量指向 $HOME/runtime-dir
export XDG_RUNTIME_DIR=$HOME/runtime-dir

# 查找可用的显示编号
for displayNumber in $(seq 1 100)
do
  [ ! -e /tmp/.X11-unix/X$displayNumber ] && break
done

# 在这里可以更改或添加选项以适应你的需求
command=("/usr/bin/Xwayland" ":${displayNumber}" "-geometry" "1920x1080" "-fullscreen" "$@")

systemd-cat -t /usr/bin/Xorg echo "Starting Xwayland:" "${command[@]}"

exec "${command[@]}"
```

4. 保存并退出编辑器。
5. 设置文件的正确权限并创建链接：

```bash
sudo chmod 0755 /usr/bin/Xorg.Xwayland
sudo ln -sf Xorg.Xwayland /usr/bin/Xorg
```

### 配置 GDM 和 GNOME 的显示器分辨率

目前，Xwayland 的分辨率是一个烦人的问题。即使使用了 `-geometry` 开关，GDM 和 GNOME 也不会遵循它。幸运的是，可以通过创建 `monitors.xml` 文件来覆盖此设置。

1. 首先，在当前用户目录下创建文件：

```bash
mkdir ~/.config
nano ~/.config/monitors.xml
```

​	2.在编辑器中粘贴以下代码（这里配置为 2560X1440 分辨率，如有需要请更改）：

```xml
<monitors version="2">
  <configuration>
    <logicalmonitor>
      <x>0</x>
      <y>0</y>
      <scale>1</scale>
      <primary>yes</primary>
      <monitor>
        <monitorspec>
          <connector>XWAYLAND0</connector>
          <vendor>unknown</vendor>
          <product>unknown</product>
          <serial>unknown</serial>
        </monitorspec>
        <mode>
          <width>2560</width>
          <height>1440</height>
          <rate>59.963</rate>
        </mode>
      </monitor>
    </logicalmonitor>
  </configuration>
</monitors>
```

​	3.保存并退出编辑器。

​	4.将此文件复制到 GDM 的主目录：

```bash
sudo mkdir /var/lib/gdm3/.config
sudo cp ~/.config/monitors.xml /var/lib/gdm3/.config/
```

 	5.设置 GDM 用户的 monitors.xml 的正确权限：

```bash
sudo chown -R gdm:gdm /var/lib/gdm3/.config/
```

​	6.使用 `wsl.exe --shutdown` 重启 WSL，然后重新打开发行版终端.

