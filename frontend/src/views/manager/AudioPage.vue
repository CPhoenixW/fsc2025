<template>
  <div class="container">
    <div class="page-header">
      <h1 class="title">有声课件生成</h1>
      <p class="subtitle">将您的 PPT 转换为有声课件或视频</p>
    </div>
    
    <div class="workflow-container">
      <!-- 步骤指引 -->
      <div class="steps-guide">
        <div class="step" :class="{ 'active': activeStep >= 1, 'completed': pptPath }">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3>上传 PPT</h3>
            <p>支持 .ppt/.pptx 格式</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': activeStep >= 2, 'completed': selectedAudio }">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3>选择语音</h3>
            <p>选择参考音频</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': activeStep >= 3, 'completed': audioFiles.length > 0 }">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3>生成音频</h3>
            <p>将 PPT 转为语音</p>
          </div>
        </div>
        <div class="step-connector"></div>
        <div class="step" :class="{ 'active': activeStep >= 4, 'completed': videoUrl }">
          <div class="step-number">4</div>
          <div class="step-content">
            <h3>生成视频</h3>
            <p>获得最终成品</p>
          </div>
        </div>
      </div>

      <!-- 主要内容区 -->
      <div class="content-panels">
        <!-- 上传 PPT 面板 -->
        <div class="panel" id="upload-panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <i class="el-icon-upload"></i> 上传 PPT
            </h2>
          </div>
          <div class="panel-body">
            <el-upload
              class="upload-demo"
              action="/api/upload-ppt"
              :limit="1"
              :on-success="handleUploadSuccess"
              :before-upload="beforeUpload"
              :show-file-list="true"
              :file-list="fileList"
              name="ppt"
              drag
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">
                <em>点击上传</em> 或将文件拖拽到此处
                <div class="upload-tip">支持 .ppt/.pptx 格式，大小 3MB~20MB</div>
              </div>
            </el-upload>
            
            <div v-if="pptPath" class="upload-success">
              <i class="el-icon-success"></i>
              <span>PPT 上传成功，已解析 {{ slides.length }} 个文本片段</span>
            </div>
          </div>
        </div>

        <!-- 选择语音面板 -->
        <div class="panel" id="voice-panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <i class="el-icon-microphone"></i> 选择参考音频
            </h2>
          </div>
          <div class="panel-body">
            <div v-if="audioList.length === 0" class="no-audio">
              <i class="el-icon-warning-outline"></i>
              <p>你还没有上传任何参考音频</p>
              <el-button type="primary" @click="goToManage" class="upload-audio-btn">
                <i class="el-icon-plus"></i> 上传音频
              </el-button>
            </div>
            <div v-else class="audio-selection">
              <div class="select-wrapper">
                <label for="selectedAudio">选择声音:</label>
                <select v-model="selectedAudio" class="select-field" @change="activeStep = 2">
                  <option disabled value="">请选择一个音频</option>
                  <option v-for="audio in audioList" :key="audio.id" :value="audio">{{ audio.name }}</option>
                </select>
              </div>

              <div v-if="selectedAudio" class="preview">
                <h3 class="section-title">预览参考音频</h3>
                <div class="audio-player-container">
                  <audio :src="`${baseURL}${selectedAudio.url}`" controls class="audio-player"></audio>
                </div>
                <div class="audio-info">
                  <p><strong>参考音频内容:</strong> {{ selectedAudio.prompt }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 操作按钮面板 -->
        <div class="panel actions-panel">
          <div class="panel-header">
            <h2 class="panel-title">
              <i class="el-icon-video-camera"></i> 生成内容
            </h2>
          </div>
          <div class="panel-body action-buttons">
            <div class="action-group">
              <el-button 
                type="primary" 
                @click="generateAudio" 
                :disabled="!pptPath || !selectedAudio || isGeneratingAudio"
                :loading="isGeneratingAudio"
                class="action-button"
              >
                <i class="el-icon-headset"></i> {{ isGeneratingAudio ? "正在生成音频..." : "生成有声课件" }}
              </el-button>
              
              <el-button 
                type="success" 
                @click="generateVideo" 
                :disabled="!audioFiles.length || isGeneratingVideo"
                :loading="isGeneratingVideo"
                class="action-button"
              >
                <i class="el-icon-video-camera"></i> {{ isGeneratingVideo ? "正在生成视频..." : "生成视频" }}
              </el-button>
            </div>
            
            <div class="generated-content" v-if="audioFiles.length > 0 || videoUrl">
              <div class="content-links">
                <a v-if="audioFiles.length > 0" class="result-link" :href="downloadUrl" target="_blank" download>
                  <i class="el-icon-headset"></i> 下载有声课件
                </a>
                <a v-if="videoUrl" class="result-link video-link" :href="`http://localhost:5000/${videoUrl}`" target="_blank" download>
                  <i class="el-icon-video-camera"></i> 下载生成视频
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";
import { jwtDecode } from "jwt-decode";

export default {
  setup() {
    const selectedVoice = ref(""); // 选中的语音
    const pptPath = ref(""); // 上传的 PPT 路径
    const slides = ref([]); // PPT 解析出的文本
    const audioFiles = ref([]); // 生成的音频文件
    const downloadUrl = ref(""); // 下载有声 PPT 链接
    const videoUrl = ref(""); // 下载视频链接
    const isGeneratingAudio = ref(false);
    const isGeneratingVideo = ref(false);
    const fileList = ref([]); // 上传文件列表
    const audioList = ref([]);
    const router = useRouter();
    const username = ref("");
    const baseURL = "http://localhost:5000";
    const selectedAudio = ref(null);
    const generatedAudio = ref("");
    const audioKey = ref(0);
    const activeStep = ref(1);

    // 检查文件大小（3MB ~ 20MB）
    const beforeUpload = (file) => {
      if (file.size < 3 * 1024 * 1024 || file.size > 20 * 1024 * 1024) {
        alert("文件大小需在 3M ~ 20M 之间");
        return false;
      }
      return true;
    };

    // 上传成功回调
    const handleUploadSuccess = (response) => {
      console.log("上传成功", response);
      pptPath.value = response.ppt_path; // 后端返回的 PPT 文件路径
      slides.value = response.slides; // 解析出的 PPT 文本
      activeStep.value = 2;
    };
    
    // token认证
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
        console.log("Token 解析失败", error);
        localStorage.removeItem("token");
        router.push("/login");
      }
    });

    // 获取参考音频列表
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
        console.log("获取音频列表出错:", error);
        audioList.value = []; // 出错时重置为空数组
      }
    };
    
    // 生成音频
    const generateAudio = async () => {
      if (!pptPath.value || !slides.value || !selectedAudio.value) {
        alert("请先上传 PPT 并选择参考音频!");
        return;
      }
      isGeneratingAudio.value = true;
      activeStep.value = 3;
      
      try {
        const token = localStorage.getItem("token");
        const res = await fetch(`${baseURL}/api/clone-ppt`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: token,
          },
          body: JSON.stringify({
            username: username.value,
            audio: selectedAudio.value.url,
            prompt: selectedAudio.value.prompt,
            text: slides.value,
          }),
        });
        
        const data = await res.json();
        console.log(data);
        if (res.ok) {
          generatedAudio.value = data.audioUrls;
          audioKey.value++; // 更新 key，确保音频重新加载
          console.log("语音生成成功:", generatedAudio.value);
          audioFiles.value = generatedAudio.value;
        } else {
          alert("语音生成失败：" + data.error);
        }
      } catch (error) {
        console.error("生成请求失败:", error);
        alert("生成请求发送失败，请检查网络连接");
      } finally {
        isGeneratingAudio.value = false;
      }
    };

    // 生成视频
    const generateVideo = async () => {
      if (!audioFiles.value.length) {
        alert("请先生成音频！");
        return;
      }

      isGeneratingVideo.value = true;
      activeStep.value = 4;
      
      try {
        const res = await axios.post("/api/generate-video", {
          ppt_path: pptPath.value,
          audio_files: audioFiles.value,
        });

        if (res.data.video_url) {
          videoUrl.value = res.data.video_url;
          console.log("视频生成成功:", videoUrl.value);
        } else {
          alert("视频生成失败！");
        }
      } catch (error) {
        console.error("生成视频失败", error);
        alert("生成视频出错！");
      } finally {
        isGeneratingVideo.value = false;
      }
    };
    
    const goToManage = () => {
      router.push("/manager/managePage");
    };
    
    // 监听选择音频变化
    watch(selectedAudio, (newValue) => {
      if (newValue && activeStep.value < 3) {
        activeStep.value = 2;
      }
    });

    return {
      selectedVoice,
      pptPath,
      slides,
      audioFiles,
      downloadUrl,
      videoUrl,
      isGeneratingAudio,
      isGeneratingVideo,
      fileList,
      beforeUpload,
      handleUploadSuccess,
      generateAudio,
      generateVideo,
      audioList,
      selectedAudio,
      fetchAudioList,
      baseURL,
      username,
      activeStep,
      goToManage
    };
  },
};
</script>

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
  width: 22%;
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

/* 上传PPT区域样式 */
.upload-demo {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.upload-demo :deep(.el-upload-dragger) {
  width: 100%;
  height: auto;
  padding: 40px 20px;
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  background: #f8fafc;
  transition: all 0.3s ease;
}

.upload-demo :deep(.el-upload-dragger:hover) {
  border-color: #3b82f6;
  background: #f1f5f9;
}

.upload-demo :deep(.el-icon-upload) {
  font-size: 48px;
  color: #64748b;
  margin-bottom: 16px;
}

.el-upload__text {
  font-size: 1rem;
  color: #64748b;
}

.el-upload__text em {
  font-style: normal;
  color: #3b82f6;
  font-weight: 600;
}

.upload-tip {
  margin-top: 8px;
  font-size: 0.875rem;
  color: #94a3b8;
}

.upload-success {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #10b981;
  font-weight: 500;
}

.upload-success i {
  font-size: 1.25rem;
}

/* 选择语音区域样式 */
.no-audio {
  text-align: center;
  padding: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.no-audio i {
  font-size: 48px;
  color: #f59e0b;
}

.no-audio p {
  color: #64748b;
  font-size: 1.125rem;
  margin: 0;
}

.upload-audio-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.upload-audio-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.select-wrapper {
  margin-bottom: 20px;
}

.select-wrapper label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #334155;
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

.section-title {
  font-size: 1.125rem;
  color: #334155;
  margin: 0 0 12px 0;
  font-weight: 600;
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
  background: #f8fafc;
  padding: 12px;
  border-radius: 8px;
}

.audio-info p {
  margin: 0;
  color: #64748b;
}

/* 操作按钮区域样式 */
.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.action-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.action-button {
  flex: 1;
  min-width: 200px;
  padding: 14px 24px;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  transition: all 0.3s ease;
}

.action-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.generated-content {
  background: #f8fafc;
  padding: 16px;
  border-radius: 8px;
}

.content-links {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.result-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: #f1f5f9;
  border-radius: 8px;
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.result-link:hover {
  background: #e0f2fe;
  transform: translateY(-2px);
}

.video-link {
  color: #10b981;
}

.video-link:hover {
  background: #d1fae5;
}

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
  
  .action-group {
    flex-direction: column;
  }
}
</style>
