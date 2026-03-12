from langchain.tools import tool, ToolRuntime

@tool(
    name_or_callable="sql_query",
    description="Generated SQL Query",
    parse_docstring=True,
)
def sql_query(query: str, runtime: ToolRuntime) -> str:
    """ONLY the raw SQL query. Do not wrap the query in markdown formatting like ```sql ... ```. Just return the raw query string perfectly formatted.

    Args:
        query (str): exact SQL query to be executed on BigQuery.

    Returns:
        str: The raw SQL query.
    """
    return query