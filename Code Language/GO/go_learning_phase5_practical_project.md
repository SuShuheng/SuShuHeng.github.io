# Go语言学习计划 - 阶段5: 实战项目

**目标：** 将前面学到的Go语言基础、核心特性、并发编程、标准库和工具链知识融会贯通，通过实际项目进行巩固和提升。

**预计时间：** 7-10天

## 1. 选择一个小型项目进行实践

### 知识点
*   **项目规划：** 明确项目需求、功能模块、技术选型。
*   **模块划分：** 如何将项目拆分为不同的Go包。
*   **代码组织：** 遵循Go语言的项目结构约定。

### 建议项目类型
*   **简单的RESTful API服务：**
    *   例如：用户管理API (增删改查用户)、待办事项API。
    *   涉及知识点：`net/http`包、JSON编解码、结构体、切片/map存储数据（内存中或简单文件）。
*   **命令行工具 (CLI)：**
    *   例如：一个简单的文件查找工具、日志分析工具、端口扫描工具。
    *   涉及知识点：`os`包、`flag`包（处理命令行参数）、`io`包、并发（如果需要处理大量文件）。
*   **数据处理脚本：**
    *   例如：从CSV/JSON文件读取数据并进行统计分析、数据转换。
    *   涉及知识点：文件I/O、`encoding/csv` / `encoding/json`、结构体、切片。
*   **简单的聊天室应用：** (进阶，可以作为挑战)
    *   涉及知识点：`net/http` (WebSocket)、Goroutine、Channel。

### 项目选择示例：构建一个简单的RESTful API服务 (用户管理)

我们将以构建一个简单的用户管理API为例，它将提供用户的增删改查功能。

## 2. 将所学知识应用于项目中，解决实际问题

### 知识点
*   **需求分析与设计：**
    *   定义`User`结构体。
    *   确定API接口：`POST /users` (创建), `GET /users` (获取所有), `GET /users/{id}` (获取单个), `PUT /users/{id}` (更新), `DELETE /users/{id}` (删除)。
*   **HTTP路由与处理函数：** 使用`net/http`或第三方Web框架。
*   **数据存储：** 内存中存储（简单起见），或使用文件（CSV/JSON）进行持久化。
*   **错误处理：** 返回合适的HTTP状态码和错误信息。
*   **JSON数据交互：** 请求体解析、响应体构建。

### 代码示例 (使用标准库`net/http`)

**项目结构：**
```
my_user_api/
├── main.go
└── models/
    └── user.go
└── handlers/
    └── user_handlers.go
```

#### `my_user_api/models/user.go`
```go
package models

import "sync"

// User represents a user in the system.
type User struct {
    ID       string `json:"id"`
    Name     string `json:"name"`
    Email    string `json:"email"`
}

// In-memory storage for users.
var (
    users = make(map[string]User)
    mu    sync.Mutex // Mutex to protect concurrent access to the users map
)

// GetUsers returns all users.
func GetUsers() []User {
    mu.Lock()
    defer mu.Unlock()

    allUsers := make([]User, 0, len(users))
    for _, user := range users {
        allUsers = append(allUsers, user)
    }
    return allUsers
}

// GetUserByID returns a user by their ID.
func GetUserByID(id string) (User, bool) {
    mu.Lock()
    defer mu.Unlock()
    user, ok := users[id]
    return user, ok
}

// AddUser adds a new user.
func AddUser(user User) {
    mu.Lock()
    defer mu.Unlock()
    users[user.ID] = user
}

// UpdateUser updates an existing user.
func UpdateUser(user User) {
    mu.Lock()
    defer mu.Unlock()
    users[user.ID] = user
}

// DeleteUser deletes a user by their ID.
func DeleteUser(id string) {
    mu.Lock()
    defer mu.Unlock()
    delete(users, id)
}
```

#### `my_user_api/handlers/user_handlers.go`
```go
package handlers

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "net/http"
    "strconv"
    "sync/atomic" // For atomic counter to generate unique IDs

    "my_user_api/models" // 导入 models 包
)

var nextUserID int64 = 1 // Atomic counter for user IDs

// GetAllUsersHandler handles GET /users requests.
func GetAllUsersHandler(w http.ResponseWriter, r *http.Request) {
    users := models.GetUsers()
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(users)
}

// GetUserByIDHandler handles GET /users/{id} requests.
func GetUserByIDHandler(w http.ResponseWriter, r *http.Request) {
    id := r.URL.Path[len("/users/"):] // Simple way to extract ID from path
    user, ok := models.GetUserByID(id)
    if !ok {
        http.NotFound(w, r)
        return
    }
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

// CreateUserHandler handles POST /users requests.
func CreateUserHandler(w http.ResponseWriter, r *http.Request) {
    var user models.User
    body, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }
    if err := json.Unmarshal(body, &user); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    if user.ID == "" { // Generate ID if not provided
        user.ID = strconv.FormatInt(atomic.AddInt64(&nextUserID, 1), 10)
    }

    models.AddUser(user)
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}

// UpdateUserHandler handles PUT /users/{id} requests.
func UpdateUserHandler(w http.ResponseWriter, r *http.Request) {
    id := r.URL.Path[len("/users/"):]
    if _, ok := models.GetUserByID(id); !ok {
        http.NotFound(w, r)
        return
    }

    var user models.User
    body, err := ioutil.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }
    if err := json.Unmarshal(body, &user); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    user.ID = id // Ensure the ID from path is used
    models.UpdateUser(user)
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

// DeleteUserHandler handles DELETE /users/{id} requests.
func DeleteUserHandler(w http.ResponseWriter, r *http.Request) {
    id := r.URL.Path[len("/users/"):]
    if _, ok := models.GetUserByID(id); !ok {
        http.NotFound(w, r)
        return
    }
    models.DeleteUser(id)
    w.WriteHeader(http.StatusNoContent)
}
```

#### `my_user_api/main.go`
```go
package main

import (
    "fmt"
    "net/http"
    "strings"

    "my_user_api/handlers" // 导入 handlers 包
)

func main() {
    // 使用自定义路由器来处理 /users 和 /users/{id}
    http.HandleFunc("/users", func(w http.ResponseWriter, r *http.Request) {
        if r.URL.Path == "/users" {
            switch r.Method {
            case "GET":
                handlers.GetAllUsersHandler(w, r)
            case "POST":
                handlers.CreateUserHandler(w, r)
            default:
                http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
            }
        } else if strings.HasPrefix(r.URL.Path, "/users/") {
            switch r.Method {
            case "GET":
                handlers.GetUserByIDHandler(w, r)
            case "PUT":
                handlers.UpdateUserHandler(w, r)
            case "DELETE":
                handlers.DeleteUserHandler(w, r)
            default:
                http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
            }
        } else {
            http.NotFound(w, r)
        }
    })

    fmt.Println("User API server listening on :8080...")
    err := http.ListenAndServe(":8080", nil)
    if err != nil {
        fmt.Println("Server error:", err)
    }
}
```

### 如何运行和测试该API

1.  **创建项目目录和文件：**
    ```bash
    mkdir my_user_api
    cd my_user_api
    mkdir models handlers
    touch main.go models/user.go handlers/user_handlers.go
    ```
2.  **复制粘贴代码到相应文件。**
3.  **初始化Go模块：**
    ```bash
    go mod init my_user_api
    ```
4.  **运行服务器：**
    ```bash
    go run main.go
    ```
5.  **使用`curl`或其他HTTP客户端测试API：**

    *   **创建用户 (POST):**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice", "email":"alice@example.com"}' http://localhost:8080/users
        ```
    *   **获取所有用户 (GET):**
        ```bash
        curl http://localhost:8080/users
        ```
    *   **获取单个用户 (GET):** (将 `1` 替换为实际的用户ID)
        ```bash
        curl http://localhost:8080/users/1
        ```
    *   **更新用户 (PUT):** (将 `1` 替换为实际的用户ID)
        ```bash
        curl -X PUT -H "Content-Type: application/json" -d '{"name":"Alice Smith", "email":"alice.smith@example.com"}' http://localhost:8080/users/1
        ```
    *   **删除用户 (DELETE):** (将 `1` 替换为实际的用户ID)
        ```bash
        curl -X DELETE http://localhost:8080/users/1
        ```

## 3. 学习使用第三方库

### 知识点
*   **Web框架：** Gin、Echo、Revel等，提供更方便的路由、中间件、模板渲染等功能。
*   **ORM库：** GORM、XORM等，简化数据库操作。
*   **日志库：** Zap、Logrus等，提供更强大的日志功能。
*   **依赖管理：** `go get`命令下载第三方库，`go mod tidy`管理依赖。

### 示例：使用Gin框架重构API (以`CreateUserHandler`为例)

#### 安装Gin：
```bash
go get github.com/gin-gonic/gin
```

#### `main.go` (使用Gin框架)
```go
package main

import (
    "github.com/gin-gonic/gin"
    "net/http"
    "sync/atomic" // For atomic counter to generate unique IDs

    "my_user_api/models"
)

var nextUserID int64 = 1

func main() {
    router := gin.Default() // 创建一个Gin路由器

    // 定义路由
    router.GET("/users", func(c *gin.Context) {
        users := models.GetUsers()
        c.JSON(http.StatusOK, users)
    })

    router.POST("/users", func(c *gin.Context) {
        var user models.User
        if err := c.ShouldBindJSON(&user); err != nil { // 自动绑定JSON到结构体
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        if user.ID == "" {
            user.ID = strconv.FormatInt(atomic.AddInt64(&nextUserID, 1), 10)
        }

        models.AddUser(user)
        c.JSON(http.StatusCreated, user)
    })

    // 其他路由 (GET /users/:id, PUT /users/:id, DELETE /users/:id) 类似方式实现

    router.Run(":8080") // 启动服务器
}
```
**注意：** 上述Gin示例仅展示了部分功能，完整的Gin版本需要您自行实现其他HTTP方法。通过对比标准库版本和Gin版本，您将体会到框架带来的便利性。

## 4. 部署您的Go应用程序

### 知识点
*   **编译：** `go build`生成可执行文件。
*   **Docker容器化：**
    *   编写`Dockerfile`。
    *   构建Docker镜像。
    *   运行Docker容器。
*   **简单的部署流程：** 将可执行文件或Docker镜像部署到服务器。

### Dockerfile 示例
在`my_user_api`项目根目录下创建`Dockerfile`：

```dockerfile
# 使用官方Go镜像作为构建阶段
FROM golang:1.22 AS builder

# 设置工作目录
WORKDIR /app

# 拷贝go.mod和go.sum文件，并下载依赖
COPY go.mod .
COPY go.sum .
RUN go mod download

# 拷贝源代码
COPY . .

# 构建应用程序
RUN CGO_ENABLED=0 GOOS=linux go build -o my_user_api .

# 使用一个轻量级的镜像作为最终运行阶段
FROM alpine:latest

# 设置工作目录
WORKDIR /root/

# 拷贝构建好的可执行文件
COPY --from=builder /app/my_user_api .

# 暴露端口
EXPOSE 8080

# 运行应用程序
CMD ["./my_user_api"]
```

### Docker 构建和运行命令
在`my_user_api`项目根目录下执行：

1.  **构建Docker镜像：**
    ```bash
    docker build -t my-user-api .
    ```
2.  **运行Docker容器：**
    ```bash
    docker run -p 8080:8080 my-user-api
    ```
    现在API将在Docker容器内运行，您仍然可以通过`http://localhost:8080`访问它。