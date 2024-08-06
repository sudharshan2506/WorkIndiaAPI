Flask Shorts API
Overview:
This Flask application provides an API for managing and retrieving "shorts" (news articles, posts, etc.). It includes endpoints for creating, filtering, and searching shorts. The API is protected with an API key for administrative actions and requires authorization for access.

Configuration
Set the API Key
Replace the placeholder "api-key" in the code with a secure API key. You can use environment variables or configuration files to manage sensitive information.

Usage
1. Create Short
Endpoint: POST /api/shorts/create
Headers:
Content-Type: application/json
API-KEY: your-secret-api-key

2. Get Shorts Feed
Endpoint: GET /api/shorts/feed
Request Headers:
No special headers required.

3. Filter Shorts
Endpoint: GET /api/shorts/filter
Headers:
Authorization: Bearer your-secret-token

