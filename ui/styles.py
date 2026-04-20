import panel as pn

CSS = """
/* Hospitality-First "Clinical Zen" Design System 2025 */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');

:root {
    --primary-blue: #1a365d;
    --accent-teal: #38b2ac;
    --soft-gray: #f8fafc;
    --warm-white: #ffffff;
    --glass-bg: rgba(255, 255, 255, 0.85);
    --shadow-premium: 0 20px 40px rgba(0, 0, 0, 0.04), 0 5px 15px rgba(0, 0, 0, 0.03);
    --radius-lg: 32px;
    --radius-md: 20px;
}

body { 
    background: linear-gradient(135deg, #f0f4f8 0%, #ffffff 100%);
    font-family: 'Outfit', sans-serif;
    color: var(--primary-blue);
    margin: 0;
}

/* Glassmorphism Container */
.chat-container {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-premium);
    padding: 40px;
    max-width: 900px;
    margin: 40px auto;
    border: 1px solid rgba(255, 255, 255, 0.5);
    animation: slideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Premium Header */
.header-bar {
    background: transparent;
    padding: 20px 0;
    margin-bottom: 30px;
}

.header-bar h2 {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: var(--primary-blue);
    letter-spacing: -0.5px;
}

/* Message Bubbles: Organic Shapes */
.user-msg {
    background: linear-gradient(135deg, var(--primary-blue) 0%, #2c5282 100%);
    color: white;
    border-radius: 24px 24px 4px 24px;
    padding: 18px 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 20px rgba(26, 54, 93, 0.1);
    font-weight: 400;
    line-height: 1.6;
}

.bot-msg {
    background: white;
    color: var(--primary-blue);
    border-radius: 24px 24px 24px 4px;
    padding: 18px 24px;
    margin-bottom: 20px;
    border: 1px solid #edf2f7;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
}

/* Chips: Minimalist Boutique Style */
.quick-chip {
    background: white;
    border: 1px solid #e2e8f0;
    color: var(--primary-blue);
    padding: 10px 22px;
    border-radius: 50px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin: 6px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.quick-chip:hover {
    background: var(--primary-blue);
    color: white;
    border-color: var(--primary-blue);
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(26, 54, 93, 0.1);
}

/* Treatment Visualizer Cards */
.treatment-card {
    background: linear-gradient(to right, #f8fafc, #ffffff);
    border-left: 4px solid var(--accent-teal);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
}

/* Input Area: Floating Bar */
.input-area {
    background: white;
    border-radius: 100px;
    padding: 8px 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    margin-top: 30px;
    border: 1px solid #edf2f7;
}

.bk-btn-primary {
    background: var(--primary-blue) !important;
    border-radius: 100px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}

/* Animations */
.stagger-1 { animation-delay: 0.1s; }
.stagger-2 { animation-delay: 0.2s; }
"""

def apply_styles():
    pn.extension(raw_css=[CSS])
