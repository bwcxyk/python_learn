import base64
import io
from PIL import Image


def base64_to_file(base64_string, output_file_path):
    # 解码Base64字符串为字节数据
    bytes_data = base64.b64decode(base64_string)

    # 将字节数据写入文件
    with open(output_file_path, 'wb') as output_file:
        output_file.write(bytes_data)


def base64_to_image(base64_string, output_image_path):
    # 解码Base64字符串为字节数据
    bytes_data = base64.b64decode(base64_string)

    # 将字节数据读入PIL Image对象
    image = Image.open(io.BytesIO(bytes_data))

    # 保存Image对象为图片文件
    image.save(output_image_path)


# 示例用法
base64_string = "iVBORw0KG...Fgo="  # 这里填入您的Base64字符串
output_file_path = "output.txt"  # 输出文件路径
output_image_path = "output.png"  # 输出图片路径

# 转换为文件
base64_to_file(base64_string, output_file_path)
print("文件转换完成，已保存为:", output_file_path)

# 转换为图片
base64_to_image(base64_string, output_image_path)
print("图片转换完成，已保存为:", output_image_path)
