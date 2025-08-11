document.addEventListener('DOMContentLoaded', () => {
    const fileTreeContainer = document.getElementById('file-tree');
    const contentContainer = document.getElementById('content');

    // 获取并构建文件目录
    fetch('file-list.json')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const treeHtml = buildTree(data);
            fileTreeContainer.innerHTML = treeHtml;
            // 给文件链接添加点击事件
            addClickListeners();
        })
        .catch(error => {
            console.error('无法加载文件列表:', error);
            fileTreeContainer.innerHTML = '<p>错误：无法加载文件目录。</p>';
        });

    /**
     * 递归构建文件目录的 HTML
     * @param {Array} nodes - 文件或文件夹节点数组
     * @returns {string} - HTML 字符串
     */
    function buildTree(nodes) {
        let html = '<ul>';
        nodes.forEach(node => {
            if (node.type === 'folder') {
                html += `<li><span class="folder">${node.name}</span>`;
                if (node.children && node.children.length > 0) {
                    html += buildTree(node.children);
                }
                html += '</li>';
            } else if (node.type === 'file') {
                html += `<li><a href="#" data-path="${node.path}">${node.name}</a></li>`;
            }
        });
        html += '</ul>';
        return html;
    }

    /**
     * 为目录中的文件链接添加点击事件监听器
     */
    function addClickListeners() {
        const fileLinks = document.querySelectorAll('#file-tree a');
        fileLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const filePath = event.target.getAttribute('data-path');
                loadFileContent(filePath);
            });
        });
    }

    /**
     * 加载并显示 Markdown 文件的内容
     * @param {string} path - 文件路径
     */
    function loadFileContent(path) {
        contentContainer.innerHTML = `<p>正在加载: ${path}...</p>`;
        fetch(path)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(markdown => {
                contentContainer.innerHTML = marked.parse(markdown);
            })
            .catch(error => {
                console.error('无法加载文件内容:', error);
                contentContainer.innerHTML = `<p>错误：无法加载文件 ${path}。</p>`;
            });
    }
});