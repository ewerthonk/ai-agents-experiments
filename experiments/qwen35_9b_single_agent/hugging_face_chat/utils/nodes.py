# Standard Imports
import sqlite3
import pandas as pd
from textwrap import dedent
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
import langwatch
from langchain_core.runnables import RunnableConfig


# Project Imports
from settings.settings import settings
from .state import State
from .prompts import query_generation_prompt
from .tools import sql_query


def context_node(state: State) -> dict:
    db_id = state.get("db_id")
    dataset = state.get("dataset", "spider_dev")
    
    if not db_id:
        return {"context": "Error: db_id not provided in state."}
        
    db_dir = getattr(settings, f"{dataset}_db_dir")
    db_path = db_dir.joinpath(db_id, f"{db_id}.sqlite")
    
    if not db_path.exists():
        return {"context": f"Error: Database {db_id} not found at {db_path}."}
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        context_parts = []
        for table_name, schema_sql in tables:
            table_info = [f"Schema:\n{schema_sql.strip()}"]
            
            try:
                sample_df = pd.read_sql_query(sql=f"SELECT * FROM `{table_name}` LIMIT 5", con=conn)
                if not sample_df.empty:
                    # Pre-process the dataframe for SQL safety
                    for col in sample_df.columns:
                        if sample_df[col].dtype == "object":
                            # Use double quotes for the Python f-string, but output single quotes for the SQL literal
                            sample_df[col] = sample_df[col].apply(
                                lambda x: f"'{str(x).replace(chr(39), chr(39)+chr(39))}'" if pd.notna(x) else "NULL"
                            )
                        else:
                            sample_df[col] = sample_df[col].fillna("NULL")
                    
                    table_info.append(f"Sample:\n{sample_df.to_markdown(index=False)}")
                else:
                    table_info.append("Sample:\n(Table is empty)")
            except Exception as e:
                table_info.append(f"Sample:\nCould not fetch sample data: {str(e)}")
                
            context_parts.append("\n\n".join(table_info))
            
        conn.close()
        
        full_context = "\n\n---\n\n".join(context_parts)
        return {"context": full_context}
        
    except Exception as e:
        return {"context": f"Error extracting schema for {db_id}: {str(e)}"}

@langwatch.span(name="query_node")
def query_node(state: State) -> dict:
    context = state.get("context")
    if context:
        context_block = dedent(
            f"""<context>
            Use the following database schema and table samples to generate the query.
            {context}
            </context>"""
        )
    else:
        context_block = ""
        
    formatted_prompt = query_generation_prompt.format(
        question=state.get("question"),
        context_block=context_block
    )
    
    model = ChatHuggingFace(
        llm=HuggingFaceEndpoint(
            repo_id="Qwen/Qwen3.5-9B",
            task="text-generation",
            provider="together",
            temperature=0.6,
            top_p=0.95,
            top_k=20,
            seed=42,
            huggingfacehub_api_token=settings.huggingfacehub_api_token,
        )
    ).bind_tools([sql_query], tool_choice="sql_query")
    
    response = model.invoke(formatted_prompt, config=RunnableConfig(callbacks=[langwatch.get_current_trace().get_langchain_callback()]))
    
    if response.tool_calls:
        query = response.tool_calls[0]["args"].get("query", "")
    else:
        query = response.content.strip()

    query_clean = query.replace('\n', ' ').replace('\r', '').strip()
    if not query_clean:
        query_clean = "SELECT 1" 
        
    return {"query": query_clean}