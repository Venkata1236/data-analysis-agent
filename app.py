# app.py
# Main entry point — Data Analysis Agent
# Concepts: Custom tools, @tool decorator, ReAct pattern

import os
from dotenv import load_dotenv
from core.data_loader import load_csv, get_dataframe_info
from core.agent import create_agent, run_analysis

# ── Load API key ──────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    print("❌ ERROR: Please set your OPENAI_API_KEY in the .env file.")
    exit(1)


def main():
    print("\n" + "=" * 60)
    print("       📊 DATA ANALYSIS AGENT")
    print("   Custom Tools + ReAct + LangChain + OpenAI")
    print("=" * 60)

    # ── Load CSV ──────────────────────────────────────────────
    print("\n📂 Enter path to your CSV file")
    print("   (Press Enter to use sample data)")
    file_path = input("Path: ").strip().strip('"').strip("'")

    if not file_path:
        file_path = "sample_data/sales_data.csv"
        print(f"   Using sample data: {file_path}")

    try:
        df = load_csv(file_path)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        exit(1)

    print("\n📋 Dataset Overview:")
    print(get_dataframe_info())

    # ── Create agent ──────────────────────────────────────────
    print("\n⏳ Initializing agent with custom tools...")
    agent = create_agent(API_KEY)
    print("✅ Agent ready with 6 custom tools!\n")

    print("-" * 60)
    print("💬 Ask questions about your data!")
    print("   Example questions:")
    print("   - What are the total sales by category?")
    print("   - Who is the top salesperson?")
    print("   - What is the average order value?")
    print("   - Show me top 5 products by sales")
    print("   - What is the correlation between quantity and sales?")
    print("   Type 'quit' to exit")
    print("-" * 60 + "\n")

    while True:
        try:
            query = input("You: ").strip()

            if not query:
                continue
            if query.lower() == "quit":
                print("\n👋 Bye!")
                break

            print("\n🤔 Analyzing...\n")
            result = run_analysis(agent, query)

            print("\n" + "=" * 60)
            print("📊 ANALYSIS RESULT")
            print("=" * 60)
            print(result["answer"])

            steps = result["steps"]
            if steps:
                print(f"\n🔧 Tools used: {len(steps)}")
                for i, step in enumerate(steps, 1):
                    action, observation = step
                    print(f"  Step {i}: {action.tool}({str(action.tool_input)[:60]})")
            print()

        except KeyboardInterrupt:
            print("\n\n👋 Bye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()