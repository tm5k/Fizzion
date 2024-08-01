# v1.4.1
# Fleasion, open sourced cache modifier made by @cro.p, intended for Phantom Forces. plz dont abuse D:
# discord.gg/v9gXTuCz8B

import os
import sys
import shutil
import time
import json
import webbrowser
import requests
from pathlib import Path

README_URL = 'https://raw.githubusercontent.com/CroppingFlea479/Fleasion/main/README.md'
FLEASION_URL = 'https://raw.githubusercontent.com/CroppingFlea479/Fleasion/main/fleasion.py'
ASSETS_URL = 'https://raw.githubusercontent.com/CroppingFlea479/Fleasion/main/assets.json'
RUN_URL = 'https://raw.githubusercontent.com/CroppingFlea479/Fleasion/main/run.bat'
README_FILE = 'README.md'
FLEASION_FILE = 'fleasion.py'
ASSETS_FILE = 'assets.json'
RUN_FILE = 'run.bat'

def fetch_lines(url, num_lines=1):
    response = requests.get(url)
    lines = response.text.splitlines()
    return lines[:num_lines], lines

def read_lines(file_name, num_lines=1):
    try:
        with open(file_name, 'r') as file:
            return [file.readline().strip() for _ in range(num_lines)]
    except FileNotFoundError:
        return [''] * num_lines

def update_file(file_name, lines):
    with open(file_name, 'w') as file:
        file.write('\n'.join(lines))

def get_version():
    readme_first_line, readme_lines = fetch_lines(README_URL)
    fleasion_first_line, fleasion_lines = fetch_lines(FLEASION_URL)
    run_lines, all_run_lines = fetch_lines(RUN_URL, 2)

    local_readme_first_line = read_lines(README_FILE)[0]
    if readme_first_line[0] == local_readme_first_line:
        print(f"ReadMe   v{readme_first_line[0]}")
    else:
        update_file(README_FILE, readme_lines)
        print(f"Updated README.md to v{readme_first_line[0]}")

    local_fleasion_first_line = read_lines(FLEASION_FILE)[0]
    fleasion_display = fleasion_first_line[0][2:]
    if fleasion_first_line[0] == local_fleasion_first_line:
        print(f"Fleasion {fleasion_display}")
    else:
        update_file(FLEASION_FILE, fleasion_lines)
        print(f"Updated fleasion.py to {fleasion_display}")
        os.execv(sys.executable, ['python'] + sys.argv)

    response_assets = requests.get(ASSETS_URL)
    response_json = response_assets.json()

    try:
        with open(ASSETS_FILE, 'r') as file:
            local_assets = json.load(file)
    except FileNotFoundError:
        local_assets = {}

    if response_json.get('version') == local_assets.get('version'):
        print(f"Assets   {response_json['version']}")
    else:
        with open(ASSETS_FILE, 'w') as file:
            json.dump(response_json, file, indent=4)
        print(f"Updated assets.json to {response_json['version']}")

    local_run_lines = read_lines(RUN_FILE, 2)
    run_version = run_lines[1][4:]
    if run_version == local_run_lines[1][4:]:
        print(f"Run.bat  {run_version}")
    else:
        update_file(RUN_FILE, all_run_lines)
        print(f"Updated run.bat to {run_version}")

    time.sleep(1)
    os.system('cls')

config_file = 'assets.json'

with open('assets.json', 'r') as file:
    data = json.load(file)

def save_data_to_file(data, filename='assets.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def dlist(area):
    current_level = data[area]
    path = [area]
    
    while isinstance(current_level, dict):
        print(f"Available keys in '{' -> '.join(path)}':")
        for key in current_level:
            print(f"{key}")

        user_input = input(f"Enter the key(s) you want to use in '{' -> '.join(path)}' (nest in keys with a period, type 'back' to go back, or 'skip' to skip): ").strip()
        
        if user_input.lower() == 'back':
            if len(path) > 1:
                path.pop()
                current_level = data[path[0]]
                for key in path[1:]:
                    current_level = current_level[key]
            else:
                print("You are already at the top level. Cannot go back.")
            continue

        if user_input.lower() == 'skip':
            print("Skipping category.")
            return
        
        selected_keys = user_input.split('.')
        selected_keys = [key.strip() for key in selected_keys]

        valid = True
        temp_level = current_level
        for key in selected_keys:
            if key in temp_level:
                temp_level = temp_level[key]
            else:
                print(f"Key '{key}' does not exist in '{' -> '.join(path)}'. Please try again.")
                valid = False
                break
        
        if valid:
            for key in selected_keys:
                path.append(key)
                current_level = current_level[key]

    return current_level
    
def add_new_area():
    new_area = input("Enter the new area name: ")
    new_key = input(f"Enter the key for '{new_area}': ")
    new_value = input(f"Enter the value for '{new_key}': ")

    if new_area not in data:
        data[new_area] = {}

    data[new_area][new_key] = new_value

    with open(config_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"New area '{new_area}' with key '{new_key}' and value '{new_value}' added to JSON file.")

def read_file_names(file_path):
            with open(file_path, 'r') as file:
                big_name_list = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            return big_name_list

def bloxstrap():
    base_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Modifications')
    nested_folders = ["PlatformContent", "pc", "textures", "sky"]
    
    if not os.path.exists(base_path):
        print("bloxstrap not found")
    else:
        path = base_path
        for folder in nested_folders:
            path = os.path.join(path, folder)
            if not os.path.exists(path):
                os.makedirs(path)
                print(f"Created folder: {path}")
            else:
                print(f"Folder already exists: {path}")

        print("All folders created successfully! Import your skyboxes into the opened folder.")
        os.startfile(path)

def delete_stuff(files_to_delete):
    for file_to_delete in files_to_delete:
        delete_file_path = os.path.join(folder_path, file_to_delete)
        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)
            print(f'{file_to_delete} has been deleted.')
        else:
            print(f'{file_to_delete} not found.')

get_version()

folder_path = os.path.join(os.getenv('TEMP'), 'roblox', 'http')

mod_cache = False
pf_cache = False

mod_cache_check_path = os.path.join(folder_path, '016a313606e2f99a85bb1a91083206fc')
pf_cache_check_path = os.path.join(folder_path, '8a7090ac9b2e858f4aee9e19a0bfd562')

if os.path.exists(mod_cache_check_path): mod_cache = True
if os.path.exists(pf_cache_check_path): pf_cache = True

if mod_cache == False or pf_cache == False: print("Missing cache, join prompted experience.")
if mod_cache == False: webbrowser.open_new_tab("https://www.roblox.com/games/18504289170/texture-game")
if pf_cache == False: webbrowser.open_new_tab("https://www.roblox.com/games/292439477/Phantom-Forces")

while mod_cache == False or pf_cache == False:
    if os.path.exists(mod_cache_check_path) and mod_cache == False:
        print("Modding cache detected")
        mod_cache = True

    if os.path.exists(pf_cache_check_path) and pf_cache == False:
        print("PF cache detected")
        pf_cache = True

with open('assets.json', 'r') as file:
    data = json.load(file)

def replace(files_to_delete, file_to_replace):
    try:
        copy_file_path = os.path.join(folder_path, file_to_replace)
        if os.path.exists(copy_file_path):
            for file_to_delete in files_to_delete:
                delete_file_path = os.path.join(folder_path, file_to_delete)
                if os.path.exists(delete_file_path):
                    os.remove(delete_file_path)
                    print(f'{file_to_delete} has been deleted.')
                else:
                    print(f'{file_to_delete} not found.')

                new_file_path = os.path.join(folder_path, file_to_delete)
                shutil.copy(copy_file_path, new_file_path)
                #print(f'{copy_file_path} has been copied to {new_file_path}.')
                print(f'{file_to_delete} has been replaced.')
        else:
            print(f'{file_to_replace} not found.')

    except Exception as e:
        if hasattr(e, 'winerror') and e.winerror == 183:
            pass
        else:
            print(f'An error occurred: {e}')

while True:
    menu = input("Enter the number corresponding to what you'd like to do:\n1: Ingame asset replacements\n2: Block (experimental, dont use)\n3: Clear Cache\n4: Change config\n5: Exit\n")
    if menu == '1':
        print("options:\n0:  Custom\n1:  Sights\n2:  Arm model tweaks\n3:  Sleeves\n4:  No textures\n5:  Default skyboxes\n6:  Gun skins\n7:  Gun Sounds\n8:  Gun smoke\n9:  Hitmarker\n10: Hitmarker sound\n11: Kill sounds")
        options = input("Enter option: ")
        try:
            match int(options):
                case 0: replace([input("Enter asset to change: ")], input("Enter replacement: "))
                case 1:
                    sight_option = input("Enter sight option:\n1: Reticle tweaks\n2: Sight model tweaks\n3: Ballistics tracker tweaks\n")
                    try:
                        match int(sight_option):
                            case 1:
                                reticle = dlist("reticles")
                                reticle_replacement = dlist("reticle replacement")
                                if reticle and reticle_replacement:
                                    replace([reticle], reticle_replacement)
                            case 2:
                                sightbackground = input(
                                    "Enter background tweak:\n1: clear coyote/reflex blue background\n2: clear delta black ring\n")
                                match int(sightbackground):
                                    case 1:
                                        replace(
                                            ['3fc9141fc7c1167c575b9361a98f04c0', '2eaae4fe3a9fce967af993d27ad68d52'],
                                            '5873cfba79134ecfec6658f559d8f320')  # clear coyote and reflex blue background
                                    case 2:
                                        replace(
                                            ['30c4d2bb30b6b8c9ac7cfeec5db25a85', '7d5652167ec33ed349e569a55a398705'],
                                            'd625adff6a3d75081d11b3407b0b417c')  # delta black ring
                            case 3:
                                replace(data["ballistics tracker"]["default"], dlist("ballistics tracker"))
                            case _:
                                print("Invalid option")
                    except Exception as e:
                        print(f"Error: {e}")
                case 2: 
                    arm_option = input("Enter arm option:\n1: No arms\n2: No sleeves\n3: Bone arms\n4: default arms\n")
                    match int(arm_option):
                        case 1: replace(data["arm models"], '5873cfba79134ecfec6658f559d8f320') # no arms
                        case 2: replace(['0417f106902be46503fc75266526817a', '18ff02c763205099ce8542cebc98ae71'], 'd625adff6a3d75081d11b3407b0b417c')
                        case 3: replace(['f5b0bcba5570d196909a78c7a697467c', '7f828aee555e5e1161d4b39faddda970'], 'c9672591983da8fffedb9cec7df1e521')
                        case 4: delete_stuff(data["arm models"])
                        case _: print("Enter a Valid Option!") 
                case 3: replace(['aa33dd87fc9db92e891361e069da1849'], dlist("skins"))
                case 4: replace(data["textures"], 'd625adff6a3d75081d11b3407b0b417c') # no textures without downside
                case 5: 
                    sky_option = input("Is Bloxstrap sky folder setup?\n1: yes\n2: no\n")
                    match int(sky_option):                    
                        case 1: replace(data["skyboxes"], 'd625adff6a3d75081d11b3407b0b417c') # forced default skybox
                        case 2: bloxstrap()
                        case _: print("Enter a Valid Option!")  
                case 6: replace([dlist("gun skins")], dlist("skins"))
                case 7: 
                    reticle = dlist("gun sounds")
                    reticle_replacement = dlist("replacement sounds")
                    if reticle and reticle_replacement:
                        replace([reticle], reticle_replacement)                     
                case 8: replace(['8194373fb18740071f5e885bab349252'], dlist("gun smoke"))
                case 9: replace(['097165b476243d2095ef0a256320b06a'], dlist("hitmarker")) # hitmarkers                                 
                case 10: replace(['a177d2c00abd3e550b873d76c97ad960'], dlist("hitsound"))
                case 11: replace(data["killsound"]["default"], dlist("killsound"))
                case _: print("Invalid number.")
        except Exception as e: print(f"Error: {e}")

    elif menu == '2':
        blockwarn = input("Warning: This is highly experimental and volatile to causing errors, only continue if you are aware of what youre doing.\nType 'done' to proceed, anything else will cancel.\n")
        if blockwarn == "done":
            file_path = r"C:\Windows\System32\drivers\etc\hosts"
            with open(file_path, "r") as file:
                content = file.read()
            
            blockedlist = []
            unblockedlist = []

            for i in range(8):
                if f"#127.0.0.1 c{i}.rbxcdn.com" in content:
                    unblockedlist.append(f"c{i}")
                elif f"127.0.0.1 c{i}.rbxcdn.com" in content:
                    blockedlist.append(f"c{i}")

                if f"#127.0.0.1 t{i}.rbxcdn.com" in content:
                    unblockedlist.append(f"t{i}")
                elif f"127.0.0.1 t{i}.rbxcdn.com" in content:
                    blockedlist.append(f"t{i}")

            print("Currently blocked:", " ".join(blockedlist))
            print("Currently unblocked:", " ".join(unblockedlist))
            
            def website_blocks():
                website_blocklist = []
                print("Enter c(num)/t(num) to block/unblock (type 'done' when finished)")
                while True:
                    website_name = input("Enter string: ")
                    if website_name.lower() == 'done':
                        break
                    website_blocklist.append(website_name)
                return website_blocklist

            website_block = website_blocks()

            try:
                modified_content = content
                for string_thing in website_block:
                    if f"#127.0.0.1 {string_thing}.rbxcdn.com" in content:
                        modified_content = modified_content.replace(f"#127.0.0.1 {string_thing}.rbxcdn.com", f"127.0.0.1 {string_thing}.rbxcdn.com")
                        print("Blocked!")
                    elif f"127.0.0.1 {string_thing}.rbxcdn.com" in content:
                        modified_content = modified_content.replace(f"127.0.0.1 {string_thing}.rbxcdn.com", f"#127.0.0.1 {string_thing}.rbxcdn.com")
                        print("Unblocked!")
                    else:
                        print("No text found, blocking it.")
                        modified_content += f"\n127.0.0.1 {string_thing}.rbxcdn.com"

            except Exception as e:
                print(f"An error occurred: {e}")

            try:
                with open(file_path, "w") as file:
                    file.write(modified_content)
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            pass

    elif menu == '3':
        resetkwarn = input("Warning: This will fully reset all tweaks and anything loaded from any game.\nType 'done' to proceed, anything else will cancel.\n")
        if resetkwarn == "done":
            def delete_all_in_directory(directory):
                try:
                    if os.path.exists(directory):
                        for filename in os.listdir(directory):
                            file_path = os.path.join(directory, filename)
                            try:
                                if os.path.isfile(file_path) or os.path.islink(file_path):
                                    os.unlink(file_path)
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path)
                            except Exception as e:
                                print(f'Failed to delete {file_path}. Reason: {e}')
                    else:
                        print(f'The directory {directory} does not exist.')
                except Exception as e:
                    print(f'Error: {e}')

            delete_all_in_directory(folder_path)
            print("Rejoin relevant experiences")

    elif menu == "4":
        add_new_area()

    elif menu == '5':
        print("Exiting the program.")
        break

    else:
        print("Invalid, type a corresponding number!")
