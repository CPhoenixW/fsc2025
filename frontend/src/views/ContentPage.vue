<template>
  <div>
    <el-container style="height: 100vh;margin: 0; padding: 0;">
      
      <!-- 侧边栏优化 -->
      <el-aside class="m-aside">
        <div class="m-sysName">
          <img src="@/assets/logo2.png" alt="logo" class="sidebar-logo">
          <span class="m-nameText">AI语音教学系统</span>
        </div>
        <!-- 优化菜单图标和间距 -->
        <el-menu 
          class="el-menu"
          :default-active="$route.path" 
          router
          active-text-color="#409EFF"
          text-color="#b0bac3"
        >
          <el-sub-menu index="home">
            <template #title>
              <el-icon :size="24"><User /></el-icon> <!-- 加大图标尺寸 -->
              <span class="menu-text">系统首页</span>
            </template>
            <el-menu-item index="/manager/indexPage">
              <template #title>
                <span class="sub-menu-text">数据概览</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/manager/personPage">
              <template #title>
                <span class="sub-menu-text">个人中心</span>
              </template>
            </el-menu-item>
          </el-sub-menu>

          <el-sub-menu index="voice">
            <template #title>
              <el-icon :size="24"><Microphone /></el-icon> <!-- 加大图标尺寸 -->
              <span class="menu-text">语音管理</span>
            </template>
            <el-menu-item index="/manager/generate">
              <template #title>
                <span class="sub-menu-text">文本生成音频</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/manager/clone">
              <template #title>
                <span class="sub-menu-text">音色克隆生成</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/manager/managePage">
              <template #title>
                <span class="sub-menu-text">音频库管理</span>
              </template>
            </el-menu-item>
            
          

          </el-sub-menu>

          <el-sub-menu index="teach">
            <template #title>
              <el-icon :size="24"><User /></el-icon> <!-- 加大图标尺寸 -->
              <span class="menu-text">教学管理</span>
            </template>
            <el-menu-item index="/manager/audio">
              <template #title>
                <span class="sub-menu-text">有声课件制作</span>
              </template>
            </el-menu-item>
            <el-menu-item index="/manager/digit">
              <template #title>
                <span class="sub-menu-text">数字人教学</span>
              </template>
            </el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <!-- 右侧容器优化 -->
      <el-container class="right-container">
        <!-- 顶部栏优化 -->
        <el-header class="top-header">
          <div class="user-info">
            <img 
              src="@/assets/bg1.jpg"
              alt="用户头像"
              class="user-avatar"
            />
            <div class="user-detail">
              <span class="welcome-text">欢迎回来</span>
              <span class="username">{{ user.username }}</span>
            </div>
          </div>
          <el-dropdown trigger="hover">
            <el-button class="setting-btn" circle>
              <el-icon :size="24"><Setting /></el-icon> <!-- 加大图标尺寸 -->
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToPersonalPage">
                  <el-icon :size="24"><User /></el-icon> <!-- 加大图标尺寸 --> 个人中心
                </el-dropdown-item>
                <el-dropdown-item divided @click="logout">
                  <el-icon :size="24"><SwitchButton /></el-icon> <!-- 加大图标尺寸 --> 退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-header>

        <!-- 内容区域优化 -->
        <el-main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade-transform" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { jwtDecode } from 'jwt-decode';
import { Home, Microphone, Setting, User, SwitchButton } from '@element-plus/icons-vue';

export default {
  name: "ContentPage",
  components: { // 关键修复：注册组件
    Home,
    Microphone,
    Setting,
    User,
    SwitchButton
  },
  setup() {
    const router = useRouter();
    const user = ref(JSON.parse(localStorage.getItem("user") || "{}"))

    // 组件加载时检查 Token
    onMounted(() => {
      const token = localStorage.getItem("token");
      if (!token) {
        router.push("/login"); // 没有 Token，跳转到登录页
      } else {
        try {
          const decoded = jwtDecode(token); // 解析 Token 获取用户名
          user.value.username = decoded.username || "用户";
        } catch (error) {
          console.error("Token 解析失败", error);
          router.push("/login");
        }
      }
    });

    // 退出登录方法
    const logout = () => {
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      router.push("/login");
    };
    
    // 前往个人中心
    const goToPersonalPage = () => {
      router.push("/manager/personPage");
    };

    return {
      user,
      logout,
      goToPersonalPage
    };
  }
};
</script>

<style scoped>
/* 左侧边栏 */
.m-aside {
  width: 320px; /* 加大侧边栏宽度 */
  background: linear-gradient(195deg, #2c3a52, #1f2937);
  transition: width 0.3s;
}

.m-sysName {
  padding: 20px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.m-nameText {
  color: #f0f4f8;
  font-size: 20px; /* 加大文字尺寸 */
  font-weight: 600;
  letter-spacing: 1px;
}

.el-menu {
  --el-menu-bg-color: transparent;
  --el-menu-hover-bg-color: rgba(255,255,255,0.05);
  border-right: none;
}

.menu-text {
  font-size: 16px; /* 加大文字尺寸 */
  margin-left: 8px;
}

.sub-menu-text {
  font-size: 15px; /* 加大文字尺寸 */
  margin-left: 12px;
}

/* 顶部栏优化 */
.top-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0;  /* 新增 */
  padding: 0 24px;  /* 确保垂直方向无padding */
  background: #ffffff;
  box-shadow: 0 1px 4px rgba(0,21,41,0.08);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-detail {
  display: flex;
  flex-direction: column;
}

.welcome-text {
  font-size: 14px; /* 加大文字尺寸 */
  color: #909399;
}

.username {
  font-size: 16px; /* 加大文字尺寸 */
  font-weight: 500;
  color: #303133;
}

.user-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s;
  cursor: pointer;
}

.user-avatar:hover {
  transform: scale(1.1);
}

.setting-btn {
  border: none;
  background: #f5f7fa;
  transition: all 0.3s;
}

.setting-btn:hover {
  background: #409EFF;
  color: white;
}

/* 内容区域优化 */
.main-content {
  background: #f5f7fa;
  padding: 20px;
  min-height: calc(100vh - 70px);
}

/* 过渡动画 */
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* 全局滚动条优化 */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-thumb {
  background-color: rgba(144,147,153,.3);
  border-radius: 4px;
}

.sidebar-logo {
  width: 80px; /* 加大logo尺寸 */
  height: 80px;
  margin-right: 12px;
}

:deep(body) {
  margin: 0;
  padding: 0;
} 
</style>