import requests

def main() -> None:
    response = requests.get("https://httpbin.org/get", timeout=5)
    print("Status:", response.status_code)
    print("Origin:", response.json()["origin"])

if __name__ == "__main__":
    main()