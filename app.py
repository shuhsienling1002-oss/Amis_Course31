import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 31: O Rakat", page_icon="🚶", layout="centered")

# --- CSS 美化 (動態藍紫色) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #E1BEE7; color: #4A148C; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #EDE7F6 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #673AB7;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #512DA8; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #F3E5F5;
        border-left: 5px solid #9575CD;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #D1C4E9; color: #311B92; border: 2px solid #673AB7; padding: 12px;
    }
    .stButton>button:hover { background-color: #B39DDB; border-color: #512DA8; }
    .stProgress > div > div > div > div { background-color: #673AB7; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 31: 18個單字 - User Fix) ---
vocab_data = [
    {"amis": "Romakat", "chi": "走 (正在走)", "icon": "🚶", "source": "Row 482", "morph": "Rakat + om"},
    {"amis": "Comikay", "chi": "跑 (正在跑)", "icon": "🏃", "source": "Row 983", "morph": "Cikay + om"},
    {"amis": "Minokay", "chi": "回家 / 回去", "icon": "🏠", "source": "Row 525", "morph": "Mi + Nokay"},
    {"amis": "Tatayra", "chi": "將去 / 要去", "icon": "🔜", "source": "Row 340", "morph": "Ta-Tayra (未來)"},
    {"amis": "Pasicowa", "chi": "朝向哪裡", "icon": "🧭", "source": "Row 731", "morph": "Pasi-Cowa"},
    {"amis": "Pasitimol", "chi": "朝向南方", "icon": "⬇️", "source": "Row 731", "morph": "Pasi-Timol"},
    {"amis": "Pakacowa", "chi": "經由哪裡", "icon": "🛤️", "source": "Row 726", "morph": "Paka-Cowa"},
    {"amis": "Kicowa", "chi": "從哪裡 / 置於哪", "icon": "📍", "source": "Row 725", "morph": "Ki-Cowa"},
    {"amis": "To'eman", "chi": "天黑 / 黑暗", "icon": "🌑", "source": "Row 525", "morph": "State"},
    {"amis": "Korakorsa", "chi": "就慢跑", "icon": "🏃‍♂️", "source": "User Fix", "morph": "Adverb"}, # 修正
    {"amis": "Dimata'", "chi": "挑 / 扛 (詞根)", "icon": "🏋️", "source": "User Fix", "morph": "Root"}, # 修正
    {"amis": "Misahalifet", "chi": "比賽 / 使勁", "icon": "🏁", "source": "Row 983", "morph": "Misa-Ha-Lifet"},
    {"amis": "Fafaed", "chi": "上面 / 表面", "icon": "⬆️", "source": "Row 734", "morph": "Locative"},
    {"amis": "Tala", "chi": "前往 / 達到", "icon": "👉", "source": "Row 734", "morph": "Direction"},
    {"amis": "Rakat", "chi": "走 / 路程 (詞根)", "icon": "👣", "source": "Root", "morph": "Root"},
    {"amis": "Cikay", "chi": "跑 (詞根)", "icon": "👟", "source": "Root", "morph": "Root"},
    {"amis": "Nokay", "chi": "回家 (詞根)", "icon": "🔙", "source": "Root", "morph": "Root"},
    {"amis": "Lifet", "chi": "測驗 / 勝負 (詞根)", "icon": "⚖️", "source": "Root", "morph": "Root"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Mingataay ciira takowanan a romakat.", "chi": "他正往我這邊走來。", "icon": "🚶", "source": "Row 482"},
    {"amis": "Misahalifet kami a comikay i cairaan.", "chi": "我們使勁地跟他們賽跑。", "icon": "🏃", "source": "Row 983"},
    {"amis": "To'emanto ko romi'ad, korakorsa a minokay.", "chi": "天黑了，就慢跑回家。", "icon": "🌑", "source": "Row 525 (Trans. Updated)"},
    {"amis": "O tatayra kita i Taypak.", "chi": "我們將去台北。", "icon": "🚅", "source": "Row 340"},
    {"amis": "Pasicowaen koni a fawahan? Pasitimolen.", "chi": "這道門要朝向哪裡？要朝向南邊。", "icon": "🚪", "source": "Row 731"},
    {"amis": "Pakacowa ko kapah no niyaro' a minokay?", "chi": "部落的年輕人經由哪裡回家？", "icon": "🛤️", "source": "Row 726"},
    {"amis": "Midimata' ca ina to kakaenen.", "chi": "媽媽他們挑著食物。", "icon": "🍱", "source": "Row 447"},
    {"amis": "Talacowa kita i fafaed no riyar?", "chi": "我們在海上要去哪裡？", "icon": "🌊", "source": "Row 734"},
    {"amis": "Kicowaen no mita a mi'araw?", "chi": "大家要從哪裡看？", "icon": "👀", "source": "Row 725"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "To'emanto ko romi'ad, korakorsa a...",
        "audio": "To'emanto ko romi'ad, korakorsa a",
        "options": ["Minokay (回家)", "Comikay (跑)", "Romakat (走)"],
        "ans": "Minokay (回家)",
        "hint": "Row 525: 天黑了就慢跑回家"
    },
    {
        "q": "單字測驗：Korakorsa",
        "audio": "Korakorsa",
        "options": ["就慢跑", "就睡覺", "就吃飯"],
        "ans": "就慢跑",
        "hint": "User Fix: Korakorsa"
    },
    {
        "q": "單字測驗：Dimata'",
        "audio": "Dimata'",
        "options": ["挑/扛 (詞根)", "推 (詞根)", "拉 (詞根)"],
        "ans": "挑/扛 (詞根)",
        "hint": "用肩膀做的事"
    },
    {
        "q": "Pasicowaen koni a fawahan?",
        "audio": "Pasicowaen koni a fawahan",
        "options": ["這道門要朝向哪裡？", "這道門要開嗎？", "這是誰的門？"],
        "ans": "這道門要朝向哪裡？",
        "hint": "Pasi-cowa (朝向哪裡)"
    },
    {
        "q": "單字測驗：Comikay",
        "audio": "Comikay",
        "options": ["跑 (正在跑)", "走 (正在走)", "飛 (正在飛)"],
        "ans": "跑 (正在跑)",
        "hint": "詞根 Cikay (跑) + om"
    },
    {
        "q": "單字測驗：Pakacowa",
        "audio": "Pakacowa",
        "options": ["經由哪裡", "朝向哪裡", "從哪裡"],
        "ans": "經由哪裡",
        "hint": "Paka- (經由/路過)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #512DA8;'>Unit 31: O Rakat</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>移動與方向 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #512DA8;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #D1C4E9; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #512DA8;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經掌握移動與方向的表達了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()
