# 💼 Mili Portfolio Advisor Agent

An AI-powered portfolio review assistant that analyzes client portfolio data, evaluates portfolio risk alignment, and generates an advisor-friendly portfolio review using deterministic Python tools and a local LLM.


>
> ⚠️ This project is an advisor-support prototype and does not provide automated financial advice or execute trades.

---

## 🚀 Overview

The Mili Portfolio Advisor Agent combines:

- Deterministic portfolio analysis using Python and Pandas
- Rule-based risk analysis
- Agent orchestration using the OpenAI Agents SDK
- Local LLM inference using Ollama
- Qwen3 4B for natural-language generation
- Streamlit for the user interface

The core design principle is:

> **Use deterministic code for financial calculations and use the LLM for interpretation and explanation.**

This reduces the risk of the LLM hallucinating or modifying numerical financial results.

---

## 🎯 Problem Statement

Financial advisors often need to quickly review a client's:

- Asset allocation
- Sector exposure
- Individual holding concentration
- Expense ratios
- Risk tolerance
- Investment horizon

Manually analyzing these values can be repetitive.

This project provides an AI-assisted workflow that takes structured portfolio and client information and produces a concise advisor-facing review.

---

# 🏗️ Architecture

```text
                         USER
                          |
                          v
                   ┌─────────────┐
                   │  Streamlit  │
                   │     UI      │
                   └──────┬──────┘
                          |
                          v
                   ┌─────────────┐
                   │    Agent    │
                   │ Agents SDK  │
                   └──────┬──────┘
                          |
             ┌────────────┴────────────┐
             |                         |
             v                         v
   ┌──────────────────┐      ┌──────────────────┐
   │ Portfolio        │      │ Risk             │
   │ Analyzer Tool    │      │ Analyzer Tool    │
   └────────┬─────────┘      └────────┬─────────┘
            |                         |
            v                         v
      Python/Pandas              Python Rules
            |                         |
            └────────────┬────────────┘
                         |
                         v
                Structured Results
                         |
                         v
                 ┌──────────────┐
                 │   Ollama     │
                 │   Qwen3 4B   │
                 └──────┬───────┘
                        |
                        v
                Advisor Review
                        |
                        v
                   Streamlit
