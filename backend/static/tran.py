import base64
from pydub import AudioSegment
from io import BytesIO


def mp3_to_base64(file_path, duration=15):
    # 加载 MP3 文件
    audio = AudioSegment.from_mp3(file_path)

    # 截取前 `duration` 秒
    trimmed_audio = audio[:duration * 1000]  # pydub 以毫秒为单位

    # 将音频数据写入内存缓冲区
    buffer = BytesIO()
    trimmed_audio.export(buffer, format="mp3")

    # 获取 Base64 编码
    base64_audio = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return base64_audio


# 示例调用
file_path = "20250220_203951.mp3"  # 替换为你的 MP3 文件路径
base64_string = mp3_to_base64(file_path)
print(base64_string[:100])  # 仅打印前 100 个字符以查看结果
