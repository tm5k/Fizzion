# v1.0.0
# Fizzion, open sourced cache modifier based on https://github.com/CroppingFlea479/Fizzion/ made by @cro.p, modified by @tm2k, intended for Phantom Forces. plz dont abuse D:
# discord.gg/v9gXTuCz8B

import os
import sys
import shutil
import time
import json
import webbrowser
import requests
from pathlib import Path

README_FILE = 'README.md'
FIZZION_FILE = 'fizzion.py'
ASSETS_FILE = 'assets.json'
RUN_FILE = 'run.bat'
GREEN, RED, BLUE, DEFAULT = '\033[32m', '\033[31m', '\033[34m', '\033[0m'


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
    

def dlist(area):
    current_level = data[area]
    path = [area]

    while isinstance(current_level, dict):
        match = {}
        print(f"\nAvailable keys in {GREEN}{' -> '.join(path)}{DEFAULT}:")
        for j, key in enumerate(current_level):
            match[str(j+1)] = key
            print(f"{j + 1}: {' ' if j < 9 else ''}{GREEN}{key}{DEFAULT}")

        user_input = input(
            f"Enter the key(name or number) you want to use in {GREEN}{' -> '.join(path)}{DEFAULT}\n(nest in keys with a period, type 'back' to go back, or 'skip' to skip)\n: ").strip().lower()

        if user_input == 'back':
            if len(path) > 1:
                path.pop()
                current_level = data[path[0]]
                for key in path[1:]:
                    current_level = current_level[key]
            else:
                print("You are already at the top level. Cannot go back.")
            continue

        if user_input == 'skip':
            print("Skipping category.")
            return

        if user_input in match.keys():
            selected_keys = [match[user_input]]
        else:
            selected_keys = user_input.split('.')
            selected_keys = [key.strip() for key in selected_keys]

        valid = True
        temp_level = current_level
        for key in selected_keys:
            if key in temp_level:
                temp_level = temp_level[key]
            else:
                print(f"{RED}Key '{key}' does not exist in '{' -> '.join(path)}'. Please try again.{DEFAULT}")
                valid = False
                break

        if valid:
            for key in selected_keys:
                path.append(key)
                current_level = current_level[key]

    return current_level


def bloxstrap():
    base_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Bloxstrap', 'Modifications')
    nested_folders = ["PlatformContent", "pc", "textures", "sky"]

    if not os.path.exists(base_path):
        print(f"{RED}bloxstrap not found{DEFAULT}")
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

        replace(data["skyboxes"], 'd625adff6a3d75081d11b3407b0b417c')


def delete_stuff(files_to_delete):
    for file_to_delete in files_to_delete:
        delete_file_path = os.path.join(folder_path, file_to_delete)
        if os.path.exists(delete_file_path):
            os.remove(delete_file_path)  #
            print(f'{file_to_delete} has been deleted.')
        else:
            print(f'{RED}{file_to_delete} not found.{DEFAULT}')


def preset_check():
    print("\nAvailable presets:")
    for idx, key in enumerate(presets.keys(), start=1):
        print(f"{idx}: {GREEN}{key}{DEFAULT}")

    choice = input(": ")

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(presets):
            return list(presets.keys())[choice - 1]
        else:
            print("Invalid number.")
            return None
    else:
        return choice
    

os.system('cls')

folder_path = os.path.join(os.getenv('TEMP'), 'roblox', 'http')

mod_cache = False
mod2_cache = False
pf_cache = False

mod_cache_check_path = os.path.join(folder_path, '016a313606e2f99a85bb1a91083206fc')
mod2_cache_check_path = os.path.join(folder_path, '3a24d59b1e8f104c593603d9a08f1849')
pf_cache_check_path = os.path.join(folder_path, '8a7090ac9b2e858f4aee9e19a0bfd562')

if os.path.exists(mod_cache_check_path): mod_cache = True
if os.path.exists(mod2_cache_check_path): mod2_cache = True
if os.path.exists(pf_cache_check_path): pf_cache = True

if mod_cache == False or mod2_cache == False or pf_cache == False: print(f"{RED}Missing cache, join prompted {'experiences' if not mod_cache or not mod2_cache or not pf_cache else 'experience'}.{DEFAULT}")
if mod_cache == False: webbrowser.open_new_tab("https://www.roblox.com/games/18504289170/texture-game")
if mod2_cache == False: webbrowser.open_new_tab("https://www.roblox.com/games/126211372078202/Assets")
if pf_cache == False: webbrowser.open_new_tab("https://www.roblox.com/games/292439477/Phantom-Forces")

while mod_cache == False or mod2_cache == False or pf_cache == False:
    if os.path.exists(mod_cache_check_path) and mod_cache == False:
        print(f"{GREEN}Modding{DEFAULT} cache detected")
        mod_cache = True

    if os.path.exists(mod2_cache_check_path) and mod2_cache == False:
        print(f"{GREEN}Custom Modding{DEFAULT} cache detected")
        mod2_cache = True

    if os.path.exists(pf_cache_check_path) and pf_cache == False:
        print(f"{GREEN}PF{DEFAULT} cache detected")
        pf_cache = True

    if mod_cache == True and mod2_cache == True and pf_cache == True:
        time.sleep(1)
        os.system('cls')
    
with open('assets.json', 'r') as file:
    data = json.load(file)

with open('presets.json', 'r') as file:
    presets = json.load(file)

def replace(files_to_delete, file_to_replace):
    try:
        copy_file_path = os.path.join(folder_path, file_to_replace)
        if os.path.exists(copy_file_path):
            for file_to_delete in files_to_delete:
                delete_file_path = os.path.join(folder_path, file_to_delete)
                if os.path.exists(delete_file_path):
                    os.remove(delete_file_path)
                    # print(f'{file_to_delete} has been deleted.')
                else:
                    print(f'{RED}{file_to_delete} not found.{DEFAULT}')

                new_file_path = os.path.join(folder_path, file_to_delete)
                shutil.copy(copy_file_path, new_file_path)
                # print(f'{copy_file_path} has been copied to {new_file_path}.')
                print(f'{BLUE}{file_to_delete} has been replaced with {file_to_replace}.{DEFAULT}')
        else:
            print(f'{RED}{file_to_replace} not found.{DEFAULT}')

    except Exception as e:
        if hasattr(e, 'winerror') and e.winerror == 183:
            pass
        else:
            print(f'{RED}An error occurred: {e}{DEFAULT}\n')

print(f"Welcome to: {GREEN}Fizzion!{DEFAULT}\n")
start = True
while True:
    if not start: print(" ")
    start = False
    menu = input(
        f"Enter the number corresponding to what you'd like to do:\n1: {GREEN}Ingame asset replacements{DEFAULT}\n2: {GREEN}Block (experimental, dont use){DEFAULT}\n3: {GREEN}Clear Cache{DEFAULT}\n4: {GREEN}Presets{DEFAULT}\n5: {GREEN}Exit{DEFAULT}\n: ")
    if menu == '1':
        print(
            f"\nasset replacements:\n0:  {GREEN}Custom{DEFAULT}\n1:  {GREEN}Sights{DEFAULT}\n2:  {GREEN}Arm models{DEFAULT}\n3:  {GREEN}Sleeves{DEFAULT}\n4:  {GREEN}No textures{DEFAULT}\n5:  {GREEN}Skyboxes{DEFAULT}\n6:  {GREEN}Gun skins{DEFAULT}\n7:  {GREEN}Gun Sounds{DEFAULT}\n8:  {GREEN}Gun smoke{DEFAULT}\n9:  {GREEN}Hit sounds{DEFAULT}\n10: {GREEN}Grenade tweaks{DEFAULT}\n11: {GREEN}Weapon models{DEFAULT}")
        options = input(": ")
        try:
            match int(options):
                case 0:
                    replace([input("\nEnter asset to change: ")], input("Enter replacement: "))
                case 1:
                    sight_option = input(
                        f"\nEnter sight option:\n1: {GREEN}Reticle tweaks{DEFAULT}\n2: {GREEN}Sight model tweaks{DEFAULT}\n3: {GREEN}Ballistics tracker tweaks{DEFAULT}\n: ")
                    try:
                        match int(sight_option):
                            case 1:
                                reticle = dlist("reticles")
                                reticle_replacement = dlist("reticle replacement")
                                if reticle and reticle_replacement:
                                    replace([reticle], reticle_replacement)
                            case 2:
                                sightbackground = input(
                                    f"\nEnter background tweak:\n1: {GREEN}clear coyote blue background{DEFAULT}\n2: {GREEN}clear reflex blue background{DEFAULT}\n3: {GREEN}clear okp-7 blue background{DEFAULT}\n4: {GREEN}clear delta black ring{DEFAULT}\n5: {GREEN}remove sniper black circle{DEFAULT}\n6: {GREEN}remove glass hack border{DEFAULT}\n: ")
                                match int(sightbackground):
                                    case 1:
                                        replace(
                                            ['3fc9141fc7c1167c575b9361a98f04c0'],'5873cfba79134ecfec6658f559d8f320')  # clear coyote blue background
                                    case 2:
                                        replace(
                                            ['2eaae4fe3a9fce967af993d27ad68d52'], '5873cfba79134ecfec6658f559d8f320')  # clear reflex blue background
                                    case 3:
                                        replace(
                                            ['2eaae4fe3a9fce967af993d27ad68d52'], '5873cfba79134ecfec6658f559d8f320')  # clear okp-7  blue background                                        
                                    case 4:
                                        replace(
                                            ['30c4d2bb30b6b8c9ac7cfeec5db25a85', '7d5652167ec33ed349e569a55a398705'],
                                            'd625adff6a3d75081d11b3407b0b417c')  # delta black ring
                                    case 5:
                                        replace(
                                            ['a883a2373ad6931556dce946c50c3690 ', '5a2a41b0da7ec98bf25780bb3f5d071f '],
                                            'd625adff6a3d75081d11b3407b0b417c')  # remove sniper junk       
                                    case 6:
                                        replace(
                                            ['1764672fe43c9f1d129b3d51dc3c40ee'],
                                            'd625adff6a3d75081d11b3407b0b417c')  # remove sniper junk                                                                              
                                    case _:
                                        print("Invalid option")
                            case 3:
                                replace([data["ballistics tracker"]["default"]], dlist("ballistics tracker"))
                            case _:
                                print("Invalid option")
                    except Exception as e:
                        print(f"{RED}Error: {e}{DEFAULT}")
                case 2:
                    arm_option = input(f"\nEnter arm option:\n1: {GREEN}Remove options{DEFAULT}\n2: {GREEN}Bone arms{DEFAULT}\n3: {GREEN}Default arms{DEFAULT}\n: ")
                    match int(arm_option):
                        case 1:
                            replace(dlist('arm models'), '5873cfba79134ecfec6658f559d8f320')
                        case 2:
                            replace(data["arm models"]["bare arms"], "5873cfba79134ecfec6658f559d8f320")
                            replace(['f5b0bcba5570d196909a78c7a697467c', '7f828aee555e5e1161d4b39faddda970'],
                                    'c9672591983da8fffedb9cec7df1e521')
                        case 3:
                            delete_stuff(data["arm models"]["everything"])
                        case _:
                            print("Enter a Valid Option!")
                case 3:
                    replace(['aa33dd87fc9db92e891361e069da1849'], dlist("skins"))
                case 4:
                    replace(data["textures"], 'd625adff6a3d75081d11b3407b0b417c')  # no textures without downside
                case 5:
                    sky_option = input(f"\nIs Bloxstrap sky folder setup?\n1: {GREEN}yes{DEFAULT}\n2: {GREEN}no{DEFAULT}\n: ")
                    match int(sky_option):
                        case 1:
                            replace(data["skyboxes"], 'd625adff6a3d75081d11b3407b0b417c')  # forced default skybox
                        case 2:
                            bloxstrap()
                        case _:
                            print("Enter a Valid Option!")
                case 6:
                    replace([dlist("gun skins")], dlist("skins"))
                case 7:
                    sound = dlist("gun sounds")
                    sound_replacement = dlist("replacement sounds")
                    if sound and sound_replacement:
                        replace([sound], sound_replacement)
                case 8:
                    replace(['8194373fb18740071f5e885bab349252'], dlist("gun smoke"))
                case 9:
                    hit_option = input(f"\nEnter hit option:\n1: {GREEN}Hitmarkers{DEFAULT}\n2: {GREEN}Hit sounds{DEFAULT}\n3: {GREEN}Kill sounds{DEFAULT}\n: ")
                    match int(hit_option):
                        case 1:
                            replace(['097165b476243d2095ef0a256320b06a'], dlist("hitmarker"))  # hitmarkers
                        case 2:
                            replace(['a177d2c00abd3e550b873d76c97ad960'], dlist("replacement sounds"))
                        case 3:
                            replace(data["replacement sounds"]["kill sounds"]["default"], dlist("replacement sounds"))
                        case _:
                            print("Enter a Valid Option!")
                case 10:
                    boom_option = input(f"\nEnter grenade option:\n1: {GREEN}Model tweaks{DEFAULT}\n2: {GREEN}Explosion sound{DEFAULT}\n3: {GREEN}Grenade sound{DEFAULT} \n: ")
                    match int(boom_option):
                        case 1:
                            model_option = input(f"\nEnter Model option:\n1: {GREEN}RGD{DEFAULT}\n2: {GREEN}Bundle{DEFAULT}\n: ")
                            match int(model_option):
                                case 1:
                                    replace(data["grenades"]["rgd"]["junk"], "5873cfba79134ecfec6658f559d8f320")
                                    replace([data["grenades"]["rgd"]["main"]], dlist("grenades"))
                                    replace([data["grenades"]["rgd"]["texture"]], dlist("grenades"))
                                case 2:
                                    replace(data["grenades"]["bundle"]["junk"], "5873cfba79134ecfec6658f559d8f320")
                                    replace(data["grenades"]["bundle"]["main"], dlist("grenades"))
                                    replace(data["grenades"]["bundle"]["texture"], dlist("grenades"))
                                case _:
                                    print("Enter a Valid Option!")
                        case 2:
                            replace(data["replacement sounds"]["explosions"]["default"], dlist("replacement sounds"))
                        case 3:
                            replace([dlist("grenade sounds")], dlist("replacement sounds"))
                        case _:
                            print("Enter a Valid Option!")
                case 11:
                    model_option = input(f"\nEnter model option:\n1: {GREEN}Guns{DEFAULT}\n2: {GREEN}Melees{DEFAULT}\n3: {GREEN}Attachments{DEFAULT}\n: ")
                    match int(model_option):
                        case 1:
                            gun_option = input(f"\nEnter weapon option:\n1: {GREEN}G50 > USP{DEFAULT}\n2: {GREEN}SCAR-L > AR2{DEFAULT}\n3: {GREEN}MODEL 870 > GRAVITY GUN{DEFAULT}\n4: {GREEN}NTW-20 > TAU CANNON{DEFAULT}\n5: {GREEN}ZIP 22 > SPRAY BOTTLE\n: ")
                            match int(gun_option):
                                case 1: #G50 > USP
                                    replace(["bddc9f845043a1557c1f60598b74dec9"], "3a24d59b1e8f104c593603d9a08f1849")
                                    replace(["581fb1e75493f5cd07c392c56cfb6913"], "01b511d3d6a49e919136a7620c1c2d75")
                                    replace(["b95f48b67fc264b3e0bed3ea67def86c"], "ce8f927a0723aecdf885ad8d2062d65f")

                                    replace(["bdd9569ccf5265e1bcba9cfdf31158b4"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["cdb896f02cec15070658302308e932a6"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["1e2e2de92f74d63670f37492036fb3c8"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["4d18ba857b6fb937b724ffe12d4c1334"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["5af556d14ce3becb61476b01831469ba"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["012aa01d8daeb6911ffa7894540aeda0"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["742acba73607468f2aabed2393a485a8"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["803dcfcc5d67796131c24808ecc81f5f"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["dd56a65175d19f74f80ef965b581f8fe"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["dd88384e2ab892de5289087d483f342f"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["f9cea0253df6177c8a4d9ade17aeb519"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["bd24d07dd480698db934a646b411c91f"], "058e54ef5ad3fb914c34a6f446a36702")

                                    replace(["29d21c6a319af85e851b10ee403beda6"], "cbf0cf37278b713d69a1224d87764b4e")
                                case 2: #SCAR-L > AR2
                                    replace(["d807565c66ffa1ef5c2bcb8df71c3316"], "d0ab035539878e8b7f8db4afbcf35c68")
                                    replace(["1bd29c76c25b635d72913cf651070211"], "9c824a1771dadc30fc47357781827d0b")

                                    replace(["0bc8f39140a0ed5dcc3a184749497983"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["4a140edf7ee3f64b158f111bfbd23154"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["4e9ec9484f5eb5f3ce1097a95cc19bb5"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["618dd900de44d24b976c71539e7fcbf8"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["7489cccbe6ce147ccbcc4416ff169633"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["105267e688312ddfe3c6d9f4bda1fdd0"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["534417e331b5ace39ce942d9985d0a08"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["665251ee6dc57621dba36792fb9b633c"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["aa0ee79510e22fbd065137957572e64d"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["b1d53f0b6ce3d9efde41f85b5e9c3be3"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["d4f1c0fcbb0b10d7657864f5561a537e"], "058e54ef5ad3fb914c34a6f446a36702")

                                    replace(["36944683beb83ae89a2f643c2fc89c0a"], "37190ca5952db9fe7c0eae8d2c719423")
                                case 3: #MODEL 870 > GRAVITY GUN
                                    replace(["d60b4c8da51f667748666d3b654447ef"], "11f5cb8d23e68bb0b46249a2324ef2e3")
                                    replace(["f2fff6168a25903e756ce8b46fd5f222"], "7a8cdc037786af2ae38bc857a6f689bc")
                                    replace(["a6f57f8e44e3e36ff63507b3201a2369"], "691ab049bccc077f4b555732c8bc95cd")

                                    replace(["4a6f27c3d1c02fec75a680fa4e38cbc4"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["64f69091b866e02a95cd63c19c6e702f"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["481db139e933fe0326cd430c7440ff7f"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["638bb4c3c30dee35672f2868367ee986"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["77930c7e6a5743577138c2cbee275207"], "058e54ef5ad3fb914c34a6f446a36702")

                                    replace(["840a637bcf78d82ea1817980c7b4e034"], "3c91d1da83166b85175b843f70abfabd")
                                case 4: #NTW-20 > TAU CANNON
                                    replace(["1dfc54edfbac54afef3149068cb5bd03"], "855b6209128f87538780d72daf80d8f1")
                                    replace(["ce02760297d953caa05ffdb7dbde7da7"], "631400c77a40f183add73cb09ac57634")
                                    replace(["153f63fb7e56c72c1ff4d99f73820019"], "70e7686f15cc964445dd26a003da5f76")
                                    replace(["61fd2d1c541098583c023d41ca3d1e2e"], "c88ed6c1af512dc5ceba8930909bb11b")

                                    replace(["3cf53b6dc15596a5dbf8b3e412180d7a"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["7ead80946bc6e1319cb3345e60f5380f"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["51ac841d64d72a6fd7ca820f5400612c"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["52a63ced811527c03386c04366d8c5c1"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["076ee7fe43824b3d094c82d7f2d31dfa"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["445cadb9fe251623c21dc0228c564558"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["529149dabb358f45dc37f65fbe69fe05"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["0555544b3a949bdfd6d678fe1ee1db11"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["a0f18c32520357cc642f7370bffdbd9a"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["a775b83d510837e6504d7702b9173745"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["b879ca0a2be08a97e1025f424414b720"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["bfce01d85c5b112edf874697e8361d33"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["c65d35d2a5b08f0de1cd5719b2a832d4"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["d04a47352d271f4af0f7f18dc1271ec3"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["eac5a3cb5fb92e128152d356e8ac69c1"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["f7b22c7fb3c2819422c9cd9f476703e5"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["f617b5d8f7d6a6ccbf6810b3a74e2c5d"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["fd1e15a13f6223d92333a0e3890d0e1d"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["64b85c4c6cbb582731cddfa47837fca4"], "058e54ef5ad3fb914c34a6f446a36702")

                                    replace(["cd5656b20061988925ce2e5faf274150"], "a488627070a3f389c4a6dddb85ef7430")
                                case 5: #ZIP 22 > SPRAY BOTTLE
                                    replace(["272147901810ade7bb3de69b6de16a41"], "4a125b503471ff8e3a1a67762c0f2271")
                                    replace(["368c5e823b66669d3fa3702d5bb83405"], "2d422447505c871a2370c8f9d86abfcf")

                                    replace(["6f18fab6028f963fe3b6a63ffd56db9f"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["25b1de3e08c6909b19323d1ec31fff77"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["223f269a9fdee763c0b125c20cdc7919"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["885cad81b3f28d0333067fa763783cfc"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["d5f2bfadc1608830ea5f618440261bb5"], "058e54ef5ad3fb914c34a6f446a36702")
                        case 2:
                            melee_option = input(f"\nEnter weapon option:\n1: {GREEN}ASP > STUN STICK{DEFAULT}\n: ")
                            match int(melee_option):
                                case 1: #ASP > STUN STICK
                                    replace(["e0c825a5deb0871b8e12376dd4fa40ba"], "f6a75145709a83372de39deacfe9ce27")
                                    replace(["02d75c76b65f1f837b2f8b1684c7b9c4"], "49c011ad1cc299fc8ba83f1356a61858")
                        case 3:
                            attachment_option = input(f"\nEnter attachment option:\n1: {GREEN}T-BRAKE > NOTHING{DEFAULT}\n2: {GREEN}POTATO GRIP > GRENADE LAUNCHER{DEFAULT}\n: ")
                            match int(attachment_option):
                                case 1: #T-BRAKE > NOTHING
                                    replace(["475298215d55f0c091fb69a043b40787"], "058e54ef5ad3fb914c34a6f446a36702")
                                case 2: #POTATO GRIP > GRENADE LAUNCHER
                                    replace(["cd2870bb0ec785064a86d3ce2f2ec2cc"], "ca7d634e856f90edf499da0c26133900")

                                    replace(["771a8d71308bcfb93af7a248e08a27ad"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["db4a504a99eab17744a3ae7a018302c8"], "058e54ef5ad3fb914c34a6f446a36702")
                                    replace(["dd9165376b8856778ab93d26ed52790e"], "058e54ef5ad3fb914c34a6f446a36702")
                        case _:
                            print("Enter a Valid Option!")
                case _:
                    print("Invalid number.")
        except Exception as e:
            print(f"{RED}Error: {e}{DEFAULT}")

    elif menu == '2':
        blockwarn = input(
            f"\n{RED}Warning: This is highly experimental and volatile to causing errors, requiring run.bat to be ran as admin to use. Only continue if you are aware of what youre doing.\nType 'done' to proceed, anything else will cancel.\n{DEFAULT}")
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

            print("\nCurrently blocked:", " ".join(blockedlist))
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
                        modified_content = modified_content.replace(f"#127.0.0.1 {string_thing}.rbxcdn.com",
                                                                    f"127.0.0.1 {string_thing}.rbxcdn.com")
                        print("Blocked!")
                    elif f"127.0.0.1 {string_thing}.rbxcdn.com" in content:
                        modified_content = modified_content.replace(f"127.0.0.1 {string_thing}.rbxcdn.com",
                                                                    f"#127.0.0.1 {string_thing}.rbxcdn.com")
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
                print(f"{RED}An error occurred: {e}{DEFAULT}")
        else:
            pass

    elif menu == '3':
        resetkwarn = input(
            f"\n{RED}Warning: This will fully reset all tweaks and anything loaded from any game.\nType 'done' to proceed, anything else will cancel.\n{DEFAULT}")
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
                        print(f'{RED}The directory {directory} does not exist.{DEFAULT}')
                except Exception as e:
                    print(f'{RED}Error: {e}{DEFAULT}')


            delete_all_in_directory(folder_path)
            print("Cleared cache, rejoin relevant experiences")

    elif menu == '4':
        preset_option = input(f"\nPresets:\n1: {GREEN}Load preset{DEFAULT}\n2: {GREEN}Add preset{DEFAULT}\n3: {GREEN}Delete preset{DEFAULT}\n: ")

        if preset_option == '1':
            if presets:
                name = preset_check()

                n_asset = 0; r_asset = 1; loops = 1
                if name:
                    values = int((len(presets[name])/2)+1)
                if name in presets:
                    while loops != values:
                        replace([presets[name][n_asset]], presets[name][r_asset])
                        n_asset += 2; r_asset += 2; loops += 1
                else:
                    print(f"{RED}{name}{DEFAULT} does not exist.")
            else:
                print("No presets available")
        elif preset_option == '2':
            new_preset = input("\nEnter preset name\n: ")
            switch = False; done = False
            while done == False:
                prompt = "\nEnter asset replacement\n: " if switch else f"\nEnter asset to change {GREEN}Type 'done' to finish{DEFAULT}\n: "
                switch = not switch
                new_value = input(prompt)
                if new_value == "done":
                    done = True
                else:
                    if new_preset not in presets:
                        presets[new_preset] = []
                    presets[new_preset].append(new_value)

                    with open('presets.json', 'w') as f:
                        json.dump(presets, f, indent=4)

        elif preset_option == '3':
            if presets:
                name = preset_check()

                if name in presets:
                    del presets[name]
                    with open(presets_file, 'w') as file:
                        json.dump(presets, file, indent=4)
                    print(f"{GREEN}{name}{DEFAULT} deleted successfully.")
                else:
                    print(f"{RED}{name}{DEFAULT} does not exist.")
            else:
                print("No presets available to delete.")
        else:
            print("Invalid option")

    elif menu == '5':
        print("\nExiting the program.")
        break

    else:
        print("Invalid, type a corresponding number!")