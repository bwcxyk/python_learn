import base64

string_to_encode = input("请输入要进行Base64编码的字符串：")
encoded_string = base64.b64encode(string_to_encode.encode('utf-8')).decode('utf-8')

print(encoded_string)