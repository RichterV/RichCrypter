# -*- coding: utf-8 -*-

import os,string,random,time
import tkinter as tk
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad,unpad
from Crypto.Protocol.KDF import PBKDF2
from tkinter import filedialog,Tk

os.system('cls' if os.name == 'nt' else 'clear')
if __name__ == "__main__":
    ###########FUNCTIONS###########
    def select_folder(msg=None):
        if msg:
            print(msg)
        selected_folder = filedialog.askdirectory(title=msg)
        return selected_folder
    def select_file(msg=None):
        if msg:
            print(msg)

        filetypes = [("BIN files", "*.bin")]
        selected_file = filedialog.askopenfilename(
            title=msg,
            filetypes=filetypes)

        return selected_file
    def rand_password(size):
        ch = string.ascii_letters + string.digits
        password = ''.join(random.choice(ch) for _ in range(size))
        return password
    def menu_decrypt():
        print("Do you want to save the decrypted files as txt?")
        print("1 - Save as txt")
        print("2 - Print on screen")
        print("0 - Return")

        choice = input("Choose the corresponding option: ")
        return choice
    def select_multiple_files(msg=None):
        if msg:
            print(msg)
        root = Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title=msg,
            filetypes=[("TXT files", "*.txt")]
        )

        root.destroy()
        return list(file_paths)
    def select_multiple_files_bin(msg=None):
        if msg:
            print(msg)
        root = Tk()
        root.withdraw()

        file_paths = filedialog.askopenfilenames(
            title=msg,
            filetypes=[("BIN files", "*.bin")]
        )

        root.destroy()
        return list(file_paths)
    def print_msg_box(msg, indent=1, width=None, title=None):
        """Print message-box with optional title."""
        lines = msg.split('\n')
        space = " " * indent
        if not width:
            if len(title)>max(map(len, lines)):
                width=len(title)
            else:
                width = max(map(len, lines))
        box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
        if title:
            box += f'║{space}{title:<{width}}{space}║\n'  # title
            box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
        box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
        box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
        print(box)

    def close_msg():
        print("The program will be closed...")
        time.sleep(15)

    ###########END FUNCTIONS###########
    print("Welcome to RichCrypter - Encryption Tool!")
    print("By: Vinicius Richter")
    print("-------------------------------------------")

    while True:
        print("\nPlease select an option:")
        print("1. Decrypt Files")
        print("2. Encrypt Files")
        print("3. Generate Encryption Key")
        print("0. Exit")
        choice = input("Enter the number corresponding to your choice: "+"\n")

        if choice == "1":
            print("Option 1: Decrypt Files")
            while True:
                user_choice = menu_decrypt()
                if user_choice == "1":
                    print("Option 1: Yes, save the decrypted files as txt")
                    key = select_file(
                        msg="Select your key (.bin) to encrypt! If you do not have any key, please close de program and generate one.")
                    with open(key, 'rb') as f:
                        key = f.read()
                    bin_files = select_multiple_files_bin(msg="Select files to decrypt")
                    save_folder = select_folder(msg="Select the folder to save the decrypted files!")
                    for bin_file in bin_files:
                        filename = os.path.basename(bin_file).replace(".bin", ".txt")

                        try:
                            with open(bin_file, 'rb') as bin_file:
                                iv_ = bin_file.read(16)
                                encrypted_data = bin_file.read()
                                cipher = AES.new(key, AES.MODE_CBC, iv=iv_)
                                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
                                decrypted_data_filtered = ''.join(' ' if not char.isprintable() else char for char in decrypted_data)
                                dir = os.path.join(save_folder,filename)
                                with open(dir, 'w', encoding='utf-8') as txt_file:
                                    txt_file.write(decrypted_data_filtered)
                                print("All decrypted files were saved successfully!")
                                close_msg()
                                exit()
                        except Exception as e:
                            print(f"Error reading file {bin_file}: {e}")
                    close_msg()
                    exit()

                elif user_choice == "2":
                    print("Option 2: No, only print on screen")
                    key = select_file(
                        msg="Select your key (.bin) to encrypt! If you do not have any key, please close de program and generate one.")
                    with open(key, 'rb') as f:
                        key = f.read()
                    bin_files = select_multiple_files_bin(msg="Select files to decrypt")
                    for bin_file in bin_files:
                        filename = os.path.basename(bin_file).replace(".bin", "")
                        print()
                        try:
                            with open(bin_file, 'rb') as bin_file:
                                iv_ = bin_file.read(16)
                                encrypted_data = bin_file.read()
                                cipher = AES.new(key, AES.MODE_CBC, iv=iv_)
                                decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size).decode('utf-8')
                                decrypted_data_filtered = ''.join(
                                    ' ' if not char.isprintable() else char for char in decrypted_data)
                                max_width = max(len(filename), len(decrypted_data_filtered)) + 20
                                title = f"Arquivo: {filename}.txt"
                                print_msg_box(decrypted_data_filtered,title=title)

                        except Exception as e:
                            print(f"Error reading file {bin_file}: {e}")
                            print(f"Make sure you are using the correct key for file decryption.")
                    close_msg()
                    exit()

                elif user_choice == "0":
                    break
                else:
                    print("Invalid option. Please choose a valid option.")


        elif choice == "2":
            print("Option 2: Encrypt Files")
            txt_files = select_multiple_files(msg="Select the txt files to encrypt")
            # Checking txt files folder
            txt_encrypted_files_save_dir = select_folder(msg="Select the folder to save your encrypted files")

            key = select_file(
                msg="Select your key (.bin) to encrypt")
            # read_key
            with open(key, 'rb') as f:
                key = f.read()
            c=0
            for txt_file in txt_files:
                filename = os.path.basename(txt_file).replace(".txt", ".bin")
                txt_contents = []
                with open(txt_file, 'r') as file:
                    lines = [line.strip() for line in file.readlines()]
                    txt_contents.append(lines)

                cipher = AES.new(key, AES.MODE_CBC)
                binary_file_name = os.path.join(txt_encrypted_files_save_dir, filename)

                with open(binary_file_name, 'wb') as binary_file:
                    # Write the IV to the start of the file
                    binary_file.write(cipher.iv)

                    for txt_content in txt_contents:
                        c+=1
                        items = []
                        for item in txt_content:
                            item_bytes = item.encode('utf-8')
                            ciphered_data = cipher.encrypt(pad(item_bytes, AES.block_size))
                            items.append(ciphered_data)

                        for item in items:
                            binary_file.write(item)
            print(f"{c} files have been successfully encrypted!")
            close_msg()
            exit()
        elif choice == "3":
            print("Option 3: Generate Encryption Key")
            salt = get_random_bytes(32)
            password = rand_password(15)
            save_directory = select_folder(msg="Select a folder to save your key!")
            key = PBKDF2(password, salt, dkLen=32)
            # Export Key
            with open(f'{save_directory}/key.bin', 'wb') as f:
                f.write(key)
            print("\n"+
                "Your key has been successfully saved in: " +"\n"
                f'"{save_directory}"'+"\n"
                "Remember to secure your key and not share it with strangers."+"\n"
                "It will be used to encrypt and decrypt your files."
                )
            close_msg()
            exit()
        elif choice == "0":
            print("Exiting RichCrypter. Thank you for using our encryption tool!")
            close_msg()
            exit()

        else:
            print("Invalid choice. Please enter a valid option.")









