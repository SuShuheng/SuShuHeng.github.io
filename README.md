# SuShuHeng's Blog

这是一个基于纯前端技术（HTML, CSS, JavaScript）构建的个人博客，可以直接托管在 GitHub Pages 上。它能够动态地加载和展示项目中的 Markdown 文件。

## 特性

-   无后端依赖，纯静态页面。
-   通过 `file-list.json` 动态生成文件目录。
-   使用 [marked.js](https://github.com/markedjs/marked) 解析和渲染 Markdown。
-   响应式布局，适配不同屏幕尺寸。
-   提供自动化脚本，简化文章添加流程。

## 如何使用

### 推荐方式：使用自动化脚本添加新文章

为了简化操作，项目在 `scripts` 目录下提供了一个 `add_post.py` 脚本。

**运行脚本：**
```bash
python scripts/add_post.py
```

**脚本会自动引导您完成以下操作：**
1.  **弹出文件选择框**：让您选择要添加的 `.md` 文件。
2.  **输入目标目录**：在命令行中输入您想存放文章的目录（如 `posts/技术`）。
3.  **自动完成**：脚本会自动复制文件到指定位置，并更新 `file-list.json`。

### 手动管理文章

如果您想进行更复杂的操作（如移动文件、修改文件名、删除文章），则需要手动进行。

#### 1. 添加或修改文章

您可以直接在项目中创建、修改或删除 `.md` 文件。建议将所有的文章都存放在 `posts` 文件夹下，以便于管理。

例如，您可以创建一个新的文件 `posts/技术/我的第二篇文章.md`。

#### 2. 更新文件目录

为了让您的新文章显示在网站的目录中，您需要**手动**更新项目根目录下的 `file-list.json` 文件。

打开 `file-list.json`，模仿现有的结构，添加一个指向您新文件的条目。

##### `file-list.json` 结构示例

这个 JSON 文件是一个由对象组成的数组，每个对象代表一个文件或文件夹。

-   **文件夹类型**:
    ```json
    {
      "type": "folder",
      "name": "文件夹名称",
      "children": [ ... ] 
    }
    ```
-   **文件类型**:
    ```json
    {
      "type": "file",
      "name": "文件显示名称.md",
      "path": "相对于根目录的完整路径/文件名.md" 
    }
    ```

#### 更新示例

假设您刚刚创建了 `posts/技术/我的第二篇文章.md`，您需要像下面这样更新 `file-list.json`：

```json
[
  {
    "type": "folder",
    "name": "posts",
    "children": [
      {
        "type": "file",
        "name": "welcome.md",
        "path": "posts/welcome.md"
      },
      {
        "type": "folder",
        "name": "技术",
        "children": [
          {
            "type": "file",
            "name": "我的第二篇文章.md",
            "path": "posts/技术/我的第二篇文章.md"
          }
        ]
      }
    ]
  }
]
```

### 3. 提交更改

将您所有的更改（包括新的 `.md` 文件和修改后的 `file-list.json`）提交并推送到 GitHub。GitHub Pages 会自动重新构建您的网站，几分钟后您的新文章就会上线。

---
*Enjoy your blogging!*
