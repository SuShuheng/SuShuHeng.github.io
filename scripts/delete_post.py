import os
import tkinter as tk
from tkinter import ttk, messagebox
import sys

# 将 scripts 目录添加到 Python 路径，以便导入 utils.py
script_dir = os.path.dirname(__file__)
project_root_dir = os.path.abspath(os.path.join(script_dir, '..'))
if project_root_dir not in sys.path:
    sys.path.append(project_root_dir)

from scripts import utils

class DeletePostApp:
    def __init__(self, master):
        self.master = master
        master.title("博客文章删除工具")
        master.geometry("800x600")

        self.project_root = utils.get_project_root()
        self.file_list_data = [] # 原始 file-list.json 数据
        self.markdown_files = [] # 扁平化的 Markdown 文件列表

        self.create_widgets()
        self.load_data_and_populate_tree()

    def create_widgets(self):
        # 创建主内容 Frame，包含左右两个 Frame
        self.main_content_frame = ttk.Frame(self.master, padding="10")
        self.main_content_frame.pack(side="top", fill="both", expand=True)

        # 创建左右两个 Frame，并放置在 main_content_frame 内部
        self.left_frame = ttk.Frame(self.main_content_frame, padding="0") # 内部 padding 设为0，由外部 main_content_frame 提供
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ttk.Frame(self.main_content_frame, padding="0") # 内部 padding 设为0
        self.right_frame.pack(side="right", fill="y", expand=False) # 不允许右侧扩展

        # 左侧 Treeview 显示文件列表
        self.tree = ttk.Treeview(self.left_frame, columns=("path"), show="tree headings", selectmode="extended")
        self.tree.heading("#0", text="显示名称")
        self.tree.heading("path", text="完整路径")
        # 调整 Treeview 的列宽，允许自适应
        self.tree.column("#0", width=400, stretch=tk.YES) # 允许显示名称列自适应扩展
        self.tree.column("path", width=150, stretch=tk.YES) # 允许路径列自适应扩展
        self.tree.pack(side="top", fill="both", expand=True)

        # 滚动条
        vsb = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        vsb.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vsb.set)

        # 右侧按钮
        self.refresh_button = ttk.Button(self.right_frame, text="刷新列表", command=self.load_data_and_populate_tree)
        self.refresh_button.pack(pady=5, fill="x")

        self.delete_button = ttk.Button(self.right_frame, text="删除选中博客", command=self.delete_selected_posts)
        self.delete_button.pack(pady=5, fill="x")

        # 日志区
        self.log_text = tk.Text(self.master, height=10, state="disabled", wrap="word", bg="#f0f0f0")
        self.log_text.pack(side="bottom", fill="x", padx=10, pady=10) # 放置在 master 底部

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.master.update_idletasks() # 强制更新 GUI

    def load_data_and_populate_tree(self):
        """加载数据并填充 Treeview"""
        self.log("正在加载文件列表...")
        self.file_list_data = utils.load_file_list(self.project_root)
        self.markdown_files = utils.list_markdown_files(self.file_list_data)
        self.populate_tree(self.file_list_data)
        self.log("文件列表加载完成。")

    def populate_tree(self, data, parent=""):
        """递归填充 Treeview"""
        self.tree.delete(*self.tree.get_children()) # 清空现有条目

        def insert_items(items, parent_id=""):
            for item in items:
                node_id = self.tree.insert(parent_id, "end", text=item["name"], open=True, values=(item.get("path", "")))
                if item["type"] == "folder" and "children" in item:
                    insert_items(item["children"], node_id)

        insert_items(data)

    def delete_selected_posts(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请选择要删除的博客文章。")
            return

        files_to_delete = []
        excluded_files = ['index.md', 'Structure.md'] # 定义不应被删除的文件

        for item_id in selected_items:
            # 确保只删除文件类型的节点，跳过文件夹节点
            # Treeview 的 path 列只对文件类型有值
            item_path = self.tree.item(item_id, "values")[0]
            if item_path: # 只有文件节点才有path值
                # 检查是否是排除文件
                if os.path.basename(item_path).lower() in [f.lower() for f in excluded_files]:
                    messagebox.showwarning("警告", f"文件 '{os.path.basename(item_path)}' 不能被删除。")
                    self.log(f"尝试删除受保护文件: {item_path}，操作已阻止。")
                    return # 阻止整个删除操作
                files_to_delete.append(item_path)

        if not files_to_delete:
            messagebox.showinfo("提示", "请选择有效的博客文章文件进行删除。")
            return

        confirm_msg = "您确定要删除以下博客文章吗？\n\n" + "\n".join(files_to_delete)
        if not messagebox.askyesno("确认删除", confirm_msg):
            self.log("删除操作已取消。")
            return

        self.log("正在执行删除操作...")
        deleted_count = 0
        for relative_path in files_to_delete:
            full_path = os.path.join(self.project_root, relative_path)
            try:
                if os.path.exists(full_path):
                    os.remove(full_path)
                    self.log(f"成功删除文件: {relative_path}")
                    deleted_count += 1
                else:
                    self.log(f"文件不存在，跳过删除: {relative_path}")
            except OSError as e:
                self.log(f"删除文件失败 {relative_path}: {e}")

        # 删除空目录（从项目根目录开始递归清理）
        self.log("正在清理空目录...")
        utils.remove_empty_dirs(self.project_root)

        # 重新生成 file-list.json
        self.log("正在重新生成 file-list.json...")
        utils.run_generate_file_list(self.project_root)

        # 刷新 GUI
        self.load_data_and_populate_tree()
        self.log(f"删除操作完成。共删除 {deleted_count} 个文件。")


def main():
    root = tk.Tk()
    app = DeletePostApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()