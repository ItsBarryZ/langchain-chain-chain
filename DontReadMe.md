Teaching chatGPT to write langchain code, written with langchain
I think in the future all code should be somewhat automated, so it bothered me when chatGPT couldn't write langchain code.

So I fed a langchain one-pager into chatGPT,
which generated the langchain code,
which can be fed more langchain documentation,
which can generate more langchain code.
Life is beautiful again

Written at 2AM with passion and love, but serious takeaways:

With the best LLMs being mostly frozen, prompt is still the best way to alter model states. ChatGPT’s 1-shot learning ability is much more impressive than I thought.
Ideally, these information should be encoded through fine-tuning (e.g. copilot) or adapters (e.g. LORA) on proprietary codebases, but for any new codebase, a “codebase card” is probably the fastest way to solve the cold start problem
I am deliberately creating things that don't scale to demonstrate ideas. If I want to scale, I need to make friends with really good data/infra engineers because that’s the part I cannot do (@Daniel said he is too busy for my bs)
Harrison chase, thank you for building langchain! Would you consider adding this module that can generate langchain code using langchain?
