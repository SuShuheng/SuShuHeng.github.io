import subprocess
import sys
import os

def run_command(command):
    """
    运行一个 shell 命令并实时打印输出，如果失败则退出。
    """
    # 确保命令在项目根目录执行
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    print(f"\n> {' '.join(command)}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=project_root,
        text=True,
        encoding='utf-8',
        shell=False  # 直接调用命令，不通过shell
    )
    
    # 实时读取输出
    if process.stdout:
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

    # 检查错误
    stderr = process.communicate()[1]
    if process.returncode != 0:
        print(f"错误: 命令 '{command}' 执行失败。")
        print(stderr.strip())
        sys.exit(1)
    
    print("-" * 20)

def main():
    """
    主函数
    """
    print("开始执行自动化发布流程...")
    
    # 1. git add
    print("步骤 1: 将所有更改添加到暂存区...")
    run_command("git add .")
    
    # 2. git status 检查
    print("检查暂存区状态...")
    run_command("git status")

    # 3. 获取 commit message
    print("步骤 2: 请输入本次提交的描述信息 (Commit Message):")
    commit_message = input("> ")
    if not commit_message:
        print("提交信息不能为空，操作取消。")
        sys.exit(1)
        
    # 4. git commit
    print("\n步骤 3: 提交更改...")
    # 使用双引号包裹提交信息以处理包含空格的情况
    run_command(['git', 'commit', '-m', commit_message])
    
    # 5. git push
    print("步骤 4: 推送到 GitHub...")
    run_command(['git', 'push'])
    
    print("发布成功！您的网站将在几分钟后更新。")

if __name__ == '__main__':
    main()