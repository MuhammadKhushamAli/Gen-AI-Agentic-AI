import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

text = "Hey My name is Muhammad Khusham Ali"

encoded_tokens = enc.encode(text=text)


print(encoded_tokens)

decoded_text = enc.decode(encoded_tokens)

print(decoded_text)