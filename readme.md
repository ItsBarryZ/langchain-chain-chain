# Teaching chatGPT to write langchain code, written with langchain


I was bothered when chatGPT couldn't even write langchain code.

So I fed a langchain one-pager into chatGPT, \
which generated the langchain code, \
which can be fed more langchain documentation, \
which can generate more langchain code. \
I did not write a single line of code. \
Life is beautiful again.

Written at 2AM, but serious takeaways:

1. With the best LLMs being mostly frozen, prompt is still the best way to alter model states. ChatGPT’s 1-shot learning ability is much more impressive than I thought.
2. Ideally, these information should be encoded through fine-tuning (like what CoPilot/CodeComplete probably did) or adapters (e.g. LoRA) on proprietary codebases, but for any new codebase, a “codebase card” is probably the fastest way to solve the cold start problem


## Example:

python main.py "https://python.langchain.com/en/latest/_sources/getting_started/getting_started.md" "write me a 21 question program using langchain"

it works, take my word for it
