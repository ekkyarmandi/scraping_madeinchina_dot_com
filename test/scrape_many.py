import functions
import asyncio
import json

urls = json.load(open("./data/many_urls.json"))
contacts = asyncio.run(functions.render_all(urls))
print(contact)