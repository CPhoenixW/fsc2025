<template>
    <div class="manage-container">
        <div class="header-section">
            <h1 class="title">你好，{{ username }}</h1>
            <p class="subtitle">管理你的参考音频</p>
            <el-avatar 
                :size="48" 
                :src="require('@/assets/logo2.png')"
                class="user-avatar"
            />
        </div>

        <!-- 步骤导航 -->
        <div class="tabs-navigation">
            <div class="tab-item" :class="{ 'active': activeTab === 'manage' }" @click="activeTab = 'manage'">
                <div class="tab-icon">
                    <el-icon><Headset /></el-icon>
                </div>
                <div class="tab-label">管理音频</div>
            </div>
            <div class="tab-item" :class="{ 'active': activeTab === 'upload' }" @click="activeTab = 'upload'">
                <div class="tab-icon">
                    <el-icon><Upload /></el-icon>
                </div>
                <div class="tab-label">上传音频</div>
            </div>
        </div>

        <!-- 管理音频面板 -->
        <div v-if="activeTab === 'manage'" class="manage-panel">
            <div class="panel-header">
                <h2 class="panel-title">
                    <el-icon><Headset /></el-icon> 我的音频
                </h2>
                <p class="panel-desc">管理已上传的参考音频</p>
            </div>

            <div v-if="audioList.length === 0" class="no-audio">
                <div class="no-audio-icon">
                    <el-icon><Mute /></el-icon>
                </div>
                <p>你还没有上传任何参考音频</p>
                <button @click="activeTab = 'upload'" class="upload-button">
                    <el-icon><Upload /></el-icon> 上传音频
                </button>
            </div>

            <div v-else class="audio-grid">
                <div v-for="audio in audioList" :key="audio.id" class="audio-card">
                    <div class="audio-card-header">
                        <h3 class="audio-name">{{ audio.name }}</h3>
                        <div class="audio-actions">
                            <button class="action-icon edit" @click="editAudio(audio)" title="编辑">
                                <el-icon><Edit /></el-icon>
                            </button>
                            <button class="action-icon delete" @click="deleteAudio(audio.id)" title="删除">
                                <el-icon><Delete /></el-icon>
                            </button>
                        </div>
                    </div>
                    
                    <div class="audio-waveform">
                        <div class="waveform">
                            <div class="bar" v-for="n in 20" :key="n" :style="{ height: (Math.random() * 70 + 30) + '%' }"></div>
                        </div>
                    </div>
                    
                    <div class="audio-player-wrapper">
                        <audio :src="`${baseURL}${audio.url}`" controls class="audio-player"></audio>
                    </div>
                    
                    <div class="audio-details">
                        <div class="detail-item">
                            <span class="detail-label">参考音频内容:</span>
                            <span class="detail-value">{{ audio.prompt }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 上传音频面板 -->
        <div v-if="activeTab === 'upload'" class="upload-panel panel">
            <div class="panel-header">
                <h2 class="panel-title">
                    <el-icon><Upload /></el-icon> 上传新音频
                </h2>
                <p class="panel-desc">上传用于声音克隆的参考音频</p>
            </div>

            <form @submit.prevent="uploadAudio" class="upload-form">
                <div class="form-group">
                    <label for="audio-name">音频名称</label>
                    <input 
                        type="text" 
                        id="audio-name" 
                        v-model="newAudioName" 
                        placeholder="请输入音频名称"
                        class="form-control"
                        required
                    >
                </div>
                
                <div class="form-group">
                    <label for="audio-prompt">参考音频内容描述</label>
                    <textarea 
                        id="audio-prompt" 
                        v-model="newPrompt" 
                        placeholder="请输入参考音频内容"
                        class="form-control textarea"
                        required
                    ></textarea>
                </div>
                
                <div class="upload-methods">
                    <div class="upload-method record" :class="{ 'active': uploadMethod === 'record' }" @click="uploadMethod = 'record'">
                        <div class="method-icon">
                            <el-icon><Microphone /></el-icon>
                        </div>
                        <div class="method-info">
                            <div class="method-title">录制音频</div>
                            <div class="method-desc">使用麦克风现场录制</div>
                        </div>
                    </div>
                    
                    <div class="upload-method file" :class="{ 'active': uploadMethod === 'file' }" @click="uploadMethod = 'file'">
                        <div class="method-icon">
                            <el-icon><Document /></el-icon>
                        </div>
                        <div class="method-info">
                            <div class="method-title">上传文件</div>
                            <div class="method-desc">选择本地音频文件</div>
                        </div>
                    </div>
                </div>
                
                <div v-if="uploadMethod === 'record'" class="record-controls">
                    <div class="record-status" :class="{ 'recording': isRecording }">
                        {{ isRecording ? '正在录音...' : '准备录制' }}
                    </div>
                    
                    <div class="record-buttons">
                        <button type="button" @click="startRecording" :disabled="isRecording" class="record-button start">
                            <el-icon><VideoPlay /></el-icon> 开始录音
                        </button>
                        <button type="button" @click="stopRecording" :disabled="!isRecording" class="record-button stop">
                            <el-icon><VideoPause /></el-icon> 停止录音
                        </button>
                    </div>
                    
                    <div v-if="audioURL" class="preview-section">
                        <h4 class="preview-title">预览录音</h4>
                        <div class="waveform-mini">
                            <div class="bar" v-for="n in 30" :key="n" :style="{ height: (Math.random() * 70 + 30) + '%' }"></div>
                        </div>
                        <audio :src="audioURL" controls class="audio-player"></audio>
                    </div>
                </div>
                
                <div v-if="uploadMethod === 'file'" class="file-upload">
                    <div class="file-drop-area" @dragover.prevent @drop.prevent="handleFileDrop">
                        <el-icon><Upload /></el-icon>
                        <p>拖放音频文件到此处，或</p>
                        <label for="file-upload" class="file-upload-btn">选择文件</label>
                        <input 
                            type="file" 
                            id="file-upload" 
                            @change="handleFileUpload" 
                            accept="audio/*" 
                            class="hidden-input"
                        >
                    </div>
                    <div v-if="newAudio" class="selected-file">
                        已选择: {{ newAudio.name }}
                    </div>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="submit-button" :disabled="!canUpload">
                        <el-icon><Upload /></el-icon> 上传音频
                    </button>
                </div>
            </form>
        </div>

        <button class="back-button" @click="back">
            <el-icon><Back /></el-icon> 返回主页
        </button>

        <!-- 修改弹窗 -->
        <el-dialog v-model="editMode" title="修改参考音频" width="500px" class="custom-dialog">
            <form @submit.prevent="saveEdit" class="edit-form">
                <div class="form-group">
                    <label for="edit-name">音频名称</label>
                    <input 
                        type="text" 
                        id="edit-name" 
                        v-model="editAudioName" 
                        placeholder="修改音频名称"
                        class="form-control"
                        required
                    >
                </div>
                
                <div class="form-group">
                    <label for="edit-prompt">声音特征描述</label>
                    <textarea 
                        id="edit-prompt" 
                        v-model="editPrompt" 
                        placeholder="修改声音特征描述"
                        class="form-control textarea"
                        required
                    ></textarea>
                </div>
                
                <div class="form-actions">
                    <button type="button" @click="cancelEdit" class="cancel-button">
                        <el-icon><Close /></el-icon> 取消
                    </button>
                    <button type="submit" class="submit-button">
                        <el-icon><Check /></el-icon> 保存修改
                    </button>
                </div>
            </form>
        </el-dialog>
    </div>
</template>

<script>
import { jwtDecode } from "jwt-decode";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { Headset, Upload, VideoPlay, VideoPause, Document, Microphone, Mute, Edit, Delete, Check, Close, Back } from '@element-plus/icons-vue';

export default {
    components: {
        Headset, Upload, VideoPlay, VideoPause, Document, 
        Microphone, Mute, Edit, Delete, Check, Close, Back
    },
    setup() {
        const router = useRouter();
        const username = ref("");
        const audioList = ref([]);
        const newAudio = ref(null);
        const newAudioName = ref("");
        const newPrompt = ref("");
        const editMode = ref(false);
        const baseURL = "http://localhost:5000";
        const activeTab = ref("manage");
        const uploadMethod = ref("record");

        const isRecording = ref(false);
        let mediaRecorder = null;
        let audioChunks = [];
        const audioBlob = ref(null);
        const audioURL = ref(null);

        const editPrompt = ref("");
        const editAudioName = ref("");
        const editAudioId = ref(null);

        const canUpload = computed(() => {
            if (!newAudioName.value || !newPrompt.value) return false;
            if (uploadMethod.value === 'record' && !audioBlob.value) return false;
            if (uploadMethod.value === 'file' && !newAudio.value) return false;
            return true;
        });

        const back = () => {
            router.push("/manager/indexPage");
        };

        onMounted(() => {
            const token = localStorage.getItem("token");
            if (!token) {
                router.push("/login");
                return;
            }
            try {
                const decoded = jwtDecode(token);
                username.value = decoded.username;
                fetchAudioList();
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
                
                if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);
                
                const data = await res.json();
                audioList.value = (data?.audioList || []).filter(Boolean);
            } catch (error) {
                console.error("获取音频列表失败:", error);
                audioList.value = [];
            }
        };

        const startRecording = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const blob = new Blob(audioChunks, { type: "audio/wav" });
                    audioBlob.value = blob;
                    audioURL.value = URL.createObjectURL(blob);
                };

                mediaRecorder.start();
                isRecording.value = true;
            } catch (error) {
                console.error("无法访问麦克风:", error);
                alert("无法访问麦克风，请检查权限");
            }
        };

        const handleFileUpload = (event) => {
            newAudio.value = event.target.files[0];
        };

        const handleFileDrop = (event) => {
            const files = event.dataTransfer.files;
            if (files.length > 0 && files[0].type.startsWith('audio/')) {
                newAudio.value = files[0];
            }
        };

        const stopRecording = () => {
            if (mediaRecorder) {
                mediaRecorder.stop();
                isRecording.value = false;
            }
        };

        const uploadAudio = async () => {
            if (!canUpload.value) {
                alert("请完成所有必填项");
                return;
            }

            const formData = new FormData();
            formData.append("name", newAudioName.value);
            formData.append("prompt", newPrompt.value);
            const token = localStorage.getItem("token");

            if (uploadMethod.value === 'file' && newAudio.value) {
                formData.append("audio", newAudio.value);
            } else if (uploadMethod.value === 'record' && audioBlob.value) {
                formData.append("audio_blob", audioBlob.value);
            }

            try {
                const res = await fetch(`${baseURL}/api/upload-audio`, {
                    method: "POST",
                    headers: { Authorization: token },
                    body: formData,
                });

                if (res.ok) {
                    await fetchAudioList();
                    newAudio.value = null;
                    audioBlob.value = null;
                    audioURL.value = null;
                    newAudioName.value = "";
                    newPrompt.value = "";
                    activeTab.value = "manage";
                } else {
                    alert("上传失败，请重试");
                }
            } catch (error) {
                console.error("上传失败:", error);
                alert("上传过程中发生错误，请检查网络连接");
            }
        };

        const deleteAudio = async (id) => {
            if (confirm("确定要删除这个音频吗？")) {
                const token = localStorage.getItem("token");
                try {
                    const res = await fetch(`${baseURL}/api/delete-audio/${id}`, {
                        method: "DELETE",
                        headers: { Authorization: token },
                    });
                    
                    if (res.ok) {
                        await fetchAudioList();
                    } else {
                        alert("删除失败，请重试");
                    }
                } catch (error) {
                    console.error("删除失败:", error);
                    alert("删除过程中发生错误，请检查网络连接");
                }
            }
        };

        const editAudio = (audio) => {
            editMode.value = true;
            editAudioName.value = audio.name;
            editPrompt.value = audio.prompt;
            editAudioId.value = audio.id;
        };

        const saveEdit = async () => {
            if (!editAudioName.value || !editPrompt.value) {
                alert("请完成所有必填项");
                return;
            }
            
            const token = localStorage.getItem("token");
            try {
                const res = await fetch(`${baseURL}/api/edit-audio/${editAudioId.value}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: token,
                    },
                    body: JSON.stringify({
                        name: editAudioName.value,
                        prompt: editPrompt.value,
                    }),
                });
                
                if (res.ok) {
                    editMode.value = false;
                    await fetchAudioList();
                } else {
                    alert("保存失败，请重试");
                }
            } catch (error) {
                console.error("修改失败:", error);
                alert("保存过程中发生错误，请检查网络连接");
            }
        };

        const cancelEdit = () => {
            editMode.value = false;
        };

        return {
            username,
            audioList,
            newAudioName,
            newPrompt,
            handleFileUpload,
            handleFileDrop,
            uploadAudio,
            deleteAudio,
            editAudio,
            editPrompt,
            editAudioName,
            saveEdit,
            cancelEdit,
            editMode,
            baseURL,
            isRecording,
            startRecording,
            stopRecording,
            audioURL,
            back,
            activeTab,
            uploadMethod,
            canUpload,
            newAudio
        };
    },
};
</script>

<style scoped>
.manage-container {
    padding: 30px;
    min-height: 100vh;
    background: linear-gradient(135deg, #f6f8fc 0%, #e9ecef 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
}

.header-section {
    text-align: center;
    margin-bottom: 2rem;
}

.title {
    font-size: 2.5rem;
    margin: 0 0 0.5rem 0;
    background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.subtitle {
    font-size: 1.125rem;
    color: #64748b;
    margin: 0;
}

/* 标签导航 */
.tabs-navigation {
    display: flex;
    gap: 20px;
    margin-bottom: 2rem;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    width: 100%;
    max-width: 700px;
    position: relative;
    z-index: 1;
}

.tab-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 18px 12px;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid transparent;
}

.tab-item:hover {
    background: rgba(241, 245, 249, 0.8);
    transform: translateY(-2px);
}

.tab-item.active {
    background: rgba(59, 130, 246, 0.08);
    border-color: rgba(59, 130, 246, 0.2);
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.tab-icon {
    font-size: 1.75rem;
    color: #3b82f6;
    margin-bottom: 10px;
    filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.2));
}

.tab-label {
    font-size: 1.125rem;
    font-weight: 600;
    color: #334155;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: -0.2px;
}

/* 面板样式 */
.manage-panel, .upload-panel {
    width: 100%;
    max-width: 900px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    padding: 24px;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.panel-header {
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.panel-title {
    font-size: 1.5rem;
    color: #1e293b;
    margin: 0 0 0.5rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.panel-desc {
    color: #64748b;
    margin: 0;
}

/* 空音频状态 */
.no-audio {
    text-align: center;
    padding: 48px;
    color: #64748b;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
}

.no-audio-icon {
    font-size: 48px;
    color: #94a3b8;
    margin-bottom: 8px;
}

.upload-button {
    padding: 14px 28px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 1.125rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.2px;
}

.upload-button:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
    background: linear-gradient(135deg, #4f8df9 0%, #2b70f8 100%);
}

.upload-button:active {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

/* 音频卡片网格 */
.audio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
}

.audio-card {
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    overflow: hidden;
    transition: all 0.3s ease;
}

.audio-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.audio-card-header {
    padding: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.audio-name {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1e293b;
    margin: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.audio-actions {
    display: flex;
    gap: 8px;
}

.action-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border: none;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.action-icon.edit {
    background: rgba(245, 158, 11, 0.15);
    color: #f59e0b;
}

.action-icon.edit:hover {
    background: rgba(245, 158, 11, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(245, 158, 11, 0.2);
}

.action-icon.delete {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
}

.action-icon.delete:hover {
    background: rgba(239, 68, 68, 0.25);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(239, 68, 68, 0.2);
}

.audio-waveform {
    padding: 16px;
    background: #f8fafc;
}

.waveform {
    height: 60px;
    display: flex;
    align-items: center;
    gap: 2px;
}

.waveform .bar {
    flex: 1;
    background: linear-gradient(to top, #3b82f6, #93c5fd);
    border-radius: 2px;
    height: 60%;
}

.audio-player-wrapper {
    padding: 16px;
}

.audio-player {
    width: 100%;
    height: 40px;
}

.audio-details {
    padding: 16px;
    border-top: 1px solid rgba(0, 0, 0, 0.05);
}

.detail-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.detail-label {
    font-size: 0.75rem;
    color: #64748b;
}

.detail-value {
    font-size: 0.875rem;
    color: #334155;
}

/* 上传表单 */
.upload-form {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-group label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #334155;
}

.form-control {
    padding: 12px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.form-control:hover {
    border-color: #cbd5e1;
}

.form-control:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.textarea {
    min-height: 100px;
    resize: vertical;
}

/* 上传方式选择 */
.upload-methods {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.upload-method {
    padding: 16px;
    border-radius: 12px;
    border: 2px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.upload-method:hover {
    transform: translateY(-2px);
    border-color: #cbd5e1;
    background: #f8fafc;
}

.upload-method.active {
    border-color: #3b82f6;
    background: rgba(59, 130, 246, 0.05);
}

.method-icon {
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

.method-info {
    flex: 1;
}

.method-title {
    font-size: 1rem;
    font-weight: 600;
    color: #334155;
    margin-bottom: 4px;
}

.method-desc {
    font-size: 0.75rem;
    color: #64748b;
}

/* 录音控件 */
.record-controls {
    padding: 16px;
    background: #f8fafc;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.record-status {
    text-align: center;
    font-size: 0.875rem;
    font-weight: 500;
    color: #64748b;
    padding: 8px;
    border-radius: 8px;
    transition: all 0.3s ease;
}

.record-status.recording {
    color: #ef4444;
    background: rgba(239, 68, 68, 0.1);
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {
        opacity: 0.7;
    }
    50% {
        opacity: 1;
    }
    100% {
        opacity: 0.7;
    }
}

.record-buttons {
    display: flex;
    gap: 12px;
}

.record-button {
    flex: 1;
    padding: 14px 16px;
    border-radius: 10px;
    font-size: 0.938rem;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    transition: all 0.3s ease;
    border: none;
    cursor: pointer;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
    font-family: 'Helvetica Neue', Arial, sans-serif;
}

.record-button.start {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
}

.record-button.start:hover:not(:disabled) {
    background: linear-gradient(135deg, #14c48c 0%, #06a574 100%);
    transform: translateY(-2px);
    box-shadow: 0 5px 12px rgba(16, 185, 129, 0.2);
}

.record-button.stop {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    color: white;
}

.record-button.stop:hover:not(:disabled) {
    background: linear-gradient(135deg, #f55858 0%, #e03a3a 100%);
    transform: translateY(-2px);
    box-shadow: 0 5px 12px rgba(239, 68, 68, 0.2);
}

.record-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

.preview-section {
    margin-top: 16px;
}

.preview-title {
    font-size: 0.875rem;
    color: #334155;
    margin: 0 0 8px 0;
}

.waveform-mini {
    height: 40px;
    display: flex;
    align-items: center;
    gap: 1px;
    margin-bottom: 8px;
}

.waveform-mini .bar {
    flex: 1;
    background: linear-gradient(to top, #10b981, #34d399);
    border-radius: 1px;
    height: 60%;
}

/* 文件上传 */
.file-upload {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.file-drop-area {
    padding: 32px;
    border: 2px dashed #cbd5e1;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    background: #f8fafc;
}

.file-drop-area:hover {
    border-color: #94a3b8;
    background: #f1f5f9;
}

.file-drop-area i {
    font-size: 2rem;
    color: #3b82f6;
}

.file-drop-area p {
    color: #64748b;
    margin: 0;
}

.file-upload-btn {
    display: inline-block;
    padding: 8px 16px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border-radius: 8px;
    font-size: 0.938rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 3px 8px rgba(59, 130, 246, 0.2);
    font-family: 'Helvetica Neue', Arial, sans-serif;
}

.file-upload-btn:hover {
    background: linear-gradient(135deg, #4f8df9 0%, #2b70f8 100%);
    transform: translateY(-2px);
    box-shadow: 0 5px 12px rgba(59, 130, 246, 0.3);
}

.hidden-input {
    display: none;
}

.selected-file {
    padding: 8px 12px;
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border-radius: 8px;
    font-size: 0.875rem;
}

/* 表单操作按钮 */
.form-actions {
    display: flex;
    gap: 12px;
    margin-top: 24px;
}

.submit-button {
    flex: 1;
    padding: 14px 28px;
    border-radius: 10px;
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    font-size: 1.125rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.2px;
}

.submit-button:hover:not(:disabled) {
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
    background: linear-gradient(135deg, #4f8df9 0%, #2b70f8 100%);
}

.submit-button:active:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.submit-button:disabled {
    background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
    cursor: not-allowed;
    box-shadow: none;
}

.cancel-button {
    padding: 14px 28px;
    border-radius: 10px;
    background: #f1f5f9;
    color: #64748b;
    border: 1px solid #e2e8f0;
    font-size: 1.125rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.2px;
}

.cancel-button:hover {
    background: #e2e8f0;
    transform: translateY(-2px);
    color: #334155;
}

.back-button {
    padding: 14px 28px;
    border-radius: 10px;
    background: #f8fafc;
    color: #64748b;
    font-size: 1.125rem;
    font-weight: 600;
    border: 1px solid #e2e8f0;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 1.5rem;
    display: flex;
    align-items: center;
    gap: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.2px;
}

.back-button:hover {
    background: #f1f5f9;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
    color: #334155;
}

/* 对话框 */
:deep(.custom-dialog) {
    border-radius: 16px;
    overflow: hidden;
}

.edit-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .manage-container {
        padding: 16px;
    }
    
    .title {
        font-size: 2rem;
    }
    
    .audio-grid {
        grid-template-columns: 1fr;
    }
    
    .upload-methods {
        grid-template-columns: 1fr;
    }
    
    .record-buttons {
        flex-direction: column;
    }
    
    .form-actions {
        flex-direction: column;
    }
}
</style>