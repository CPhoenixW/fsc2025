<template>
    <div class="clone-container">
        <div class="header-section">
            <h1 class="title">你好，{{ username }}</h1>
            <p class="subtitle">请选择参考音频并输入文本生成克隆语音</p>
        </div>

        <!-- 步骤引导组件 -->
        <div class="steps-guide">
            <div class="step" :class="{ 'active': true, 'completed': selectedAudio }">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>选择参考音频</h3>
                    <p>选择您喜欢的声音</p>
                </div>
            </div>
            <div class="step-connector"></div>
            <div class="step" :class="{ 'active': selectedAudio, 'completed': selectedAudio && inputText }">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>输入文本</h3>
                    <p>输入想要转换的文字</p>
                </div>
            </div>
            <div class="step-connector"></div>
            <div class="step" :class="{ 'active': selectedAudio && inputText, 'completed': generatedAudioUrl }">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>生成语音</h3>
                    <p>等待AI克隆语音</p>
                </div>
            </div>
        </div>

        <div v-if="audioList.length === 0" class="no-audio">
            <div class="no-audio-icon">
                <i class="el-icon-microphone-off"></i>
            </div>
            <p>你还没有上传任何参考音频</p>
            <el-button type="primary" @click="goToManage" class="upload-button">
                <i class="el-icon-upload"></i> 上传音频
            </el-button>
        </div>

        <div v-else class="content-wrapper">
            <div class="audio-selection panel">
                <h3 class="panel-title">
                    <i class="el-icon-headset"></i> 选择参考音频
                </h3>
                
                <!-- 音频示例卡片组件 -->
                <div class="audio-cards" v-if="audioList.length > 0">
                    <div 
                        v-for="audio in audioList" 
                        :key="audio.id" 
                        class="audio-card"
                        :class="{ 'selected': selectedAudio && selectedAudio.id === audio.id }"
                        @click="selectedAudio = audio"
                    >
                        <div class="audio-card-icon">
                            <i class="el-icon-headset"></i>
                        </div>
                        <div class="audio-card-info">
                            <div class="audio-card-name">{{ audio.name }}</div>
                            <div class="audio-card-prompt">{{ audio.prompt }}</div>
                        </div>
                        <div class="audio-card-play">
                            <i class="el-icon-video-play"></i>
                        </div>
                    </div>
                </div>
                
                <div class="select-container">
                    <label for="audio-select">或从下拉列表选择：</label>
                    <select id="audio-select" v-model="selectedAudio" class="select-field">
                        <option v-for="audio in audioList" :key="audio.id" :value="audio"> {{ audio.name }} </option>
                    </select>
                </div>
            </div>

            <div v-if="selectedAudio" class="preview panel">
                <h3 class="panel-title">
                    <i class="el-icon-video-play"></i> 预览参考音频
                </h3>
                <div class="audio-wrapper">
                    <audio :src="`${baseURL}${selectedAudio.url}`" controls class="audio-player"></audio>
                </div>
                <div class="audio-info">
                    <div class="info-item">
                        <span class="label">声音名称:</span>
                        <span class="value">{{ selectedAudio.name }}</span>
                    </div>
                    <div class="info-item">
                        <span class="label">音频内容:</span>
                        <span class="value">{{ selectedAudio.prompt }}</span>
                    </div>
                </div>
            </div>

            <div class="text-input panel">
                <h3 class="panel-title">
                    <i class="el-icon-edit"></i> 输入要生成的文本
                </h3> 
                <textarea v-model="inputText" placeholder="请输入需要生成的文本" class="input-field"></textarea>
                <div class="text-counter" :class="{ 'warning': inputText.length > 200 }">
                    已输入 {{ inputText.length }} 个字符
                </div>
                
                <!-- 语音质量选择组件 -->
                <div class="quality-selector">
                    <h4>选择语音质量</h4>
                    <div class="quality-options">
                        <div 
                            class="quality-option" 
                            :class="{ 'active': voiceQuality === 'standard' }"
                            @click="voiceQuality = 'standard'"
                        >
                            <div class="quality-icon">
                                <el-icon><Check /></el-icon>
                            </div>
                            <div class="quality-info">
                                <div class="quality-title">标准质量</div>
                                <div class="quality-desc">生成较快，适合一般用途</div>
                            </div>
                        </div>
                        <div 
                            class="quality-option" 
                            :class="{ 'active': voiceQuality === 'high' }"
                            @click="voiceQuality = 'high'"
                        >
                            <div class="quality-icon">
                                <el-icon><Medal /></el-icon>
                            </div>
                            <div class="quality-info">
                                <div class="quality-title">高质量</div>
                                <div class="quality-desc">生成较慢，音质更佳</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="action-section">
                <button @click="generateSpeech" :disabled="!selectedAudio || !inputText || generatingAudio" class="action-button">
                    <el-icon><PromotionFilled /></el-icon>
                    {{ generatingAudio ? "正在生成..." : "生成语音" }}
                </button>
                <div v-if="generatingAudio" class="loading-animation">
                    <div class="loading-bar"></div>
                </div>
            </div>

            <div v-if="generatedAudioUrl" class="output panel">
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
                    <audio :src="generatedAudioUrl" :key="audioKey" controls class="audio-player"></audio>
                </div>
                <div class="action-buttons">
                    <a :href="generatedAudioUrl" download="cloned_voice.mp3" class="download-button">
                        <el-icon><Download /></el-icon> 下载语音
                    </a>
                    <button @click="resetGeneration" class="reset-button">
                        <el-icon><Refresh /></el-icon> 重新生成
                    </button>
                </div>
                
                <!-- 常见应用场景组件 -->
                <div class="usage-suggestions">
                    <h4>应用建议</h4>
                    <div class="suggestion-cards">
                        <div class="suggestion-card" @click="suggestUsage('视频配音')">
                            <el-icon><VideoCamera /></el-icon>
                            <p>视频配音</p>
                        </div>
                        <div class="suggestion-card" @click="suggestUsage('课件教学')">
                            <el-icon><Reading /></el-icon>
                            <p>课件教学</p>
                        </div>
                        <div class="suggestion-card" @click="suggestUsage('数字人合成')">
                            <el-icon><User /></el-icon>
                            <p>数字人合成</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <button class="back-button" @click="goBack">
            <el-icon><Back /></el-icon> 返回主页
        </button>
    </div>
</template>

<script>
import { jwtDecode } from "jwt-decode";
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue' 
import { Medal, Check, VideoCamera, Reading, User, Download, Refresh, Back, PromotionFilled } from '@element-plus/icons-vue'


export default {
    setup() {
        const router = useRouter();
        const username = ref("");
        const audioList = ref([]);
        const selectedAudio = ref(null);
        const inputText = ref("");
        const generatedAudioUrl = ref("");
        const baseURL = "http://localhost:5000";
        const audioKey = ref(0); // 确保每次生成的音频都会更新
        const generatingAudio = ref(false);
        const voiceQuality = ref("standard");
        
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

        const generateSpeech = async () => {
            if (!selectedAudio.value || !inputText.value) return;
            
            generatingAudio.value = true;
            
            try {
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
                        quality: voiceQuality.value, // 添加质量参数
                    }),
                });

                const data = await res.json();
                if (res.ok) {
                    generatedAudioUrl.value = `${baseURL}${data.audioUrl}?${Date.now()}`;
                    audioKey.value++; // 更新 key，确保音频重新加载
                    console.log("语音生成成功:", generatedAudioUrl.value);
                } else {
                    alert("语音生成失败：" + data.error);
                }
            } catch (error) {
                console.error("生成请求失败:", error);
                alert("生成请求发送失败，请检查网络连接");
            } finally {
                generatingAudio.value = false;
            }
        };
        
        const resetGeneration = () => {
            generatedAudioUrl.value = "";
            inputText.value = "";
        };
        
        const goToManage = () => {
            router.push("/manager/managePage");
        };

        const goBack = () => {
            router.push("/content");
        };
        
        const suggestUsage = (type) => {
            if (type === '视频配音') {
                router.push("/manager/digitPage");
            } else if (type === '课件教学') {
                router.push("/manager/audioPage");
            } else {
                alert("建议您尝试使用该音频进行" + type + "，获得更好的效果！");
            }
        };

        return {
            username,
            audioList,
            selectedAudio,
            inputText,
            generatedAudioUrl,
            generateSpeech,
            baseURL,
            audioKey,
            goBack,
            generatingAudio,
            resetGeneration,
            goToManage,
            voiceQuality,
            suggestUsage
        };
    },
};
</script>

<style scoped>
.clone-container {
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

.no-audio {
    text-align: center;
    padding: 48px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    color: #64748b;
    font-size: 1.125rem;
    width: 100%;
    max-width: 600px;
    margin: 2rem auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    position: relative;
    z-index: 1;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.no-audio-icon {
    font-size: 48px;
    color: #94a3b8;
    margin-bottom: 16px;
}

.upload-button {
    margin-top: 16px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    border: none;
    padding: 10px 20px;
    border-radius: 8px;
    color: white;
    font-weight: 500;
    transition: all 0.3s ease;
}

.upload-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

/* 音频卡片组件样式 */
.audio-cards {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}

.audio-card {
    background: #fff;
    border-radius: 12px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.audio-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.audio-card.selected {
    border-color: #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
}

.audio-card-icon {
    font-size: 2rem;
    color: #3b82f6;
    margin-bottom: 12px;
}

.audio-card-info {
    text-align: center;
    margin-bottom: 12px;
}

.audio-card-name {
    font-size: 1rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 4px;
}

.audio-card-prompt {
    font-size: 0.875rem;
    color: #64748b;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
}

.audio-card-play {
    font-size: 1.25rem;
    color: #3b82f6;
    opacity: 0;
    transition: all 0.3s ease;
}

.audio-card:hover .audio-card-play {
    opacity: 1;
}

.select-container {
    margin-top: 10px;
}

.select-container label {
    display: block;
    font-size: 0.875rem;
    color: #64748b;
    margin-bottom: 8px;
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

.audio-info {
    background: #f8fafc;
    padding: 12px;
    border-radius: 8px;
}

.info-item {
    display: flex;
    margin-bottom: 8px;
}

.info-item .label {
    font-weight: 600;
    color: #334155;
    width: 80px;
    flex-shrink: 0;
}

.info-item .value {
    color: #64748b;
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

/* 语音质量选择器样式 */
.quality-selector {
    margin-top: 24px;
    border-top: 1px solid #e2e8f0;
    padding-top: 20px;
}

.quality-selector h4 {
    font-size: 1rem;
    color: #334155;
    margin: 0 0 12px 0;
    font-weight: 600;
}

.quality-options {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.quality-option {
    padding: 16px;
    background: #f8fafc;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}

.quality-option:hover {
    background: #f1f5f9;
    transform: translateY(-2px);
}

.quality-option.active {
    border-color: #3b82f6;
    background: rgba(59, 130, 246, 0.05);
}

.quality-icon {
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

.quality-info {
    flex: 1;
}

.quality-title {
    font-size: 1rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 4px;
}

.quality-desc {
    font-size: 0.75rem;
    color: #64748b;
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

.action-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 16px;
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

/* 常见应用场景组件样式 */
.usage-suggestions {
    margin-top: 24px;
    border-top: 1px solid #e2e8f0;
    padding-top: 20px;
}

.usage-suggestions h4 {
    font-size: 1rem;
    color: #334155;
    margin: 0 0 12px 0;
    font-weight: 600;
}

.suggestion-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 12px;
}

.suggestion-card {
    background: #f8fafc;
    border-radius: 8px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.suggestion-card:hover {
    background: #f1f5f9;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.suggestion-card i {
    font-size: 1.5rem;
    color: #3b82f6;
}

.suggestion-card p {
    margin: 0;
    font-size: 0.875rem;
    color: #334155;
    font-weight: 500;
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
    .clone-container {
        padding: 16px;
    }
    
    .title {
        font-size: 2rem;
    }
    
    .panel {
        padding: 16px;
    }
    
    .no-audio {
        padding: 32px 16px;
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
    
    .quality-options {
        grid-template-columns: 1fr;
    }
    
    .suggestion-cards {
        grid-template-columns: repeat(2, 1fr);
    }
}
</style>