from nestor.dialogue.manager import DialogueManager

def main():
    dm = DialogueManager()
    print("Nestor CLI — type 'exit' to quit.")
    while True:
        u = input("You: ")
        if u.strip().lower() in {"exit","quit"}:
            break
        a = dm.respond(u)
        print("Nestor:", a)

if __name__ == "__main__":
    main()
