import panel as pn

CSS = """
/* Professional Dental "Clinical Zen" Design System */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

:root {
    --primary-blue: #1a365d;
    --secondary-blue: #2c5282;
    --medical-blue: #ebf8ff;
    --accent-teal: #38b2ac;
    --bg-light: #f7fafc;
    --text-dark: #2d3748;
    --shadow-soft: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
}

body { 
    background-color: var(--bg-light); 
    font-family: 'Outfit', sans-serif;
    color: var(--text-dark);
}

/* Main Container: Boutique Clinic Style */
.chat-container {
    background: white;
    border-radius: 30px;
    box-shadow: var(--shadow-soft);
    padding: 30px;
    max-width: 1000px;
    margin: 20px auto;
    border: 1px solid #edf2f7;
    position: relative;
    overflow: hidden;
}

/* Background Watermark */
.chat-container::before {
    content: "🦷";
    position: absolute;
    top: -50px;
    right: -50px;
    font-size: 300px;
    opacity: 0.03;
    pointer-events: none;
}

/* Header: Professional Nav */
.header-bar {
    background: white;
    color: var(--primary-blue);
    padding: 20px 40px;
    border-radius: 20px;
    margin-bottom: 20px;
    border: 1px solid #edf2f7;
    box-shadow: var(--shadow-soft);
}

.header-bar h2 {
    font-weight: 600;
    letter-spacing: -0.5px;
}

/* Chat Area Scrollbar */
.chat-area::-webkit-scrollbar {
    width: 6px;
}
.chat-area::-webkit-scrollbar-thumb {
    background: #cbd5e0;
    border-radius: 10px;
}

/* Message Bubbles: Fade-in Animation */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-msg, .bot-msg {
    animation: fadeInUp 0.4s ease-out forwards;
    position: relative;
    max-width: 80%;
}

/* User Message: Clean Blue */
.user-msg {
    background: var(--primary-blue);
    color: white;
    border-radius: 20px 20px 0 20px;
    padding: 15px 25px;
    margin-bottom: 15px;
    box-shadow: 0 4px 12px rgba(26, 54, 93, 0.1);
}

/* Bot Message: Clinical White/Gray */
.bot-msg {
    background: var(--medical-blue);
    color: var(--primary-blue);
    border-radius: 20px 20px 20px 0;
    padding: 15px 25px;
    margin-bottom: 15px;
    border: 1px solid #bee3f8;
}

/* Quick Action Chips */
.quick-chip {
    background: white;
    border: 1px solid var(--primary-blue);
    color: var(--primary-blue);
    padding: 8px 18px;
    border-radius: 50px;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
    margin: 5px;
    display: inline-block;
}

.quick-chip:hover {
    background: var(--primary-blue);
    color: white;
    transform: scale(1.05);
}

/* Typing Indicator */
.typing-dots {
    display: flex;
    gap: 4px;
    padding: 10px;
}
.dot {
    width: 8px;
    height: 8px;
    background: var(--primary-blue);
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out;
}
.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
    0%, 80%, 100% { transform: scale(0); }
    40% { transform: scale(1); }
}

/* Input Area: Glassmorphism */
.input-area {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border-top: 1px solid #edf2f7;
    padding-top: 20px;
    margin-top: 10px;
}

/* Custom Primary Button */
.bk-btn-primary {
    background-color: var(--primary-blue) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
}
"""

def apply_styles():
    pn.extension(raw_css=[CSS])
