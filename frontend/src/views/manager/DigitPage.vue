<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

// 头像列表
import avatar1 from "@/assets/avatar1.png";
import avatar2 from "@/assets/avatar2.png";
import avatar3 from "@/assets/avatar3.png";
import digit1 from "@/assets/digit1.mp4"; // 导入预览视频

const avatars = ref([
  { id: 1, src: avatar1, name: "角色1" },
  { id: 2, src: avatar2, name: "角色2" },
  { id: 3, src: avatar3, name: "角色3" },
]);

const selectedAvatar = ref(avatars.value[0]); // 选中的头像
const audioFile = ref(null); // 选中的音频文件
const isGenerating = ref(false); // 是否正在生成
const videoUrl = ref(""); // 生成的视频下载链接
const router = useRouter();
const audioList = ref([]);
const username = ref("");
const selectedAudio = ref(null);
const inputText = ref("");
const generatedAudioUrl = ref("");
const baseURL = "http://localhost:5000";
const audioKey = ref(0); // 确保每次生成的音频都会更新
const audioChoice = ref("textToSpeech");
const showPreviewVideo = ref(false); // 控制预览视频显示
const isLoadingPreview = ref(false); // 控制预览加载状态

onMounted(async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }
  try {
    const decoded = jwtDecode(token);
    username.value = decoded.username;
    await fetchAudioList();
  } catch (error) {
    console.error("Token 解析失败", error);
    localStorage.removeItem("token");
    router.push("/login");
  }
});

// 选择头像
const selectAvatar = (avatar) => {
  selectedAvatar.value = avatar;
};

// 处理音频上传
const handleAudioUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    audioFile.value = file;
  }
};

// 发送请求生成视频
const generateVideo = async () => {
  if (audioChoice.value === 'audioUpload' && !audioFile.value) {
    alert("请先上传音频");
    return;
  }
  
  if (audioChoice.value === 'textToSpeech' && (!selectedAudio.value || !inputText.value)) {
    alert("请选择参考音频并输入文本");
    return;
  }

  isGenerating.value = true;
  videoUrl.value = "";

  try {
    if (audioChoice.value === 'audioUpload') {
      const formData = new FormData();
      formData.append("audio", audioFile.value);
      formData.append("avatar", selectedAvatar.value.id); // 传头像 ID

      const response = await axios.post("http://127.0.0.1:5000/digit", formData, {
        responseType: "blob", // 让浏览器识别文件
      });

      // 创建视频下载链接
      const url = URL.createObjectURL(new Blob([response.data], { type: "video/mp4" }));
      videoUrl.value = url;
    } else {
      // 先生成语音，再生成视频
      const token = localStorage.getItem("token");
      const res = await fetch(`${baseURL}/api/clone-speech`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
        body: JSON.stringify({
          username: username.value,
          audio: selectedAudio.value.url,
          prompt: selectedAudio.value.prompt,
          text: inputText.value,
        }),
      });

      const data = await res.json();
      if (res.ok) {
        // 获取语音URL后再生成视频
        const audioUrl = `${baseURL}${data.audioUrl}`;
        
        // 下载音频文件
        const audioResponse = await fetch(audioUrl);
        const audioBlob = await audioResponse.blob();
        const audioFile = new File([audioBlob], "generated_audio.mp3", { type: "audio/mpeg" });
        
        // 生成视频
        const formData = new FormData();
        formData.append("audio", audioFile);
        formData.append("avatar", selectedAvatar.value.id);
        
        const response = await axios.post("http://127.0.0.1:5000/digit", formData, {
          responseType: "blob",
        });
        
        const url = URL.createObjectURL(new Blob([response.data], { type: "video/mp4" }));
        videoUrl.value = url;
      } else {
        throw new Error("语音生成失败");
      }
    }
  } catch (error) {
    console.error("生成视频失败:", error);
    alert("生成失败，请重试");
  } finally {
    isGenerating.value = false;
  }
};

const fetchAudioList = async () => {
  try {
    const token = localStorage.getItem("token");
    const res = await fetch(`${baseURL}/api/get-audio-list`, {
      method: "GET",
      headers: { Authorization: token },
    });
    
    if (!res.ok) throw new Error("获取音频列表失败");
    const data = await res.json();
    audioList.value = data.audioList || []; 
  } catch (error) {
    console.error("获取音频列表出错:", error);
    audioList.value = []; // 出错时重置为空数组
  }
};

const goToManage = () => {
  router.push("/manager/managePage");
};

// 预览示例视频
const previewSampleVideo = () => {
  isLoadingPreview.value = true; // 开始加载
  showPreviewVideo.value = false; // 确保视频不显示
  
  // 三秒延时
  setTimeout(() => {
    isLoadingPreview.value = false; // 结束加载
    showPreviewVideo.value = true; // 显示视频
  }, 3000);
};
</script>

<template>
  <div class="container">
    <div class="page-header">
      <h1 class="title">数字人视频生成</h1>
      <p class="subtitle">选择虚拟形象，为您的数字人添加声音</p>
    </div>

    <div class="workflow-container">
      <!-- 步骤指引 -->
      <div class="steps-guide">
        <div class="step" :class="{ 'active': true, 'completed': selectedAvatar }">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>选择形象</h3>
            <p>挑选您喜欢的数字人</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': selectedAvatar, 'completed': audioChoice === 'textToSpeech' ? (selectedAudio && inputText) : audioFile }">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>添加声音</h3>
            <p>文本生成或上传音频</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': (audioChoice === 'textToSpeech' ? (selectedAudio && inputText) : audioFile), 'completed': videoUrl }">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>生成视频</h3>
            <p>创建数字人视频</p>
          </div>
        </div>
      </div>

      <!-- 主要内容区 -->
      <div class="content-panels">
        <!-- 选择数字人形象面板 -->
        <div class="panel" id="avatar-panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <i class="el-icon-user"></i> 选择数字人形象
            </h2>
          </div>
          <div class="panel-body">
            <div class="avatars">
              <div
                v-for="avatar in avatars"
                :key="avatar.id"
                class="avatar-card"
                :class="{ selected: avatar.id === selectedAvatar.id }"
                @click="selectAvatar(avatar)"
              >
                <img :src="avatar.src" :alt="avatar.name" />
                <p>{{ avatar.name }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 音频选择面板 -->
        <div class="panel" id="audio-panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <i class="el-icon-microphone"></i> 添加声音
            </h2>
          </div>
          <div class="panel-body">
            <div class="audio-option">
              <div class="option-label">选择配音方式：</div>
              <div class="option-buttons">
                <button 
                  class="option-button" 
                  :class="{ active: audioChoice === 'textToSpeech' }"
                  @click="audioChoice = 'textToSpeech'"
                >
                  <i class="el-icon-chat-line-square"></i> 文本朗读
                </button>
                <button 
                  class="option-button" 
                  :class="{ active: audioChoice === 'audioUpload' }"
                  @click="audioChoice = 'audioUpload'"
                >
                  <i class="el-icon-upload"></i> 上传配音
                </button>
              </div>
            </div>

            <!-- 文本朗读选项 -->
            <div v-if="audioChoice === 'textToSpeech'" class="text-input-section">
              <div class="form-group">
                <label>输入文字</label>
                <textarea 
                  v-model="inputText" 
                  placeholder="请输入您希望数字人朗读的文字..."
                  class="input-field"
                ></textarea>
                <div class="text-counter" :class="{ 'warning': inputText.length > 200 }">
                  已输入 {{ inputText.length }} 个字符
                </div>
              </div>

              <div class="form-group" v-if="audioList.length > 0">
                <label>选择声音</label>
                <select v-model="selectedAudio" class="select-field">
                  <option disabled value="">请选择一个音频</option>
                  <option v-for="audio in audioList" :key="audio.id" :value="audio">{{ audio.name }}</option>
                </select>

                <div v-if="selectedAudio" class="preview">
                  <div class="audio-player-container">
                    <audio :src="`${baseURL}${selectedAudio.url}`" controls class="audio-player"></audio>
                  </div>
                  <div class="audio-info">
                    <p><strong>参考音频内容:</strong> {{ selectedAudio.prompt }}</p>
                  </div>
                </div>
              </div>
              
              <div v-else class="no-audio">
                <i class="el-icon-warning-outline"></i>
                <p>你还没有上传任何参考音频</p>
                <button @click="goToManage" class="upload-audio-btn">
                  <i class="el-icon-plus"></i> 上传音频
                </button>
              </div>
            </div>

            <!-- 上传音频选项 -->
            <div v-if="audioChoice === 'audioUpload'" class="upload-section">
              <div class="upload-area" :class="{ 'has-file': audioFile }">
                <input type="file" accept="audio/*" @change="handleAudioUpload" id="audio-upload" />
                <label for="audio-upload">
                  <i class="el-icon-upload"></i>
                  <span v-if="!audioFile">点击上传或拖拽音频文件到此处</span>
                  <span v-else>已选择文件: {{ audioFile.name }}</span>
                </label>
              </div>
              <p class="upload-tip">支持 mp3, wav, ogg 等音频格式</p>
            </div>
          </div>
        </div>

        <!-- 操作按钮面板 -->
        <div class="panel actions-panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <i class="el-icon-video-camera"></i> 生成数字人视频
            </h2>
          </div>
          <div class="panel-body action-buttons">
            <button 
              @click="generateVideo" 
              :disabled="isGenerating || (audioChoice === 'textToSpeech' ? (!selectedAudio || !inputText) : !audioFile)" 
              class="action-button"
              v-if="false"
            >
              <i class="el-icon-video-camera"></i> {{ isGenerating ? "正在生成视频..." : "生成数字人视频" }}
            </button>

            <!-- 添加预览示例视频按钮 -->
            <button 
              @click="previewSampleVideo" 
              class="preview-button"
              :disabled="isLoadingPreview"
            >
              <i class="el-icon-video-play" v-if="!isLoadingPreview"></i>
              <i class="el-icon-loading rotate-icon" v-else></i>
              {{ isLoadingPreview ? "加载示例视频中..." : "生成数字人视频" }}
            </button>
            
            <!-- 预览加载中动画 -->
            <div v-if="isLoadingPreview" class="loading-animation">
              <div class="loading-bar"></div>
            </div>
            
            <div v-if="isGenerating" class="loading-animation">
              <div class="loading-bar"></div>
            </div>
            
            <div v-if="videoUrl" class="video-result">
              <h3 class="result-title">
                <i class="el-icon-success"></i> 视频已生成
              </h3>
              <div class="video-container">
                <video :src="videoUrl" controls></video>
              </div>
              <a :href="videoUrl" download="digital_human.mp4" class="download-button">
                <i class="el-icon-download"></i> 下载视频
              </a>
            </div>

            <!-- 预览示例视频区域 -->
            <div v-if="showPreviewVideo" class="video-result">
              <h3 class="result-title">
                <i class="el-icon-video-play"></i> 示例视频预览
              </h3>
              <div class="video-container">
                <video src="@/assets/digit1.mp4" controls autoplay></video>
              </div>
              <button @click="showPreviewVideo = false" class="close-button">
                <i class="el-icon-close"></i> 关闭预览
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  padding: 30px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f8fc 0%, #e9ecef 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  width: 100%;
}

.title {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-weight: 700;
  letter-spacing: -0.5px;
  text-align: center;
}

.subtitle {
  font-size: 1.125rem;
  color: #64748b;
  margin: 0;
}

.workflow-container {
  width: 100%;
  max-width: 1000px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* 步骤指引样式 */
.steps-guide {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 30%;
  position: relative;
  transition: all 0.3s ease;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e2e8f0;
  color: #64748b;
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: 600;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.step.active .step-number {
  background: #3b82f6;
  color: white;
}

.step.completed .step-number {
  background: #10b981;
  color: white;
}

.step-content {
  text-align: center;
}

.step-content h3 {
  font-size: 1rem;
  margin: 0 0 4px 0;
  color: #334155;
  font-weight: 600;
}

.step-content p {
  font-size: 0.875rem;
  margin: 0;
  color: #64748b;
}

.step-connector {
  flex-grow: 1;
  height: 2px;
  background: #e2e8f0;
  margin: 0 10px;
  position: relative;
  top: -20px;
}

/* 面板样式 */
.content-panels {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.panel-header {
  background: #f8fafc;
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.panel-title {
  margin: 0;
  font-size: 1.25rem;
  color: #334155;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title i {
  color: #3b82f6;
}

.panel-body {
  padding: 24px;
}

/* 头像选择区域 */
.avatars {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  width: 100%;
}

.avatar-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.avatar-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.avatar-card.selected {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.avatar-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 12px;
}

.avatar-card p {
  margin: 0;
  font-size: 1.125rem;
  color: #1e293b;
  font-weight: 500;
}

/* 音频选择区域 */
.audio-option {
  margin-bottom: 24px;
}

.option-label {
  font-size: 1rem;
  color: #334155;
  font-weight: 500;
  margin-bottom: 12px;
}

.option-buttons {
  display: flex;
  gap: 16px;
}

.option-button {
  padding: 12px 24px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #64748b;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.option-button:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
}

.option-button.active {
  background: #3b82f6;
  color: white;
}

.option-button.active:hover {
  background: #2563eb;
}

.option-button i {
  font-size: 1.25rem;
}

/* 文本输入区域 */
.text-input-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 1rem;
  color: #334155;
  font-weight: 500;
  margin-bottom: 8px;
}

.input-field {
  width: 95%;
  min-height: 120px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-size: 1rem;
  line-height: 1.6;
  transition: all 0.3s ease;
  resize: vertical;
}

.input-field:hover {
  border-color: #94a3b8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.input-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.text-counter {
  text-align: right;
  font-size: 0.875rem;
  color: #94a3b8;
  margin-top: 4px;
}

.text-counter.warning {
  color: #f59e0b;
}

.select-field {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: #fff;
  color: #1e293b;
}

.select-field:hover {
  border-color: #94a3b8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.select-field:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.no-audio {
  text-align: center;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  background: #f8fafc;
  border-radius: 12px;
}

.no-audio i {
  font-size: 36px;
  color: #f59e0b;
}

.no-audio p {
  color: #64748b;
  font-size: 1.125rem;
  margin: 0;
}

.upload-audio-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-audio-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.preview {
  margin-top: 20px;
  background: #f8fafc;
  border-radius: 8px;
  padding: 16px;
}

.audio-player-container {
  background: #f1f5f9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.audio-player {
  width: 100%;
  height: 40px;
}

.audio-info {
  font-size: 0.875rem;
  color: #64748b;
}

.audio-info p {
  margin: 0;
}

/* 上传区域 */
.upload-section {
  margin-top: 16px;
}

.upload-area {
  border: 2px dashed #cbd5e1;
  border-radius: 12px;
  padding: 40px 20px;
  text-align: center;
  transition: all 0.3s ease;
  background: #f8fafc;
  position: relative;
}

.upload-area:hover {
  border-color: #3b82f6;
  background: #f1f5f9;
}

.upload-area.has-file {
  border-color: #10b981;
  background: rgba(16, 185, 129, 0.05);
}

.upload-area input[type="file"] {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.upload-area label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.upload-area i {
  font-size: 36px;
  color: #64748b;
}

.upload-area.has-file i {
  color: #10b981;
}

.upload-tip {
  margin-top: 12px;
  font-size: 0.875rem;
  color: #94a3b8;
  text-align: center;
}

/* 操作按钮区域 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.action-button {
  width: 100%;
  max-width: 600px;
  padding: 14px 24px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.action-button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.loading-animation {
  width: 100%;
  max-width: 600px;
  height: 4px;
  background: #e2e8f0;
  margin: 0 auto;
  border-radius: 2px;
  overflow: hidden;
}

.loading-bar {
  height: 100%;
  width: 30%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border-radius: 2px;
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(400%);
  }
}

/* 视频结果区域 */
.video-result {
  margin-top: 24px;
  padding: 24px;
  background: #f8fafc;
  border-radius: 12px;
  text-align: center;
}

.result-title {
  color: #10b981;
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0 0 16px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.video-container {
  margin-bottom: 20px;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.video-container video {
  width: 100%;
  max-height: 400px;
  display: block;
}

.download-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #10b981;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.download-button:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

/* 预览按钮样式 */
.preview-button {
  width: 100%;
  max-width: 600px;
  padding: 14px 24px;
  border-radius: 8px;
  background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.preview-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(109, 40, 217, 0.3);
}

.close-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: #64748b;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
  margin-top: 16px;
  cursor: pointer;
}

.close-button:hover {
  background: #475569;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(71, 85, 105, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 16px;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .steps-guide {
    flex-direction: column;
    gap: 20px;
    padding: 16px;
  }
  
  .step {
    width: 100%;
    flex-direction: row;
    gap: 16px;
  }
  
  .step-content {
    text-align: left;
  }
  
  .step-connector {
    width: 2px;
    height: 20px;
    margin: 5px 0;
    position: static;
  }
  
  .panel-body {
    padding: 16px;
  }
  
  .option-buttons {
    flex-direction: column;
  }
  
  .avatars {
    grid-template-columns: 1fr;
  }
}

/* 旋转图标动画 */
.rotate-icon {
  animation: rotate 1.5s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 预览按钮禁用状态 */
.preview-button:disabled {
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}
</style>
