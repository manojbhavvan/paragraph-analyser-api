# Paragraph Analyser API

## Introduction
This project is an API for analyzing paragraphs and indexing words in a PostgreSQL database. It includes endpoints for creating paragraphs and searching for specific words within those paragraphs.

## Installation
1. Clone the repository: `git clone https://github.com/your_username/paragraph-analyser-api.git`
2. Navigate to the project directory: `cd paragraph-analyser-api`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
### Creating Paragraphs
To create paragraphs, send a POST request to the endpoint `/api/paragraphs/` with the following JSON payload:
Endpoint: `/api/paragraphs/`
Method: POST
Payload:
```json
{
  "content": "Your paragraph content here"
}
```

Replace "Your paragraph content here" with the actual paragraph content.

The response to be received would be
```json
{
    "message": "Paragraph created successfully",
    "paragraph_id": "Paragraph id's"
}
```

### Search functionality
To search word in paragraphs, send a GET request to the endpoint `/api/search/`
Endpoint: `/api/search/`
Method: GET
Payload:
```json
{
    "word": "Your word to search"
}
```

Replace "Your word to search" with the actual word to search.

The response to be received would be
```json
{
    "word": "Your word",
    "output": "Paragraphs containing the word"
}
```

### User Registration
To register a new user, send a POST request to the endpoint `/api/register/` with the following JSON payload:
Endpoint: `/api/register/`
Method: POST
Payload:
```json
{
  "username": "Your username",
  "email": "Your email",
  "password": "Your password"
}
```
Replace "Your username", "Your email", and "Your password" with the user's details.

Upon successful registration, you will receive a confirmation message.

### User Authentication
User authentication is required to access certain functionalities. Use the following endpoint to authenticate users:

Endpoint: /api/login/
Method: POST
Payload:
```json
{
  "email": "Your email",
  "password": "Your password"
}
```

Replace "Your email" and "Your password" with the user's email and password.

Upon successful authentication, you will receive a JWT token in the response, which you can use as an access token for subsequent requests that require authentication, such as accessing the /api/paragraphs/ and /api/search/ endpoints.

## Contributing
1. Fork the repository.
2. Create a new branch: git checkout -b feature/your-feature
3. Make your changes and commit them following the commit message guidelines.
4. Push to the branch: git push origin feature/your-feature
5. Submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details
You can further customize and expand the README.md file based on your project's specific details and requirements.
