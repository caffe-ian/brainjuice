import random
import os
from PIL import Image
import time
import json

# print("Generating in 3 seconds..")
# time.sleep(3)

L = 90
M = 44
R = 30
C = 16

La = 64
Ma = 16
Ra = 8
Ca = 4

name = "Brain Juice"
total_supply = 2000
average_count = 25

legendary_count = total_supply * 0.05 # 100
mythical_count = total_supply * 0.15 # 300
rare_count = total_supply * 0.3 # 600
common_count = total_supply * 0.5 # 1000

if any(str(count)[-2:] != ".0" for count in [legendary_count, mythical_count, rare_count, common_count]):
    exit("There are decimals in count")

# background 1:2:4:13/20 2000
# flesh 1:4:7:10/22 2000
# eye 0:1:3:4/8 2000
# accessories 2:5:10:13/30 2000

legendary = ["glow.png", "golden_wings.png", "brain_flower.png", "horizon.png"]
mythical = ["devil_wings.png", "angel_wings.png", "rainbow_puke.png", "city.png", "night_city.png", "laser.png", "non_la.png", "winter.png", "acidic.png", "fungal.png", "kraken.png", "neon.png"]
rare = ["infected.png", "glitch.png", "space.png", "steampunk.png", "terrarium.png", "sob.png", "furious.png", "angel_halo.png", "devil_horns.png", "monocle.png", "scarf.png", "fedora.png", "waterfall.png", "cloud.png", "cigarette.png", "rabbit_ears.png", "white_moustache.png", "cyborg.png", "googly.png", "closed.png", "light_red.png", "purple.png", "spring.png", "turquoise.png"]
common = ["algae.png", "bloody.png", "futuristic.png", "lava.png", "matrix.png", "melting.png", "normal.png", "pierced.png", "soda.png", "worms.png", "arrow.png", "bubblegum.png", "cap.png", "cowboy_hat.png", "face_mask.png", "goatee.png", "headband.png", "knife.png", "moustache.png", "popsicle.png", "shark_fin.png", "top_hat.png", "crown.png", "blue.png", "ivory.png", "lemon.png", "light_blue.png", "light_gray.png", "light_green.png", "light_orange.png", "light_pink.png", "orange.png", "peach.png", "silver.png", "tan.png", "light_purple.png", "mad.png", "open.png", "sad.png", "sleepy.png"]

# print(len(legendary), len(mythical), len(rare), len(common))

def background_path(image):
    return os.path.join(r"C:\Windows (x86)\BrainJuice\phase1\images\background\vector", image)
def flesh_path(image):
    return os.path.join(r"C:\Windows (x86)\BrainJuice\phase1\images\flesh\vector", image)
def eye_path(image):
    return os.path.join(r"C:\Windows (x86)\BrainJuice\phase1\images\eye\vector", image)
def accessories_path(image):
    return os.path.join(r"C:\Windows (x86)\BrainJuice\phase1\images\accessories\vector", image)

def create_metadata(uid, background, flesh, eye, accessory, rarity):

    background = background.split("\vector")[-1].split(".")[0].replace("_", " ").title()
    flesh = flesh.split("\vector")[-1].split(".")[0].replace("_", " ").title()
    eye = eye.split("\vector")[-1].split(".")[0].replace("_", " ").title()
    accessory = accessory.split("\vector")[-1].split(".")[0].replace("_", " ").title()

    data = {
        "name": f"{name} #{uid:04}",
        "description": "Brain Juice is a phase based NFT collection consist of marvelous brains.",
        "image": "_REPLACE",
        "attributes": [
            {
                "trait_type": "Background",
                "value": background
            },
            {
                "trait_type": "Flesh",
                "value": flesh
            },
            {
                "trait_type": "Eye",
                "value": eye
            },
            {
                "trait_type": "Accessory",
                "value": accessory
            },
            {
              "trait_type": "Rarity",
              "value": rarity
            },
            {
                "trait_type": "Phase",
                "value": "1"
            }
        ]
    }

    with open(r"C:\Windows (x86)\BrainJuice\phase1\product\metadata\{0}.json".format(uid+1), 'w') as file:
        json.dump(data, file, indent=4)

generated = []
rarities = {"L":0,"M":0,"R":0,"C":0}

def generate_combination():

    background = [img for img in os.listdir(r"C:\Windows (x86)\BrainJuice\phase1\images\background\vector")]*100
    flesh = [img for img in os.listdir(r"C:\Windows (x86)\BrainJuice\phase1\images\flesh\vector")]*91
    eye = [img for img in os.listdir(r"C:\Windows (x86)\BrainJuice\phase1\images\eye\vector")]*250
    accessories = [img for img in os.listdir(r"C:\Windows (x86)\BrainJuice\phase1\images\accessories\vector")]*67

    generated = []
    rarities = {"L":0,"M":0,"R":0,"C":0}

    print("Generating combinations")

    for i in range(2000):

        bg = random.randint(0, len(background)-1)
        fl = random.randint(0, len(flesh)-1)
        ey = random.randint(0, len(eye)-1)
        acc = random.randint(0, len(accessories)-1)
        rarity = 0
        rarity += sum(La if p in legendary else Ma if p in mythical else Ra if p in rare else Ca for p in [background[bg], flesh[fl], eye[ey], accessories[acc]])
        nft = [background[bg], flesh[fl], eye[ey], accessories[acc], rarity]
            

        while nft in generated:
            bg = random.randint(0, len(background)-1)
            fl = random.randint(0, len(flesh)-1)
            ey = random.randint(0, len(eye)-1)
            acc = random.randint(0, len(accessories)-1)
            rarity = 0
            rarity += sum(La if p in legendary else Ma if p in mythical else Ra if p in rare else Ca for p in [background[bg], flesh[fl], eye[ey], accessories[acc]])
            nft = [background[bg], flesh[fl], eye[ey], accessories[acc], rarity]

        background.pop(bg)
        flesh.pop(fl)
        eye.pop(ey)
        accessories.pop(acc)

        # print(f"Brain Juice #{i+1}: Combination generated")

        if nft[4] >= L:
            nft[4] = "Legendary"
            rarities["L"] += 1
        elif nft[4] >= M:
            nft[4] = "Mythical"
            rarities["M"] += 1
        elif nft[4] >= R:
            nft[4] = "Rare"
            rarities["R"] += 1
        else:
            nft[4] = "Common"
            rarities["C"] += 1

        generated.append(nft)

    print(rarities)
    print("Leftovers", background, flesh, eye, accessories)
    return False if any([rarities["L"] not in range(95, 100), rarities["M"] not in range(300, 310), rarities["R"] not in range(595, 610)]) else generated

while True:
    if generated:=generate_combination():
        break

input("Enter to continue")

random.shuffle(generated)

print("Generating images and metadata")

for i in range(2000):

    create_metadata(i, generated[i][0], generated[i][1], generated[i][2], generated[i][3], generated[i][4])

    # Background
    nft = Image.open(background_path(generated[i][0])).convert("RGBA")

    # Pasting the flesh
    flesh = Image.open(flesh_path(generated[i][1])).convert("RGBA")
    nft.paste(flesh, mask=flesh)

    # Pasting the eye
    eye = Image.open(eye_path(generated[i][2])).convert("RGBA")
    nft.paste(eye, mask=eye)

    # Pasting the accessories
    accessories = Image.open(accessories_path(generated[i][3])).convert("RGBA")
    nft.paste(accessories, mask=accessories)

    nft.save(f"C:/Windows (x86)/BrainJuice/phase1/product/image/{i+1}.png")

    print(f"Brain Juice #{i}: Image and metadata generated")
