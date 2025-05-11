import secrets

# Generate the key
secret_key = secrets.token_hex(32)

# Print the key
print("Generated Secret Key:")
print(secret_key)

# Keep the window open to see the output
input("Press Enter to close...")
