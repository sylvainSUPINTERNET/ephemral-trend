sizes = "34.5\n35\n36\n36.5\n37\n38\n38.5\n39\nÉpuisé\n40\n40.5\n41\n42\n42.5\n43\n44\nÉpuisé\n44.5\nÉpuisé\n45\nÉpuisé\n46\nÉpuisé\n47\nSeulement 1 article en stock"
size_arr = sizes.split("\n")

formatted = [];
for (i, val) in enumerate(size_arr):
	try:
		float(size_arr[i])
		formatted.append(val)
	except ValueError:
		formatted[len(formatted) - 1] = f"{formatted[len(formatted) - 1:][0] } {val}"

print(formatted)
# document.querySelectorAll("body > div:nth-child(20) > div > div.F8If-J.mZoZK2.KLaowZ.hj1pfK._8n7CyI.JCuRr_ > div > form > div")[0].innerText

