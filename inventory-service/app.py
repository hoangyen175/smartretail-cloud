from flask import Flask, jsonify
import redis, json, os

app = Flask(__name__)

REDIS_URL = os.environ.get(
    'REDIS_URL',
    'redis://localhost:6379'
)

try:
    r = redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True
    )
    r.ping()
    print("[OK] Redis connected")
except Exception as e:
    r = None
    print("[WARN] Redis not connected")
    print(e)

PRODUCTS = [
    {"id": "P001", "name": "Ao thun", "price": 150000},
    {"id": "P002", "name": "Quan jean", "price": 350000}
]

@app.route('/products')
def get_products():

    if r:
        cached = r.get('products')

        if cached:
            print("[CACHE HIT]")
            return jsonify(json.loads(cached))

        r.setex(
            'products',
            60,
            json.dumps(PRODUCTS)
        )

        print("[CACHE MISS]")

    return jsonify(PRODUCTS)

@app.route('/health')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
