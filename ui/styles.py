import panel as pn

CSS = """
/* 🦷 BrightSmile Minimalist Medical Theme (Gray & Off-White) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

:root {
    --bg-offwhite: #fcfcfc;
    --container-white: #ffffff;
    --border-gray: #e2e8f0;
    --text-primary: #1a202c;
    --text-secondary: #4a5568;
    --text-muted: #718096;
    --accent-blue: #2d3748; /* Deep Steel/Slate Gray for buttons */
    --user-bubble: #edf2f7;
    --bot-bubble: #f8fafc;
}

body { 
    background-color: var(--bg-offwhite) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Global Container Fixes */
.chat-container {
    background: var(--container-white) !important;
    border-radius: 16px !important;
    border: 1px solid var(--border-gray) !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
    padding: 24px !important;
    max-width: 800px !important;
    margin: 40px auto !important;
}

/* Chat Area */
.chat-area {
    padding: 10px !important;
}

/* Message Bubbles - Clean & Minimal */
.user-msg {
    background: var(--user-bubble) !important;
    color: var(--text-primary) !important;
    border-radius: 12px 12px 2px 12px !important;
    padding: 12px 16px !important;
    margin-left: auto !important;
    max-width: 80% !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    border: 1px solid var(--border-gray) !important;
}

.bot-msg {
    background: var(--bot-bubble) !important;
    color: var(--text-primary) !important;
    border-radius: 12px 12px 12px 2px !important;
    padding: 12px 16px !important;
    margin-right: auto !important;
    max-width: 85% !important;
    font-size: 14px !important;
    border: 1px solid var(--border-gray) !important;
}

/* Headers & Labels */
h1, h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    margin-bottom: 10px !important;
}

.msg-label {
    font-size: 10px !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 4px !important;
}

/* Input Bar - Gemini Inspired Minimalist */
.input-wrapper {
    background: var(--bot-bubble) !important;
    border: 1px solid var(--border-gray) !important;
    border-radius: 24px !important;
    padding: 6px 12px !important;
    margin-top: 20px !important;
    display: flex !important;
    align-items: center !important;
}

.input-wrapper:focus-within {
    border-color: var(--text-muted) !important;
}

/* Buttons */
.bk-btn-primary {
    background-color: var(--accent-blue) !important;
    color: white !important;
    border-radius: 20px !important;
    font-weight: 500 !important;
}

.icon-btn {
    background: transparent !important;
    border: none !important;
    color: var(--text-muted) !important;
    cursor: pointer !important;
    font-size: 16px !important;
}

.quick-chip {
    background: white !important;
    border: 1px solid var(--border-gray) !important;
    color: var(--text-secondary) !important;
    padding: 6px 14px !important;
    border-radius: 100px !important;
    font-size: 13px !important;
    margin: 4px !important;
    transition: all 0.2s !important;
}

.quick-chip:hover {
    background: var(--user-bubble) !important;
    border-color: var(--text-muted) !important;
}

/* Footer Disclaimer */
.footer-text {
    font-size: 11px !important;
    color: var(--text-muted) !important;
    text-align: center !important;
    margin-top: 16px !important;
}
"""

def apply_styles():
    pn.extension(raw_css=[CSS])
