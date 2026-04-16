from src import SimpleFTS


fts = SimpleFTS()
to_index = [
    "最新のiPhoneで、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック",
    "最新のAndroidで、あそこの美しい風景を楽しく撮影しました。 #全文検索ロジック",
    "最新のGalaxy Note 7で、あそこの美しい風景を楽しく撮影しました。Galaxyはとても便利です。 #全文検索ロジック",
    "最新のGalaxy S26で、あそこの美しい風景を楽しく撮影しました。Galaxyはとても便利です。 #全文検索ロジック",
    "iPhoneの最新ロジック"
]

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