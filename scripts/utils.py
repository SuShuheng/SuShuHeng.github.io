import os
import json
import subprocess
import sys

def get_project_root():
    """
    获取项目根目录的绝对路径。
    假设脚本位于 project_root/scripts/
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def load_file_list(project_root):
    """
    加载 file-list.json 文件并返回其内容。
    """
    json_path = os.path.join(project_root, 'file-list.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_file_list(project_root, data):
    """
    将数据保存到 file-list.json 文件。
    """
    json_path = os.path.join(project_root, 'file-list.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_generate_file_list(project_root):
    """
    调用 scripts/generate_file_list.py 脚本重新生成 file-list.json。
    """
    script_path = os.path.join(project_root, 'scripts', 'generate_file_list.py')
    print(f"正在运行 {script_path} 重新生成 file-list.json...")
    try:
        # 使用 subprocess.run 运行脚本，并捕获输出
        result = subprocess.run(
            ['python', script_path],
            capture_output=True,
            text=True,
            check=True,
            cwd=project_root # 确保在项目根目录执行，以便 generate_file_list.py 正确扫描
        )
        print("generate_file_list.py 输出:")
        print(result.stdout)
        if result.stderr:
            print("generate_file_list.py 错误输出:")
            print(result.stderr)
        print("file-list.json 已重新生成。")
    except subprocess.CalledProcessError as e:
        print(f"调用 generate_file_list.py 失败: {e}", file=sys.stderr)
        print(f"stdout: {e.stdout}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"错误: 未找到 Python 解释器或脚本文件 '{script_path}'。", file=sys.stderr)

def list_markdown_files(file_list_data):
    """
    递归遍历 file-list.json 数据，提取所有 Markdown 文件的 name 和 path。
    返回一个字典列表，每个字典包含 'name' 和 'path'。
    """
    markdown_files = []
    excluded_markdown_files = ['index.md', 'structure.md'] # 新增排除列表

    for item in file_list_data:
        if item['type'] == 'file' and item['name'].lower().endswith('.md'):
            if item['name'].lower() not in excluded_markdown_files: # 检查是否在排除列表中
                markdown_files.append({'name': item['name'], 'path': item['path']})
        elif item['type'] == 'folder' and 'children' in item:
            markdown_files.extend(list_markdown_files(item['children']))
    return markdown_files

def remove_empty_dirs(path):
    """
    递归删除指定路径下的所有空目录。
    """
    if not os.path.isdir(path):
        return

    # 先处理子目录
    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path):
            remove_empty_dirs(entry_path)

    # 如果当前目录为空，则删除
    try:
        if not os.listdir(path):
            os.rmdir(path)
            print(f"已删除空目录: {path}")
    except OSError as e:
        print(f"无法删除目录 {path}: {e}", file=sys.stderr)