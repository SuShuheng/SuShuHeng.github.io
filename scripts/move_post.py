import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys

# 将 scripts 目录添加到 Python 路径，以便导入 utils.py
script_dir = os.path.dirname(__file__)
project_root_dir = os.path.abspath(os.path.join(script_dir, '..'))
if project_root_dir not in sys.path:
    sys.path.append(project_root_dir)

from scripts import utils

class MovePostApp:
    def __init__(self, master):
        self.master = master
        master.title("博客文章移动工具")
        master.geometry("800x600")

        self.project_root = utils.get_project_root()
        self.file_list_data = [] # 原始 file-list.json 数据
        self.markdown_files = [] # 扁平化的 Markdown 文件列表
        self.selected_target_dir = tk.StringVar() # 用于存储目标目录

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
        self.tree = ttk.Treeview(self.left_frame, columns=("path"), show="tree headings", selectmode="browse") # browse 模式只允许单选
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

        # 右侧按钮和目标目录选择
        self.refresh_button = ttk.Button(self.right_frame, text="刷新列表", command=self.load_data_and_populate_tree)
        self.refresh_button.pack(pady=5, fill="x")

        ttk.Label(self.right_frame, text="目标目录:").pack(pady=(10,0), fill="x")
        self.target_dir_entry = ttk.Entry(self.right_frame, textvariable=self.selected_target_dir, state="readonly")
        self.target_dir_entry.pack(pady=2, fill="x")

        self.select_dir_button = ttk.Button(self.right_frame, text="选择目标目录", command=self.select_target_directory)
        self.select_dir_button.pack(pady=5, fill="x")

        self.move_button = ttk.Button(self.right_frame, text="移动选中博客", command=self.move_selected_post)
        self.move_button.pack(pady=5, fill="x")

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
        self.log(f"Treeview 已清空。准备填充数据。数据结构: {data[:2]}...") # 打印前两个元素以便调试

        def insert_items(items, parent_id=""):
            for item in items:
                # 检查 item 是否包含 'name' 和 'type' 键
                if 'name' not in item or 'type' not in item:
                    self.log(f"警告: 无效的 file-list.json 条目，缺少 'name' 或 'type' 键: {item}")
                    continue

                node_id = self.tree.insert(parent_id, "end", text=item["name"], open=True, values=(item.get("path", "")))
                if item["type"] == "folder" and "children" in item:
                    insert_items(item["children"], node_id)
                elif item["type"] == "file" and not item.get("path"):
                    self.log(f"警告: 文件条目缺少 'path' 键: {item}")

        insert_items(data)
        self.log("Treeview 填充完成。")

    def select_target_directory(self):
        target_dir = filedialog.askdirectory(
            title="选择目标目录",
            initialdir=self.project_root # 默认从项目根目录开始
        )
        if target_dir:
            # 确保路径是相对于项目根目录的
            relative_target_dir = os.path.relpath(target_dir, self.project_root).replace('\\', '/')
            self.selected_target_dir.set(relative_target_dir)
            self.log(f"已选择目标目录: {relative_target_dir}")
        else:
            self.log("未选择目标目录。")

    def move_selected_post(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("提示", "请选择要移动的博客文章。")
            return
        elif len(selected_items) > 1:
            messagebox.showinfo("提示", "一次只能移动一篇博客文章。")
            return
        else:
            # 确保选中了有效的单个项目
            if selected_items:
                item_id = selected_items[0]
            else:
                messagebox.showinfo("提示", "请选择要移动的博客文章。")
                self.log("错误: 未选中任何项目。")
                return
        
        original_relative_path = self.tree.item(item_id, "values")[0]
        self.log(f"选中的原始相对路径: {original_relative_path}")
        if not original_relative_path: # 确保选中是文件节点
            messagebox.showinfo("提示", "请选择有效的博客文章文件进行移动。")
            self.log("错误: 未选中有效的博客文章文件。")
            return
        
        excluded_files = ['index.md', 'Structure.md'] # 定义不应被移动的文件
        if os.path.basename(original_relative_path).lower() in [f.lower() for f in excluded_files]:
            messagebox.showwarning("警告", f"文件 '{os.path.basename(original_relative_path)}' 不能被移动。")
            self.log(f"尝试移动受保护文件: {original_relative_path}，操作已阻止。")
            return # 阻止移动操作

        target_relative_dir = self.selected_target_dir.get()
        self.log(f"选定的目标相对目录: {target_relative_dir}")
        if not target_relative_dir:
            messagebox.showinfo("提示", "请选择目标目录。")
            self.log("错误: 未选择目标目录。")
            return

        original_full_path = os.path.join(self.project_root, original_relative_path)
        new_dir_full_path = os.path.join(self.project_root, target_relative_dir)
        new_file_name = os.path.basename(original_relative_path)
        new_full_path = os.path.join(new_dir_full_path, new_file_name)

        self.log(f"原始完整路径: {original_full_path}")
        self.log(f"新目录完整路径: {new_dir_full_path}")
        self.log(f"新文件完整路径: {new_full_path}")

        if not os.path.exists(original_full_path):
            messagebox.showerror("错误", f"源文件不存在: {original_relative_path}")
            self.log(f"错误: 源文件不存在: {original_relative_path}")
            return

        # 确保目标目录存在
        if not os.path.exists(new_dir_full_path):
            self.log(f"目标目录不存在，正在创建: {new_dir_full_path}")
            os.makedirs(new_dir_full_path)
            self.log(f"已创建目录: {target_relative_dir}")
        else:
            self.log(f"目标目录已存在: {new_dir_full_path}")

        confirm_msg = (f"您确定要将博客文章从\n'{original_relative_path}'\n移动到\n'{target_relative_dir}'\n吗？")
        if not messagebox.askyesno("确认移动", confirm_msg):
            self.log("移动操作已取消。")
            return

        self.log("正在执行移动操作...")
        try:
            shutil.move(original_full_path, new_full_path)
            self.log(f"成功移动文件: '{original_relative_path}' -> '{target_relative_dir}/{new_file_name}'")

            # 清理原目录（如果为空）
            original_dir = os.path.dirname(original_full_path)
            self.log(f"正在尝试清理原目录 (如果为空): {original_dir}")
            utils.remove_empty_dirs(original_dir)

            # 重新生成 file-list.json
            self.log("正在重新生成 file-list.json...")
            utils.run_generate_file_list(self.project_root)

            # 刷新 GUI
            self.load_data_and_populate_tree()
            self.log("移动操作完成。")

        except shutil.Error as e:
            messagebox.showerror("移动失败", f"移动文件失败: {e}")
            self.log(f"移动文件失败: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"发生未知错误: {e}")
            self.log(f"发生未知错误: {e}")

def main():
    root = tk.Tk()
    app = MovePostApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()