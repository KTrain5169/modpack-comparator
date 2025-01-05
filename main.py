import json
import os
import zipfile
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def read_json_from_mrpack(file_path):
	with zipfile.ZipFile(file_path, 'r') as zip_ref:
		with zip_ref.open('modrinth.index.json') as file:
			return json.load(file)

def count_mods(modpack_json):
	return len(modpack_json.get('files', []))

def get_mod_paths(modpack_json):
	return {mod['path'] for mod in modpack_json.get('files', [])}

def compare_modpacks(modpack1_path, modpack2_path):
	modpack1_json = read_json_from_mrpack(modpack1_path)
	modpack2_json = read_json_from_mrpack(modpack2_path)
	
	modpack1_mod_count = count_mods(modpack1_json)
	modpack2_mod_count = count_mods(modpack2_json)
	
	print(f"Modpack 1 has {modpack1_mod_count} mods.")
	print(f"Modpack 2 has {modpack2_mod_count} mods.")
	
	if modpack1_mod_count > modpack2_mod_count:
		print("Modpack 1 has more mods.")
	elif modpack1_mod_count < modpack2_mod_count:
		print("Modpack 2 has more mods.")
	else:
		print("Both modpacks have the same number of mods.")
	
	modpack1_mod_paths = get_mod_paths(modpack1_json)
	modpack2_mod_paths = get_mod_paths(modpack2_json)
	
	mods_only_in_modpack1 = modpack1_mod_paths - modpack2_mod_paths
	mods_only_in_modpack2 = modpack2_mod_paths - modpack1_mod_paths
	
	if mods_only_in_modpack1:
		print("Mods only in Modpack 1:")
		for mod_path in mods_only_in_modpack1:
			print(mod_path)
	else:
		print("No mods are unique to Modpack 1.")
	
	if mods_only_in_modpack2:
		print("Mods only in Modpack 2:")
		for mod_path in mods_only_in_modpack2:
			print(mod_path)
	else:
		print("No mods are unique to Modpack 2.")

def select_file():
	Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
	file_path = askopenfilename(filetypes=[("Modrinth Modpack files", "*.mrpack")])
	return file_path

# Example usage
print("Select the first modpack .mrpack file:")
modpack1_path = select_file()
print("Select the second modpack .mrpack file:")
modpack2_path = select_file()

compare_modpacks(modpack1_path, modpack2_path)
