import asyncio
import langwatch
from typing import Any, Dict, List
from tqdm.asyncio import tqdm_asyncio

async def abatch_with_tqdm(graph, inputs: List[Dict[str, Any]], config: Dict[str, Any] = None) -> List[Any]:
    """
    Runs a LangGraph concurrently over a list of inputs with a tqdm async progress bar.
    This bypasses graph.abatch to natively support progress tracking using tqdm_asyncio.gather.
    """
    max_concurrency = config.get("max_concurrency", 4) if config else 4
    sem = asyncio.Semaphore(max_concurrency)

    @langwatch.trace()
    async def _run_one(inp):
        async with sem:
            return await graph.ainvoke(inp, config=config)

    tasks = [_run_one(inp) for inp in inputs]
    return await tqdm_asyncio.gather(*tasks, desc="Processing batch")

