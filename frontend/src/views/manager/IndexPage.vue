<template>
  <div class="index-page">
    <!-- 首屏展示区 -->
    <section class="hero-section">
      <el-row :gutter="20" class="hero-content">
        <el-col :span="12">
          <h1 class="hero-title">
            <span class="gradient-text">AI语音教学系统</span>
          </h1>
          <p class="hero-description">
            基于深度学习技术的智能语音解决方案<br>
            提供全流程语音交互服务，覆盖教育、客服、娱乐等多场景应用
          </p>
          <div class="cta-buttons">
            <el-button type="primary" size="large" round @click="handleExperience">立即体验</el-button>
            <el-button size="large" round>功能演示</el-button>
          </div>
          <div class="system-benefits">
            <p class="benefit-item">
              <el-icon class="benefit-icon"><Checkmark /></el-icon>
              支持100+语言及方言的高精度语音合成
            </p>
            <p class="benefit-item">
              <el-icon class="benefit-icon"><Checkmark /></el-icon>
              毫秒级响应速度，支持实时流式合成
            </p>
            <p class="benefit-item">
              <el-icon class="benefit-icon"><Checkmark /></el-icon>
              企业级安全防护，数据加密存储
            </p>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="hero-media">
            <img 
              src="@/assets/logo.png" 
              alt="语音交互示意图"
              class="hero-image animate-float"
            >
          </div>
        </el-col>
      </el-row>
    </section>

    <!-- 核心功能模块 -->
    <section class="features-section">
      <h2 class="section-title">核心功能特性</h2>
      <el-row :gutter="20" class="feature-grid">
        <!-- 功能项1 -->
        <el-col :span="8">
          <article class="feature-card">
            <div class="feature-icon-wrapper">
              <el-icon class="feature-icon"><Microphone /></el-icon>
            </div>
            <h3 class="feature-title">智能文本转语音</h3>
            <p class="feature-description">
              采用Tacotron2+WaveNet架构，支持：<br>
              ▶ 多语言混合合成（如中英双语）<br>
              ▶ 情感语音生成（快乐/悲伤/严肃等）<br>
              ▶ 多音字智能纠错（准确率>99.8%）<br>
              &nbsp;<br>
              &nbsp;
            </p>
          </article>
        </el-col>

        <!-- 功能项2 -->
        <el-col :span="8">
          <article class="feature-card">
            <div class="feature-icon-wrapper">
              <el-icon class="feature-icon"><User /></el-icon>
            </div>
            <h3 class="feature-title">个性化音色克隆</h3>
            <p class="feature-description">
              基于说话人嵌入技术，实现：<br>
              ▶ 5分钟样本快速克隆<br>
              ▶ 多音色混合生成（如童声+播音员声线）<br>
              ▶ 声纹特征参数化调节（音高/共振峰等）<br>
              &nbsp;<br>
              &nbsp;
            </p>
          </article>
        </el-col>

        <!-- 功能项3 -->
        <el-col :span="8">
          <article class="feature-card">
            <div class="feature-icon-wrapper">
              <el-icon class="feature-icon"><Document /></el-icon>
            </div>
            <h3 class="feature-title">语音资源管理</h3>
            <p class="feature-description">
              提供可视化管理平台，支持：<br>
              ▶ 百万级语音文件秒级检索<br>
              ▶ 多格式批量转换（MP3/WAV/OGG等）<br>
              ▶ 云端-本地双向同步（支持增量更新）<br>
              &nbsp;<br>
              &nbsp;
            </p>
          </article>
        </el-col>
      </el-row>
    </section>
    
    <!-- 数据统计卡片 -->
    <section class="dashboard-section">
      <el-row :gutter="20">
        <!-- 统计卡片1 -->
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon speech-icon">
              <el-icon><Microphone /></el-icon>
            </div>
            <div class="stat-content">
              <h3 class="stat-value">14,582</h3>
              <p class="stat-label">语音生成总数</p>
              <div class="stat-trend">
                <span class="trend-value">+24%</span>
                <span class="trend-period">较上月</span>
              </div>
            </div>
          </div>
        </el-col>
        
        <!-- 统计卡片2 -->
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon user-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <h3 class="stat-value">865</h3>
              <p class="stat-label">活跃用户数</p>
              <div class="stat-trend">
                <span class="trend-value">+18%</span>
                <span class="trend-period">较上月</span>
              </div>
            </div>
          </div>
        </el-col>
        
        <!-- 统计卡片3 -->
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon time-icon">
              <el-icon><Timer /></el-icon>
            </div>
            <div class="stat-content">
              <h3 class="stat-value">342h</h3>
              <p class="stat-label">合成总时长</p>
              <div class="stat-trend">
                <span class="trend-value">+31%</span>
                <span class="trend-period">较上月</span>
              </div>
            </div>
          </div>
        </el-col>
        
        <!-- 统计卡片4 -->
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-icon storage-icon">
              <el-icon><FolderOpened /></el-icon>
            </div>
            <div class="stat-content">
              <h3 class="stat-value">143.36GB</h3>
              <p class="stat-label">存储空间</p>
              <div class="storage-bar">
                <div class="storage-progress" style="width: 14%"></div>
              </div>
              <p class="storage-text">14% 已使用</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </section>
    
    <!-- 图表展示区域 -->
    <section class="charts-section">
      <!-- 资源使用率 -->
      <el-row>
        <el-col :span="24">
          <div class="chart-card">
            <div class="chart-header">
              <h3 class="chart-title">系统资源使用率</h3>
              <div class="chart-actions">
                <el-dropdown>
                  <span class="el-dropdown-link">
                    {{resourceViewOption}}<el-icon class="el-icon--right"><arrow-down /></el-icon>
                  </span>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item @click="resourceViewOption = '最近7天'">最近7天</el-dropdown-item>
                      <el-dropdown-item @click="resourceViewOption = '最近30天'">最近30天</el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </div>
            <div class="chart-body">
              <div ref="resourceUsageChart" class="chart-container"></div>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- 用户使用趋势图 -->
      <el-row class="chart-row">
        <el-col :span="24">
          <div class="chart-card">
            <div class="chart-header">
              <h3 class="chart-title">用户使用趋势</h3>
              <div class="chart-actions">
                <el-radio-group v-model="trendTimeRange" size="small">
                  <el-radio-button label="week">本周</el-radio-button>
                  <el-radio-button label="month">本月</el-radio-button>
                  <el-radio-button label="year">全年</el-radio-button>
                </el-radio-group>
              </div>
            </div>
            <div class="chart-body">
              <div ref="userTrendChart" class="chart-container"></div>
            </div>
          </div>
        </el-col>
      </el-row>
      
      <!-- 语音合成类型分布 -->
      <el-row class="chart-row">
        <el-col :span="24">
          <div class="chart-card">
            <div class="chart-header">
              <h3 class="chart-title">语音合成类型分布</h3>
            </div>
            <div class="chart-body pie-chart-container">
              <div ref="synthesisTypeChart" class="chart-container"></div>
              <div class="chart-legend">
                <div class="legend-item" v-for="(item, index) in synthesisTypes" :key="index">
                  <span class="legend-color" :style="{backgroundColor: pieColors[index]}"></span>
                  <span class="legend-label">{{item.name}}</span>
                  <span class="legend-value">{{item.value}}%</span>
                </div>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch, onUnmounted } from 'vue';
import { Microphone, User, Document, Checkmark, Timer, FolderOpened, ArrowDown } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';
import * as echarts from 'echarts/core';
import { LineChart, BarChart, PieChart } from 'echarts/charts';
import { 
  TitleComponent, 
  TooltipComponent, 
  GridComponent, 
  LegendComponent,
  ToolboxComponent 
} from 'echarts/components';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  LineChart,
  BarChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  ToolboxComponent,
  CanvasRenderer
]);

const router = useRouter();
const trendTimeRange = ref('week');
const resourceViewOption = ref('最近7天');

// 图表DOM引用
const userTrendChart = ref(null);
const synthesisTypeChart = ref(null);
const resourceUsageChart = ref(null);

// 图表实例
let userTrendInstance = null;
let synthesisTypeInstance = null;
let resourceUsageInstance = null;

// 饼图数据和颜色
const synthesisTypes = ref([
  { name: '标准语音', value: 39 },
  { name: '情感语音', value: 20 },
  { name: '克隆语音', value: 29 },
  { name: '定制语音', value: 12 }
]);

const pieColors = [
  '#4e7ee7', 
  '#6e94f2', 
  '#8eaaf7', 
  '#abbffc'
];

// 初始化折线图
const initUserTrendChart = () => {
  if (!userTrendChart.value) return;
  
  userTrendInstance = echarts.init(userTrendChart.value);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [
      {
        name: '语音合成数',
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#4e7ee7'
        },
        areaStyle: {
          opacity: 0.2,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: '#4e7ee7'
            },
            {
              offset: 1,
              color: 'rgba(78, 126, 231, 0)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: [820, 932, 901, 934, 1290, 1330, 1320]
      },
      {
        name: '活跃用户',
        type: 'line',
        smooth: true,
        lineStyle: {
          width: 3,
          color: '#6e94f2'
        },
        areaStyle: {
          opacity: 0.2,
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            {
              offset: 0,
              color: '#6e94f2'
            },
            {
              offset: 1,
              color: 'rgba(110, 148, 242, 0)'
            }
          ])
        },
        emphasis: {
          focus: 'series'
        },
        data: [220, 282, 291, 334, 390, 440, 410]
      }
    ]
  };
  
  userTrendInstance.setOption(option);
};

// 初始化饼图
const initSynthesisTypeChart = () => {
  if (!synthesisTypeChart.value) return;
  
  synthesisTypeInstance = echarts.init(synthesisTypeChart.value);
  
  const option = {
    title: {
      text: '',
      left: 'center',
      top: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    series: [
      {
        name: '语音合成类型',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: false
          },
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        labelLine: {
          show: false
        },
        data: synthesisTypes.value.map((item, index) => ({
          value: item.value,
          name: item.name,
          itemStyle: {
            color: pieColors[index]
          }
        }))
      }
    ]
  };
  
  synthesisTypeInstance.setOption(option);
};

// 初始化柱状图
const initResourceUsageChart = () => {
  if (!resourceUsageChart.value) return;
  
  resourceUsageInstance = echarts.init(resourceUsageChart.value);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['GPU使用率', '内存使用率', '网络带宽'],
      top: 0,
      right: 10,
      textStyle: {
        color: '#666'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          type: 'dashed'
        }
      },
      axisLabel: {
        formatter: '{value}%'
      }
    },
    series: [
      {
        name: 'GPU使用率',
        type: 'bar',
        data: [45, 52, 38, 44, 78, 72, 71],
        itemStyle: {
          color: '#4e7ee7'
        }
      },
      {
        name: '内存使用率',
        type: 'bar',
        data: [62, 64, 49, 54, 88, 82, 89],
        itemStyle: {
          color: '#6e94f2'
        }
      },
      {
        name: '网络带宽',
        type: 'bar',
        data: [52, 45, 42, 48, 84, 78, 76],
        itemStyle: {
          color: '#8eaaf7'
        }
      }
    ]
  };
  
  resourceUsageInstance.setOption(option);
};

// 处理窗口大小变化
const handleResize = () => {
  userTrendInstance && userTrendInstance.resize();
  synthesisTypeInstance && synthesisTypeInstance.resize();
  resourceUsageInstance && resourceUsageInstance.resize();
};

// 时间范围变化处理
const handleTimeRangeChange = () => {
  // 这里可以根据不同的时间范围加载不同的数据
  console.log('时间范围变化:', trendTimeRange.value);
};

// 页面跳转
const handleExperience = () => {
  router.push('/manager/generate');
};

// 监听时间范围变化
watch(trendTimeRange, () => {
  handleTimeRangeChange();
});

onMounted(async () => {
  await nextTick();
  // 初始化所有图表
  initUserTrendChart();
  initSynthesisTypeChart();
  initResourceUsageChart();
  
  // 添加窗口大小变化监听
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  // 移除窗口大小变化监听
  window.removeEventListener('resize', handleResize);
  
  // 销毁图表实例
  userTrendInstance && userTrendInstance.dispose();
  synthesisTypeInstance && synthesisTypeInstance.dispose();
  resourceUsageInstance && resourceUsageInstance.dispose();
});
</script>

<style scoped>
/* 基础布局 */
.index-page {
@apply max-w-7xl mx-auto px-4 sm:px-6 lg:px-8;
font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

/* 数据统计卡片 */
.dashboard-section {
  margin: 2rem 0;
}

.stat-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  height: 100%;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
}

.stat-card:nth-child(1)::before {
  background: linear-gradient(to bottom, #4e7ee7, #6e94f2);
}

.stat-card:nth-child(2)::before {
  background: linear-gradient(to bottom, #7367f0, #9e95f5);
}

.stat-card:nth-child(3)::before {
  background: linear-gradient(to bottom, #ff9f43, #ffb976);
}

.stat-card:nth-child(4)::before {
  background: linear-gradient(to bottom, #28c76f, #48da89);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.speech-icon {
  background: rgba(78, 126, 231, 0.1);
  color: #4e7ee7;
}

.user-icon {
  background: rgba(115, 103, 240, 0.1);
  color: #7367f0;
}

.time-icon {
  background: rgba(255, 159, 67, 0.1);
  color: #ff9f43;
}

.storage-icon {
  background: rgba(40, 199, 111, 0.1);
  color: #28c76f;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem 0;
}

.stat-label {
  font-size: 1rem;
  color: #64748b;
  margin: 0 0 1rem 0;
}

.stat-trend {
  display: flex;
  align-items: center;
  margin-top: 0.5rem;
}

.trend-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #28c76f;
  margin-right: 0.5rem;
}

.trend-period {
  font-size: 0.75rem;
  color: #64748b;
}

.storage-bar {
  height: 6px;
  background: #e2e8f0;
  border-radius: 3px;
  margin: 0.75rem 0 0.5rem;
  overflow: hidden;
}

.storage-progress {
  height: 100%;
  background: linear-gradient(90deg, #28c76f, #48da89);
  border-radius: 3px;
  transition: width 1s ease-out;
}

.storage-text {
  font-size: 0.75rem;
  color: #64748b;
  margin: 0;
}

/* 图表区域 */
.charts-section {
  margin-bottom: 3rem;
}

.chart-row {
  margin-top: 2rem;
}

.chart-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  height: 100%;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
}

.chart-container {
  height: 300px;
}

.pie-chart-container {
  display: flex;
  align-items: center;
}

.pie-chart-container .chart-container {
  width: 60%;
}

.chart-legend {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
  width: 40%;
}

.legend-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
  margin-right: 0.5rem;
}

.legend-label {
  font-size: 0.875rem;
  color: #64748b;
  flex: 1;
}

.legend-value {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
}

.el-dropdown-link {
  cursor: pointer;
  color: #4e7ee7;
  display: flex;
  align-items: center;
  font-size: 0.875rem;
}

/* 首屏区域 */
.hero-title {
font-family: 'Barlow', system-ui, sans-serif;
font-weight: 800;
letter-spacing: -0.03em;
}
.hero-section {
@apply py-20 gap-16;
background: linear-gradient(135deg, #f4f9ff 0%, #dee7ee 100%);
border-radius: 0.75rem;
}

.hero-content {
@apply space-y-8;
}

.hero-media {
@apply flex justify-center;
}

/* 渐变文字 */
.gradient-text {
@apply text-6xl md:text-7xl font-extrabold bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent;
text-shadow: 0 4px 12px rgba(79, 70, 229, 0.15);
}

/* 描述文字 */
.hero-description {
@apply text-2xl text-gray-700 leading-relaxed max-w-2xl;
text-shadow: 0 2px 4px rgba(255,255,255,0.8);
}

/* 系统优势 */
.system-benefits {
@apply mt-12 space-y-4;
}

.benefit-item {
@apply flex items-center gap-4 text-lg text-gray-600;
}

.benefit-icon {
@apply text-3xl text-green-500;
}

/* 功能卡片容器 */
.el-col {
@apply py-5; /* 增加布局缓冲 */
transition: padding 0.3s ease;
}

/* 功能卡片 */
.feature-card {
@apply p-10 rounded-3xl relative transition-transform duration-300 z-10;
background: rgba(255,255,255,0.9);
box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
transform-origin: center bottom;
will-change: transform;
}

/* 悬停状态 */
.feature-card:hover {
@apply z-20;
transform: translateY(-10px) scale(1.02) perspective(1000px) rotateX(5deg);
box-shadow: 0 12px 24px rgba(33,150,243,0.15);
}

/* 扩展点击区域 */
.feature-card::before {
content: '';
@apply absolute -inset-3 z-0;
}

/* 图标容器 */
.feature-icon-wrapper {
@apply w-24 h-24 rounded-full flex items-center justify-center mb-8 bg-[#e3f2fd];
box-shadow: 0 4px 6px rgba(33,150,243,0.1);
transition: transform 0.3s ease;
}

.feature-icon-wrapper:hover {
transform: rotate(15deg) scale(1.1);
}

.feature-icon {
@apply text-5xl text-[#1976d2];
filter: drop-shadow(0 2px 4px rgba(25,118,210,0.2));
}

/* 标题样式 */
.feature-title {
@apply text-3xl font-bold text-gray-800 mb-6;
}

.feature-description {
@apply text-lg text-gray-700 leading-relaxed mb-4;
}

/* 图片动画 */
.hero-image {
width: 350px;
height: 350px;
object-fit: contain;
animation: float 4s ease-in-out infinite;
}

@keyframes float {
0%, 100% { transform: translateY(0) rotate(-2deg); }
50% { transform: translateY(-20px) rotate(2deg); }
}

/* 按钮样式 */
.cta-buttons .el-button {
@apply rounded-[25px] px-8 py-4 text-lg;
transition: 
  transform 0.2s ease,
  box-shadow 0.3s ease;
box-shadow: 
  0 4px 6px rgba(33,150,243,0.2),
  0 1px 3px rgba(0,0,0,0.05);
}

.cta-buttons .el-button:hover {
transform: translateY(-2px);
box-shadow: 
  0 6px 12px rgba(33,150,243,0.25),
  0 2px 4px rgba(0,0,0,0.1);
}

.cta-buttons .el-button--primary {
background: linear-gradient(135deg, #2196f3, #1976d2);
border: none;
}

/* 响应式优化 */
@media (max-width: 1024px) {
.hero-section {
  @apply text-center;
}

.cta-buttons {
  @apply justify-center;
}

.hero-image {
  @apply max-w-[80%];
}
}

@media (max-width: 768px) {
.feature-grid {
  @apply grid-cols-1;
}

.el-col {
  @apply px-0;
}
}

/* 章节标题 */
.section-title {
@apply text-4xl text-center mb-16 relative;
background: linear-gradient(135deg, #2196f3 30%, #1976d2 70%);
-webkit-background-clip: text;
background-clip: text;
color: transparent;
}

.section-title::after {
content: "";
@apply absolute bottom-0 left-1/2 -translate-x-1/2 w-16 h-1;
background: linear-gradient(90deg, #2196f3, rgba(33,150,243,0.2));
}

/* 增加响应式图表支持 */
@media (max-width: 1200px) {
  .chart-container {
    height: 250px;
  }
}

@media (max-width: 768px) {
  .chart-container {
    height: 200px;
  }
  
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>