import panel as pn

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-main: #0e141b;
    --bg-elev: #111923;
    --surface: #141d28;
    --surface-soft: #1a2531;
    --surface-highlight: #202d3b;
    --text-primary: #e6edf5;
    --text-secondary: #9db0c4;
    --text-muted: #7f93a8;
    --accent: #69a6ff;
    --accent-strong: #8ab8ff;
    --border: #263647;
    --ring: rgba(105, 166, 255, 0.25);
    --radius-lg: 16px;
    --radius-md: 10px;
    --shadow-sm: 0 3px 14px rgba(0, 0, 0, 0.25);
    --shadow-md: 0 18px 32px rgba(0, 0, 0, 0.3);
}

body {
    background: linear-gradient(180deg, #0b1118 0%, #0f1720 100%) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em;
}

.bk-root, .bk, .bk-clearfix {
    color: var(--text-primary) !important;
}

.app-shell {
    max-width: 1240px !important;
    margin: 14px auto 28px auto !important;
    padding: 0 16px !important;
}

.top-nav {
    background: rgba(20, 29, 40, 0.88) !important;
    backdrop-filter: blur(10px);
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 9px 12px !important;
    margin-bottom: 12px !important;
}

.brand-title {
    margin: 0 !important;
    font-size: 0.95rem !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em;
}

.main-content {
    min-height: 80vh;
}

.chat-container, .admin-surface {
    background: linear-gradient(180deg, var(--surface), var(--surface-soft)) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-md) !important;
    padding: 16px !important;
    margin: 0 auto !important;
    width: min(1020px, 100%) !important;
}

.chat-area {
    background: #101a24 !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 10px !important;
    margin: 10px 0 !important;
}

.user-msg {
    background: linear-gradient(135deg, #2f4f6f, #385f86) !important;
    color: #eff6ff !important;
    border: 1px solid #45688d !important;
    border-radius: 12px 12px 3px 12px !important;
    padding: 9px 12px !important;
    margin-left: auto !important;
    max-width: 70% !important;
    font-size: 13px !important;
    line-height: 1.45 !important;
    box-shadow: var(--shadow-sm) !important;
}

.bot-msg {
    background: #182430 !important;
    color: var(--text-primary) !important;
    border-radius: 12px 12px 12px 3px !important;
    padding: 9px 12px !important;
    margin-right: auto !important;
    max-width: 76% !important;
    font-size: 13px !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow-sm) !important;
}

.msg-label {
    font-size: 9px !important;
    font-weight: 600 !important;
    color: var(--text-muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.09em !important;
    margin-bottom: 5px !important;
}

.input-wrapper {
    background: #121b25 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 5px 7px !important;
    margin-top: 10px !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    box-shadow: var(--shadow-sm) !important;
}

.input-wrapper:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 4px var(--ring) !important;
}

.icon-btn {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
    background: #1b2734 !important;
    color: var(--text-secondary) !important;
    min-height: 34px !important;
}

.bk-btn-primary, .nav-btn {
    background-color: #2f4560 !important;
    color: #ecf4ff !important;
    border-radius: 7px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s ease !important;
}

.bk-btn-primary:hover, .nav-btn:hover {
    background-color: #3f5d80 !important;
    transform: translateY(-1px);
}

.quick-chip {
    background: #16222f !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    padding: 6px 12px !important;
    border-radius: 999px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    margin: 4px !important;
    transition: all 0.2s !important;
}

.quick-chip:hover {
    background: #1d2b39 !important;
    border-color: #3a4f65 !important;
    transform: translateY(-1px) !important;
}

.admin-card {
    background: #161f2b !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important;
    padding: 12px !important;
    box-shadow: var(--shadow-sm) !important;
}

.stat-value {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #8bb9ff !important;
}

.bk-input, .bk-form-input, .bk-password-input {
    background: #111a24 !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 8px !important;
    min-height: 36px !important;
}

.bk-input::placeholder, .bk-form-input::placeholder, .bk-password-input::placeholder {
    color: var(--text-muted) !important;
}

.bk-tab {
    color: var(--text-secondary) !important;
}

.bk-tab.bk-active {
    color: var(--text-primary) !important;
    border-color: var(--accent) !important;
}

.bk p, .bk li, .bk label, .bk span, .bk div {
    line-height: 1.4 !important;
}
"""

def apply_styles():
    pn.extension(raw_css=[CSS])
