import json

print("Replacing images key")

for i in range(2000):
    with open(f"C:\\Windows (x86)\\BrainJuice\\phase1\\product\\metadata\\{i+1}.json", "r+") as file:
        data = json.load(file)

        data["image"] = f"https://brainjuicenft.up.railway.app/api/image/{i+1}.png"

        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

print("Done")