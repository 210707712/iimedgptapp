def validate_and_reset_messages(messages):
    # 检查列表是否为空或第一个元素的role不是'system'
    if not messages or messages[0]['role'] != 'system':
        messages.clear()
        return messages

    # 获取messages中除了第一个元素以外的role列表
    actual_roles = [msg['role'] for msg in messages[1:]]

    # 检查剩余元素的role是否按'user'和'assistant'交替的顺序出现
    # 我们需要确保列表长度是奇数（因为第一个元素是'system'）
    # 并且从第二个元素开始，'user'和'assistant'交替
    if len(actual_roles) % 2 == 0 or not all(actual_roles[i] == 'user' and actual_roles[i + 1] == 'assistant' for i in range(0, len(actual_roles) - 1, 2)):
        messages.clear()

    return messages

# 示例使用
messages = [
    {'role': 'system', 'content': '你是一名医疗专业人员，遵循指令输出markdown格式文本'},
    {'role': 'user', 'content': '你好'},
    {'role': 'assistant', 'content': '您好！我是MedGPT...'},
    {'role': 'user', 'content': '你好'},
    {'role': 'assistant', 'content': '您好！我是MedGPT...'},
    {'role': 'user', 'content': '胃痛'},
    {'role': 'assistant', 'content': '您好！我是MedGPT...'},
    {'role': 'user', 'content': '胃痛'},
]

# 调用方法验证并重置
messages = validate_and_reset_messages(messages)

# 输出结果以验证
print(messages)