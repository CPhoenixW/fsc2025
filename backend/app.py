from flask import Flask, request, jsonify, send_from_directory
import os, requests, jwt, datetime, pptx
from flask_cors import CORS, cross_origin
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import sqlite3
from moviepy import *
import comtypes.client
import pythoncom
from PIL import Image

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# 🔐 配置 JWT
JWT_SECRET = "Phoenix W's jwt secret key"  # 这里换成更安全的密钥
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_SECONDS = 36000  # 1 小时

# 配置生成音频文件保存路径
AUDIO_FOLDER = os.path.join(app.root_path, 'static', 'audio')
if not os.path.exists(AUDIO_FOLDER):
    os.makedirs(AUDIO_FOLDER)

# 配置自定义音频文件保存路径
UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 配置生成视频文件保存路径
VIDEO_FOLDER = os.path.join(app.root_path, r"static\videos")
if not os.path.exists(VIDEO_FOLDER):
    os.makedirs(VIDEO_FOLDER)
# 配置 CosyVoice后端服务器地址
COSYVOICE_SERVER_URL = "http://localhost:5001"


# 📌 连接数据库
def get_db_connection():
    conn = sqlite3.connect("database.sqlite")
    conn.row_factory = sqlite3.Row
    return conn


# 🔒 自定义 Token 认证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401
        return f(*args, **kwargs)

    return decorated


# 🔒 从 Token 中获取用户名
def token_get(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded["username"]
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token!"}), 401


# ✅ 登录 API（生成 JWT Token）
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()

    if user is None:
        return jsonify({"success": False, "message": "用户不存在"}), 401
    if not check_password_hash(user["password"], password):
        return jsonify({"success": False, "message": "密码错误"}), 401
    token_payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_SECONDS)
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return jsonify({"success": True, "message": "登录成功", "token": token})


# ✅ 注册 API（存储加密密码）
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

    if user:
        conn.close()
        return jsonify({"success": False, "message": "用户名已存在"}), 409

    hashed_password = generate_password_hash(password)
    conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                 (username, hashed_password, role))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "注册成功"}), 201


# ✅ 获取自定义声音列表 API
@app.route("/api/get-audio-list", methods=["GET"])
def get_audio_list():
    token = request.headers.get("Authorization")
    username = token_get(token)
    if not username:
        return jsonify({"error": "Invalid token"}), 401

    conn = get_db_connection()
    cursor = conn.execute("SELECT id, file_path, prompt, voice_name FROM audios WHERE username = ?", (username,))
    audios = [
        {"id": row["id"], "url": f"/uploads/{row['file_path']}", "prompt": row["prompt"], "name": row["voice_name"]} for
        row in cursor.fetchall()]
    conn.close()

    return jsonify({"audioList": audios})


# ✅ 上传自定义声音 API
@app.route("/api/upload-audio", methods=["POST"])
def upload_audio():
    token = request.headers.get("Authorization")
    username = token_get(token)
    if not username:
        return jsonify({"error": "Invalid token"}), 401

    # 如果上传的是文件
    file = request.files.get("audio")
    # 如果上传的是录音 blob（audioBlob）
    audio_blob = request.files.get("audio_blob")

    prompt = request.form.get("prompt")
    name = request.form.get("name")
    
    if not prompt or not name:
        return jsonify({"error": "Missing prompt or name"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
    elif audio_blob:
        # 处理录音 blob 数据
        filename = "recorded_audio.wav"  # 您可以根据需要修改文件名
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(file_path, "wb") as f:
            f.write(audio_blob.read())  # 将 audioBlob 数据保存为文件
    else:
        return jsonify({"error": "Missing file or audio blob"}), 400

    # 保存音频信息到数据库
    conn = get_db_connection()
    conn.execute("INSERT INTO audios (username, file_path, prompt, voice_name) VALUES (?, ?, ?, ?)",
                 (username, filename, prompt, name))
    conn.commit()
    conn.close()

    return jsonify({"message": "Upload successful"})


# ✅ 删除自定义声音 API
@app.route("/api/delete-audio/<int:audio_id>", methods=["DELETE"])
def delete_audio(audio_id):
    token = request.headers.get("Authorization")
    username = token_get(token)
    if not username:
        return jsonify({"error": "Invalid token"}), 401

    conn = get_db_connection()
    conn.execute("DELETE FROM audios WHERE id = ? AND username = ?", (audio_id, username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Deleted successfully"})


# ✅ 编辑自定义声音 API
@app.route("/api/edit-audio/<int:audio_id>", methods=["PUT"])
def edit_audio(audio_id):
    token = request.headers.get("Authorization")
    username = token_get(token)
    if not username:
        return jsonify({"error": "Invalid token"}), 401

    data = request.get_json()
    new_prompt = data.get("prompt")

    conn = get_db_connection()
    conn.execute("UPDATE audios SET prompt = ? WHERE id = ? AND username = ?", (new_prompt, audio_id, username))
    conn.commit()
    conn.close()

    return jsonify({"message": "Updated successfully"})


# ✅ 生成声音文件 API
@app.route("/api/generate-speech", methods=["POST"])
@token_required
def generate_speech():
    data = request.get_json()
    url = COSYVOICE_SERVER_URL + '/generate-speech'
    response = requests.post(url, json=data)
    return jsonify(response.json()), response.status_code


# ✅ 生成声音文件 API
@app.route("/api/clone-speech", methods=["POST"])
@token_required
def clone_speech():
    data = request.get_json()
    url = COSYVOICE_SERVER_URL + '/clone-speech'
    response = requests.post(url, json=data)
    return jsonify(response.json()), response.status_code


# ✅ 生成声音文件 API
@app.route("/api/clone-ppt", methods=["POST"])
@token_required
def clone_ppt():
    data = request.get_json()
    url = COSYVOICE_SERVER_URL + '/clone-ppt'
    response = requests.post(url, json=data)
    return jsonify(response.json()), response.status_code


# ✅ 获取声音文件
@app.route("/static/audio/<filename>")
# @token_required
def get_audio(filename):
    return send_from_directory("static/audio", filename)


# ✅ 获取声音文件
@app.route("/uploads/<filename>")
# @token_required
def gets_audio(filename):
    return send_from_directory("uploads", filename)


# 📌 解析 PPT 文本内容
def extract_text_from_ppt(ppt_path):
    ppt = pptx.Presentation(ppt_path)
    slides_text = []
    for slide in ppt.slides:
        text = "\n".join([shape.text for shape in slide.shapes if hasattr(shape, "text")])
        slides_text.append(text)
    print(len(slides_text))
    return slides_text


# ✅ 上传 PPT 课件
@app.route("/api/upload-ppt", methods=["POST"])
def upload_ppt():
    file = request.files.get("ppt")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    ppt_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(ppt_path)

    slides_text = extract_text_from_ppt(ppt_path)
    print(slides_text)
    return jsonify({"message": "Upload successful", "slides": slides_text, "ppt_path": filename})


# ✅ 生成语音（每页 PPT 对应一个音频）
@app.route("/api/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json()
    ppt_path = data.get("ppt_path")
    selected_voice = data.get("voice")  # 选定的声音样本
    slides_text = data.get("slides")

    if not ppt_path or not slides_text:
        return jsonify({"error": "Missing parameters"}), 400

    audio_files = []
    for idx, text in enumerate(slides_text):
        response = requests.post(f"{COSYVOICE_SERVER_URL}/generate-speech",
                                 json={"text": text, "voice": selected_voice})
        if response.status_code == 200:
            audio_filename = f"audio_slide_{idx + 1}.mp3"
            audio_path = os.path.join(AUDIO_FOLDER, audio_filename)
            with open(audio_path, "wb") as f:
                f.write(response.content)
            audio_files.append(audio_filename)
        else:
            return jsonify({"error": "Speech synthesis failed"}), 500

    return jsonify({"message": "Audio generated", "audio_files": audio_files})


def convert_ppt_to_images(ppt_path, output_folder):
    """使用 PowerPoint 将 PPT/PPTX 转换为 PNG"""
    pythoncom.CoInitialize()
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 启动 PowerPoint
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1  # 让 PowerPoint 运行但不显示界面

    # 打开 PPT 文件
    presentation = powerpoint.Presentations.Open(ppt_path, WithWindow=False)

    # 以 PNG 格式导出幻灯片
    presentation.SaveAs(output_folder, 17)  # 17 表示导出为 PNG
    presentation.Close()  # 关闭 PPT
    powerpoint.Quit()  # 退出 PowerPoint

    # 获取导出的 PNG 图片
    images = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith(".JPG")]
    images.sort()  # 确保图片按顺序排列
    print(images)
    return images


def resize_image(img_path, height):
    """使用 Pillow 调整图片大小"""
    img = Image.open(img_path)
    width, orig_height = img.size
    new_width = int(width * height / orig_height)
    img_resized = img.resize((new_width, height))

    # 保存调整后的图片
    resized_path = img_path.replace(".png", "_resized.png")
    img_resized.save(resized_path)
    return resized_path


@app.route("/api/generate-video", methods=["POST"])
def generate_video():
    data = request.get_json()
    ppt_path = os.path.join(UPLOAD_FOLDER, data.get("ppt_path"))
    audio_files = [r"E:/Program/fcs/project3.29/backend" + f for f in data.get("audio_files")]

    # 1. 将 PPT 幻灯片转换为图片
    image_folder = os.path.join(UPLOAD_FOLDER, "slides")
    image_paths = convert_ppt_to_images(ppt_path, image_folder)

    if len(image_paths) != len(audio_files):
        print(len(image_paths), len(audio_files))
        return jsonify({"error": "幻灯片数量和音频文件数量不匹配！"}), 400

    # 2. 创建视频片段
    video_clips = []
    for idx, img_path in enumerate(image_paths):
        # 调整图像大小
        resized_img_path = resize_image(img_path, height=720)
        print(f"音频路径: {audio_files[idx]}, 是否存在: {os.path.exists(audio_files[idx])}")
        # 加载音频文件
        audio_clip = AudioFileClip(audio_files[idx])

        # 使用调整后的图片创建视频片段
        img_clip = ImageClip(resized_img_path).with_duration(audio_clip.duration)

        # 将音频加入视频
        video_clips.append(img_clip.with_audio(audio_clip))

    # 3. 合成最终视频
    final_video = concatenate_videoclips(video_clips, method="compose")
    video_filename = "final_presentation.mp4"
    final_video_path = os.path.join(VIDEO_FOLDER, video_filename)
    final_video.write_videofile(final_video_path, fps=24)

    return jsonify({"message": "视频生成成功！", "video_url": rf"\static\videos\{video_filename}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

