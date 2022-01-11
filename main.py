import pandas as pd
import functions
import asyncio
import json, os

# prepare output folder and the urls
dest = "./output/"
functions.check_folder(dest)
output_path = os.path.join(dest,"contacts.csv")
urls = json.load(open("./data/many_urls.json"))

# scrape all (max. 80 urls at once)
contacts = asyncio.run(functions.render_all(urls))

# write the output
df = pd.DataFrame(contacts)
df.to_csv(output_path, index=False)