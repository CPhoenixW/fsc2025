<template>
    <div class="register-wrapper">
        <div class="register-container">
            <h1 class="welcome-title">用户注册</h1>
            <form @submit.prevent="register" class="register-form">
                <div class="form-group">
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
                    <label for="password" class="input-label">密码</label>
                    <input 
                        id="password"
                        v-model="password" 
                        type="password" 
                        required 
                        class="form-input"
                        placeholder="请输入密码">
                </div>
                <div class="form-group">
                    <label for="role" class="input-label">角色</label>
                    <select 
                        id="role"
                        v-model="role" 
                        class="form-input role">
                        <option value="user">user</option>
                        <option value="admin">admin</option>
                    </select>
                </div>
                <button type="submit" class="register-btn">注 册</button>
                <p v-if="message" :class="{'success-message': message.includes('注册成功')}" class="error-message">
                    ⚠️ {{ message }}
                </p>
                <div class="auth-links">
                    <router-link to="/login" class="link-item">
                        已经拥有帐户？<span class="link-text">立即登录</span>
                    </router-link>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    export default {
        data() {
            return {
                username: "",
                password: "",
                role: "user",
                message: "",
            };
        },
        methods: {
            async register() {
                if (!this.username || !this.password) {
                    this.message = "用户名和密码不能为空";
                    return;
                }

                try {
                    const response = await axios.post("http://localhost:5000/api/register", {
                        username: this.username,
                        password: this.password,
                        role: this.role,
                    });

                    if (response.data.success) {
                        this.message = "注册成功，跳转到登录...";
                        setTimeout(() => {
                            this.$router.push("/login");
                        }, 2000);
                    } else {
                        this.message = response.data.message;
                    }
                } catch (error) {
                    this.message = error.response?.data?.message || "注册失败";
                }
            },
        },
    };
</script>

<style scoped>
    .register-wrapper {
        min-height: 100vh;
        display: flex;
        align-items: center;
        backdrop-filter: blur(5px);
        justify-content: center;
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
            url('@/assets/bg1.jpg') center/cover;
    }


   .register-container {
        width: 400px;
        padding: 40px;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        transform: translateY(-5%);
        transition: transform 0.3s ease;
    }

   .register-container:hover {
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
        margin-left: -30px;
        color: #34495e;
        font-size: 16px;
        font-weight: 500px;
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

   .role {
        flex: 1;
        padding: 16px;
        border: 2px solid #bdc3c7;
        border-radius: 10px;
        font-size: 16px;
        transition: all 0.3s ease;
        box-sizing: border-box;
    }

   .role:focus {
        border-color: #2980b9;
        box-shadow: 0 0 12px rgba(41, 128, 185, 0.3);
        outline: none;
    }

   .register-btn {
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

   .register-btn:hover {
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

   .success-message {
        color: white;
        background: #4CAF50; /* 绿色背景 */
        box-shadow: 0 2px 6px rgba(76, 175, 80, 0.1);
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