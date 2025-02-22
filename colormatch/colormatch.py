from PIL import Image

background = [
	"gainsboro", # Light Gray
    "bisque", # Light Orange
    "lightpink", # Light Pink
    "silver", # Silver
    "plum", # Light Purple
    "wheat", # Peach
    "lightgreen", # Light Green
    "paleturquoise", # Light Blue
    "lemonchiffon", # Lemon
    "violet", # Purple
    "royalblue", # Blue
    "salmon", # Light Red
    "ivory", # White
    "tan", # Tan
    "turquoise", # Turquoise
    "mediumspringgreen", # Spring
    "sandybrown", # Orange
]

color_dispatcher = {
	"gainsboro": "light_gray", # Light Gray
	"bisque": "light_orange", # Light Orange
	"lightpink": "light_pink", # Light Pink
	"silver": "silver", # Silver
	"plum": "light_purple", # Light Purple
	"wheat": "peach", # Peach
	"lightgreen": "light_green", # Light Green
	"paleturquoise": "light_blue", # Light Blue
	"lemonchiffon": "lemon", # Lemon
	"violet": "purple", # Purple
	"royalblue": "blue", # Blue
	"salmon": "light_red", # Light Red
	"ivory": "ivory", # White
	"tan": "tan", # Tan
	"turquoise": "turquoise", # Turquoise
	"mediumspringgreen": "spring", # Spring
	"sandybrown": "orange", # Orange
}

for color in background:
	nft = Image.new("RGBA", size=(640, 640), color=color)
	nft.save(rf"C:/Windows (x86)/BrainJuice/colormatch/{color_dispatcher[color]}.png")