# 🦷 BrightSmile Dental Portal (Professional AI Agent)

A premium, enterprise-grade AI conversational agent and clinic management portal designed for modern dental practices.

![AI Engine](https://img.shields.io/badge/AI-Gemini%201.5%20/%202.0%20Flash-blue)
![UI Framework](https://img.shields.io/badge/UI-Panel%20(Clinical%20Zen)-teal)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20MVVM-green)

## ✨ Peak Features

### 🧠 Advanced AI & Knowledge
- **RAG-Powered Intelligence:** Uses Retrieval-Augmented Generation to provide expert-verified answers from a local dental knowledge base.
- **Sentiment-Aware Triage:** Automatically detects dental emergencies and pain, escalating them to an priority hotline protocol.
- **Multilingual Support:** Seamlessly communicates in the patient's native language.

### 💎 Clinical Zen UI
- **Premium Aesthetics:** A high-end "Medical Blue" theme with glassmorphism and modern typography.
- **Micro-Animations:** Fluid message fade-ins and animated typing indicators for an organic feel.
- **Quick Action Chips:** Tap-to-interact buttons for common tasks like booking, hours, and location.

### 🏥 Staff Command Center
- **Secure Dashboard:** Password-protected staff portal (Admin Access).
- **Live Analytics:** Real-time stats on appointment volume and status.
- **Data Export:** One-click CSV export of all patient consultation records.

## 📂 Project Structure

```text
dental_bot/
├── app.py                # Main Entry Point & Router
├── config.py             # Global Configuration & Security
├── core/                 # Business Logic Layer
│   ├── gemini_helper.py  # Gemini AI & RAG Integration
│   ├── database.py       # SQLite Persistence
│   ├── admin_logic.py    # Staff Analytics & Export
│   ├── booking_parser.py # Appointment Payload Normalization
│   ├── faq.py            # FAQ Keyword Matching
│   ├── session.py        # Session Expiry Logic
│   ├── logger.py         # Production-grade Logging
│   └── knowledge_base/   # Expert Dental Documentation
├── ui/                   # Presentation Layer
│   ├── styles.py         # "Clinical Zen" Design System
│   └── views/            # Modular UI Components (Chat/Admin)
├── tests/                # Unit Tests (pytest)
├── .github/workflows/    # CI/CD (GitHub Actions)
└── data/                 # Persistent Storage
```

## 🚀 Getting Started

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Copy `.env.example` to `.env` and fill your real values:
   ```bash
   cp .env.example .env
   # PowerShell:
   # Copy-Item .env.example .env
   ```

   Required variables:
   ```text
   GEMINI_API_KEY=your_key_here
   ACCESS_CODE=your_patient_portal_code
   ADMIN_PASSWORD=your_staff_dashboard_password
   ALLOWED_WEBSOCKET_ORIGIN=your-domain.com
   ADMIN_SESSION_TIMEOUT_MINUTES=15
   ```

3. **Run the Portal:**
   ```bash
   python app.py
   ```

---
*Developed with ❤️ for premium dental care.*
