# Go语言学习计划 - 阶段2: Go语言核心特性

**目标：** 深入理解Go语言的复合数据类型、面向对象编程思想（通过结构体和接口）、以及错误处理机制。

**预计时间：** 3-5天

## 1. 深入理解数组(array)、切片(slice)和映射(map)

### 知识点
*   **数组 (Array)：** 固定长度、值类型、定义与初始化。
*   **切片 (Slice)：** 动态长度、引用类型、基于数组、定义、`make()`创建、`append()`、`copy()`、切片操作 (reslice)、容量 (capacity) 和长度 (length)。
*   **映射 (Map)：** 键值对集合、无序、引用类型、`make()`创建、增删改查、`len()`、`delete()`、判断键是否存在。

### 代码示例

#### 数组
```go
package main

import "fmt"

func main() {
    // 声明并初始化一个长度为5的整数数组
    var a [5]int
    a[0] = 10
    a[1] = 20
    fmt.Println("array a:", a) // 输出: array a: [10 20 0 0 0]

    // 声明时初始化
    b := [3]int{1, 2, 3}
    fmt.Println("array b:", b)

    // 自动推断长度
    c := [...]int{1, 2, 3, 4, 5}
    fmt.Println("array c:", c, "length:", len(c))
}
```

#### 切片
```go
package main

import "fmt"

func main() {
    // 从数组创建切片
    arr := [5]int{1, 2, 3, 4, 5}
    s := arr[1:4] // s 包含 arr[1], arr[2], arr[3]
    fmt.Printf("slice s: %v, len: %d, cap: %d\n", s, len(s), cap(s)) // cap是底层数组从切片起始元素到末尾的长度

    // 使用 make 创建切片
    s2 := make([]int, 3, 5) // 类型、长度、容量
    fmt.Printf("slice s2: %v, len: %d, cap: %d\n", s2, len(s2), cap(s2))

    // append 操作
    s2 = append(s2, 1, 2)
    fmt.Printf("slice s2 after append: %v, len: %d, cap: %d\n", s2, len(s2), cap(s2))

    // 当容量不足时，append会重新分配更大的底层数组
    s2 = append(s2, 3, 4, 5)
    fmt.Printf("slice s2 after more append: %v, len: %d, cap: %d\n", s2, len(s2), cap(s2))

    // copy 操作
    s3 := []int{10, 20, 30}
    s4 := make([]int, len(s3))
    copy(s4, s3) // 将s3的内容复制到s4
    fmt.Printf("slice s4 after copy: %v\n", s4)
}
```

#### 映射
```go
package main

import "fmt"

func main() {
    // 使用 make 创建 map
    m := make(map[string]int)

    // 添加元素
    m["apple"] = 1
    m["banana"] = 2
    m["orange"] = 3
    fmt.Println("map m:", m)

    // 获取元素
    fmt.Println("apple count:", m["apple"])

    // 判断键是否存在
    value, ok := m["grape"]
    if ok {
        fmt.Println("grape count:", value)
    } else {
        fmt.Println("grape not found")
    }

    // 删除元素
    delete(m, "banana")
    fmt.Println("map m after delete banana:", m)

    // 遍历 map
    for key, value := range m {
        fmt.Printf("key: %s, value: %d\n", key, value)
    }
}
```

## 2. 掌握结构体(struct)和方法(method)

### 知识点
*   **结构体 (Struct)：** 定义自定义类型，聚合不同类型的数据字段。
*   **匿名结构体：** 临时使用。
*   **结构体嵌套：** 模拟继承。
*   **方法 (Method)：** 带有接收者的函数，接收者可以是值类型或指针类型。
*   **值接收者 vs. 指针接收者：** 理解它们的区别和使用场景。

### 代码示例

#### 结构体
```go
package main

import "fmt"

// Person 结构体定义
type Person struct {
    Name    string
    Age     int
    City    string
}

// 定义一个匿名结构体
type AnonymousStruct struct {
    ID     int
    Name   string
}

func main() {
    // 创建 Person 结构体实例
    p1 := Person{"Alice", 30, "New York"}
    fmt.Println("Person 1:", p1)

    p2 := Person{Name: "Bob", Age: 25} // 部分字段初始化，未初始化的为零值
    fmt.Println("Person 2:", p2)

    // 访问和修改字段
    p1.Age = 31
    fmt.Println("Person 1 (updated age):", p1)

    // 匿名结构体
    anon := struct {
        ID   int
        Name string
    }{
        ID:   1,
        Name: "Temp User",
    }
    fmt.Println("Anonymous Struct:", anon)
}
```

#### 方法
```go
package main

import "fmt"

type Rectangle struct {
    Width  float64
    Height float64
}

// Area 是一个值接收者方法，不会修改 Rectangle 实例
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// Scale 是一个指针接收者方法，可以修改 Rectangle 实例
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}

func main() {
    rect := Rectangle{Width: 10, Height: 5}
    fmt.Printf("Initial Rectangle: Width=%.2f, Height=%.2f, Area=%.2f\n", rect.Width, rect.Height, rect.Area())

    rect.Scale(2) // 调用指针接收者方法
    fmt.Printf("Scaled Rectangle: Width=%.2f, Height=%.2f, Area=%.2f\n", rect.Width, rect.Height, rect.Area())
}
```

## 3. 理解接口(interface)

### 知识点
*   **接口定义：** 一组方法签名。
*   **隐式实现：** 任何类型只要实现了接口中定义的所有方法，就被认为实现了该接口。
*   **空接口 (empty interface{})：** 可以存储任何类型的值。
*   **类型断言 (Type Assertion)：** 判断接口变量底层存储的具体类型。
*   **类型选择 (Type Switch)：** 简化类型断言。

### 代码示例

#### 接口定义与实现
```go
package main

import "fmt"

// Shape 接口定义
type Shape interface {
    Area() float64
    Perimeter() float64
}

// Circle 结构体
type Circle struct {
    Radius float64
}

// Circle 实现 Shape 接口的 Area 方法
func (c Circle) Area() float64 {
    return 3.14159 * c.Radius * c.Radius
}

// Circle 实现 Shape 接口的 Perimeter 方法
func (c Circle) Perimeter() float64 {
    return 2 * 3.14159 * c.Radius
}

// Rectangle 结构体
type Rect struct {
    Width  float64
    Height float64
}

// Rect 实现 Shape 接口的 Area 方法
func (r Rect) Area() float64 {
    return r.Width * r.Height
}

// Rect 实现 Shape 接口的 Perimeter 方法
func (r Rect) Perimeter() float64 {
    return 2 * (r.Width + r.Height)
}

// Measure 函数接收一个 Shape 接口类型参数
func Measure(s Shape) {
    fmt.Printf("Type: %T, Area: %.2f, Perimeter: %.2f\n", s, s.Area(), s.Perimeter())
}

func main() {
    c := Circle{Radius: 5}
    r := Rect{Width: 4, Height: 6}

    Measure(c) // Circle 实现了 Shape 接口
    Measure(r) // Rect 实现了 Shape 接口
}
```

#### 空接口与类型断言
```go
package main

import "fmt"

func main() {
    var i interface{} // 声明一个空接口变量

    i = 10           // 存储一个整数
    fmt.Printf("Value: %v, Type: %T\n", i, i)

    i = "hello"      // 存储一个字符串
    fmt.Printf("Value: %v, Type: %T\n", i, i)

    // 类型断言
    s, ok := i.(string) // 断言 i 是否为 string 类型
    if ok {
        fmt.Printf("i 是一个字符串，值为: %s\n", s)
    } else {
        fmt.Println("i 不是一个字符串")
    }

    i = 123
    // 类型选择 (Type Switch)
    switch v := i.(type) {
    case int:
        fmt.Printf("i 是一个整数，值为: %d\n", v)
    case string:
        fmt.Printf("i 是一个字符串，值为: %s\n", v)
    default:
        fmt.Printf("i 是未知类型: %T\n", v)
    }
}
```

## 4. 学习Go语言的错误处理机制

### 知识点
*   **`error`接口：** Go语言内置的错误类型，任何实现了`Error() string`方法的类型都是`error`。
*   **多返回值模式：** 函数通常返回 (结果, error)。
*   **错误检查：** 始终检查函数返回的`error`，并进行相应处理。
*   **`defer`语句：** 确保函数退出时执行某些操作（如资源释放），无论是否发生错误。
*   **`panic`和`recover`：** `panic`用于不可恢复的错误，`recover`用于捕获`panic`并恢复程序执行（通常只在极少数情况下使用，如在`defer`函数中）。

### 代码示例

#### 错误处理
```go
package main

import (
    "errors"
    "fmt"
)

// Divide 函数，返回商和错误
func Divide(dividend, divisor float64) (float64, error) {
    if divisor == 0 {
        return 0, errors.New("除数不能为0") // 返回一个自定义错误
    }
    return dividend / divisor, nil
}

func main() {
    result, err := Divide(10, 2)
    if err != nil {
        fmt.Println("错误:", err)
    } else {
        fmt.Println("结果:", result)
    }

    result, err = Divide(10, 0)
    if err != nil {
        fmt.Println("错误:", err) // 会打印 "错误: 除数不能为0"
    } else {
        fmt.Println("结果:", result)
    }
}
```

#### defer 语句
```go
package main

import "fmt"

func main() {
    fmt.Println("开始执行")

    // defer 会在函数返回前执行
    defer fmt.Println("defer 1")
    defer fmt.Println("defer 2") // defer 语句按LIFO（后进先出）顺序执行

    fmt.Println("中间执行")
    // return 语句在 defer 语句之前执行
    // 但 defer 语句是在 return 语句执行后才执行
    // 如果有命名返回值，defer 可以修改命名返回值
    // 如果没有命名返回值，defer 无法修改匿名返回值
    // 请自行测试
    // return

    fmt.Println("结束执行")
}
```

#### panic 和 recover
```go
package main

import "fmt"

func main() {
    // recover 必须在 defer 函数中调用
    defer func() {
        if r := recover(); r != nil { // 捕获 panic
            fmt.Println("Recovered from panic:", r)
        }
    }()

    fmt.Println("Before panic")
    panic("Something went wrong!") // 触发 panic
    fmt.Println("After panic") // 这行代码不会被执行
}
```

## 5. 编写包含这些核心特性的中等难度程序

### 知识点
*   将所学核心特性融会贯通，应用于稍复杂的场景。
*   提升代码设计和组织能力。

### 练习题示例
1.  **学生管理系统：**
    *   使用结构体定义学生信息（姓名、年龄、学号、成绩）。
    *   使用切片存储学生列表。
    *   实现添加、删除、查找、更新学生信息的功能。
    *   使用函数和错误处理机制来处理无效输入或操作。
2.  **简易文件解析器：**
    *   读取一个文本文件（例如CSV文件）。
    *   解析文件内容，将每行数据存储到结构体切片中。
    *   实现按照某个字段进行过滤或排序的功能。
    *   处理文件不存在或文件格式错误等异常情况。