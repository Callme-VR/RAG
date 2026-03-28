import argparse
import sys
from src.search import SearchRag


def main():
    parser = argparse.ArgumentParser(description="RAG Search CLI")
    parser.add_argument(
        "query",
        nargs="?",
        help="Question to ask (if not provided, runs in interactive mode)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of relevant documents to retrieve (default: 3)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama-3.1-8b-instant",
        help="LLM model to use (default: llama-3.1-8b-instant)"
    )

    args = parser.parse_args()

    print("=" * 50)
    print("RAG Search CLI")
    print("=" * 50)

    # Initialize RAG
    print("\nInitializing RAG system...")
    rag = SearchRag(llm_model=args.model)

    if args.query:
        # Single query mode
        print(f"\nQuery: {args.query}")
        print("-" * 50)
        result = rag.search_summarize(args.query, top_k=args.top_k)
        print(result)
    else:
        # Interactive mode
        print("\nInteractive mode. Type 'quit' to exit.")
        while True:
            print("\n" + "-" * 50)
            query = input("Question: ").strip()

            if query.lower() in ('quit', 'exit', 'q'):
                print("Goodbye!")
                break

            if not query:
                continue

            result = rag.search_summarize(query, top_k=args.top_k)
            print("\nAnswer:")
            print(result)


if __name__ == "__main__":
    main()
