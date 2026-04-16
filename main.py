from src import SimpleFTS


fts = SimpleFTS()
to_index = []

for text in to_index:
    fts.add_index(text)

try:
    while True:
        query = input("Enter Query: ")
        results = fts.search(query)
    
        for i in range(len(results)):
            print(f"Result ({i}): {results[i]}")
        print("------")
except KeyboardInterrupt:
    print("\n")