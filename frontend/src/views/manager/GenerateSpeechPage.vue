<template>
  <div class="generate-container">
    <div class="header-section">
      <h1 class="title">文本转语音</h1>
      <p class="subtitle">请输入文本内容，选择合适的声音，生成高质量语音</p>
    </div>

    <!-- 步骤引导组件 -->
    <div class="steps-guide">
      <div class="step" :class="{ 'active': true, 'completed': inputText }">
        <div class="step-number">1</div>
        <div class="step-content">
          <h3>输入文本</h3>
          <p>输入想要转换的文字</p>
        </div>
      </div>
      <div class="step-connector"></div>
      <div class="step" :class="{ 'active': inputText, 'completed': inputText && voice }">
        <div class="step-number">2</div>
        <div class="step-content">
          <h3>选择声音</h3>
          <p>调整声音与语速</p>
        </div>
      </div>
      <div class="step-connector"></div>
      <div class="step" :class="{ 'active': inputText && voice, 'completed': audioUrl }">
        <div class="step-number">3</div>
        <div class="step-content">
          <h3>生成语音</h3>
          <p>等待AI生成语音</p>
        </div>
      </div>
    </div>

    <div class="content-wrapper">
      <div class="text-input panel">
        <h3 class="panel-title">
          <i class="el-icon-edit"></i> 输入要生成的文本
        </h3>
        <textarea 
          v-model="inputText" 
          placeholder="请输入需要生成的文本" 
          class="input-field"
        ></textarea>
        <div class="text-counter" :class="{ 'warning': inputText.length > 500 }">
          已输入 {{ inputText.length }} 个字符
        </div>
      </div>

      <div class="voice-settings panel">
        <h3 class="panel-title">
          <i class="el-icon-setting"></i> 语音设置
        </h3>
        
        <div class="voice-selector">
          <h4>选择声音</h4>
          <div class="voice-options">
            <div 
              v-for="option in ['中文女', '中文男', '英文女', '英文男', '粤语男','粤语女','日语男', '日语女', '韩语男','韩语女']" 
              :key="option"
              class="voice-option" 
              :class="{ 'active': voice === option }"
              @click="voice = option"
            >
              <div class="voice-icon">
                <el-icon><Microphone /></el-icon>
              </div>
              <div class="voice-name">{{ option }}</div>
            </div>
          </div>
        </div>
        
        <div class="speed-selector">
          <h4>语速调整</h4>
          <div class="speed-control">
            <span class="speed-icon slow"><i class="el-icon-arrow-left"></i></span>
            <el-slider v-model="speed" :min="0.25" :max="2" :step="0.01" class="slider-field"></el-slider>
            <span class="speed-icon fast"><i class="el-icon-arrow-right"></i></span>
          </div>
          <div class="speed-value">速度: X {{ speed.toFixed(2) }}</div>
        </div>
      </div>

      <div class="action-section">
        <button 
          @click="generateSpeech" 
          :disabled="!inputText || loading" 
          class="action-button"
        >
          <i class="el-icon-s-promotion"></i>
          {{ loading ? "正在生成..." : "生成语音" }}
        </button>
        <div v-if="loading" class="loading-animation">
          <div class="loading-bar"></div>
        </div>
      </div>

      <div v-if="audioUrl" class="output panel">
        <h3 class="panel-title">
          <i class="el-icon-success"></i> 生成的语音
        </h3>
        
        <!-- 结果可视化组件 -->
        <div class="result-visualization">
          <div class="waveform-container">
            <div class="waveform">
              <div class="bar" v-for="n in 30" :key="n" :style="{ height: (Math.random() * 70 + 30) + '%' }"></div>
            </div>
          </div>
        </div>
        
        <div class="audio-wrapper">
          <audio :src="`${baseURL}${audioUrl}?${Date.now()}`" ref="audioPlayer" controls class="audio-player"></audio>
        </div>
        
        <div class="action-buttons">
          <a :href="`${baseURL}${audioUrl}`" download="generated_voice.mp3" class="download-button">
            <i class="el-icon-download"></i> 下载语音
          </a>
          <button @click="resetGeneration" class="reset-button">
            <i class="el-icon-refresh"></i> 重新生成
          </button>
        </div>
      </div>
    </div>

    <button class="back-button" @click="back">
      <i class="el-icon-back"></i> 返回主页
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { jwtDecode } from "jwt-decode";
import { Microphone } from '@element-plus/icons-vue'

const router = useRouter();
const inputText = ref("");
const voice = ref("中文女");
const speed = ref(1);
const audioUrl = ref("");
const loading = ref(false);
const baseURL = "http://localhost:5000";
const audioPlayer = ref(null);
const username = ref("");

onMounted(() => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }
  try {
    const decoded = jwtDecode(token);
    username.value = decoded.username;
  } catch (error) {
    console.log("Token 解析失败", error);
    localStorage.removeItem("token");
    router.push("/login");
  }
});

const generateSpeech = async () => {
  if (!inputText.value) return;
  
  loading.value = true;
  /*await new Promise(resolve => setTimeout(resolve, 3000));
  audioUrl.value = "/static/audio/speech_-1374564094101821601.wav";
  loading.value = false;*/

  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("未登录");
      router.push("/login");
      return;
    }
    
    const response = await fetch(`${baseURL}/api/generate-speech`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": token,
      },
      body: JSON.stringify({
        text: inputText.value,
        voice: voice.value,
        speed: speed.value,
      }),
    });
    const data = await response.json();
    if (data.audioUrl) {
      audioUrl.value = data.audioUrl;
      console.log("语音生成成功:", audioUrl.value);

      if (audioPlayer.value) {
        audioPlayer.value.pause();
        audioPlayer.value.load();
        audioPlayer.value.play();
      }
    } else {
      alert(data.error || "语音生成失败");
    }
  } catch (error) {
    console.error("语音生成失败:", error);
    alert("生成请求发送失败，请检查网络连接");
  } finally {
    loading.value = false;
  }
};

const resetGeneration = () => {
  audioUrl.value = "";
  inputText.value = "";
};

const back = () => {
  router.push("/content");
};
</script>

<style scoped>
.generate-container {
  padding: 30px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f6f8fc 0%, #e9ecef 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.header-section {
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
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

/* 步骤引导样式 */
.steps-guide {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 700px;
  position: relative;
  z-index: 1;
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
  transform: scale(1.1);
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

.content-wrapper {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  z-index: 1;
}

.panel {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  padding: 24px;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.panel:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
}

.panel-title {
  font-size: 1.25rem;
  color: #334155;
  margin: 0 0 1rem 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.panel-title i {
  color: #3b82f6;
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
  margin-bottom: 8px;
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
}

.text-counter.warning {
  color: #f59e0b;
}

/* 语音选择器样式 */
.voice-selector, .speed-selector {
  margin-bottom: 24px;
}

.voice-selector h4, .speed-selector h4 {
  font-size: 1rem;
  color: #334155;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.voice-options {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 12px;
}

.voice-option {
  background: #f8fafc;
  border-radius: 8px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.voice-option:hover {
  background: #f1f5f9;
  transform: translateY(-2px);
}

.voice-option.active {
  border-color: #3b82f6;
  background: rgba(59, 130, 246, 0.05);
}

.voice-icon {
  font-size: 1.5rem;
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 8px;
}

.voice-name {
  font-size: 0.875rem;
  color: #334155;
  font-weight: 500;
}

.speed-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.speed-icon {
  font-size: 1.25rem;
  color: #64748b;
}

.speed-icon.slow {
  color: #3b82f6;
}

.speed-icon.fast {
  color: #ef4444;
}

.slider-field {
  flex: 1;
}

.speed-value {
  text-align: center;
  font-size: 0.9rem;
  color: #64748b;
  font-weight: 500;
  margin-top: 8px;
}

.action-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.action-button {
  width: 100%;
  max-width: 400px;
  padding: 14px 24px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
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
  max-width: 400px;
  height: 4px;
  background: #e2e8f0;
  margin-top: 12px;
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

/* 结果可视化组件样式 */
.result-visualization {
  margin-bottom: 20px;
}

.waveform-container {
  height: 80px;
  background: #f1f5f9;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 10px;
}

.waveform {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  height: 100%;
}

.waveform .bar {
  flex: 1;
  margin: 0 1px;
  background: linear-gradient(to top, #3b82f6, #93c5fd);
  border-radius: 2px;
  height: 60%;
  animation: equalizer 1.2s ease-in-out infinite alternate;
  animation-delay: calc(var(--i) * 0.1s);
}

@keyframes equalizer {
  0% {
    height: 20%;
  }
  100% {
    height: var(--random-height, 60%);
  }
}

.audio-wrapper {
  background: #f1f5f9;
  padding: 12px;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.audio-player {
  width: 100%;
  height: 40px;
}

.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.download-button, .reset-button {
  flex: 1;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
  min-width: 120px;
}

.download-button {
  background: #10b981;
  color: white;
  text-decoration: none;
  border: none;
}

.download-button:hover {
  background: #059669;
  transform: translateY(-2px);
}

.reset-button {
  background: #f1f5f9;
  color: #64748b;
  border: none;
  cursor: pointer;
}

.reset-button:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
}

.back-button {
  padding: 12px 24px;
  border-radius: 8px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 3rem;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.back-button:hover {
  background: #e2e8f0;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .generate-container {
    padding: 16px;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .panel {
    padding: 16px;
  }
  
  .action-buttons {
    flex-direction: column;
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
  
  .voice-options {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>