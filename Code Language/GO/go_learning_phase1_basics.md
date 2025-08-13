# Go语言学习计划 - 阶段1: Go语言基础

**目标：** 掌握Go语言的基础语法、开发环境搭建和基本程序结构。

**预计时间：** 2-3天

## 1. 搭建Go语言开发环境

### 知识点
*   **Go SDK安装：** 了解如何从Go官方网站下载并安装Go SDK。
*   **环境变量配置：** 配置`GOPATH`和`GOROOT`环境变量（Go 1.11+版本`GOPATH`重要性降低，但了解其概念仍有益）。
*   **IDE配置：** 推荐使用VS Code，并安装Go插件（如Go by Go Team）。

### 代码示例 (无需代码，仅为步骤说明)
1.  访问 [Go官方网站](https://golang.org/dl/) 下载对应操作系统的安装包。
2.  按照安装向导进行安装。
3.  验证安装成功：在终端输入 `go version`，应显示Go版本信息。
4.  在VS Code中安装Go插件。

## 2. 掌握Go语言基本语法

### 知识点
*   **程序结构：** `package main`、`import`、`func main()`。
*   **变量与常量：** 声明、初始化、类型推断、`var`、`const`、`iota`。
*   **数据类型：** 整型 (int, int8等)、浮点型 (float32, float64)、布尔型 (bool)、字符串 (string)。
*   **运算符：** 算术、关系、逻辑、位、赋值运算符。
*   **控制流语句：**
    *   `if/else if/else`：条件判断，支持短声明。
    *   `for`：Go语言中唯一的循环结构，可模拟while、range等。
    *   `switch`：多条件分支，支持类型判断，`fallthrough`。

### 代码示例

#### Hello World!
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, Go!")
}
```

#### 变量与常量
```go
package main

import "fmt"

func main() {
    // 变量声明与初始化
    var a int = 10
    var b = "Go语言" // 类型推断
    c := true         // 短声明，只能在函数内部使用

    fmt.Printf("a: %d, b: %s, c: %t\n", a, b, c)

    // 常量
    const PI float64 = 3.1415926
    const E = 2.718 // 类型推断
    fmt.Printf("PI: %f, E: %f\n", PI, E)

    // iota
    const (
        _  = iota // 0
        KB = 1 << (10 * iota) // 1 << 10 = 1024
        MB = 1 << (10 * iota) // 1 << 20
        GB = 1 << (10 * iota) // 1 << 30
    )
    fmt.Printf("KB: %d, MB: %d, GB: %d\n", KB, MB, GB)
}
```

#### 控制流语句
```go
package main

import "fmt"

func main() {
    // if/else
    if num := 10; num % 2 == 0 { // 短声明
        fmt.Println("10 是偶数")
    } else {
        fmt.Println("10 是奇数")
    }

    // for 循环
    sum := 0
    for i := 1; i <= 10; i++ {
        sum += i
    }
    fmt.Printf("1到10的和为: %d\n", sum)

    // for 模拟 while
    j := 0
    for j < 5 {
        fmt.Printf("%d ", j)
        j++
    }
    fmt.Println()

    // switch
    grade := "B"
    switch grade {
    case "A":
        fmt.Println("优秀")
    case "B", "C": // 多个case值
        fmt.Println("良好")
    case "D":
        fmt.Println("及格")
    default:
        fmt.Println("不及格")
    }

    // switch 类型判断
    var i interface{} = "hello"
    switch v := i.(type) {
    case int:
        fmt.Printf("i 是一个整数，值为 %d\n", v)
    case string:
        fmt.Printf("i 是一个字符串，值为 %s\n", v)
    default:
        fmt.Printf("i 是未知类型 %T\n", v)
    }
}
```

## 3. 理解函数

### 知识点
*   **函数定义与调用：** `func`关键字、参数、返回值。
*   **多返回值：** Go函数可以返回多个值，常用于返回结果和错误。
*   **命名返回值：** 提高可读性。
*   **匿名函数与闭包：** 作为参数、作为返回值、捕获外部变量。

### 代码示例

#### 基本函数与多返回值
```go
package main

import "fmt"

// greeting 函数，返回一个字符串
func greeting(name string) string {
    return "Hello, " + name + "!"
}

// divide 函数，返回商和余数
func divide(dividend, divisor int) (quotient, remainder int) {
    quotient = dividend / divisor
    remainder = dividend % divisor
    return // 自动返回命名返回值
}

func main() {
    fmt.Println(greeting("Kilo Code"))

    q, r := divide(10, 3)
    fmt.Printf("10除以3，商为%d，余数为%d\n", q, r)

    // 忽略返回值
    _, r2 := divide(10, 4)
    fmt.Printf("10除以4，余数为%d\n", r2)
}
```

#### 匿名函数与闭包
```go
package main

import "fmt"

func main() {
    // 匿名函数直接调用
    func() {
        fmt.Println("这是一个匿名函数")
    }()

    // 匿名函数赋值给变量
    add := func(a, b int) int {
        return a + b
    }
    fmt.Printf("1 + 2 = %d\n", add(1, 2))

    // 闭包
    // outer函数返回一个匿名函数，该匿名函数“记住”了outer函数中的x
    outer := func() func() int {
        x := 0
        return func() int {
            x++
            return x
        }
    }

    increment := outer()
    fmt.Println(increment()) // 1
    fmt.Println(increment()) // 2
    fmt.Println(increment()) // 3

    anotherIncrement := outer() // 再次调用outer，会创建新的x
    fmt.Println(anotherIncrement()) // 1
}
```

## 4. 学习包(package)和模块(module)的概念及使用

### 知识点
*   **包(Package)：** Go语言代码组织的基本单位，每个目录通常是一个包。`main`包是可执行程序的入口。
*   **导入包：** `import`关键字，路径规则。
*   **可见性规则：** 首字母大写表示可导出（public），小写表示私有（private）。
*   **模块(Module)：** Go 1.11+ 引入的依赖管理机制，用于管理项目依赖的版本。
*   **`go mod`命令：** `go mod init`、`go mod tidy`、`go mod download`等。

### 代码示例

#### 包的使用 (假设在`myproject/utils/math.go`和`myproject/main.go`中)

**`myproject/utils/math.go`:**
```go
package utils

// Add 函数，计算两个整数的和
func Add(a, b int) int {
    return a + b
}

// subtract 函数 (小写字母开头，私有函数)
func subtract(a, b int) int {
    return a - b
}
```

**`myproject/main.go`:**
```go
package main

import (
    "fmt"
    "myproject/utils" // 导入自定义包
)

func main() {
    result := utils.Add(5, 3)
    fmt.Printf("5 + 3 = %d\n", result)

    // 无法直接访问私有函数
    // fmt.Println(utils.subtract(5, 3)) // 编译错误
}
```

#### 模块的使用 (命令行操作)

1.  **初始化模块：**
    ```bash
    mkdir myproject
    cd myproject
    go mod init myproject # 或者 go mod init github.com/yourusername/myproject
    ```
    这会创建一个`go.mod`文件。

2.  **添加依赖（例如：一个流行的Web框架 Gin）：**
    ```bash
    go get github.com/gin-gonic/gin
    ```
    `go.mod`文件会被更新，`go.sum`文件会被创建。

3.  **编写代码使用依赖：**
    ```go
    // main.go
    package main

    import (
        "github.com/gin-gonic/gin"
        "net/http"
    )

    func main() {
        r := gin.Default()
        r.GET("/ping", func(c *gin.Context) {
            c.JSON(http.StatusOK, gin.H{
                "message": "pong",
            })
        })
        r.Run(":8080") // listen and serve on 0.0.0.0:8080
    }
    ```

4.  **整理依赖：**
    ```bash
    go mod tidy
    ```
    这会移除未使用的依赖，并添加缺少的依赖。

## 5. 完成简单的练习题

### 知识点
*   将所学的基础知识应用于实际问题。
*   培养独立解决问题的能力。

### 练习题示例
1.  **计算器：** 编写一个程序，接收两个数字和一个运算符（+,-,*,/），然后输出计算结果。
2.  **斐波那契数列：** 编写一个函数，生成斐波那契数列的前N项。
3.  **判断素数：** 编写一个函数，判断一个给定的整数是否为素数。