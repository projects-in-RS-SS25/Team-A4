from pydantic import BaseModel
from backend.utils.generate import generate, RecommendationRequest
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)



@app.route('/recommend', methods=['POST'])
def recommend():
    '''
    data = request.get_json()
    req = RecommendationRequest(**data)
    return generate(req)
    '''
    return 'Hi'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)