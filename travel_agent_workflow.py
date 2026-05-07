import gradio as gr
import requests
import time


# 核心通用大模型调用函数
def call_deepseek(api_key, prompt, system_prompt):
    if not api_key: return "⚠️ 请在顶部设置 API Key"
    url = "https://api.deepseek.com/chat/completions"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    data = {
        "model": "deepseek-v4-flash",
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
        "temperature": 0.6
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code != 200: return f"❌ API 错误: {res.text}"
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"❌ 运行异常: {e}"


# ==========================================
# 系统 A：旅拍多 Agent 流水线
# ==========================================
def travel_pipeline(api_key, user_req, camera_model):
    # 阶段 1：向导规划
    yield "🔄 [Agent 1: 本地向导] 正在进行空间时序规划...", "生成中...", "等待前置条件..."
    route = call_deepseek(api_key, user_req, "你是一个资深本地向导。请给出排版清晰、带时间轴的 Citywalk 路线。")
    if "❌" in route or "⚠️" in route:
        yield "❌ 流水线中断", route, ""
        return

    # 阶段 2：摄影指导 (依赖阶段 1 的结果)
    yield "🔄 [Agent 2: 摄影指导] 正在读取路线并适配参数...", route, "生成中..."
    photo = call_deepseek(api_key, f"规划路线如下：\n{route}\n用户设备：{camera_model}",
                          "你是一个商业摄影师。请针对上述路线中的打卡点，给出该相机的具体拍摄参数（光圈、快门、色彩）。")

    yield "✅ 旅拍流水线执行完毕！", route, photo


# ==========================================
# 系统 B：雅思多 Agent 流水线
# ==========================================
def ielts_pipeline(api_key, topic, target_score):
    # 阶段 1：词汇与思路拓展
    yield "🔄 [Agent 1: 语料大师] 正在提取高频词汇与短语...", "生成中...", "等待语料...", "等待范文..."
    vocab = call_deepseek(api_key, f"话题：{topic}\n目标分数：{target_score}",
                          "你是一个雅思词汇专家。请针对给定话题，输出 5 个地道的高分短语（Idioms/Collocations）和 3 个核心论点。")
    if "❌" in vocab or "⚠️" in vocab:
        yield "❌ 流水线中断", vocab, "", ""
        return

    # 阶段 2：范文撰写 (依赖阶段 1)
    yield "🔄 [Agent 2: 写作考官] 正在应用语料撰写满分范文...", vocab, "生成中...", "等待范文..."
    essay = call_deepseek(api_key, f"话题：{topic}\n必须使用的词汇与论点：\n{vocab}",
                          f"你是一个雅思写作考官。请使用上文提供的词汇，写一篇目标为 {target_score} 的高分段落。要求逻辑严密。")

    # 阶段 3：精批与解析 (依赖阶段 2)
    yield "🔄 [Agent 3: 语法助教] 正在对范文进行高光解析...", vocab, essay, "生成中..."
    review = call_deepseek(api_key, f"生成的范文：\n{essay}", "你是一个英语助教。请对上述范文进行赏析，指出为什么它能拿高分（分析复杂的句型和衔接词）。")

    yield "✅ 雅思流水线执行完毕！", vocab, essay, review


# ==========================================
# 前端 UI 设计 (双系统架构)
# ==========================================
# 采用极客暗色调，凸显高级感
custom_theme = gr.themes.Monochrome(
    primary_hue="indigo",
    font=[gr.themes.GoogleFont("Inter"), "sans-serif"]
)

with gr.Blocks(theme=custom_theme, title="AI Agent 双子星系统") as demo:
    # 全局头部
    gr.HTML("""
        <div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #1e1b4b, #312e81); border-radius: 12px; margin-bottom: 20px; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h1 style="margin: 0; font-size: 2.2em; font-weight: 800;">🌌 个人双领域多 Agent 调度中心</h1>
            <p style="margin-top: 8px; font-size: 1.1em; opacity: 0.85;">Domain-Driven Multi-Agent Architecture: 包含独立的生活服务与学术训练流水线</p>
        </div>
    """)

    # 全局设置
    with gr.Accordion("⚙️ 全局设置 (点击输入您的 API Key)", open=False):
        api_key_input = gr.Textbox(label="DeepSeek API Key", type="password")

    # 双系统大 Tab 切换
    with gr.Tabs():
        # -----------------------------------------------------
        # 系统 A：旅拍向导
        # -----------------------------------------------------
        with gr.TabItem("🧳 旅拍多 Agent 工作流"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📥 输入条件")
                    travel_req = gr.Textbox(label="行程需求", value="明天到达上海，第一天去武康路，第二天外滩。要求不累。", lines=4)
                    camera_model = gr.Textbox(label="摄影设备", value="佳能 G7X Mark III")
                    travel_btn = gr.Button("🚀 启动 [路线 -> 摄影] 协同流水线", variant="primary")
                    travel_status = gr.Markdown("状态：闲置中", label="当前执行状态")

                with gr.Column(scale=2):
                    gr.Markdown("### 📊 协同生成结果")
                    with gr.Accordion("📌 Agent 1 产出：时空路线规划", open=True):
                        route_out = gr.Markdown("等待执行...")
                    with gr.Accordion("📸 Agent 2 产出：硬件参数适配", open=True):
                        photo_out = gr.Markdown("等待前置节点完成...")

            travel_btn.click(
                travel_pipeline,
                inputs=[api_key_input, travel_req, camera_model],
                outputs=[travel_status, route_out, photo_out]
            )

        # -----------------------------------------------------
        # 系统 B：雅思陪练
        # -----------------------------------------------------
        with gr.TabItem("🎓 雅思多 Agent 工作流"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 📥 训练课题")
                    ielts_topic = gr.Textbox(label="雅思话题 (Task 2 或 Part 2)", value="Describe a long walk you ever had.",
                                             lines=3)
                    ielts_score = gr.Radio(label="目标分数", choices=["Band 6.5", "Band 7.5", "Band 8.0+"],
                                           value="Band 7.5")
                    ielts_btn = gr.Button("🚀 启动 [语料 -> 撰写 -> 批改] 协同流水线", variant="primary")
                    ielts_status = gr.Markdown("状态：闲置中", label="当前执行状态")

                with gr.Column(scale=2):
                    gr.Markdown("### 📊 协同生成结果")
                    with gr.Tabs():
                        with gr.TabItem("📚 Agent 1: 高分语料"):
                            vocab_out = gr.Markdown("等待提取...")
                        with gr.TabItem("✍️ Agent 2: 定制范文"):
                            essay_out = gr.Markdown("等待前置语料输入...")
                        with gr.TabItem("🔍 Agent 3: 考官解析"):
                            review_out = gr.Markdown("等待范文生成...")

            ielts_btn.click(
                ielts_pipeline,
                inputs=[api_key_input, ielts_topic, ielts_score],
                outputs=[ielts_status, vocab_out, essay_out, review_out]
            )

if __name__ == "__main__":
    demo.launch()