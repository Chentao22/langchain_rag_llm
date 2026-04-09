🩺 Molly 医疗精灵 —— 基于 RAG 与大模型的医学问答助手
专业医学问答 | 私有知识库检索 | 多轮对话记忆 | PDF 文档解析
项目介绍
Molly 医疗精灵是一款基于 RAG（检索增强生成） 技术与大模型开发的专业医学领域智能问答系统。
系统能够读取 PDF 医学文献构建私有知识库，结合对话记忆能力，为用户提供精准、可溯源、安全可靠的医学问答服务，有效避免大模型幻觉，严格遵循参考资料进行回答。
核心功能
✅ 专业医学问答
专属医学专家角色 Molly，礼貌、专业、严格基于医学知识回答。
✅ RAG 私有知识库
支持 PDF 文档自动上传、解析、切片、向量化，构建本地医学知识库。
✅ 多轮对话记忆
基于 SQLite 数据库持久化存储对话历史，支持多会话管理、切换、删除。
✅ 完整对话管理
新建对话
切换历史对话
删除对话记录
保留上下文理解用户意图
✅ 友好 Web 界面
基于 Streamlit 开发，简洁美观，开箱即用，支持流式输出。
✅ 安全回答机制
无相关资料时不编造答案，引导用户咨询专业医生，保障医疗问答安全性。
技术栈
表格
模块	技术
前端界面	Streamlit
大模型	DeepSeek / OpenAI 兼容大模型
向量嵌入	智谱 AI Embedding
向量数据库	Chroma
文档处理	PDFMinerLoader（PDF 解析）
文本分割	RecursiveCharacterTextSplitter
对话记忆	SQLChatMessageHistory + SQLite
开发框架	LangChain
环境配置	python-dotenv
项目文件结构
plaintext
medical-chatbot-main/
├── main.py              # 项目入口，Streamlit 界面初始化
├── robot.py             # 医疗机器人核心类，对话 + 记忆 + RAG 逻辑
├── chroma.py            # PDF 解析、向量库、文档入库封装
├── funcs.py             # 会话管理、界面交互工具函数
├── requirements.txt     # 项目依赖
├── .env                 # 密钥配置文件
├── files/
│   ├── docs/            # 存放 PDF 医学文档
│   └── chat_history.db   # SQLite 对话历史数据库
└── README.md
