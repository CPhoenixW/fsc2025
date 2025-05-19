<template>
    <div class="login-wrapper">
        <div class="login-container">
            <h1 class="welcome-title">欢迎回来</h1>
            <form @submit.prevent="handleLogin" class="login-form">
                <div class="form-group">
                    <!-- 将 label 标签移到 input 标签之前 -->
                    <label for="username" class="input-label">用户名</label>
                    <input 
                        id="username"
                        v-model="username" 
                        type="text" 
                        required 
                        class="form-input"
                        placeholder="请输入用户名">
                </div>
                <div class="form-group">
                    <!-- 将 label 标签移到 input 标签之前 -->
                    <label for="password" class="input-label">密码</label>
                    <input 
                        id="password"
                        v-model="password" 
                        type="password" 
                        required 
                        class="form-input"
                        placeholder="请输入密码">
                </div>
                <button type="submit" class="login-btn">登 录</button>
                <p v-if="errorMessage" class="error-message">
                    ⚠️ {{ errorMessage }}
                </p>
                <div class="auth-links">
                    <router-link to="/register" class="link-item">
                        还没有帐户？<span class="link-text">立即注册</span>
                    </router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            username: '',
            password: '',
            errorMessage: ''
        }
    },
    methods: {
        async handleLogin() {
            try {
                console.log(this.username, this.password);
                const response = await axios.post("http://localhost:5000/api/login", {
                    username: this.username,
                    password: this.password
                });

                if (response.data.success) {
                    console.log(response.data.token);
                    localStorage.setItem("token", response.data.token); // ✅ 存储 JWT Token
                    this.$router.push("/content"); // ✅ 跳转到语音生成页面
                } else {
                    this.errorMessage = response.data.message; // 显示错误信息
                }
            } catch (error) {
                this.errorMessage = "登录失败，请检查用户名和密码";
                console.error("登录请求失败:", error);
            }
        }
    }
}
</script>

<style scoped>
.login-wrapper {
    min-height: 100vh;
    display: flex;
    align-items: center;
    backdrop-filter: blur(5px);
    justify-content: center;
    background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
        url('@/assets/bg1.jpg') center/cover;
}

.login-container {
    width: 400px;
    padding: 40px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    transform: translateY(-5%);
    transition: transform 0.3s ease;
}

.login-container:hover {
    transform: translateY(-8%);
}

.welcome-title {
    color: #34495e;
    font-size: 2.5em;
    margin-bottom: 40px;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.form-group {
    margin-bottom: 25px;
    display: flex;
    align-items: center;
}

.input-label {
    /* 修改为右外边距 */
    margin-left: -30px;
    color: #34495e;
    font-size: 16px;
    font-weight: 500px;
    /* 设置固定宽度，保证输入框对齐 */
    width: 90px;
    text-align: center;
}

.form-input {
    flex: 1;
    padding: 16px;
    border: 2px solid #bdc3c7;
    border-radius: 10px;
    font-size: 16px;
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.form-input:focus {
    border-color: #2980b9;
    box-shadow: 0 0 12px rgba(41, 128, 185, 0.3);
    outline: none;
}

.login-btn {
    width: 100%;
    padding: 16px;
    background: #2980b9;
    color: white;
    border: none;
    border-radius: 10px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(41, 128, 185, 0.2);
}

.login-btn:hover {
    background: #2471a3;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(41, 128, 185, 0.3);
}

.error-message {
    color: #e74c3c;
    background: #f2d7d5;
    padding: 12px;
    border-radius: 8px;
    margin: 20px 0;
    font-size: 14px;
    box-shadow: 0 2px 6px rgba(231, 76, 60, 0.1);
    text-align: center;
}

.auth-links {
    margin-top: 25px;
    text-align: center;
}

.link-item {
    color: #7f8c8d;
    font-size: 14px;
    text-decoration: none;
}

.link-text {
    color: #2980b9;
    font-weight: 500;
    transition: color 0.3s ease;
}

.link-text:hover {
    color: #2471a3;
    text-decoration: underline;
}
</style>