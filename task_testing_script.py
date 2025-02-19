import requests

# =============== DATAGEN =======================
# run this first just in case if data is not found for some tasks - this will regenerate the data
url = "http://localhost:8000/run?task= generate the data folder for the user with email daniel.putta@gramener.com"

# =============== TASKS RANDOM A and B =========================
# url = "http://localhost:8000/run?task=count sundays in data/dates.txt and put the value in data/dates-sundays.txt"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=extract email from data/email.txt and write the result to data/sender-email.txt"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=sort the people in data/contact.json and put it in data/contact-sorted.json"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=write the content from 3 most recent files in data/logs and write them to data/logs-recent.txt"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=extract the titles in from all files in data/docs and put it in data/docs/index.json"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=write my credit card number from data/credit_card.png to data/creadit-card.txt"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=find the two sentences that talks about similar things in data/comments.txt and write them t data/comments-similar.txt"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=In /data/ticket-sales.db has a tickets with columns type, units, and price. Each row is a customer bid for a concert ticket. What is the total sales of all the items in the “Gold” ticket type? Write the number in /data/ticket-sales-gold.txt"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=clone this repo https://github.com/danielrayappa2210/TDS-GA2.git to data/new_rpo"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=compress the credit_card.png in data folder and save it in compressed-credit-card.png"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task= convert the format.md file in data folder to a html file data/format.html"  # Example: httpbin.org echoes back the request
# url = "http://localhost:8000/run?task=format the format.md file in data folder using prettier"

# ============ ACCESS DENIED ====================
# url = "http://localhost:8000/run?task= get the card number from images_test_data/image1.jpg and write the number to data/credit-card.txt"  # Example: httpbin.org echoes back the request

# ============ DELETING FILES ===================
# url = "http://localhost:8000/run?task= delete the file data/comments.txt"

try:
    response = requests.post(url, verify=False)  # Use json=data for JSON payload
    # Or, for form data: response = requests.post(url, data=data)

    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

    print("Status Code:", response.status_code)
    print("Response Content:", response.json())  # If the response is JSON
    # Or print("Response Content:", response.text) for other content types

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")