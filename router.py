providers = {
    "1": "Google",
    "2": "Groq",
    "3": "Local Qwen"
}

print("AI Router")

prompt = input("\nEnter your request: ")

print("\nChoose a provider:")

for number, provider in providers.items():
    print(f"{number}. {provider}")

choice = input("\nEnter provider number: ")

if choice in providers:
    provider = providers[choice]

    print(f"\nSending request to {provider}...")
    print(f"\n[{provider}] Received your request:")
    print(prompt)

else:
    print("\nInvalid provider selection.")
