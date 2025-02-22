import requests

def ask_server():
    url = "http://127.0.0.1:5000/ask"
    
    while True:
        question = input("Enter your question (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            print("Exiting...")
            break
        
        data = {"question": question}
        try:
            response = requests.post(url, json=data)
            print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ask_server()
