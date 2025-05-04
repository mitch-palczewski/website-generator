import base64

email = ""
encoded_email = base64.b64encode(email.encode()).decode()

print("Encoded email:", encoded_email)