# 📊 Data Analysis Agent

> Upload any CSV — ask questions in plain English — powered by custom LangChain tools

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3.7-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange)
![Pandas](https://img.shields.io/badge/Pandas-2.2.2-purple)
![Streamlit](https://img.shields.io/badge/Streamlit-1.41.1-red)

---

## 📌 What Is This?

A data analysis agent that takes any CSV file and answers questions about it in plain English. Built using custom LangChain tools — every tool is written from scratch using the `@tool` decorator.

---

## 🗺️ Simple Flow

```
Upload CSV file
        ↓
Agent calls get_dataset_info
(understands columns and structure)
        ↓
You ask: "What are total sales by region?"
        ↓
Agent picks the right custom tool
(group_and_aggregate)
        ↓
Tool runs pandas code on your data
        ↓
Agent returns clear answer with insights
```

---

## 🏗️ Detailed Architecture

```
User
 ├── streamlit_app.py   → Web UI (3-step flow)
 └── app.py             → Terminal interface
          │
          ▼
      core/
      ├── data_loader.py     → Load CSV → global pandas DataFrame
      ├── custom_tools.py    → 6 custom tools with @tool decorator
      └── agent.py           → create_react_agent + AgentExecutor
          │
          ▼
   6 Custom Tools
   ├── get_dataset_info      → understand data structure
   ├── calculate_statistics  → mean, sum, min, max, std
   ├── filter_data           → filter rows by condition
   ├── group_and_aggregate   → group by + sum/mean/count
   ├── find_top_n            → top or bottom N rows
   └── calculate_correlation → correlation between columns
          │
          ▼
      OpenAI API
   gpt-3.5-turbo generates final answer
```

---

## 📁 Project Structure

```
data_analysis_agent/
├── app.py                   ← Terminal version
├── streamlit_app.py         ← Web UI (deploy this)
├── sample_data/
│   └── sales_data.csv       ← Sample data for testing
├── core/
│   ├── __init__.py
│   ├── data_loader.py       ← Load CSV + global DataFrame
│   ├── custom_tools.py      ← 6 custom tools with @tool
│   └── agent.py             ← ReAct agent setup
├── .env                     ← API key (never push!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Custom Tools Built from Scratch

| Tool | Input Format | Example |
|---|---|---|
| `get_dataset_info` | any string | `"info"` |
| `calculate_statistics` | column name | `"total_sales"` |
| `filter_data` | column=value | `"region=North"` |
| `group_and_aggregate` | group,col,func | `"category,total_sales,sum"` |
| `find_top_n` | n,column,direction | `"5,total_sales,top"` |
| `calculate_correlation` | col1,col2 | `"quantity,total_sales"` |

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| **@tool decorator** | Turns any Python function into a LangChain tool |
| **Tool docstring** | Agent reads this to decide WHEN to use the tool |
| **Global DataFrame** | Shared across all tools via get_dataframe() |
| **ReAct pattern** | Agent thinks before every tool call |
| **temperature=0.0** | Zero creativity — precise data analysis |

---

## 💡 The @tool Decorator

```python
# Without @tool — just a Python function
def calculate_statistics(column_name: str) -> str:
    ...

# With @tool — becomes a LangChain tool
@tool
def calculate_statistics(column_name: str) -> str:
    """
    Agent reads THIS docstring to decide when to use this tool.
    Clear docstring = smarter agent decisions.
    """
    ...
```

---

## 💬 Example Questions

```
What are the total sales by category?
Who is the top salesperson by total sales?
Show me top 5 products by total sales
What is the average order value?
What is the correlation between quantity and total sales?
Filter orders where total_sales > 2000
What are the sales by region?
```

---

## ⚙️ Local Setup

**Step 1 — Clone the repo:**
```bash
git clone https://github.com/YOUR_USERNAME/data-analysis-agent.git
cd data_analysis_agent
```

**Step 2 — Install dependencies:**
```bash
pip install -r requirements.txt
```

**Step 3 — Add your OpenAI API key in `.env`:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

**Step 4 — Run:**

Streamlit UI:
```bash
python -m streamlit run streamlit_app.py
```

Terminal version:
```bash
python app.py
```

---

## 🚀 Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → select `streamlit_app.py`
4. Go to Settings → Secrets → add:
```toml
OPENAI_API_KEY = "sk-your-key-here"
```
5. Click Deploy ✅

---

## 📦 Tech Stack

- **LangChain** — @tool decorator, create_react_agent, AgentExecutor
- **OpenAI** — GPT-3.5-turbo
- **Pandas** — CSV loading, filtering, grouping, statistics
- **NumPy** — Mathematical calculations
- **Streamlit** — Web UI with 3-step flow
- **python-dotenv** — API key management

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)