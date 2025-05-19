<template>
    <div class="home">
        <nav class="navbar">
            <button v-for="(item, index) in navItems" :key="index" class="nav-btn">
                {{ item }}
            </button>
        </nav>
        <div class="slider-container">
            <div class="slider" ref="slider">
                <img v-for="(image, index) in images" :key="index" :src="image" class="slide" />
            </div>
            <button class="prev" @click="prevSlide">‹</button>
            <button class="next" @click="nextSlide">›</button>
        </div>
        <section class="about">
            <h2>关于我们</h2>
            <p>我们支持把文字转化为语音文件</p>
        </section>
        <button class="try-now" @click="tryNow">Try Now</button>
    </div>
</template>

<script>
import { nextTick } from "vue"; // ✅ 确保 DOM 加载完成

export default {
    data() {
        return {
            navItems: ["首页", "功能", "价格", "联系我们", "登录"],
            images: [
                "http://localhost:8080/img/cover1.jpg",
                "http://localhost:8080/img/cover2.jpg",
                "http://localhost:8080/img/cover3.jpg",
                "http://localhost:8080/img/cover4.jpg",
                "http://localhost:8080/img/cover5.jpg",
                
                
            ],
            currentIndex: 0,
            autoSlideInterval: null,
        };
    },
    methods: {
        nextSlide() {
            this.currentIndex = (this.currentIndex + 1) % this.images.length;
            this.updateSlide();
        },
        prevSlide() {
            this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
            this.updateSlide();
        },
        updateSlide() {
            nextTick(() => {
                const slider = this.$refs.slider;
                if (slider) {
                    slider.style.transform = `translateX(-${this.currentIndex * 100}%)`;
                }
            });
        },
        startAutoSlide() {
            this.autoSlideInterval = setInterval(this.nextSlide, 3000);
        },
        stopAutoSlide() {
            clearInterval(this.autoSlideInterval);
        },
        tryNow() {
            this.$router.push("/login");
        },
    },
    mounted() {
        nextTick(() => {
            this.startAutoSlide(); // ✅ 确保 DOM 生成后再执行
        });
    },
    beforeDestroy() {
        this.stopAutoSlide();
    },
};
</script>
  
<style scoped>
/* 基础布局 */
.home {
    max-width: 2000px;
    margin: 0 auto;
    overflow-x: hidden;
    font-family: 'Segoe UI', system-ui, sans-serif;
}

/* 导航栏样式 */
.navbar {
    display: flex;
    height: 70px;
    justify-content: space-around;
    align-items: center;
    background: linear-gradient(135deg, #2c3e50, #3498db);
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
    padding: 0 2rem;
}

.nav-btn {
    background: none;
    border: none;
    color: white;
    font-size: 1.1rem;
    cursor: pointer;
    padding: 12px 20px;
    border-radius: 25px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.nav-btn:hover {
    background: rgba(255,255,255,0.15);
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    text-decoration: none;
}

/* 轮播图容器 */
.slider-container {
    position: relative;
    width: 95%;
    overflow: hidden;
    margin: 80px auto 20px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.slider {
    display: flex;
    width: 100%;
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide {
    width: 100%;
    height: 80vh;
    flex: 0 0 auto;
    object-fit: cover;
    object-position: center 30%;
    border-radius: 15px;
}

/* 导航按钮 */
.prev, .next {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(5px);
    color: white;
    border: none;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    font-size: 24px;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

.prev:hover, .next:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-50%) scale(1.1);
}

.prev {
    left: 20px;
}

.next {
    right: 20px;
}

/* 关于我们 */
.about {
    text-align: center;
    padding: 40px 20px;
    margin: 40px 0;
    background: linear-gradient(45deg, #f8f9fa, #ffffff);
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.about h2 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #2c3e50;
    background: linear-gradient(135deg, #3498db, #2c3e50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.about p {
    font-size: 1.2rem;
    color: #666;
    line-height: 1.6;
    max-width: 800px;
    margin: 0 auto;
}

/* 立即体验按钮 */
.try-now {
    display: block;
    margin: 40px auto;
    padding: 1.2rem 6rem;
    background: linear-gradient(135deg, #00c853, #009624);
    color: white;
    border: none;
    font-size: 1.4rem;
    border-radius: 35px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 5px 15px rgba(0,200,83,0.3);
    position: relative;
    overflow: hidden;
}

.try-now::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(255,255,255,0.3),
        transparent
    );
    transition: all 0.5s;
}

.try-now:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,200,83,0.5);
}

.try-now:hover::before {
    left: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
    .navbar {
        height: 60px;
        padding: 0 1rem;
    }

    .nav-btn {
        font-size: 0.9rem;
        padding: 8px 15px;
    }

    .slider-container {
        width: 100%;
        margin-top: 60px;
        border-radius: 0;
    }

    .slide {
        height: 60vh;
    }

    .about {
        padding: 30px 15px;
        margin: 30px 10px;
    }

    .about h2 {
        font-size: 2rem;
    }

    .try-now {
        padding: 1rem 4rem;
        font-size: 1.2rem;
    }
}

@media (max-width: 480px) {
    .nav-btn {
        font-size: 0.8rem;
        padding: 6px 12px;
    }

    .slide {
        height: 50vh;
    }

    .prev, .next {
        width: 35px;
        height: 35px;
        font-size: 20px;
    }

    .about h2 {
        font-size: 1.8rem;
    }

    .try-now {
        width: 90%;
        padding: 1rem;
        font-size: 1.1rem;
    }
}
</style>