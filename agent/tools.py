def multiply(a:int ,b:int) ->int:
    return a*b

# 加法
def add(a:int,b:int) -> int:
    return a+b

ADD_TOOL = {
    "type":"function",
    "function":{
        "name":"add",
        "description":"计算两个整数的和。",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{
                    "type":"integer",
                    "description":"第一个整数",
                },
                "b":{
                    "type":"integer",
                    "description":"第二个整数",
                },
            },
            "required":["a","b"]
        },

    },
}

MULTIPLY_TOOL = {
    "type":"function",
    "function":{
        "name":"multiply",
        "description":"计算两个整数的乘积。",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{
                    "type":"integer",
                    "description":"第一个整数",
                },
                "b":{
                    "type":"integer",
                    "description":"第二个整数",
                },
            },
            "required":["a","b"]
        }
    }
}

TOOL_DEFINITION = [
    MULTIPLY_TOOL,
    ADD_TOOL,
]

TOOL_FUNCTION = {
    "multiply":multiply,
    "add":add,
}

if __name__ == "__main__":
    arguments = {"a":128,"b":998}
    result = add(**arguments)
    print("add执行结果",result)
    result = multiply(**arguments)
    print("工具参数：", arguments)
    print("执行结果：", result)