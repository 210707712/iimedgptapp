<template>
    <div class="document-list">
      <div class="document-item" v-for="(doc, index) in documents" :key="index">
        <div class="snippet-button" @mouseover="showSnippet(index)" @mouseleave="hideSnippet">
        <div class="title">{{ doc.title }}</div>
        <a :href="`http://xinli.g60health.com:8000/xinliimg/aizheng/${doc.title}`" target="_blank" class="view-document-link">查看文献</a>
        <div class="score">语义相似度评分: {{ doc.score }}</div>
   
        <!-- <p style="text-align: center;font-size: 13px">语义检索片段</p> -->
        <div class="snippet-box" v-if="hoveredIndex === index" :style="{ whiteSpace: 'normal' }">
            <p class="snippet-text">{{ doc.text }}</p>
        </div>
        
      </div>
      </div>
    </div>
  </template>   
  
  <script>
      
  export default {
    props: {
        documents: {
        type: Array,
        required: true,
        default: () => []
      }
    },
    data() {
      return {
        hoveredIndex: null
      };
      
    }
    ,
  methods: {
    showSnippet(index) {
      this.hoveredIndex = index;
    },
    hideSnippet() {
      this.hoveredIndex = null;
    }
  }
  };
  </script>
  
  <style scoped>
.snippet-button {
  /* height: 10px;
  position: relative;
  display: inline-block;
  /* padding: -1px 20px; */
  /* background-color: #f0f0f0;
  border: none;
  cursor: pointer;  */
}

.snippet-box {
  width: 20%;
  position: fixed; /* 固定在视口中 */
  top: 1%; /* 紧贴在视口顶部 */
  left: 5%; /* 紧贴在视口右侧（如果需要的话，可以根据需要调整） */
  padding: 10px; /* 添加一些内边距以改善可读性 */
  background-color: white;
  border: 1px solid #ccc;
  display: none; /* 初始时隐藏 */
  z-index: 1000; /* 确保它位于其他元素之上 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  white-space: nowrap; /* 根据需要调整换行行为 */
  /* 可能还需要添加其他样式来适应固定位置，如宽度、最大宽度等 */
}

.snippet-text {
  font-size: 12px; /* 调整字体大小 */
  text-align: center; /* 文本居中 */
  white-space: normal; /* 允许文本自动换行 */
  word-wrap: break-word; /* 处理长单词换行 */
}

.snippet-button:hover .snippet-box,
.snippet-box[style*="display: block"] {
  display: block;
}
  .document-list {
    list-style-type: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    width: 100%; /* 确保列表宽度占满整个容器 */
  }
  
  .document-item {
    display: flex;
    flex-direction: column;
    width: 100%; /* 确保每个项目宽度占满整个容器 */
    border-bottom: 1px solid #ddd;
    padding: 15px 0;
  }
  
  .title {
    font-size: 13px;
    /* font-weight: bold; */
    margin-bottom: 10px;
  }
  
  .view-document-link {
    color: #007bff;
    text-decoration: none;
    font-size: 13px;
    cursor: pointer;
  }
  
  .view-document-link:hover {
    text-decoration: underline;
  }
  
  .score {
    font-size: 14px;
    color: #888;
    margin-top: 5px; /* 微调评分与上方内容的间距 */
  }
  </style>