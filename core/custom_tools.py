# core/custom_tools.py
# Custom tools built from scratch using @tool decorator
# Concept: Tool definition — any Python function becomes an agent tool

import pandas as pd
import numpy as np
from langchain.tools import tool
from core.data_loader import get_dataframe, get_dataframe_info


# ── Tool 1: Get Dataset Info ──────────────────────────────────
@tool
def get_dataset_info(query: str) -> str:
    """
    Returns information about the loaded dataset.
    Use this FIRST before any other tool to understand
    the structure, columns, and sample data.
    Input: any string like 'info' or 'describe dataset'
    """
    try:
        return get_dataframe_info()
    except Exception as e:
        return f"Error: {str(e)}"


# ── Tool 2: Calculate Statistics ─────────────────────────────
@tool
def calculate_statistics(column_name: str) -> str:
    """
    Calculates statistics for a numeric column.
    Returns: mean, median, min, max, sum, std deviation.
    Input: the exact column name from the dataset.
    Example input: 'total_sales' or 'quantity'
    """
    try:
        df = get_dataframe()

        if column_name not in df.columns:
            return f"Column '{column_name}' not found. Available columns: {list(df.columns)}"

        if not pd.api.types.is_numeric_dtype(df[column_name]):
            return f"Column '{column_name}' is not numeric."

        col = df[column_name]
        stats = {
            "count": len(col),
            "sum": round(col.sum(), 2),
            "mean": round(col.mean(), 2),
            "median": round(col.median(), 2),
            "min": round(col.min(), 2),
            "max": round(col.max(), 2),
            "std_deviation": round(col.std(), 2)
        }

        result = f"Statistics for '{column_name}':\n"
        for key, value in stats.items():
            result += f"  {key}: {value}\n"

        return result

    except Exception as e:
        return f"Error calculating statistics: {str(e)}"


# ── Tool 3: Filter and Query ──────────────────────────────────
@tool
def filter_data(filter_query: str) -> str:
    """
    Filters the dataset based on a condition and returns results.
    Input format: 'column_name=value' or 'column_name>value'
    Supports operators: =, >, <, >=, <=
    Examples:
    - 'category=Electronics'
    - 'total_sales>1000'
    - 'region=North'
    """
    try:
        df = get_dataframe()

        # Parse operators
        for op in ['>=', '<=', '>', '<', '=']:
            if op in filter_query:
                parts = filter_query.split(op, 1)
                column = parts[0].strip()
                value = parts[1].strip()

                if column not in df.columns:
                    return f"Column '{column}' not found. Available: {list(df.columns)}"

                # Apply filter
                if op == '=':
                    # Try numeric first, then string
                    try:
                        filtered = df[df[column] == float(value)]
                    except ValueError:
                        filtered = df[df[column] == value]
                elif op == '>':
                    filtered = df[df[column] > float(value)]
                elif op == '<':
                    filtered = df[df[column] < float(value)]
                elif op == '>=':
                    filtered = df[df[column] >= float(value)]
                elif op == '<=':
                    filtered = df[df[column] <= float(value)]

                if len(filtered) == 0:
                    return f"No records found for filter: {filter_query}"

                return f"Found {len(filtered)} records:\n{filtered.to_string(index=False)}"

        return "Invalid filter format. Use: column=value or column>value"

    except Exception as e:
        return f"Error filtering data: {str(e)}"


# ── Tool 4: Group and Aggregate ───────────────────────────────
@tool
def group_and_aggregate(query: str) -> str:
    """
    Groups data by a column and calculates aggregations.
    Input format: 'group_by_column,agg_column,agg_function'
    Supported functions: sum, mean, count, max, min
    Examples:
    - 'category,total_sales,sum'
    - 'region,total_sales,mean'
    - 'salesperson,quantity,sum'
    - 'product,total_sales,sum'
    """
    try:
        df = get_dataframe()
        parts = [p.strip() for p in query.split(',')]
        parts = [p.strip().strip("'").strip('"') for p in query.split(',')]

        if len(parts) != 3:
            return "Input format: 'group_column,agg_column,function'"

        group_col, agg_col, func = parts

        if group_col not in df.columns:
            return f"Column '{group_col}' not found. Available: {list(df.columns)}"
        if agg_col not in df.columns:
            return f"Column '{agg_col}' not found. Available: {list(df.columns)}"

        agg_map = {
            'sum': 'sum', 'mean': 'mean', 'avg': 'mean',
            'count': 'count', 'max': 'max', 'min': 'min'
        }

        if func.lower() not in agg_map:
            return f"Function '{func}' not supported. Use: sum, mean, count, max, min"

        result = df.groupby(group_col)[agg_col].agg(agg_map[func.lower()]).round(2)
        result = result.sort_values(ascending=False)

        output = f"Group by '{group_col}', {func} of '{agg_col}':\n"
        for idx, val in result.items():
            output += f"  {idx}: {val}\n"

        return output

    except Exception as e:
        return f"Error in group aggregation: {str(e)}"


# ── Tool 5: Find Top/Bottom N ─────────────────────────────────
@tool
def find_top_n(query: str) -> str:
    """
    Finds top or bottom N rows based on a numeric column.
    Input format: 'n,column_name,top_or_bottom'
    Examples:
    - '5,total_sales,top'     → top 5 by total_sales
    - '3,quantity,bottom'     → bottom 3 by quantity
    - '10,unit_price,top'     → top 10 by unit_price
    """
    try:
        df = get_dataframe()
        parts = [p.strip() for p in query.split(',')]

        if len(parts) != 3:
            return "Input format: 'n,column_name,top_or_bottom'"

        n, column, direction = parts
        n = int(n)

        if column not in df.columns:
            return f"Column '{column}' not found. Available: {list(df.columns)}"

        if direction.lower() == 'top':
            result = df.nlargest(n, column)
        elif direction.lower() == 'bottom':
            result = df.nsmallest(n, column)
        else:
            return "Direction must be 'top' or 'bottom'"

        return f"{direction.capitalize()} {n} by '{column}':\n{result.to_string(index=False)}"

    except Exception as e:
        return f"Error finding top/bottom N: {str(e)}"


# ── Tool 6: Calculate Correlation ────────────────────────────
@tool
def calculate_correlation(query: str) -> str:
    """
    Calculates correlation between two numeric columns.
    Input format: 'column1,column2'
    Example: 'quantity,total_sales'
    Returns: correlation coefficient (-1 to 1)
    1 = perfect positive, -1 = perfect negative, 0 = no correlation
    """
    try:
        df = get_dataframe()
        parts = [p.strip() for p in query.split(',')]

        if len(parts) != 2:
            return "Input format: 'column1,column2'"

        col1, col2 = parts

        if col1 not in df.columns:
            return f"Column '{col1}' not found."
        if col2 not in df.columns:
            return f"Column '{col2}' not found."

        corr = round(df[col1].corr(df[col2]), 4)

        if abs(corr) > 0.8:
            strength = "Strong"
        elif abs(corr) > 0.5:
            strength = "Moderate"
        else:
            strength = "Weak"

        direction = "positive" if corr > 0 else "negative"

        return (
            f"Correlation between '{col1}' and '{col2}': {corr}\n"
            f"Interpretation: {strength} {direction} correlation"
        )

    except Exception as e:
        return f"Error calculating correlation: {str(e)}"


def get_all_tools() -> list:
    """Returns all custom tools for the agent."""
    tools = [
        get_dataset_info,
        calculate_statistics,
        filter_data,
        group_and_aggregate,
        find_top_n,
        calculate_correlation
    ]
    print(f"✅ Loaded {len(tools)} custom tools: {[t.name for t in tools]}")
    return tools