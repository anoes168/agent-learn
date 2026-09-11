def multiply(a:int ,b:int) ->int:
    return a*b

MULTIPLY_TOOL = {
    "type":"function",
    "function":"multiply",
    "description":"计算两个成绩。",
    "parameters":{
        "type":"object",
        "properties":{
            "a":{
                "type":"interger",
                "description":"第一个整数",
            },
            "b":{
                "type":"integer",
                "description":"第二个整数",
            },
            "required":["a","b"],
        },
    },
}

if __name__ == "__main__":
    arguments = {"a":128,"b":998}
    result = multiply(**arguments)
    print("工具参数：", arguments)
    print("执行结果：", result)