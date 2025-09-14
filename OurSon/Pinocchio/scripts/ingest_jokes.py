import argparse, json, pathlib
from nestor.storage.vector import VectorStore

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default="data/jokes", help="folder with .jsonl files")
    args = ap.parse_args()
    vec = VectorStore()
    items = []
    for p in pathlib.Path(args.path).rglob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            obj = json.loads(line)
            items.append({"id": obj.get("id") or str(len(items)), "text": obj["text"], "rating": obj.get("rating","G")})
    if items:
        vec.add(items, namespace="jokes")
        print(f"Ingested {len(items)} jokes.")
    else:
        print("No jokes found.")

if __name__ == "__main__":
    main()
