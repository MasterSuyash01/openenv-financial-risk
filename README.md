# 💰 Financial Compliance & Fraud Detection OpenEnv

## 🚀 Overview

This project implements a **real-world OpenEnv environment** simulating financial fraud detection workflows used by banks and fintech companies.

Agents act as fraud analysts who must:
- Analyze transactions
- Assess risk
- Make decisions:
  - approve
  - flag
  - escalate

---

## 🧠 Why This Matters

Fraud detection is a critical real-world problem involving:
- Risk analysis
- Pattern recognition
- Decision-making under uncertainty
- Regulatory compliance

This environment enables evaluation of AI agents in a **high-impact, real-world scenario**.

---

## ⚙️ Environment Design

### 🔍 Observation Space

Each step provides:
- Transaction details (amount, country, history, pattern)
- Step number
- Hints
- Feedback from previous actions

---

### 🎯 Action Space

Agents must output:

```json
{
  "action_type": "analyze | decide",
  "content": "text or decision"
}
