from pyngrok import ngrok 


def init_ngrok(port=5000):
    print("Opening ngrok tunnel...")
    ngrok.connect(port)
    tunnels = ngrok.get_tunnels()
    https_url = tunnels[1].public_url if tunnels[1].public_url.startswith("https") else tunnels[0].public_url
    print("Opened at", https_url)
    return https_url


if __name__ == "__main__":
    ngrok_url = init_ngrok()
