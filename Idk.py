import requests

def get_fun_fact():
    try:
        #  Facts API
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        data = response.json()

        # Extract the fact from the API response
        return data.get("text", "No fun fact found.")
    except requests.exceptions.RequestException as e:
        return f"opps try agyain: {e}"

if __name__ == "__main__":
    while True:
        print("Fetching a fun fact...")
        fun_fact = get_fun_fact()
        print(f"Fun Fact: {fun_fact}")

        # Ask if the fact was funny
        user_input = input("Was this interesting? (yes/no): ").strip().lower()

        if user_input == "yes":
            print("yippie")
            break
        elif user_input == "no":
            print("ok one more!")
        else:
            print("Please answer with 'yes' or 'no'.")
