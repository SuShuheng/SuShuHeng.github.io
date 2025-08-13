document.addEventListener('DOMContentLoaded', () => {
    const fileTreeContainer = document.getElementById('file-tree');
    const contentContainer = document.getElementById('content');
    const homeButton = document.getElementById('homeButton');
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebarToggle');

    // 初始化 Marked.js 渲染器
    const renderer = new marked.Renderer(); // 保持 renderer 定义，以便 marked.parse 使用

    marked.setOptions({
        renderer: renderer, // 确保 marked.js 使用自定义的渲染器
        highlight: null, // 禁用 marked.js 内部高亮
        langPrefix: '', // 禁用语言前缀
        gfm: true, // 启用 GitHub Flavored Markdown
        breaks: false, // 不支持 GitHub Flavored Markdown 换行符
        pedantic: false, // 不启用 pedantic 选项
        sanitize: false, // 禁用 HTML 过滤
        smartLists: true, // 启用智能列表
        smartypants: false // 禁用智能标点
    });

    // 页面加载时默认加载 index.md
    loadFileContent('index.md');

    // “首页”按钮点击事件
    homeButton.addEventListener('click', (event) => {
        event.preventDefault();
        loadFileContent('index.md');
    });

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
            // 给文件和文件夹添加点击事件
            addClickListeners();
            addFolderToggleListeners();
        })
        .catch(error => {
            console.error('无法加载文件列表:', error);
            fileTreeContainer.innerHTML = '<p>错误：无法加载文件目录。</p>';
        });

    function addFolderToggleListeners() {
        const folderHeaders = document.querySelectorAll('.folder-header');
        folderHeaders.forEach(header => {
            header.addEventListener('click', (event) => {
                const caret = header.querySelector('.caret');
                const nestedUl = header.nextElementSibling; // 获取紧邻的兄弟元素，即 ul.nested

                if (nestedUl && nestedUl.classList.contains('nested')) {
                    nestedUl.classList.toggle('active');
                    caret.classList.toggle('caret-down');
                }
            });
        });
    }

    // 侧边栏切换按钮点击事件
    sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('collapsed');
        contentContainer.classList.toggle('expanded');

        const arrow = sidebarToggle.querySelector('.arrow');
        if (sidebar.classList.contains('collapsed')) {
            arrow.classList.remove('left');
            arrow.classList.add('right');
        } else {
            arrow.classList.remove('right');
            arrow.classList.add('left');
        }
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
                html += `<li>
                            <div class="folder-header">
                                <span class="caret"></span>
                                <span class="folder-name">${node.name}</span>
                            </div>`;
                if (node.children && node.children.length > 0) {
                    html += `<ul class="nested">` + buildTree(node.children).slice(4, -5) + `</ul>`;
                }
                html += `</li>`;
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
                contentContainer.innerHTML = marked.parse(markdown); // 让 marked.js 正常解析所有 Markdown

                // 手动处理代码块，添加语言显示和复制按钮
                document.querySelectorAll('pre code').forEach(block => {
                    const parentPre = block.parentNode;
                    const langClass = block.className.split(' ').find(cls => cls.startsWith('language-'));
                    let languageName = 'PLAINTEXT';
                    let fileName = '';

                    if (langClass) {
                        const parts = langClass.replace('language-', '').split(':');
                        languageName = parts[0] ? parts[0].toUpperCase() : 'PLAINTEXT';
                        if (parts.length > 1) {
                            fileName = parts.slice(1).join(':'); // Handle filenames with colons
                        }
                    }
                    const codeContent = block.textContent;

                    const codeContainer = document.createElement('div');
                    codeContainer.className = 'code-block-container';

                    const header = document.createElement('div');
                    header.className = 'code-block-header';

                    const langSpan = document.createElement('span');
                    langSpan.className = 'code-language';
                    langSpan.textContent = languageName;

                    const fileNameSpan = document.createElement('span');
                    fileNameSpan.className = 'code-filename';
                    fileNameSpan.textContent = fileName;
                    if (fileName) {
                        header.insertBefore(fileNameSpan, langSpan.nextSibling); // Insert after language, before copy button
                    }

                    const copyButton = document.createElement('button');
                    copyButton.className = 'copy-code-button';
                    copyButton.textContent = '复制';
                    copyButton.dataset.code = encodeURIComponent(codeContent);

                    header.appendChild(langSpan);
                    header.appendChild(copyButton);
                    codeContainer.appendChild(header);
                    codeContainer.appendChild(parentPre.cloneNode(true)); // 复制原始的 pre 元素

                    parentPre.replaceWith(codeContainer); // 替换原始的 pre 元素

                    // 添加复制按钮事件监听器
                    copyButton.addEventListener('click', () => {
                        navigator.clipboard.writeText(codeContent).then(() => {
                            copyButton.textContent = '已复制!';
                            copyButton.classList.add('copied'); // Add copied class
                            setTimeout(() => {
                                copyButton.textContent = '复制';
                                copyButton.classList.remove('copied'); // Remove copied class
                            }, 2000);
                        }).catch(err => {
                            console.error('复制失败:', err);
                        });
                    });
                });

                // 确保 highlight.js 在所有代码块元素都存在于 DOM 中后运行
                hljs.highlightAll();
            })
            .catch(error => {
                console.error('无法加载文件内容:', error);
                contentContainer.innerHTML = `<p>错误：无法加载文件 ${path}。</p>`;
            });
    }
});