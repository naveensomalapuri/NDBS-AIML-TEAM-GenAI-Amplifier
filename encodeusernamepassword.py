from urllib.parse import quote_plus

# Original username and password
username = "aimlteamndbs"
password = "aimlteamndbs@101"  # Contains special character @

# URL encode the username and password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# Print the encoded username and password
print(f"Encoded Username: {encoded_username}")
print(f"Encoded Password: {encoded_password}")

# Construct the MongoDB URI
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@genaiamplifier.1jwrr.mongodb.net/?retryWrites=true&w=majority&appName=GenAIAmplifier"
print(f"Encoded URI: {uri}")
