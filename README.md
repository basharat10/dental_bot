# 🦷 BrightSmile DentalBot

A premium, AI-powered conversational assistant for modern dental clinics. Built with Gemini 1.5/2.0 Flash and Panel.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![AI](https://img.shields.io/badge/AI-Gemini%20Flash-orange)

## ✨ Features
- **💎 Premium UI:** Modern teal-themed chat interface with a secure clinic portal.
- **🧠 Hybrid AI:** Combines Gemini 1.5/2.0 Flash with a local FAQ engine for lightning-fast responses.
- **🗄️ Database Integration:** Saves all appointments automatically to a local SQLite database.
- **🔐 Secure Access:** Protected by a clinic access code to prevent spam bookings.
- **⚡ Instant Answers:** Local FAQ system handles common clinic questions instantly without API calls.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+
- A Google AI Studio API Key

### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory and add your key:
```text
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the App
```bash
python app.py
```
**Access Code:** `SMILE2025`

## 📂 Project Structure
- `app.py`: Main UI and application logic.
- `core/`: Backend modules (Database, FAQ, AI Helper).
- `data/`: SQLite database storage.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

---
*Created with ❤️ for BrightSmile Dental Clinic.*
