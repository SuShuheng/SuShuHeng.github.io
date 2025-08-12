以下是在 Windows 的 WSL Ubuntu 终端上搭建 Anaconda 机器学习与深度学习环境的详细步骤：

---

### **步骤 1：启用 WSL 并安装 Ubuntu**
1. **启用 WSL 功能**：
   - 以管理员身份打开 PowerShell，运行：
     ```powershell
     wsl --install
     ```
   - 如果失败，手动启用：
     ```powershell
     dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
     dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
     ```
   - 重启电脑。

2. **安装 Ubuntu**：
   - 打开 Microsoft Store，搜索并安装 **Ubuntu**（推荐 24.04 LTS）。
   - 首次启动时会要求设置用户名和密码。

---

### **步骤 2：更新系统和安装依赖**
1. **更新包列表和升级软件**：
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **安装必要工具**：
   ```bash
   sudo apt install -y wget curl git unzip
   ```

---

### **步骤 3：安装 Anaconda**
1. **下载安装脚本**：
   ```bash
   wget https://repo.anaconda.com/archive/Anaconda3-2025.05-1-Linux-x86_64.sh
   ```
   （替换为[官网](https://www.anaconda.com/download)最新链接）

2. **运行安装脚本**：
   ```bash
   bash Anaconda3-*-Linux-x86_64.sh
   ```
   - 按回车阅读协议，输入 `yes` 同意。
   - 确认安装路径（默认按回车）。
   - 提示是否初始化时，选择 `yes`。

3. **激活环境变量**：
   ```bash
   source ~/.bashrc
   ```

4. **验证安装**：
   ```bash
   conda --version
   ```

---

### **步骤 4：Nvidia CUDA Toolkit**

1. **去官网寻找windows 对应的CUDA版本的CUDA Toolkit 并获取安装命令**：

   ```bash
   wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-ubuntu2404.pin
   sudo mv cuda-ubuntu2404.pin /etc/apt/preferences.d/cuda-repository-pin-600
   wget https://developer.download.nvidia.com/compute/cuda/12.9.0/local_installers/cuda-repo-ubuntu2404-12-9-local_12.9.0-575.51.03-1_amd64.deb
   sudo dpkg -i cuda-repo-ubuntu2404-12-9-local_12.9.0-575.51.03-1_amd64.deb
   sudo cp /var/cuda-repo-ubuntu2404-12-9-local/cuda-*-keyring.gpg /usr/share/keyrings/
   sudo apt-get update
   sudo apt-get -y install cuda-toolkit-12-9
   ```

2. **安装cuDNN**：

   ```bash
   wget https://developer.download.nvidia.com/compute/cudnn/9.12.0/local_installers/cudnn-local-repo-ubuntu2404-9.12.0_1.0-1_amd64.deb
   sudo dpkg -i cudnn-local-repo-ubuntu2404-9.12.0_1.0-1_amd64.deb
   sudo cp /var/cudnn-local-repo-ubuntu2404-9.12.0/cudnn-*-keyring.gpg /usr/share/keyrings/
   sudo apt-get update
   
   # 对于 CUDA12
   sudo apt-get -y install cudnn9-cuda-12
   
   # 对于 CUDA13
   sudo apt-get -y install cudnn9-cuda-13
   ```

---

### 

### **步骤 5：创建虚拟环境**

1. **新建环境（例如 `ml_dl`）**：
   ```bash
   conda create -n ml_dl python=3.9 -y
   ```

2. **激活环境**：
   ```bash
   conda activate ml_dl
   ```

---

### **步骤 6：安装机器学习库**
```bash
conda install -y numpy pandas scikit-learn matplotlib seaborn jupyter
```

---

### **步骤 7：安装深度学习框架**
#### **TensorFlow**
- **CPU 版本**：
  ```bash
  pip install tensorflow
  ```
- **GPU 版本（需 CUDA）**：
  ```bash
  pip install tensorflow[and-cuda]
  ```

#### **PyTorch**
- 访问 [PyTorch官网](https://pytorch.org/) 获取安装命令（根据 CUDA 版本选择）：
  ```bash
  # 示例（CUDA 11.8）：
  conda install -y pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
  ```

#### **验证 GPU 支持**：
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -c "import torch; print(torch.cuda.is_available())"
```

---

### **步骤 8：安装其他工具（可选）**
1. **Jupyter Lab**：
   ```bash
   conda install -y jupyterlab
   ```

2. **配置 Jupyter 远程访问**：
   ```bash
   jupyter notebook --generate-config
   echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py
   jupyter notebook password  # 设置密码
   ```
   - 启动 Jupyter：
     ```bash
     jupyter notebook --no-browser --port=8888
     ```
   - 在 Windows 浏览器访问 `http://localhost:8888`。

---

### **步骤 9：验证环境**
1. **运行测试代码**：
   ```python
   import tensorflow as tf
   print("TensorFlow Version:", tf.__version__)
   print("GPU Available:", tf.config.list_physical_devices('GPU'))
   
   import torch
   print("PyTorch Version:", torch.__version__)
   print("CUDA Available:", torch.cuda.is_available())
   ```

---

### **常见问题解决**
1. **CUDA 驱动问题**：
   - 确保 Windows 已安装 [NVIDIA 驱动](https://www.nvidia.com/Download/index.aspx)。
   - WSL 2 需 Windows 11 或 Windows 10 21H2 及以上版本。

2. **conda 命令未找到**：
   ```bash
   source ~/.bashrc  # 重新加载配置
   ```

3. **下载速度慢**：
   - 使用国内镜像（如清华源）：
     ```bash
     conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
     conda config --set show_channel_urls yes
     ```

---

完成以上步骤后，你已拥有一个支持机器学习和深度学习的 Anaconda 环境！