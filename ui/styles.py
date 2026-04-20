import panel as pn

CSS = """
/* 🦷 BrightSmile "Sleek Professional" Design System 2025 */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg-main: #f8fafc;
    --card-white: #ffffff;
    --text-deep: #0f172a;
    --text-muted: #64748b;
    --user-blue: #1e293b;
    --bot-gray: #f1f5f9;
    --accent-blue: #3b82f6;
    --border-subtle: #e2e8f0;
    --shadow-sm: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
}

body { 
    background-color: var(--bg-main) !important;
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-deep) !important;
}

/* Centralized Card Container */
.chat-container {
    background: var(--card-white) !important;
    border-radius: 24px !important;
    border: 1px solid var(--border-subtle) !important;
    box-shadow: var(--shadow-lg) !important;
    padding: 32px !important;
    max-width: 800px !important;
    margin: 60px auto !important;
}

/* Chat History Window */
.chat-area {
    padding: 10px !important;
    margin-bottom: 20px !important;
}

/* Message Bubbles - Sophisticated Design */
.user-msg {
    background: var(--user-blue) !important;
    color: white !important;
    border-radius: 20px 20px 4px 20px !important;
    padding: 14px 20px !important;
    margin-left: auto !important;
    max-width: 75% !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    box-shadow: var(--shadow-sm) !important;
}

.bot-msg {
    background: var(--bot-gray) !important;
    color: var(--text-deep) !important;
    border-radius: 20px 20px 20px 4px !important;
    padding: 14px 20px !important;
    margin-right: auto !important;
    max-width: 80% !important;
    font-size: 15px !important;
    border: 1px solid var(--border-subtle) !important;
}

/* Labels */
.msg-label {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    margin-bottom: 6px !important;
    opacity: 0.8;
}

/* Modern Input Wrapper */
.input-wrapper {
    background: var(--bot-gray) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 100px !important;
    padding: 10px 20px !important;
    margin-top: 24px !important;
    display: flex !important;
    align-items: center !important;
    transition: all 0.3s ease !important;
}

.input-wrapper:focus-within {
    background: white !important;
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1) !important;
}

/* Buttons */
.bk-btn-primary {
    background-color: var(--accent-blue) !important;
    border-radius: 100px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
}

.quick-chip {
    background: white !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-deep) !important;
    padding: 8px 18px !important;
    border-radius: 100px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    margin: 6px !important;
    transition: all 0.2s !important;
    cursor: pointer !important;
}

.quick-chip:hover {
    background: var(--bot-gray) !important;
    border-color: var(--text-muted) !important;
    transform: translateY(-1px) !important;
}

/* Scrollbar */
.chat-area::-webkit-scrollbar { width: 6px; }
.chat-area::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
"""

def apply_styles():
    pn.extension(raw_css=[CSS])
