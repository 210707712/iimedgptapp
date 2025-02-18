<template>
  <div class="home">
    <!-- <div class="prompt-container">
      <h3>大模型循证诊治-文献语义检索</h3>
      <div v-if="loading">加载中...</div>
    <div v-else-if="error">{{ errorMessage }}</div>
    <div v-else>
    <p>语义检索结果: </p>
    <zhishi :documents="documents" />
    <div style="margin: 30px;"></div>
  </div>
  </div> -->
  <div class="prompt-container">
    请选择您不舒服的位置：
    <div style="margin: 30px;"></div>
    <body1></body1>

    <div style="margin: 30px;"></div>
    
  </div>
    <div class="home-right">
      <div class="right-version">
        <div class="llm-chat-demo">
          <span class="chat-demo">中科（G60）智慧健康创新研究院-大模型导诊平台</span>
          <span class="version">（试用版）</span>
        </div>
      </div>
      <div class="right-body" :class="messages.length === 0 ? 'nodata' : ''" ref="messageContainer">
        <div v-for="(message, index) in messages" class="main-message" :key="index"
             :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'assistant'}">
          <!-- 显示用户标识和图片 -->
          <div class="message-sender"
               :class="{'user-message': message.sender === 'user', 'friend-message': message.sender === 'assistant'}">
            <img v-if="message.sender === 'user'" src="@/assets/我的.png" alt="User Icon">
            <img v-else-if="message.sender === 'assistant'" src="@/assets/我的2.png" alt="Friend Icon">
            <span class="message-sender-name"
                  :class="message.sender === 'user' ? 'user-color' : 'friend-color'">{{ message.sender }}:</span>
          </div>
          <div v-if="message.sender === 'user'" class="user-message">{{ message.content }}</div>
          <div v-else class="friend-message" v-html="message.content"></div>
        </div>
      </div>
      <div class="right-input" @keyup.enter="handleSearch">
        <!-- 输入框 -->
        <el-input v-model="queryKeyword" placeholder="给IIMedGPT大模型发送消息" class="input"></el-input>
        <!-- 查询按钮 -->
        <el-button v-if="!loading" type="primary" @click="handleSearch">
          <img class="up-load" src="@/assets/上传.png">
        </el-button>
        <el-button v-if="loading" type="primary" @click="closeEventSource">
          <img class="up-load" src="@/assets/等待.png">
        </el-button>
        <!-- 设置按钮 -->
        <el-button type="text" @click="toggleSettings">配置 </el-button>
      </div>
      <div v-if="showSettings" class="settings-modal">
      <!-- 配置弹框 -->
      <div class="settings-content">
    <h2>设置</h2>
    <!-- 选项选择器 -->
    <div class="form-group">
      <label for="optionsSelect">应用提示词选择:</label>
      <el-select id="optionsSelect" v-model="appselectedOption" placeholder="请选择" @change="handleOptionChange">
        <el-option
          v-for="item in appoptions"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </div>
    <!-- 应用描述输入框 -->
    <div class="form-group">
      <label for="appDescription">自定义应用提示词:</label>
      <el-input id="appDescription"  v-model="settingInput" placeholder="请输入您的应用提示词" type="textarea"></el-input>
    </div>

    <!-- 选项选择器 -->
    <!-- <div class="form-group">
      <label for="optionsSelect">请选择您要使用的模型:</label>
      <el-select id="optionsSelect" v-model="modelselectedOption" placeholder="请选择">
        <el-option
          v-for="item in modeloptions"
          :key="item.value"
          :label="item.label"
          :value="item.value">
        </el-option>
      </el-select>
    </div> -->

    <!-- 关闭弹框按钮 -->
    <el-button type="text" class="close-button" @click="toggleSettings">关闭</el-button>
  </div>
    </div>
      <div class="sec-notice">中科（G60）智慧健康创新研究院-大模型导诊平台，生成内容仅供学习，具体病情请询问医师。</div>
    </div>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import markdownItFootnote from 'markdown-it-footnote';
import markdownItTaskLists from 'markdown-it-task-lists';
import markdownItAbbr from 'markdown-it-abbr';
import markdownItContainer from 'markdown-it-container';
import hljs from 'highlight.js';
import markdownItHighlightjs from 'markdown-it-highlightjs';
import body1 from './body';
import zhishi from './zhishi'; // 确保路径正确
import axios from 'axios';
export default {
  name: 'HomeView',
  components: {body1,zhishi},
  computed: {
    // 将 Markdown 文本渲染为 HTML
    html() {
      return this.md.render(this.message);
    }
  },
  data() {
    return {
      result: null,
      loading: true,
      error: false,
      errorMessage: '',
      documents: [],
      // [
      //   {'text': '', 'title': '1穴位注射治疗急性胰腺炎胃肠功能障碍的研究进展_袁红.pdf', 'score': 0.7211015224456787}
      //   ,
      //   {'text': '位 注射不、减 轻', 'title': '穴位注射治疗急性胰腺炎胃肠功能障碍的研究进展_袁红.pdf', 'score': 0.7211015224456787}
      //   ,
      //   {'text': '2 年12 月 指导、依据穴位作用和药物性能产生复合作用，是 集针刺、穴位、药物相结合的一种新疗法 [9]。穴位 注射不仅能通过注射针发挥针刺样治疗作用，还可 通过药物局部反应产生酸、麻、重、胀等类似针感 作用，促使循经感传，同时药物局部渗透进入全身 循环发挥治疗作用，有研究表明以上三种作用可能 存在着某种积极的相互影响 [10]。相关临床研究表明 穴位注射足三里能促进胃肠蠕动、解决肠麻痹、减 轻', 'title': '穴位注射治疗急性胰腺炎胃肠功能障碍的研究进展_袁红.pdf', 'score': 0.7211015224456787}
      //   ,
      //   {'text': '2 年12 月 指导、依据穴位作用和药物性能产生复合作用，是 集针刺、穴位、药物相结合的一种新疗法 [9]。穴位 注射不仅能通过注射针发挥针刺样治疗作用，还可 通过药物局部反应产生酸、麻、重、胀等类似针感 作用，促使循经感传，同时药物局部渗透进入全身 循环发挥治疗作用，有研究表明以上三种作用可能 存在着某种积极的相互影响 [10]。相关临床研究表明 穴位注射足三里能促进胃肠蠕动、解决肠麻痹、减 轻', 'title': '穴位注射治疗急性胰腺炎胃肠功能障碍的研究进展_袁红.pdf', 'score': 0.7211015224456787}
      //   ,
      //   {'text': '2 年12 月 指导、依据穴位作用和药物性能产生复合作用，是 集针刺、穴位、药物相结合的一种新疗法 [9]。穴位 注射不仅能通过注射针发挥针刺样治疗作用，还可 通过药物局部反应产生酸、麻、重、胀等类似针感 作用，促使循经感传，同时药物局部渗透进入全身 循环发挥治疗作用，有研究表明以上三种作用可能 存在着某种积极的相互影响 [10]。相关临床研究表明 穴位注射足三里能促进胃肠蠕动、解决肠麻痹、减 轻', 'title': '穴位注射治疗急性胰腺炎胃肠功能障碍的研究进展_袁红.pdf', 'score': 0.7211015224456787}
      
      //     // ... 其他文档对象（此处省略，与第一个对象结构相同）
      //   ]
      md: new MarkdownIt()
          .use(markdownItFootnote)
          .use(markdownItTaskLists, {enabled: true})
          .use(markdownItAbbr)
          .use(markdownItContainer, 'warning')
          .use(markdownItHighlightjs, {hljs}), // 添加 markdown-it-highlightjs 插件
      queryKeyword: '',
      tempResult: {},
      loading: false,
      messages: [],
      socket: null,
      eventSource: null, // 添加事件源变量
      stopIcon: '@/assets/等待.png',
      uploadIcon: '@/assets/上传.png',
      showSettings: false ,// 控制设置弹框的显示与隐藏
      settingInput: '', // 文本输入框的数据绑定
      modelselectedOption: '', // 选择器的数据绑定
      appselectedOption: '', // 选择器的数据绑定
      modeloptions: [ // 选择器的选项列表
        { value: '1', label: 'IIMedGPT1.0' },
        { value: '2', label: 'IIMedGPT2.0' },
        { value: '3', label: 'IIMedGPT3.0' }
      ],
      // 基于IIMedGPT的脓毒症急性胃肠功能障碍中西医结合诊治方法
      appoptions: [ // 选择器的选项列表
        { value: '您是西医专家,您熟练知道脓毒症引起的急性胃肠功能障碍的西医治疗策略，包括常用药物、治疗原则及可能的并发症管理。', label: '西医专家' },
        { value: '您是中医专家,您熟练知道中医在治疗脓毒症引起的急性胃肠功能障碍中的作用，具体包括使用的中药方剂、针灸和其他传统疗法，以及这些方法对症状改善的机制。', label: '中医专家' },
        { value: '您是中西医结合研究者,您熟练知道中西医结合在治疗脓毒症急性胃肠功能障碍中的优势，探讨不同治疗方法的协同效应，以及如何根据患者具体情况选择最佳治疗方案。', label: '中西医结合研究者' }
      ]
     }
  },  mounted() {
    document.title = 'IIMedGPT';
   
  },
  created() {
    // this.fetchData();
  },
  methods: {
    fetchData() {
      axios.get('http://202.127.200.31:30012/llm/zhishi?query='+this.queryKeyword)
      // axios.get('http://127.0.0.1:5000/llm/zhishi?query='+this.queryKeyword)
        .then(response => {
          // this.result = response.data; // 假设后端返回的数据在response.data中
          this.documents=response.data["data"]["querytext"]
          // console.log(this.documents[0]['text']);
          // console.log(response.data); // 打印实际的数据
          this.loading = false; // 请求成功完成后关闭加载状态
        })
        .catch(error => {
          this.error = true;
          this.errorMessage = '加载数据失败: ' + error.message;
          this.loading = false; // 请求失败时也关闭加载状态
        });
    }
  ,
  async waitForDocuments() {
  while (true) {
    await this.fetchData();
    if (this.documents && this.documents.length > 0) {
      break; // 当 documents 不为空时跳出循环
    }
    await new Promise(resolve => setTimeout(resolve, 1000)); // 等待 1 秒后继续轮询
  }
  // documents 已不为空，继续执行后续操作...
},
    handleOptionChange(value) {
    // 查找选中的选项对象
    const selectedOption = this.appoptions.find(option => option.value === value);
    if (selectedOption) {
      // 将选中选项的值赋给settingInput
      this.settingInput = selectedOption.value;
    }
  },
    async handleSearch() {
      // 如果正在加载中，则不执行新的搜索操作
      if (this.loading) {
        return;
      }

      const keyword = this.queryKeyword;
      this.loading = true;
      try {
  //       try {
  //   await this.waitForDocuments.call(this); // 使用 call 方法来确保 this 的上下文正确
  //   // 在这里继续执行当 documents 不为空时的操作
  // } catch (error) {
  //   console.error('Error waiting for documents:', error);
  // }
        console.log(this.documents);
        let zxakey = "zxa";
        // 初始化一个用于 SSE 的 message 对象
        let sseMessage = {
          orgcontent: '',
          content: '',
          sender: 'assistant',
          zxakey: zxakey
        };

        this.messages.push({
          content: keyword,
          sender: 'user'
        });

        this.$nextTick(() => {
          this.scrollToBottom();
        });

        let friendMessage = sseMessage;
        // 创建一个新的 EventSource 实例
        
        // this.eventSource = new EventSource('http://daozhenapi.czshmily.cn/llm/requestIIMedGPT?query=' + keyword);
        if (this.modelselectedOption == '1') {
          this.eventSource = new EventSource('http://202.127.200.31:30012/llm/requestIIMedGPT?query=' + keyword+"请参考以下知识作答："+this.documents[0].text+'&prompt=' + this.settingInput);
        } else if (this.modelselectedOption == '2') {
          this.eventSource = new EventSource('http://127.0.0.1:5000/llm/requestIIMedGPT?query=' +"请参考以下知识: "+this.documents[0].text+"。 回答问题: "+ keyword+'&prompt=' + this.settingInput);
        }else if (this.modelselectedOption == '3') {
          this.eventSource = new EventSource('http://127.0.0.1:5000/llm/requestIIMedGPT?query=' + keyword+"请参考以下知识作答："+this.documents[0].text+'&prompt=' + this.settingInput);
        }else {
          this.eventSource = new EventSource('http://202.127.200.31:30012/llm/requestIIMedGPT?query=' + keyword+'&prompt=' + this.settingInput);
          // this.eventSource = new EventSource('http://127.0.0.1:5000/llm/requestIIMedGPT?query=' +"请参考以下知识: "+this.documents[0].text+"。 回答问题: "+ keyword+'&prompt=' + this.settingInput);
        
        }
        // this.eventSource = new EventSource('http://127.0.0.1:5000/llm/requestIIMedGPT?query=' + keyword+'&prompt=' + this.settingInput);
        // 设置消息事件监听器
        this.eventSource.onmessage = (event) => {
          try {
            const dataObject = JSON.parse(event.data);
            // 判断是否为最后一个消息，如果是，则关闭事件源
            if (dataObject.message === 'done') {
              this.eventSource.close();
              this.loading = false;
            }
            if (dataObject.message != 'done') {
              // 累加接收到的数据到 friendMessage.orgcontent 中
              friendMessage.orgcontent += dataObject.message.toLocaleString();
              friendMessage.orgcontent = friendMessage.orgcontent.replace(/\*\*\s*([^*]*?)\s*(:\s*)?\*\*/g, '**$1$2**');
              // 更新 friendMessage.content，这里假设 md.render 可以处理累加的字符串
              friendMessage.content = this.md.render(friendMessage.orgcontent);
            }
            this.scrollToBottom();
          } catch (e) {
            console.error('Error parsing JSON:', e);
          }
        };
        this.messages.push(sseMessage);
        this.queryKeyword = ''; // 清空输入框
        this.eventSource.onerror = error => {
          console.error('EventSource failed:', error);
          this.eventSource.close();
        };
      } catch (error) {
           // 可以在 finally 块中添加清理代码，如关闭加载状态
    this.loading = false;
        console.error('发送消息时出错：', error);
      } finally {
           // 可以在 finally 块中添加清理代码，如关闭加载状态
        this.loading = false;
      }
    },
    closeEventSource() {
      this.loading = false;
      if (this.eventSource) {
        this.eventSource.close();
      }
    },
    scrollToBottom() {
      const messageContainer = this.$refs.messageContainer;
      if (messageContainer) {
        messageContainer.scrollTop = messageContainer.scrollHeight;
      }
    },
    beforeDestroy() {
      if (this.eventSource) {
        this.eventSource.close();
      }
    },
    toggleSettings() {
      this.showSettings = !this.showSettings;
    }
  },
}
</script>

<style scoped>

.form-group {
  margin-bottom: 15px; /* 每个表单组的下边距 */
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px; /* 标签与输入框之间的间距 */
}

.form-group input,
.form-group select {
  width: calc(100% - 20px); /* 输入框和选择器的宽度，留出一些内边距 */
  padding: 8px; /* 内边距 */
  box-sizing: border-box; /* 包含内边距和边框在元素总宽度内 */
}

.close-button {
  display: block; /* 让按钮占满整行 */
  text-align: right; /* 按钮文本右对齐 */
  padding: 10px 0; /* 上下内边距 */
}
.settings-modal {
  position: fixed;
  top: 10%; /* 调整顶部位置，留出一些空间 */
  left: 10%; /* 调整左边位置，留出一些空间 */
  right: 10%; /* 调整右边位置，留出一些空间 */
  bottom: 10%; /* 调整底部位置，留出一些空间 */
  /* background: rgba(0, 0, 0, 0.5); */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.auto-resize-input {
  width: 100%; /* 或者你需要的宽度 */
  padding: 10px; /* 内边距，可以根据需要调整 */
  border: 1px solid #dcdcdc; /* 边框颜色和宽度 */
  border-radius: 4px; /* 圆角 */
  box-sizing: border-box; /* 包含内边距和边框在元素总宽度内 */
  transition: border-color 0.3s, box-shadow 0.3s; /* 过渡效果 */
  resize: vertical; /* 允许垂直调整大小 */
  overflow-y: auto; /* 启用垂直滚动条 */
  min-height: 40px; /* 最小高度 */
  max-height: 200px; /* 最大高度，根据需要调整 */
}

.auto-resize-input:focus {
  border-color: #409eff; /* 聚焦时的边框颜色 */
  box-shadow: 0 0 5px rgba(64, 158, 255, 0.5); /* 聚焦时的阴影效果 */
  outline: none; /* 移除默认的聚焦轮廓 */
}
.settings-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
  width: 80%; /* 设置弹框内容的宽度为视口宽度的80% */
  max-width: 800px; /* 设置弹框内容的最大宽度，以防视口过大 */
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1); 
}

.settings-content h2 {
  margin-top: 0;
}

.settings-content p {
  margin: 10px 0;
}
.prompt-container {
  position: relative;
  height: 83%;
  width: 20%;
  top: 10%;
  left: 5%;
  padding: 10px; /* 添加内边距，使文本和<body1>元素有一定的空间 */
  background-color: #f9f9f9; /* 添加背景色，提高可读性 */
  border-radius: 5px; /* 添加圆角，使容器看起来更柔和 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 添加阴影，增加立体感 */
}
.custom-image-size {
  /* width: 500px;   */
  height: 1200px; 
}
.home {
  height: 100%;
  display: flex;
}

.home-right {
  width: 100%;
}

.right-version {
  /* width: 60%; */
  margin: auto;
  /* background-color: #F9FFD8; */
  height: 5%;
  display: flex;
  justify-content: start;
  align-items: center;
  border-radius: 15px;
  margin-bottom: 12px;
}

.version {
  color: rgb(155, 155, 155);
}

.llm-chat-demo {
  width: 58%;
  margin: auto;
  /* margin-left: 20px; */
  font-family: "黑体", "SimHei", sans-serif;
  font-family: Söhne, ui-sans-serif, system;
  font-variation-settings: normal;
  font-weight: 550;
  font-size: 18px;
  cursor: pointer;
  color-scheme: light;
}

.chat-demo {
  opacity: 0.65; /* 设置透明度为 0.7，您可以根据需要调整这个值 */
}

.right-body {
  height: 85%;
  overflow-y: auto;
}

.user-color {
  color: #1296db;
}

.friend-color {
  color: #77FC5D;
}
.nodata {
  background-image: url("@/assets/IIMedGPT.png");
  background-repeat: no-repeat;
  background-size: 35%;
  background-position: center 50%;
}

.main-message {
  margin: auto;
  width: 58%;
  justify-content: center;
}

.message-sender-name {
  margin-left: 10px;
  //font-family: "黑体", "SimHei", sans-serif;
  font-family: Söhne, ui-sans-serif, system;
  font-weight: 550;
  font-size: 18px;
}

.right-input {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 6.5%;

  position: relative;
}

.sec-notice {
  height: 3.5%;
  font-size: 12px;
  font-family: Söhne, ui-sans-serif;
  color: rgb(155, 155, 155);
  display: flex;
  justify-content: center;
}

.input {
  width: 58%;
  margin-right: 5px;
}

.up-load {
  //width: 30px;
}

::v-deep .el-button {
  padding: 5px 6px;
}

::v-deep .el-input__inner {
  height: 52px;
  border-radius: 15px;
  border: 1px solid #DCDFE6;
}

::v-deep .el-button--primary {
  position: relative;
  right: 3.5%;
  background-color: rgba(180, 180, 180, 0.3) !important;
  color: black !important;
  border-color: rgba(180, 180, 180, 0.3) !important;
}

.user-message {
  text-align: left;
  padding: 5px;
  margin-bottom: 5px;
  border-radius: 15px;

}

.friend-message {
  background-color: rgba(227, 255, 255, 0.2); /* 这里的 0.5 是透明度，你可以根据需要调整 */
  text-align: left;
  padding: 5px;
  margin-bottom: 5px;
}

::v-deep .friend-message pre .hljs {
  border-radius: 10px !important; /* 圆角 */
  background-color: #FAF7F7; /* 例子中的背景色 */
}

/* 设置滚动条的样式 */
::-webkit-scrollbar {
  width: 6px; /* 设置滚动条宽度 */
}

/* 设置滚动条轨道的样式 */
::-webkit-scrollbar-track {
  background: #f1f1f1; /* 设置滚动条轨道的背景色 */
}

/* 设置滚动条滑块的样式 */
::-webkit-scrollbar-thumb {
  background: #888; /* 设置滚动条滑块的背景色 */
  border-radius: 3px; /* 设置滚动条滑块的圆角 */
}

/* 鼠标悬停时滚动条滑块的样式 */
::-webkit-scrollbar-thumb:hover {
  background: #555; /* 设置鼠标悬停时滚动条滑块的背景色 */
}
</style>
