import os
import json
import sys

def build_tree(path):
    """
    递归构建文件树，只包含 .md 文件和包含 .md 文件的目录。
    """
    tree = []
    # 忽略的目录
    excluded_dirs = ['.git', 'scripts', '.vscode', '__pycache__']
    # 忽略的文件
    excluded_files = ['readme.md']

    try:
        items = sorted(os.listdir(path))
    except FileNotFoundError:
        return []

    for item in items:
        item_path = os.path.join(path, item)
        # 忽略隐藏文件和目录
        if item.startswith('.'):
            continue

        if os.path.isdir(item_path):
            if item in excluded_dirs:
                continue
            # 递归构建子目录
            children = build_tree(item_path)
            # 只添加非空的目录
            if children:
                tree.append({'type': 'folder', 'name': item, 'children': children})
        elif os.path.isfile(item_path):
            if item.lower() in excluded_files:
                continue
            if item.endswith('.md'):
                # 使用相对于当前工作目录的路径，并用斜杠'/'
                relative_path = os.path.relpath(item_path, os.getcwd()).replace('\\', '/')
                tree.append({'type': 'file', 'name': item, 'path': relative_path})
    return tree

def main():
    """
    主函数，生成 file-list.json
    """
    try:
        # 从当前工作目录开始扫描
        project_root = os.getcwd()
        print(f"项目根目录: {project_root}")

        file_structure = build_tree(project_root)
        
        output_path = os.path.join(project_root, 'file-list.json')
        print(f"正在写入文件到: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(file_structure, f, indent=2, ensure_ascii=False)
            
        print(f"文件列表已成功生成到: {output_path}")
        print("JSON内容:")
        print(json.dumps(file_structure, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"生成文件列表时发生错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()