API Reference
-------------

1. Register User
    - URL: /api/register/
    - Method: POST
    - Description: Registers a new user.
    - Request Body:
        ```
        {
            "email": "mail@mail.com",
            "name": "Ritesh Mahale",
            "password": "pass"
        }
    - Response:
        - 201 Created: On successful registration.
        - 400 Bad Request: If there are validation errors in the request.

2. Verify OTP
    - URL: /api/verify/
    - Method: POST
    - Description: Verifies the OTP sent to the user's email during registration.
    - Request Body:
        ```
        {
            "email": "mail@mail.com",
            "otp": 1243
        }
    - Response:
        - 200 OK: If the OTP is valid.
        - 400 Bad Request: If the OTP is invalid or user not found.

3. Login
    - URL: /api/login/
    - Method: POST
    - Description: Authenticates a user and generates access tokens.
    - Request Body:
        ```
        {
            "email": "mail@mail.com",
            "password": "pass"
        }
    - Response:
        - 200 OK: With access and refresh tokens on successful authentication.
        - 401 Unauthorized: If the credentials are invalid.

4. Forgot Password
    - URL: /api/forgot-password/
    - Method: POST
    - Description: Sends a password reset link to the user's email.
    - Request Body:
        ```
        {
            "email": "mail@mail.com"
        }
    - Response:
        - 200 OK: If the password reset link is sent successfully.
        - 404 Not Found: If the user with the provided email is not found.

5. Reset Password
    - URL: /api/reset-password/<uidb64>/<token>/
    - Method: POST
    - Description: Resets the user's password using the provided reset link.
    - Request Body:
        ```
        {
            "new_password": "pasword"
        }
    - Response:
        - 200 OK: If the password is reset successfully.
        - 400 Bad Request: If the reset link is invalid.

6. Profile
    - URL: /api/profile/
    - Method: GET
    - Description: Retrieves the user's profile information.
    - Authorization: Bearer Token
    - Response:
        ```
        {
            "email": "user@mail.com",
            "name": "nsme"
        }
