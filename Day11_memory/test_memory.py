from memory import (
    create_database,
    save_memory,
    search_semantic_memories
)
 
def test_memory():
    create_database()

    save_memory(
        "My name is Sushma.",
        "Nice to meet you, Sushma."
    )

    save_memory(
        "I am learning Python.",
        "Python is useful for AI development."
    )

    save_memory(
        "I am learning about MCP.",
        "MCP allows AI applications to use tools."
    )


    results = search_semantic_memories(
        "What is my name"
    )

    print("\nRelevant Memories")
    print("-----------------")

    for result in results:
        print("\nScore:", result["score"])
        print("User:", result["user_message"])
        print("Assistant:", result["assistant_message"])


test_memory()