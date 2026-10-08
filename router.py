import json
import os

from providers.groq_provider import send_to_groq


CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "google": {
        "api_keys": []
    },
    "groq": {
        "api_keys": []
    }
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def manage_api_keys(config):
    providers = list(config.keys())

    while True:
        print("\nProviders:")

        for i, provider in enumerate(providers, 1):
            print(f"{i}. {provider.capitalize()}")

        print(f"{len(providers) + 1}. Back")

        choice = input("\nChoose provider: ")

        if not choice.isdigit():
            print("Invalid choice.")
            continue

        choice = int(choice)

        if choice == len(providers) + 1:
            return

        if choice < 1 or choice > len(providers):
            print("Invalid choice.")
            continue

        provider = providers[choice - 1]

        while True:
            print(f"\n{provider.capitalize()} API keys: {len(config[provider]['api_keys'])}")
            print("1. Add API key")
            print("2. Remove API key")
            print("3. Back")

            action = input("\nChoose: ")

            if action == "1":
                key = input("Enter API key: ").strip()

                if key:
                    config[provider]["api_keys"].append(key)
                    save_config(config)
                    print("API key added successfully.")
                else:
                    print("API key cannot be empty.")

            elif action == "2":
                keys = config[provider]["api_keys"]

                if not keys:
                    print("No API keys configured.")
                    continue

                print("\nConfigured keys:")

                for i in range(len(keys)):
                    print(f"{i + 1}. Key {i + 1}")

                key_choice = input("\nChoose key to remove: ")

                if key_choice.isdigit():
                    key_choice = int(key_choice)

                    if 1 <= key_choice <= len(keys):
                        keys.pop(key_choice - 1)
                        save_config(config)
                        print("API key removed.")
                    else:
                        print("Invalid key number.")
                else:
                    print("Invalid choice.")

            elif action == "3":
                break

            else:
                print("Invalid choice.")


def start_router(config):
    prompt = input("\nEnter your request: ")

    print("\nChoose a provider:")
    print("1. Groq")
    print("2. Google")
    print("3. Local Qwen")

    choice = input("\nEnter provider number: ")

    if choice == "1":
        keys = config["groq"]["api_keys"]

        if not keys:
            print("\nNo Groq API keys configured.")
            return

        try:
            response = send_to_groq(prompt, keys[0])
            print("\nGroq response:")
            print(response)

        except Exception as error:
            print("\nGroq request failed.")
            print(error)

    elif choice == "2":
        print("\nGoogle provider will be added next.")

    elif choice == "3":
        print("\nLocal Qwen will be added later.")

    else:
        print("\nInvalid provider selection.")


def main():
    config = load_config()

    while True:
        print("\nAI Router")
        print("1. Manage API keys")
        print("2. Start router")
        print("3. Exit")

        choice = input("\nChoose: ")

        if choice == "1":
            manage_api_keys(config)

        elif choice == "2":
            start_router(config)

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
