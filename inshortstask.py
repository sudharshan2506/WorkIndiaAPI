from flask import Flask, request, jsonify
from flask_cors import CORS
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app) 
posts = []
API_KEY = "WorkIndia"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shorts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
def authenticate_request(req):
    api_key = req.headers.get('X-API-KEY')
    return api_key == API_KEY

@app.route('/api/shorts/create', methods=['POST'])
def create_short():
    if not authenticate_request(request):
        return jsonify({
            "message": "Unauthorized access. Invalid API key.",
            "status_code": 403
        }), 403
    data = request.json
    
    # Validate required fields
    required_fields = ["category", "title", "author", "publish_date", "content"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "message": f"Missing required field: {field}",
                "status_code": 400
            }), 400

    # Generate a unique ID for the new post
    short_id = str(uuid4())

    # Create the new post
    new_post = {
        "short_id": short_id,
        "category": data.get("category"),
        "title": data.get("title"),
        "author": data.get("author"),
        "publish_date": data.get("publish_date"),
        "content": data.get("content"),
        "actual_content_link": data.get("actual_content_link", ""),
        "image": data.get("image", ""),
        "votes": data.get("votes", {"upvote": 0, "downvote": 0})
    }

    # Save the new post
    posts.append(new_post)

    return jsonify({
        "message": "Short added successfully",
        "short_id": short_id,
        "status_code": 200
    })

@app.route('/api/shorts/feed', methods=['GET'])
def get_shorts_feed():
    if not authenticate_request(request):
        return jsonify({
            "message": "Unauthorized access. Invalid API key.",
            "status_code": 403
        }), 403
    # Sort posts by publish_date in descending order
    sorted_posts = sorted(posts, key=lambda x: x['publish_date'], reverse=True)
    return jsonify(sorted_posts)
@app.route('/api/login', methods=['POST'])
def login():
    if not authenticate_request(request):
        return jsonify({
            "message": "Unauthorized access. Invalid API key.",
            "status_code": 403
        }), 403
    mock_user = {
        "username": "example_user",
        "password": "example_password"
    }
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Check if the credentials match the mock user data
    if username == mock_user['username'] and password == mock_user['password']:
        response = {
            "status": "Login successful",
            "status_code": 200,
            "user_id": "12345",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        }
    else:
        response = {
            "status": "Incorrect username/password provided. Please retry",
            "status_code": 401
        }    
    return jsonify(response)

@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        if not authenticate_request(request):
            return jsonify({
            "message": "Unauthorized access. Invalid API key.",
            "status_code": 403
            }), 403
        data = request.get_json()
        if not data:
            return jsonify({"status": "Invalid input", "status_code": 400}), 400
        # Extract fields from the request data
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        # Check if all required fields are present
        if not username or not password or not email:
            return jsonify({"status": "Missing fields", "status_code": 400}), 400
        response = {
            "status": "Account successfully created",
            "status_code": 200,
            "user_id": "123445"
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e), "status_code": 500}), 500
@app.route('/api/shorts/filter', methods=['GET'])
def filter_shorts():
    if not authenticate_request(request):
        return jsonify({
            "message": "Unauthorized access. Invalid token.",
            "status_code": 403
        }), 403

    filters = {
        "category": request.args.get('category'),
        "publish_date": request.args.get('publish_date'),
        "upvotes": request.args.get('upvotes')
    }
    search = {
        "title": request.args.get('title'),
        "keyword": request.args.get('keyword'),
        "author": request.args.get('author')
    }

    filtered_posts = posts

    # Apply filters
    if filters['category']:
        filtered_posts = [post for post in filtered_posts if post['category'] == filters['category']]
    if filters['publish_date']:
        try:
            filter_date = datetime.fromisoformat(filters['publish_date'].replace('Z', '+00:00'))
            filtered_posts = [post for post in filtered_posts if datetime.fromisoformat(post['publish_date'].replace('Z', '+00:00')) >= filter_date]
        except ValueError:
            pass  # Handle invalid date format
    if filters['upvotes']:
        try:
            min_upvotes = int(filters['upvotes'])
            filtered_posts = [post for post in filtered_posts if post['votes']['upvote'] > min_upvotes]
        except ValueError:
            pass  # Handle invalid upvotes format

    # Apply searches
    results = []
    for post in filtered_posts:
        contains_title = search['title'] and search['title'].lower() in post['title'].lower()
        contains_content = search['keyword'] and (search['keyword'].lower() in post['title'].lower() or search['keyword'].lower() in post['content'].lower())
        contains_author = search['author'] and search['author'].lower() in post['author'].lower()

        if contains_title or contains_content or contains_author:
            results.append({
                **post,
                "contains_title": contains_title,
                "contains_content": contains_content,
                "contains_author": contains_author
            })

    if results:
        return jsonify(results)
    else:
        return jsonify({
            "status": "No short matches your search criteria",
            "status_code": 400
        }), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8090, debug=True)
