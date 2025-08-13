# Go语言学习计划 - 阶段4: Go标准库和常用工具

**目标：** 熟悉Go语言常用的标准库，掌握Web服务构建、JSON数据处理，并深入理解测试和构建工具。

**预计时间：** 5-7天

## 1. 熟悉常用的标准库

### 知识点
*   **`fmt`包：** 格式化输入输出，`Printf`、`Sprintf`、`Scanf`等。
*   **`io`包：** 基本的I/O原语。
*   **`os`包：** 操作系统功能，文件操作、进程管理、环境变量。
*   **`strings`包：** 字符串操作，查找、替换、分割、合并。
*   **`strconv`包：** 字符串和基本数据类型之间的转换。
*   **`time`包：** 时间和日期处理，时间点、时间段、格式化。

### 代码示例

#### `fmt`包
```go
package main

import "fmt"

func main() {
    name := "Alice"
    age := 30
    fmt.Printf("Name: %s, Age: %d\n", name, age) // 格式化输出到控制台

    s := fmt.Sprintf("Name: %s, Age: %d", name, age) // 格式化输出到字符串
    fmt.Println(s)

    var inputName string
    var inputAge int
    fmt.Print("Enter your name and age: ")
    fmt.Scanf("%s %d", &inputName, &inputAge) // 从控制台读取输入
    fmt.Printf("You entered: Name=%s, Age=%d\n", inputName, inputAge)
}
```

#### `os`包
```go
package main

import (
    "fmt"
    "os"
)

func main() {
    // 获取当前工作目录
    pwd, err := os.Getwd()
    if err != nil {
        fmt.Println("Error getting current directory:", err)
    } else {
        fmt.Println("Current working directory:", pwd)
    }

    // 创建目录
    err = os.Mkdir("my_dir", 0755)
    if err != nil {
        fmt.Println("Error creating directory:", err)
    } else {
        fmt.Println("Directory 'my_dir' created.")
    }

    // 创建文件
    file, err := os.Create("my_file.txt")
    if err != nil {
        fmt.Println("Error creating file:", err)
    } else {
        fmt.Println("File 'my_file.txt' created.")
        file.WriteString("Hello, Go OS package!")
        file.Close()
    }

    // 读取文件
    data, err := os.ReadFile("my_file.txt")
    if err != nil {
        fmt.Println("Error reading file:", err)
    } else {
        fmt.Println("Content of my_file.txt:", string(data))
    }

    // 删除文件
    err = os.Remove("my_file.txt")
    if err != nil {
        fmt.Println("Error removing file:", err)
    } else {
        fmt.Println("File 'my_file.txt' removed.")
    }

    // 删除目录
    err = os.Remove("my_dir")
    if err != nil {
        fmt.Println("Error removing directory:", err)
    } else {
        fmt.Println("Directory 'my_dir' removed.")
    }
}
```

#### `strings`和`strconv`包
```go
package main

import (
    "fmt"
    "strconv"
    "strings"
)

func main() {
    // strings 包
    s := "hello, world, go"
    fmt.Println("Contains 'world':", strings.Contains(s, "world"))
    fmt.Println("Replace 'o' with '0':", strings.ReplaceAll(s, "o", "0"))
    parts := strings.Split(s, ",")
    fmt.Println("Split by ',':", parts)
    fmt.Println("Join with '-':", strings.Join(parts, "-"))

    // strconv 包
    numStr := "123"
    num, err := strconv.Atoi(numStr) // string to int
    if err != nil {
        fmt.Println("Error converting string to int:", err)
    } else {
        fmt.Println("String to int:", num+1)
    }

    intStr := strconv.Itoa(456) // int to string
    fmt.Println("Int to string:", intStr + "789")

    fStr := "3.14"
    f, err := strconv.ParseFloat(fStr, 64) // string to float
    if err != nil {
        fmt.Println("Error converting string to float:", err)
    } else {
        fmt.Println("String to float:", f*2)
    }
}
```

#### `time`包
```go
package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now() // 获取当前时间
    fmt.Println("Current time:", now)
    fmt.Println("Year:", now.Year(), "Month:", now.Month(), "Day:", now.Day())

    // 格式化时间
    fmt.Println("Formatted time (YYYY-MM-DD HH:MM:SS):", now.Format("2006-01-02 15:04:05"))

    // 解析时间字符串
    t, err := time.Parse("2006-01-02", "2023-10-26")
    if err != nil {
        fmt.Println("Error parsing time:", err)
    } else {
        fmt.Println("Parsed time:", t)
    }

    // 时间间隔
    duration := 2 * time.Hour + 30 * time.Minute
    fmt.Println("Duration:", duration)

    // 时间计算
    future := now.Add(duration)
    fmt.Println("Time after duration:", future)

    // 定时器
    timer := time.NewTimer(1 * time.Second)
    <-timer.C // 阻塞直到1秒后
    fmt.Println("1 second passed!")

    // 周期性执行
    ticker := time.NewTicker(500 * time.Millisecond)
    done := make(chan bool)
    go func() {
        for {
            select {
            case <-done:
                return
            case t := <-ticker.C:
                fmt.Println("Tick at", t)
            }
        }
    }()
    time.Sleep(2 * time.Second)
    ticker.Stop()
    done <- true
    fmt.Println("Ticker stopped.")
}
```

## 2. 学习使用`net/http`包构建Web服务

### 知识点
*   **HTTP服务器：** `http.HandleFunc`注册路由，`http.ListenAndServe`启动服务器。
*   **HTTP客户端：** `http.Get`、`http.Post`、`http.Client`。
*   **请求和响应：** `http.Request`和`http.ResponseWriter`。
*   **路由：** 简单的路径匹配。

### 代码示例

#### HTTP服务器
```go
package main

import (
    "fmt"
    "net/http"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello, Go Web! You requested: %s\n", r.URL.Path)
}

func main() {
    http.HandleFunc("/", helloHandler) // 注册路由处理函数
    fmt.Println("Server listening on :8080...")
    err := http.ListenAndServe(":8080", nil) // 启动HTTP服务器
    if err != nil {
        fmt.Println("Server error:", err)
    }
}
```
**运行上述代码后，在浏览器访问 `http://localhost:8080` 和 `http://localhost:8080/anypath` 查看效果。**

#### HTTP客户端
```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
)

func main() {
    // 发送GET请求
    resp, err := http.Get("http://localhost:8080")
    if err != nil {
        fmt.Println("Error making GET request:", err)
        return
    }
    defer resp.Body.Close() // 确保关闭响应体

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        fmt.Println("Error reading response body:", err)
        return
    }
    fmt.Println("GET Response Status:", resp.Status)
    fmt.Println("GET Response Body:", string(body))

    // 假设有一个可以处理POST请求的服务器
    // resp, err = http.Post("http://localhost:8080/post", "application/json", bytes.NewBuffer([]byte(`{"name":"Go"}`)))
    // if err != nil {
    //     fmt.Println("Error making POST request:", err)
    //     return
    // }
    // defer resp.Body.Close()
    // fmt.Println("POST Response Status:", resp.Status)
}
```

## 3. 掌握`encoding/json`包进行JSON数据的编解码

### 知识点
*   **`json.Marshal`：** 将Go结构体编码为JSON字符串。
*   **`json.Unmarshal`：** 将JSON字符串解码为Go结构体。
*   **`json`标签：** 控制结构体字段在JSON中的名称、忽略字段等。

### 代码示例
```go
package main

import (
    "encoding/json"
    "fmt"
)

// User 结构体定义，包含json标签
type User struct {
    ID       int    `json:"id"`
    Username string `json:"username"`
    Email    string `json:"email,omitempty"` // omitempty表示如果字段为空值，则在JSON中忽略
    Password string `json:"-"`               // - 表示该字段不参与JSON编解码
}

func main() {
    // 编码 (Marshal)
    user1 := User{
        ID:       1,
        Username: "kilo",
        Email:    "kilo@example.com",
        Password: "secretpassword",
    }

    jsonData, err := json.Marshal(user1)
    if err != nil {
        fmt.Println("Error marshaling JSON:", err)
        return
    }
    fmt.Println("Marshaled JSON:", string(jsonData))

    // 解码 (Unmarshal)
    jsonString := `{"id":2, "username":"code", "email":"code@example.com"}`
    var user2 User
    err = json.Unmarshal([]byte(jsonString), &user2)
    if err != nil {
        fmt.Println("Error unmarshaling JSON:", err)
        return
    }
    fmt.Printf("Unmarshaled User: ID=%d, Username=%s, Email=%s, Password=%s\n",
        user2.ID, user2.Username, user2.Email, user2.Password)

    // 解码到 map[string]interface{}
    var rawMap map[string]interface{}
    json.Unmarshal([]byte(jsonString), &rawMap)
    fmt.Println("Unmarshaled to map:", rawMap)
}
```

## 4. 理解`context`包

### 知识点
*   **`context.Context`接口：** 用于在API边界之间传递截止日期、取消信号和其他请求范围的值。
*   **`context.Background()`：** 根Context，通常用于主函数、初始化和测试。
*   **`context.TODO()`：** 占位符Context，当不确定使用哪个Context时使用。
*   **`context.WithCancel()`：** 创建一个可取消的Context。
*   **`context.WithTimeout()`：** 创建一个带超时的Context。
*   **`context.WithValue()`：** 创建一个带值的Context。

### 代码示例
```go
package main

import (
    "context"
    "fmt"
    "time"
)

func worker(ctx context.Context, name string) {
    for {
        select {
        case <-ctx.Done(): // 监听取消信号
            fmt.Printf("Worker %s: Canceled, exiting.\n", name)
            return
        case <-time.After(500 * time.Millisecond):
            fmt.Printf("Worker %s: Working...\n", name)
        }
    }
}

func main() {
    // WithCancel 示例
    ctxCancel, cancel := context.WithCancel(context.Background())
    go worker(ctxCancel, "CancelWorker")
    time.Sleep(2 * time.Second)
    cancel() // 发送取消信号
    time.Sleep(1 * time.Second) // 等待worker退出

    fmt.Println("---")

    // WithTimeout 示例
    ctxTimeout, cancelTimeout := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancelTimeout() // 确保资源释放
    go worker(ctxTimeout, "TimeoutWorker")
    time.Sleep(4 * time.Second) // 等待超时

    fmt.Println("---")

    // WithValue 示例
    type favContextKey string
    faveKey := favContextKey("favorite-dish")
    ctxValue := context.WithValue(context.Background(), faveKey, "Pizza")

    processRequest(ctxValue)
}

func processRequest(ctx context.Context) {
    if dish, ok := ctx.Value(favContextKey("favorite-dish")).(string); ok {
        fmt.Printf("Processing request for favorite dish: %s\n", dish)
    } else {
        fmt.Println("Favorite dish not found in context.")
    }
}
```

## 5. 深入了解`go test`进行单元测试和基准测试

### 知识点
*   **测试文件命名：** `_test.go`结尾。
*   **测试函数：** `func TestXxx(t *testing.T)`。
*   **断言：** `t.Error`、`t.Errorf`、`t.Fatal`、`t.Fatalf`。
*   **基准测试：** `func BenchmarkXxx(b *testing.B)`。
*   **测试覆盖率：** `go test -cover`。

### 代码示例

#### 待测试的函数 (`math.go`)
```go
package math

// Add returns the sum of two integers.
func Add(a, b int) int {
    return a + b
}

// Subtract returns the difference between two integers.
func Subtract(a, b int) int {
    return a - b
}
```

#### 单元测试文件 (`math_test.go`)
```go
package math

import (
    "testing"
)

func TestAdd(t *testing.T) {
    result := Add(1, 2)
    expected := 3
    if result != expected {
        t.Errorf("Add(1, 2) = %d; want %d", result, expected)
    }

    result = Add(-1, 1)
    expected = 0
    if result != expected {
        t.Errorf("Add(-1, 1) = %d; want %d", result, expected)
    }
}

func TestSubtract(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 5, 3, 2},
        {"negative numbers", -5, -3, -2},
        {"zero result", 10, 10, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) { // 子测试
            result := Subtract(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Subtract(%d, %d) = %d; want %d", tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```
**运行测试：**
```bash
go test ./...         # 运行当前模块所有测试
go test -v ./...      # 运行所有测试并显示详细信息
go test -run TestAdd  # 运行指定测试函数
```

#### 基准测试文件 (`math_test.go`，与单元测试在同一文件或单独文件)
```go
package math

import (
    "testing"
)

func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(i, i+1)
    }
}

func BenchmarkSubtract(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Subtract(i*2, i)
    }
}
```
**运行基准测试：**
```bash
go test -bench=.      # 运行所有基准测试
go test -bench=BenchmarkAdd # 运行指定基准测试
```

## 6. 学习使用`go build`、`go run`、`go install`等命令

### 知识点
*   **`go run`：** 编译并运行Go源文件或包。
*   **`go build`：** 编译Go源文件或包，生成可执行文件。
*   **`go install`：** 编译并安装包或命令到`GOPATH/bin`（或`GOBIN`）目录。
*   **`go mod tidy`：** 清理和同步模块依赖。
*   **`go fmt`：** 格式化Go代码。
*   **`go vet`：** 检查Go代码中的常见错误。

### 命令行操作示例
假设您有一个`main.go`文件：
```go
// main.go
package main

import "fmt"

func main() {
    fmt.Println("Hello from Go command line!")
}
```

1.  **运行 Go 程序：**
    ```bash
    go run main.go
    ```

2.  **编译 Go 程序：**
    ```bash
    go build main.go
    # 这会在当前目录生成一个名为 main (Windows下为 main.exe) 的可执行文件
    # 可以指定输出文件名：go build -o myapp main.go
    ```

3.  **安装 Go 程序（通常用于命令行工具）：**
    ```bash
    go install
    # 这会将当前模块编译并安装到 $GOPATH/bin (或 $GOBIN) 目录下
    # 确保 $GOPATH/bin 在你的 PATH 环境变量中，这样就可以直接运行命令了
    ```

4.  **格式化代码：**
    ```bash
    go fmt ./... # 格式化当前目录及其子目录下的所有Go文件
    ```

5.  **检查潜在错误：**
    ```bash
    go vet ./...