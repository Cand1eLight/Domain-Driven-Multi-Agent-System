# Domain-Driven-Multi-Agent-System
A personal dual-track AI Agent workflow station for travel planning and IELTS training.

# 🌌 Domain-Driven Multi-Agent System (双子星智能体调度中心)

基于原生 Python 与 Gradio 构建的个人双轨 Agent 自动化工作流系统，旨在解决长链路、跨领域（生活辅助与学术训练）的复杂逻辑推理任务。

## 🎯 核心架构与解决痛点

传统单体大模型在处理复杂需求时容易产生幻觉或丢失上下文。本项目采用**领域驱动（Domain-Driven）**架构，将复杂任务动态路由并拆解为多 Agent 串行协同：

- **Planner (规划节点)**：负责宏观目标拆解（如时空路线规划、雅思核心语料提取）。
- **Executor (执行节点)**：依托前置上下文进行跨模态推理（如特定硬件参数自适应、限定语料范文撰写）。
- **Reviewer (评估节点)**：进行逻辑长文本的质量解析与二次反馈。

## 🚀 业务模块展示

### 1. 🧳 旅拍调度工作流 (Travel Pipeline)
- **Agent A (本地向导)**：时空路径推理，生成带时间轴的坐标点。
- **Agent B (摄影师)**：读取前置空间数据，结合用户实际硬件设备（如 G7X M3）计算并下发场景机内参数。

### 2. 🎓 学术训练工作流 (IELTS Pipeline)
- **Agent A (语料库)**：提取目标分数词汇。
- **Agent B (撰写者)**：依赖前置词汇生成强逻辑文本。
- **Agent C (评估者)**：对成文进行语法与连贯性长文本重评估。

## 📸 运行效果截图

*(💡提示：小米审核老师，请看以下原生部署截图证明)*

![系统主界面与 Agent 调度过程](https://204180371.xyz/PicGo/20260507142336785.png)

## 🛠️ 快速启动

```bash
# 1. 安装核心依赖
pip install gradio requests

# 2. 启动系统
python travel_agent_workflow.py
