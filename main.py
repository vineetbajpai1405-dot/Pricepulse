from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_amazon_price(item):
    try:
        url = f"https://www.amazon.in/s?k={item}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        
        price = soup.find("span", {"class": "a-price-whole"})
        if price:
            return f"₹{price.text}"
        return "Not Found"
    except:
        return "Error"

@app.get("/compare")
def compare(item: str):
    print(f"🔍 Searching real price for: {item}")
    
    
    amazon_p = get_amazon_price(item)
    
    
    results = [
        {"site": "Amazon", "price": amazon_p, "link": f"https://www.amazon.in/s?k={item}"},
        {"site": "Flipkart", "price": "₹69,999 (Check Site)", "link": f"https://www.flipkart.com/search?q={item}"}
    ]
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
