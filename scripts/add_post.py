import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog

def update_file_list(project_root, relative_target_dir, new_files):
    """
    更新 file-list.json 文件
    """
    json_path = os.path.join(project_root, 'file-list.json')

    # 1. 读取现有的 JSON 数据
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # 2. 找到或创建目标目录节点
    path_parts = [part for part in relative_target_dir.split('/') if part]
    current_level = data
    
    for part in path_parts:
        node = next((item for item in current_level if item.get('name') == part and item.get('type') == 'folder'), None)
        if not node:
            node = {'type': 'folder', 'name': part, 'children': []}
            current_level.append(node)
        current_level = node['children']
    
    # 3. 添加新文件节点
    for file_name in new_files:
        file_path = f"{relative_target_dir}/{file_name}".lstrip('/')
        # 检查文件是否已存在
        if not any(item.get('name') == file_name for item in current_level):
            current_level.append({'type': 'file', 'name': file_name, 'path': file_path})
            print(f"  - 已添加 '{file_path}' 到 file-list.json")
        else:
            print(f"  - '{file_path}' 已存在于 file-list.json，跳过。")

    # 4. 写回 JSON 文件
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    """
    主函数
    """
    # 初始化 Tkinter
    root = tk.Tk()
    root.withdraw() # 隐藏主窗口

    # 1. 选择要添加的 Markdown 文件
    print("步骤 1: 请选择一个或多个要添加的 Markdown 文件 (.md)")
    source_files = filedialog.askopenfilenames(
        title="选择 Markdown 文件",
        filetypes=[("Markdown files", "*.md"), ("All files", "*.*")]
    )

    if not source_files:
        print("没有选择文件，操作取消。")
        return

    print("\n已选择文件:")
    for f in source_files:
        print(f" - {f}")

    # 2. 获取项目根目录和目标目录
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    relative_target_dir = input(f"\n步骤 2: 请输入您想将文件复制到的目标目录 (相对于项目根目录 '{os.path.basename(project_root)}')\n例如: posts/技术\n> ").strip().replace('\\', '/')

    target_dir_path = os.path.join(project_root, relative_target_dir)

    # 3. 创建目标目录（如果不存在）
    if not os.path.exists(target_dir_path):
        os.makedirs(target_dir_path)
        print(f"\n已创建目录: {target_dir_path}")

    # 4. 复制文件并收集新文件名
    print("\n步骤 3: 正在复制文件...")
    new_files = []
    for source_file in source_files:
        file_name = os.path.basename(source_file)
        destination_file = os.path.join(target_dir_path, file_name)
        shutil.copy(source_file, destination_file)
        new_files.append(file_name)
        print(f" - '{source_file}' 已复制到 '{destination_file}'")

    # 5. 更新 file-list.json
    print("\n步骤 4: 正在更新 file-list.json...")
    update_file_list(project_root, relative_target_dir, new_files)
    
    print("\n操作完成！")

if __name__ == '__main__':
    main()