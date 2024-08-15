import os as _os
import zipfile as _zipfile
import json as _json
import random as _random
import shutil as _shutil
import ctypes as _ctypes
import tkinter as _tk
from tkinter import filedialog as _filedialog, messagebox as _messagebox, scrolledtext as _scrolledtext, Menu as _Menu, ttk as _ttk, simpledialog as _simpledialog
import uuid as _uuid
import re as _re
import logging as _logging
import urllib.request as _request
import tempfile as _tempfile

class _T1:
    def __init__(self, _p1):
        self._p1 = _p1
        self._w1 = _tk.Toplevel(_p1)
        self._w1.title("Terms of Use and License - AutoBE - TBL")
        self._w1.geometry("800x600")
        self._w1.configure(bg='#0A0A0A')

        self._s1 = _tk.Scrollbar(self._w1)
        self._s1.pack(side=_tk.RIGHT, fill=_tk.Y)

        self._t1 = _tk.Text(self._w1, wrap=_tk.WORD, yscrollcommand=self._s1.set, bg='#0A0A0A', fg='#E1E1E1', font=("Helvetica", 12))
        self._t1.pack(padx=10, pady=10, fill=_tk.BOTH, expand=True)

        _terms_text = """
        Terms of Use and Terms of Service
        ---------------------------------

        1. This software is provided "as is", without warranty of any kind.
        2. You may use this software for personal and commercial purposes.
        3. Redistribution of this software is prohibited without prior consent.
        4. You are responsible for ensuring that you have
        the legal right to use and modify any add-ons you merge using this tool.
        5. The Bedrock Lab and its developers are not responsible
        for any misuse of this tool, including the violation of Mojang's terms or third-party rights.
        6. You agree not to use this tool to distribute any 
        merged add-ons that infringe on the intellectual property rights of others.
        7. You agree to comply with Mojang's guidelines and 
        policies regarding the use of Minecraft and its associated content.

        By using this software, you agree to these terms.

        License
        -------

        1. Definitions
        - "Software" refers to the AutoBE tool developed by The Bedrock Lab.
        - "User" refers to any individual or entity using the Software.

        2. Grant of License
        - The Bedrock Lab grants the User a non-exclusive, non-transferable license to use the Software.

        3. Restrictions
        - The User may not reverse engineer, decompile, or disassemble the Software.
        - The User may not distribute, sublicense, or lease the Software to any third party.

        4. Ownership
        - The Bedrock Lab retains all rights, title, and interest in and to the Software.

        5. Disclaimer of Warranty
        - The Software is provided "as is" without warranty of any kind, either express or implied.

        6. Limitation of Liability
        - In no event shall The Bedrock Lab be liable for any damages arising out of the use or inability to use the Software.

        7. Termination
        - This license is effective until terminated. The User may terminate it at any time by destroying all copies of the Software.
        - This license will terminate immediately without notice from The Bedrock Lab if the User fails to comply with any provision of this license.

        8. Governing Law
        - This license shall be governed by the laws of the jurisdiction in which The Bedrock Lab is located.

        9. Contact Information
        - For inquiries, please contact The Bedrock Lab at TheBedrockLab@gmail.com.
        """

        self._t1.insert(_tk.END, _terms_text)
        self._t1.config(state=_tk.DISABLED)
        self._s1.config(command=self._t1.yview)

        self._b1 = _tk.Button(self._w1, text="I Agree", command=self._accept, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12, "bold"))
        self._b1.pack(pady=10)

    def _accept(self):
        self._w1.destroy()
        self._p1.deiconify()

class MCPackerWindow(_tk.Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Minecraft File Processor")
        self.geometry("600x200")

        self.files_var = _tk.StringVar()
        self.output_dir_var = _tk.StringVar()

        _tk.Label(self, text="Selected Files:").grid(row=0, column=0, padx=10, pady=10)
        _tk.Entry(self, textvariable=self.files_var, width=50).grid(row=0, column=1, padx=10, pady=10)
        _tk.Button(self, text="Browse", command=self.select_files).grid(row=0, column=2, padx=10, pady=10)

        _tk.Label(self, text="Output Directory:").grid(row=1, column=0, padx=10, pady=10)
        _tk.Entry(self, textvariable=self.output_dir_var, width=50).grid(row=1, column=1, padx=10, pady=10)
        _tk.Button(self, text="Browse", command=self.select_output_directory).grid(row=1, column=2, padx=10, pady=10)

        _tk.Button(self, text="Start", command=self.start_process).grid(row=2, column=1, pady=20)

    def check_manifest(self, file_path):
        with _zipfile.ZipFile(file_path, 'r') as zip_ref:
            return 'manifest.json' in zip_ref.namelist()

    def sanitize_filename(self, filename):
        return _re.sub(r'[^\w\-_\. ]', '_', filename)

    def process_files(self, files, output_dir):
        for file in files:
            file_extension = _os.path.splitext(file)[1]
            if file_extension not in ['.mcpack', '.mcaddon']:
                continue
            
            normalized_output_dir = _os.path.normpath(output_dir)
            
            if self.check_manifest(file):
                new_file = _os.path.join(normalized_output_dir, _os.path.basename(file))
                new_file = _os.path.splitext(new_file)[0] + '.mcpack'
                new_file = _os.path.normpath(new_file)
                _shutil.copyfile(file, new_file)
            else:
                with _zipfile.ZipFile(file, 'r') as zip_ref:
                    top_level_dirs = {_name.split('/')[0] for _name in zip_ref.namelist() if '/' in _name and _name.split('/')[0]}
                    
                    for top_dir in top_level_dirs:
                        sanitized_dir = self.sanitize_filename(top_dir)
                        top_dir_path = _os.path.join(normalized_output_dir, sanitized_dir + '.zip')
                        top_dir_path = _os.path.normpath(top_dir_path)
                        with _zipfile.ZipFile(top_dir_path, 'w') as new_zip_ref:
                            for member in zip_ref.namelist():
                                if member.startswith(top_dir + '/'):
                                    member_name = member[len(top_dir) + 1:]
                                    if member_name:  # Ensure the member name is not empty
                                        data = zip_ref.read(member)
                                        new_zip_ref.writestr(member_name, data)
                        
                        new_mcpack_path = _os.path.splitext(top_dir_path)[0] + '.mcpack'
                        new_mcpack_path = _os.path.normpath(new_mcpack_path)
                        _shutil.move(top_dir_path, new_mcpack_path)

    def select_files(self):
        file_paths = _filedialog.askopenfilenames(
            title="Select .mcpack and .mcaddon Files",
            filetypes=[("Minecraft Files", "*.mcpack *.mcaddon")]
        )
        self.files_var.set(','.join(file_paths))

    def select_output_directory(self):
        directory = _filedialog.askdirectory(title="Select Output Directory")
        self.output_dir_var.set(directory)

    def start_process(self):
        files = self.files_var.get().split(',')
        output_dir = self.output_dir_var.get()
        
        if not files or not output_dir:
            _messagebox.showerror("Error", "Please select files and an output directory.")
            return
        
        self.process_files(files, output_dir)
        _messagebox.showinfo("Success", "Process completed successfully.")

class _App1:
    def __init__(self, _root):
        self._root = _root
        self._root.title("AutoBEv2- TBL")
        self._root.geometry("800x600")
        self._root.minsize(800, 600)
        self._root.configure(bg='#0A0A0A')

        self._files = []
        self._out_dir = ""

        self._menu_bar = _Menu(self._root, bg='#0A0A0A', fg='#FFFFFF')
        self._root.config(menu=self._menu_bar)
        self._help_menu = _Menu(self._menu_bar, tearoff=0, bg='#0A0A0A', fg='#FFFFFF')
        self._menu_bar.add_cascade(label="Help", menu=self._help_menu)
        self._help_menu.add_command(label="Help Contents", command=self._show_help)

        # Adding the Update Check Tab
        self._update_menu = _Menu(self._menu_bar, tearoff=0, bg='#0A0A0A', fg='#FFFFFF')
        self._menu_bar.add_cascade(label="Check for Updates", menu=self._update_menu)
        self._update_menu.add_command(label="Check Now", command=self._check_for_updates)
        
        # Adding the MCPACKER Tab
        self._mcpacker_menu = _Menu(self._menu_bar, tearoff=0, bg='#0A0A0A', fg='#FFFFFF')
        self._menu_bar.add_cascade(label="MCPACKER", menu=self._mcpacker_menu)
        self._mcpacker_menu.add_command(label="Open MCPACKER", command=self._mcpacker)

        self._show_terms()
        self._create_widgets()

    def _show_terms(self):
        self._root.withdraw()
        self._terms_window = _T1(self._root)
        self._root.wait_window(self._terms_window._w1)
        _logging.debug('Terms of Use window closed.')

    def _create_widgets(self):
        self._frame_files = _tk.LabelFrame(self._root, text="Select .mcpack Files", bg='#0A0A0A', fg='#FFFFFF', font=("Helvetica", 14))
        self._frame_files.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self._file_list = _tk.Listbox(self._frame_files, selectmode=_tk.MULTIPLE, width=84, bg='#1A1A1A', fg='#A50CAC', font=("Helvetica", 12))
        self._file_list.grid(row=0, column=0, padx=10, pady=10)

        self._btn_add = _tk.Button(self._frame_files, text="Add Files", command=self._add_files, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12))
        self._btn_add.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self._btn_remove = _tk.Button(self._frame_files, text="Remove Selected", command=self._remove_files, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12))
        self._btn_remove.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self._frame_output = _tk.LabelFrame(self._root, text="Select Output Directory", bg='#0A0A0A', fg='#FFFFFF', font=("Helvetica", 14))
        self._frame_output.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self._output_dir_var = _tk.StringVar()
        self._entry_output_dir = _tk.Entry(self._frame_output, textvariable=self._output_dir_var, width=50, bg='#1A1A1A', fg='#A50CAC', font=("Helvetica", 12))
        self._entry_output_dir.grid(row=0, column=0, padx=5, pady=5)

        self._btn_select_output = _tk.Button(self._frame_output, text="Browse", command=self._select_output_dir, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12))
        self._btn_select_output.grid(row=0, column=1, padx=5, pady=5)

        self._frame_buttons = _tk.Frame(self._root, bg='#0A0A0A')
        self._frame_buttons.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self._btn_start = _tk.Button(self._frame_buttons, text="Start Process", command=self._process_and_create_manifest, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12, "bold"))
        self._btn_start.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self._btn_check = _tk.Button(self._frame_buttons, text="Check Manifest", command=self._check_compatibility, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12))
        self._btn_check.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self._btn_preview = _tk.Button(self._frame_buttons, text="Preview Changes", command=self._preview_changes, bg='#A50CAC', fg='#FFFFFF', font=("Helvetica", 12))
        self._btn_preview.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self._frame_buttons.grid_columnconfigure(0, weight=1)
        self._frame_buttons.grid_columnconfigure(1, weight=1)
        self._frame_buttons.grid_columnconfigure(2, weight=1)

        self._progress = _ttk.Progressbar(self._root, orient='horizontal', length=400, mode='determinate')
        self._progress.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self._trademark_label = _tk.Label(self._root, text="TBL ©2024", bg='#0A0A0A', fg='#FFFFFF', font=("Helvetica", 14, "bold"))
        self._trademark_label.place(relx=0.5, rely=0.582, anchor=_tk.CENTER)
        self._trademark_label.lift()
        
    def _check_for_updates(self):
        try:
            _url = "https://raw.githubusercontent.com/your-username/your-repo/main/your_script.py"
            _temp_dir = _tempfile.mkdtemp()
            _temp_file = _os.path.join(_temp_dir, "latest_script.py")

            with _request.urlopen(_url) as response, open(_temp_file, 'wb') as out_file:
                _shutil.copyfileobj(response, out_file)

            # Here, you can compare the version if you have a versioning system
            _message = "An update was found. Do you want to update?"
            if _messagebox.askyesno("Update Available", _message):
                _current_file = __file__
                _shutil.copy2(_temp_file, _current_file)
                _messagebox.showinfo("Update Successful", "The script was updated successfully. Please restart the application.")
                self._root.quit()
        except Exception as e:
            _messagebox.showerror("Update Failed", f"Failed to check for updates: {str(e)}")
        finally:
            _shutil.rmtree(_temp_dir)

    def _mcpacker(self):
        # Open the MCPACKER window
        MCPackerWindow(self._root)

    def _add_files(self):
        _files = _filedialog.askopenfilenames(filetypes=[("McPack files", "*.mcpack")])
        for _file in _files:
            self._file_list.insert(_tk.END, _file)
        self._files = _files

    def _remove_files(self):
        _selected_indices = self._file_list.curselection()
        for _index in reversed(_selected_indices):
            self._file_list.delete(_index)
        self._files = [self._file_list.get(_i) for _i in range(self._file_list.size())]

    def _select_output_dir(self):
        _dir_name = _filedialog.askdirectory()
        if _dir_name:
            self._output_dir_var.set(_dir_name)
            self._out_dir = _dir_name

    def _preview_changes(self):
        _message = "Coming Soon..."
        _messagebox.showinfo("Tool Updates Preview", _message)

    def _process_and_create_manifest(self):
        if not self._files:
            _messagebox.showerror("Error", "Please select .mcpack files")
            _logging.error("No .mcpack files selected")
            return
        if not self._out_dir:
            _messagebox.showerror("Error", "Please select an output directory")
            _logging.error("No output directory selected")
            return

        if not self._validate_files():
            return

        try:
            self._start_process()
            
            # Reset memory and clear the list
            self._files = []
            self._file_list.delete(0, _tk.END)
            
        except Exception as _e:
            _logging.error("An error occurred during the process", exc_info=True)
            _messagebox.showerror("Error", f"An error occurred: {_e}")

    def _start_process(self):
        """
        Starts the processing of selected .mcpack files and saves the output to the specified directory.
        """
        _selected_files = self._file_list.get(0, _tk.END)
        _output_dir = self._output_dir_var.get()

        if not _selected_files:
            _messagebox.showerror("Error", "Please select at least one .mcpack file.")
            return
        if not _output_dir:
            _messagebox.showerror("Error", "Please select an output directory.")
            return

        new_selected_files = []
        new_mcpack_paths = []

        for file_path in _selected_files:
            try:
                with _zipfile.ZipFile(file_path, 'r') as zip_ref:
                    # Check if 'subpacks' folder exists
                    if 'subpacks/' in zip_ref.namelist():
                        subpack_folders = [name.split('/')[1] for name in zip_ref.namelist() if name.startswith('subpacks/') and name.count('/') == 2]

                        if not subpack_folders:
                            _messagebox.showerror("Error", f"No subfolders found in 'subpacks' for {file_path}.")
                            continue

                        # Prompt the user to select a subpack folder by numeric index
                        selected_subpack_index = _simpledialog.askinteger(
                            "Select Subpack Folder",
                            f"Select a subpack folder by its numeric index from {_os.path.basename(file_path)}:\n\nAvailable subpacks:\n" + "\n".join(f"{i+1}. {folder}" for i, folder in enumerate(subpack_folders)),
                            parent=_root,
                            minvalue=1,
                            maxvalue=len(subpack_folders)
                        )

                        if selected_subpack_index is None:
                            _messagebox.showwarning("Error", "No subpack folder selected.")
                            continue

                        selected_subpack_name = subpack_folders[selected_subpack_index - 1]

                        # Extract the selected subpack folder
                        temp_dir = _os.path.join(_os.getcwd(), 'temp_extract')
                        zip_ref.extractall(temp_dir)

                        subpack_path = _os.path.join(temp_dir, 'subpacks', selected_subpack_name)

                        # Move the contents of the selected folder outside the 'subpacks' folder
                        for item in _os.listdir(subpack_path):
                            s = _os.path.join(subpack_path, item)
                            d = _os.path.join(temp_dir, item)
                            if _os.path.exists(d):
                                if _os.path.isdir(d):
                                    _shutil.copytree(s, d, dirs_exist_ok=True)
                                else:
                                    _shutil.move(s, d)
                            else:
                                _shutil.move(s, d)

                        # Remove the now empty 'subpacks' folder
                        _shutil.rmtree(_os.path.join(temp_dir, 'subpacks'))

                        # Repack the .mcpack file
                        new_mcpack_path = file_path.replace('.mcpack', '_modified.mcpack')
                        with _zipfile.ZipFile(new_mcpack_path, 'w') as new_zip_ref:
                            for folder_name, subfolders, filenames in _os.walk(temp_dir):
                                for filename in filenames:
                                    file_path = _os.path.join(folder_name, filename)
                                    arcname = _os.path.relpath(file_path, temp_dir)
                                    new_zip_ref.write(file_path, arcname)

                        # Clean up the temporary directory
                        _shutil.rmtree(temp_dir)

                        # Add the new modified file to the list
                        new_selected_files.append(new_mcpack_path)
                        new_mcpack_paths.append(new_mcpack_path)
                    else:
                        # No 'subpacks' folder found, add the original file to the list
                        new_selected_files.append(file_path)
            except Exception as e:
                _messagebox.showerror("Error", f"An error occurred while processing {file_path}: {str(e)}")
                continue

        if not new_selected_files:
            _messagebox.showerror("Error", "No valid .mcpack files to process.")
            return

        try:
            # Process packs
            self._process_packs(new_selected_files, _output_dir)
        except Exception as e:
            pass

        try:
            # Delete manifest files
            self._delete_manifest_files()
        except Exception as e:
            pass

        try:
            # Create manifest
            self._create_manifest()
        except Exception as e:
            pass
            _messagebox.showinfo("Success", "Process 1/4 Completed Successfully!")

        try:
            # Move tick and delete functions
            self._move_tick_and_delete_functions()
        except Exception as e:
            pass

        try:
            # Process files
            self._process_files(new_selected_files)
        except Exception as e:
            pass
            _messagebox.showinfo("Success", "Process 2/4 Completed Successfully!")

        try:
            # Move and cleanup
            self._move_and_cleanup()
        except Exception as e:
            pass

        try:
            # Update behavior pack
            self._update_behavior_pack()
        except Exception as e:
            pass
            _messagebox.showinfo("Success", "Process 3/4 Completed Successfully!")

        try:
            # Merge flipbook textures
            self._merge_flipbook_textures(new_selected_files)
        except Exception as e:
            pass

        try:
            # Merge textures list
            self._merge_textures_list(new_selected_files)
        except Exception as e:
            pass

        try:
            # Extract and delete zip files
            self._extract_and_delete_zip_files()
        except Exception as e:
            pass

        try:
            # Move to resource pack
            self._move_to_resource_pack()
        except Exception as e:
            pass

        # Define paths for behavior and resource packs
        _bp_path = _os.path.join(self._out_dir, "behavior_pack.zip")
        _rp_path = _os.path.join(self._out_dir, "resource_pack.zip")
        
        _bp_new_path = _os.path.join(self._out_dir, "behavior_pack.mcpack")
        _rp_new_path = _os.path.join(self._out_dir, "resource_pack.mcpack")
        
        _scripts_path = _os.path.join(self._out_dir, "scripts")
        _temp_dir = _os.path.join(self._out_dir, "temp_unpack")
        _tempr_dir = _os.path.join(self._out_dir, "temp_unpack_resource_pack")
        _flipbook_textures_source = _os.path.join(self._out_dir, "flipbook_textures.json")
        _textures_list_source = _os.path.join(self._out_dir, "textures_list.json")
            

        try:
            # Move and rename the packs if they exist
            if _os.path.exists(_bp_path):
                _shutil.move(_bp_path, _bp_new_path)
        except Exception as e:
            _messagebox.showerror("Error", f"Error moving behavior_pack.zip: {str(e)}")

        try:
            if _os.path.exists(_rp_path):
                _shutil.move(_rp_path, _rp_new_path)
        except Exception as e:
            _messagebox.showerror("Error", f"Error moving resource_pack.zip: {str(e)}")

        try:
            if _os.path.exists(_scripts_path):
                _shutil.rmtree(_scripts_path)
        except Exception as e:
            pass

        try:
            if _os.path.exists(_temp_dir):
                _shutil.rmtree(_temp_dir)
        except Exception as e:
            pass

        try:
            if _os.path.exists(_tempr_dir):
                _shutil.rmtree(_tempr_dir)
        except Exception as e:
            pass

        try:
            if _os.path.exists(_flipbook_textures_source):
                _shutil.rmtree(_flipbook_textures_source)
        except Exception as e:
            pass
            

        try:
            if _os.path.exists(_textures_list_source):
                _shutil.rmtree(_textures_list_source)
        except Exception as e:
            pass
            
        # Cleanup: Delete the newly modified .mcpack files
        for new_file in new_mcpack_paths:
            try:
                if _os.path.exists(new_file):
                    _os.remove(new_file)
            except Exception as e:
                _messagebox.showerror("Error", f"Error deleting file {new_file}: {str(e)}")

        # Show success message
        _messagebox.showinfo("Success", "Operation Complete")

    def _check_compatibility(self):
        _incompatible_files = []
        _missing_manifest_files = []

        _selected_files = self._files

        for _file in _selected_files:
            with _zipfile.ZipFile(_file, 'r') as _pack_zip:
                _pack_namelist = _pack_zip.namelist()

                if 'manifest.json' not in _pack_namelist:
                    _missing_manifest_files.append(_file)

        if _incompatible_files or _missing_manifest_files:
            _message = "The Following Issues Were Found With Selected MCPacks:\n\n"

            if _missing_manifest_files:
                _message += "Missing manifest.json:\n"
                for _file in _missing_manifest_files:
                    _message += f"- {_os.path.basename(_file)}\n"
                _message += "\n"

            _messagebox.showwarning("Compatibility Check", _message)
        else:
            _messagebox.showinfo("Compatibility Check", "All Selected MCPacks Have Manifest.")

    def _validate_files(self):
        invalid_files = []

        for _file in self._files:
            try:
                with _zipfile.ZipFile(_file, 'r') as _pack_zip:
                    if 'manifest.json' not in _pack_zip.namelist():
                        invalid_files.append(_file)
            except _zipfile.BadZipFile:
                invalid_files.append(_file)

        if invalid_files:
            _message = "The following files are invalid or missing manifest.json:\n\n"
            for _file in invalid_files:
                _message += f"- {_os.path.basename(_file)}\n"
            _messagebox.showerror("Invalid Files", _message)
            _logging.error(f"Invalid files detected: {invalid_files}")
            return False
        
        return True

    def _process_packs(self, _files, _output_dir):
        _output_zip_path_resource = _os.path.join(_output_dir, "resource_pack.zip")
        _output_zip_path_behavior = _os.path.join(_output_dir, "behavior_pack.zip")

        _json_contents_resource = {}
        _json_contents_behavior = {}
        _lang_contents_resource = {}
        _lang_contents_behavior = {}
        _material_contents = {}
        _mcfunction_contents = {}

        _mergeable_files = {
            "item_texture.json", "terrain_texture.json", "tick.json", "sounds.json", "blocks.json",
            "biomes_client.json", "sound_definitions.json", "music_definitions.json", "flipbook_textures.json",
            "textures_list.json", "_ui_defs.json", "hud_screen.json", "npc_interact_screen.json", 
            "_global_variables.json", "ui_common.json", "splashes.json", "player.json",
            "player.animation_controllers.json", "player.animation.json", "player.render_controllers.json"
        }

        self._progress['value'] = 0
        self._progress['maximum'] = len(_files)

        for _i, _file in enumerate(_files):
            _manifest_data = self._get_manifest_data(_file)
            if not _manifest_data:
                _logging.warning(f"Skipping {_file} - manifest.json not found or invalid.")
                continue

            _module_type = _manifest_data.get("modules", [{}])[0].get("type", "")
            if _module_type == "resources":
                _output_zip_path = _output_zip_path_resource
            elif _module_type in {"data", "script"}:
                _output_zip_path = _output_zip_path_behavior
            else:
                _logging.warning(f"Skipping {_file} - Unsupported module type '{_module_type}' in manifest.json.")
                continue

            with _zipfile.ZipFile(_file, 'r') as _pack_zip:
                with _zipfile.ZipFile(_output_zip_path, 'a') as _output_zip:
                    for _item in _pack_zip.infolist():
                        _item_name = _item.filename

                        if _item_name.startswith("feature_rules"):
                            _feature_rules_folder_name = f"feature_rules/{_os.path.basename(_file).replace('.mcpack', '')}"
                            self._extract_feature_rules(_pack_zip, _item, _feature_rules_folder_name, _output_zip)
                            continue

                        if _item_name.endswith(".json"):
                            if _os.path.dirname(_item_name) in {"entities", "entity"} and _os.path.basename(_item_name) == "player.json":
                                self._handle_json_item(_pack_zip, _item, 
                                    _json_contents_resource if _module_type == "resources" else _json_contents_behavior, _output_zip)
                            elif _os.path.basename(_item_name) not in _mergeable_files:
                                self._copy_to_zip(_pack_zip, _item, _output_zip)
                            else:
                                self._handle_json_item(_pack_zip, _item, 
                                    _json_contents_resource if _module_type == "resources" else _json_contents_behavior, _output_zip)
                        elif _item_name.endswith(".lang"):
                            if _module_type == "resources":
                                with _pack_zip.open(_item) as _lang_file:
                                    _lang_data = _lang_file.read().decode('latin-1')
                                    _lang_contents_resource.setdefault(_item_name, []).append(_lang_data)
                            elif _module_type in {"data", "script"}:
                                with _pack_zip.open(_item) as _lang_file:
                                    _lang_data = _lang_file.read().decode('latin-1')
                                    _lang_contents_behavior.setdefault(_item_name, []).append(_lang_data)
                        elif _item_name.endswith(".material"):
                            self._handle_json_item(_pack_zip, _item, _material_contents, _output_zip)
                        elif _item_name.endswith(".mcfunction"):
                            with _pack_zip.open(_item) as _mcfunction_file:
                                _mcfunction_data = _mcfunction_file.read().decode('latin-1')
                                _mcfunction_contents.setdefault(_item_name, []).append(_mcfunction_data)
                        else:
                            self._copy_to_zip(_pack_zip, _item, _output_zip)

            self._progress['value'] = _i + 1

        self._merge_and_write_files(_json_contents_resource, _output_zip_path_resource)
        self._merge_and_write_files(_json_contents_behavior, _output_zip_path_behavior)
        self._merge_and_write_lang_files(_lang_contents_resource, _output_zip_path_resource)
        self._merge_and_write_lang_files(_lang_contents_behavior, _output_zip_path_behavior)
        self._merge_and_write_material_files(_material_contents, _output_zip_path_resource)
        self._merge_and_write_mcfunction_files(_mcfunction_contents, _output_zip_path_behavior)

        self._progress['value'] = len(_files)

        self._remove_empty_files(_output_zip_path_resource)
        self._remove_empty_files(_output_zip_path_behavior)

    def _copy_to_zip(self, _pack_zip, _item, _output_zip, _json_data=None):
        with _pack_zip.open(_item) as _file_data:
            if _json_data is not None:
                _output_zip.writestr(_item.filename, _json.dumps(_json_data, indent=2))
            else:
                _output_zip.writestr(_item.filename, _file_data.read())

    def _handle_json_item(self, _pack_zip, _item, _json_contents, _output_zip, _module_type=None):
        with _pack_zip.open(_item) as _json_file:
            try:
                _json_data = self._load_json_with_comments(_json_file)
                if isinstance(_json_data, dict):
                    _json_contents.setdefault(_item.filename, []).append(_json_data)
            except _json.JSONDecodeError:
                self._copy_to_zip(_pack_zip, _item, _output_zip)

    def _merge_and_write_files(self, _json_contents, _output_zip_path):
        for _json_file, _json_list in _json_contents.items():
            _merged_content = self._merge_json(_json_list, _os.path.basename(_json_file))
            with _zipfile.ZipFile(_output_zip_path, 'a') as _output_zip:
                _output_zip.writestr(_json_file, _json.dumps(_merged_content, indent=2))

    def _merge_and_write_lang_files(self, _lang_contents, _output_zip_path):
        for _lang_file, _lang_list in _lang_contents.items():
            _merged_lang_content = self._merge_lang_files(_lang_list)
            with _zipfile.ZipFile(_output_zip_path, 'a') as _output_zip:
                _output_zip.writestr(_lang_file, _merged_lang_content)

    def _merge_and_write_material_files(self, _material_contents, _output_zip_path):
        for _material_file, _material_list in _material_contents.items():
            _merged_material_content = self._merge_json(_material_list, _os.path.basename(_material_file))
            with _zipfile.ZipFile(_output_zip_path, 'a') as _output_zip:
                _output_zip.writestr(_material_file, _json.dumps(_merged_material_content, indent=2))

    def _merge_and_write_mcfunction_files(self, _mcfunction_contents, _output_zip_path):
        for _mcfunction_file, _mcfunction_list in _mcfunction_contents.items():
            _merged_mcfunction_content = "\n".join(_mcfunction_list)
            with _zipfile.ZipFile(_output_zip_path, 'a') as _output_zip:
                _output_zip.writestr(_mcfunction_file, _merged_mcfunction_content)

    def _remove_empty_files(self, _zip_path):
        with _zipfile.ZipFile(_zip_path, 'r') as _zip:
            file_list = _zip.infolist()
            temp_file_path = _zip_path + ".temp"
            with _zipfile.ZipFile(temp_file_path, 'w') as temp_zip:
                for file in file_list:
                    if file.file_size > 0:
                        temp_zip.writestr(file, _zip.read(file.filename))

        _os.remove(_zip_path)
        _os.rename(temp_file_path, _zip_path)
    
    def _process_files(self, _selected_files):
        _renamed_files = {}
        _imported_files = []

        _bp_path = _os.path.join(self._out_dir, "Behavior_packs")
        _scripts_path = _os.path.join(_bp_path, "scripts")

        # Ensure the scripts directory is empty or create it if it doesn't exist
        if _os.path.exists(_scripts_path):
            _shutil.rmtree(_scripts_path)  # Remove the existing directory and its contents

        _main_js_path = _os.path.join(_scripts_path, "TBL.js")

        # Track renamed JS files for each pack
        _pack_renamed_files = {}

        for _mcpack_file in _selected_files:
            _pack_renamed_files[_mcpack_file] = {}
            try:
                with _zipfile.ZipFile(_mcpack_file, 'r') as _zip_ref:
                    for _item in _zip_ref.namelist():
                        if _item.startswith('scripts/'):
                            _zip_ref.extract(_item, _scripts_path)
                    try:
                        # Read the manifest file content using latin-1
                        _manifest_data = _zip_ref.read('manifest.json').decode('latin-1')
                        # Remove block and line comments
                        _manifest_data_clean = _re.sub(r'/\*[\s\S]*?\*/|([^\\:]|^)//.*$', '', _manifest_data)
                        # Remove the "version" field
                        # This regex assumes that "version" is a JSON array of numbers and will match
                        # the key and its value (array). It works for the structure "version": [major, minor, patch]
                        _manifest_data_clean = _re.sub(r'"version"\s*:\s*\[[^]]*\]\s*,?', '', _manifest_data_clean)
                        # Optional: remove trailing commas before closing braces/brackets
                        _manifest_data_clean = _re.sub(r',\s*([}\]])', r'\1', _manifest_data_clean)
                        # Use a library that supports comments in JSON
                        # Extract content between first '{' and last '}'
                        start_index = _manifest_data_clean.find('{')
                        end_index = _manifest_data_clean.rfind('}')
                        _manifest_data_trimmed = _manifest_data_clean[start_index:end_index+1]

                        # Parse JSON using json5 library
                        import json5 as _json
                        _manifest_json = _json.loads(_manifest_data_trimmed)
                    except KeyError:
                        _messagebox.showerror("Error", f"manifest.json not found in {_os.path.basename(_mcpack_file)}")
                        continue
                    except Exception as _e:
                        _messagebox.showerror("Error", f"Error reading manifest.json in {_os.path.basename(_mcpack_file)}: {str(_e)}")
                        continue

                    _entries = [_module.get("entry") for _module in _manifest_json.get("modules", []) if "entry" in _module]

                    for _entry in _entries:
                        if _entry:
                            try:
                                _script_folder = _os.path.dirname(_entry)
                                for _item in _zip_ref.namelist():
                                    if _item.startswith(_script_folder):
                                        _zip_ref.extract(_item, _scripts_path)

                                _old_script_path = _os.path.join(_scripts_path, _entry)
                                if _os.path.exists(_old_script_path):
                                    _random_number = _random.randint(1000, 9999)
                                    _new_script_name = f"{_random_number}_{_os.path.basename(_entry)}"
                                    _new_script_path = _os.path.join(_scripts_path, _script_folder, _new_script_name)
                                    _os.rename(_old_script_path, _new_script_path)
                                    _renamed_files[_os.path.basename(_entry)] = _new_script_name
                                    _pack_renamed_files[_mcpack_file][_os.path.basename(_entry)] = _new_script_name
                                    _imported_files.append(_new_script_path)
                                else:
                                    _imported_files.append(_os.path.join(_scripts_path, _entry))

                            except Exception as _e:
                                _messagebox.showerror("Error", f"Error processing entry {_entry} in {_os.path.basename(_mcpack_file)}: {str(_e)}")
                                continue
            except Exception as _e:
                _messagebox.showerror("Error", f"Failed to process {_os.path.basename(_mcpack_file)}: {str(_e)}")

        # Update references between renamed files for each pack
        for _mcpack_file, _renamed_files_in_pack in _pack_renamed_files.items():
            for _root, _, _files in _os.walk(_scripts_path):
                for _file in _files:
                    if _file.endswith('.js'):
                        try:
                            _file_path = _os.path.join(_root, _file)
                            with open(_file_path, 'r', encoding='latin-1') as _js_file:
                                _content = _js_file.read()

                            for _old_name, _new_name in _renamed_files_in_pack.items():
                                _old_name_with_ext = f'./{_old_name}'
                                _old_name_without_ext = f'./{_old_name.rsplit(".", 1)[0]}'

                                # Update content for old names with or without the .js extension
                                _content = _re.sub(rf"'{_old_name_with_ext}'", f"'{_new_name}'", _content)
                                _content = _re.sub(rf"'{_old_name_without_ext}'", f"'{_new_name}'", _content)

                            with open(_file_path, 'w', encoding='latin-1') as _js_file:
                                _js_file.write(_content)
                        except Exception as _e:
                            _messagebox.showerror("Error", f"Error updating import statements in {_file}: {str(_e)}")
                            continue

        # Write imports to TBL.js only if the files exist
        with open(_main_js_path, 'w') as _main_js_file:
            for _imported_file in _imported_files:
                if _os.path.exists(_imported_file):
                    try:
                        _file_name = _os.path.relpath(_imported_file, _scripts_path).replace("\\", "/")
                        _main_js_file.write(f'import "./{_file_name}";\n')
                    except Exception as _e:
                        _messagebox.showerror("Error", f"Error writing to TBL.js for {_imported_file}: {str(_e)}")
                        continue

        try:
            with open(_main_js_path, 'r') as _main_js_file:
                _main_js_content = _main_js_file.read()

            _main_js_content = _main_js_content.replace('./scripts', '.')
            _main_js_content = _main_js_content.replace('import "./main.js";', '')
            _main_js_content = _main_js_content.replace('import "./Main.js";', '')

            with open(_main_js_path, 'w') as _main_js_file:
                _main_js_file.write(_main_js_content)
        except Exception as _e:
            _messagebox.showerror("Error", f"Error finalizing TBL.js: {str(_e)}")

        _messagebox.showinfo("Success", "Process 2/4 Completed Successfully!")
    
    def _extract_feature_rules(self, _pack_zip, _item, _folder_name, _output_zip):
        with _pack_zip.open(_item) as _file_data:
            _output_zip.writestr(_os.path.join(_folder_name, _os.path.basename(_item.filename)), _file_data.read())
        
    def _merge_json(self, _json_list, _file_name):
        def normalize_string(s):
            try:
                s = _re.sub(r'\s*=\s*', '=', s)
                s = s.replace("1st_person", "first_person").replace("3rd_person", "third_person")
                s = s.replace("v.is_first_person", "variable.is_first_person").replace("q.is_spectator", "query.is_spectator")
                return s
            except Exception as e:
                print(f"Error normalizing string '{s}': {e}")
                return s

        def remove_duplicates_from_list(_list, check_keys=False):
            unique_list = []
            seen = set()
            for item in _list:
                try:
                    if isinstance(item, str):
                        normalized_item = normalize_string(item)
                        if normalized_item not in seen:
                            unique_list.append(item)
                            seen.add(normalized_item)
                    elif isinstance(item, dict):
                        normalized_dict = {normalize_string(k): normalize_string(v) if isinstance(v, str) else v for k, v in item.items()}
                        item_tuple = tuple(sorted(normalized_dict.keys())) if check_keys else tuple(sorted(normalized_dict.items()))
                        if item_tuple not in seen:
                            unique_list.append(item)
                            seen.add(item_tuple)
                except Exception as e:
                    print(f"Error processing item '{item}': {e}")
            return unique_list

        def track_and_remove_duplicates(merged_dict, new_dict):
            for k, v in new_dict.items():
                try:
                    norm_key = normalize_string(k)
                    if norm_key in merged_dict:
                        if isinstance(merged_dict[norm_key], dict) and isinstance(v, dict):
                            merged_dict[norm_key] = self._merge_json([merged_dict[norm_key], v], _file_name)
                        elif isinstance(merged_dict[norm_key], list) and isinstance(v, list):
                            check_keys = _file_name == "player.json" and norm_key in ['render_controllers', 'animations', 'animate', 'particle_effects']
                            merged_dict[norm_key] = remove_duplicates_from_list(merged_dict[norm_key] + v, check_keys)
                        else:
                            if normalize_string(str(v)) != normalize_string(str(merged_dict[norm_key])):
                                print(f"Duplicate detected and removed: {_file_name}: {k}")
                    else:
                        merged_dict[norm_key] = v
                except Exception as e:
                    print(f"Error processing key '{k}' with value '{v}': {e}")
            return merged_dict

        _merged = {}
        _format_version_set = False
        _format_version = None
        _warning_shown = False  # Flag to track if the warning has been shown

        if _file_name == "tick.json":
            _merged["values"] = []
            for _json_data in _json_list:
                try:
                    if "values" in _json_data and isinstance(_json_data["values"], list):
                        _merged["values"].extend(_json_data["values"])
                except Exception as e:
                    print(f"Error processing tick.json data: {e}")
            return _merged

        for _json_data in _json_list:
            try:
                if "format_version" in _json_data:
                    if _format_version is None:
                        _format_version = _json_data["format_version"]
                    elif _format_version != _json_data["format_version"] and not _warning_shown:
                        _messagebox.showwarning("Warning", "The addons you are using may not be compatible and a bug may occur while playing.")
                        _warning_shown = True  # Set the flag to True after showing the warning

                for _key, _value in _json_data.items():
                    if (_key == "format_version") and (not _format_version_set):
                        _merged[_key] = _value
                        _format_version_set = True
                    elif _file_name == "_ui_defs.json":
                        if _key not in _merged:
                            _merged[_key] = _value
                        else:
                            if isinstance(_value, list):
                                if not isinstance(_merged[_key], list):
                                    _merged[_key] = [_merged[_key]]
                                _merged[_key].extend(_value)
                                _merged[_key] = remove_duplicates_from_list(_merged[_key])
                            elif isinstance(_value, str):
                                if isinstance(_merged[_key], list):
                                    normalized_value = normalize_string(_value)
                                    existing_values = [normalize_string(i) for i in _merged[_key]]
                                    if normalized_value not in existing_values:
                                        _merged[_key].append(_value)
                                else:
                                    _merged[_key] = [_merged[_key], _value]
                            else:
                                _merged[_key] = _value
                    elif _file_name == "player.json":
                        if _key not in _merged:
                            _merged[_key] = _value
                        else:
                            if isinstance(_value, list):
                                check_keys = _key in ['render_controllers', 'animations', 'animate', 'particle_effects']
                                merged_list = _merged[_key] + _value
                                _merged[_key] = remove_duplicates_from_list(merged_list, check_keys)
                            elif isinstance(_merged[_key], dict) and isinstance(_value, dict):
                                _merged[_key] = self._merge_json([_merged[_key], _value], _file_name)
                            else:
                                _merged[_key] = _value
                    else:
                        if _key not in _merged:
                            _merged[_key] = _value
                        else:
                            if isinstance(_merged[_key], list) and isinstance(_value, list):
                                _merged[_key].extend(_value)
                                _merged[_key] = remove_duplicates_from_list(_merged[_key])
                            elif isinstance(_merged[_key], dict) and isinstance(_value, dict):
                                _merged[_key] = self._merge_json([_merged[_key], _value], _file_name)
                            else:
                                _merged[_key] = _value
            except Exception as e:
                print(f"Error processing JSON data for file '{_file_name}': {e}")

        return _merged
    
    def _merge_player_json(self, _player_json_list):
        _merged = {}
        for _json_data in _player_json_list:
            _merged = self._merge_dicts(_merged, _json_data)
        return _merged

    def _merge_dicts(self, _dict1, _dict2):
        for _key, _value in _dict2.items():
            if _key in _dict1:
                if isinstance(_dict1[_key], dict) and isinstance(_value, dict):
                    _dict1[_key] = self._merge_dicts(_dict1[_key], _value)
                elif isinstance(_dict1[_key], list) and isinstance(_value, list):
                    _dict1[_key].extend(_value)
                else:
                    _dict1[_key] = _value
            else:
                _dict1[_key] = _value
        return _dict1

    def _merge_lang_files(self, _lang_list):
        _merged_lang = {}
        for _lang_data in _lang_list:
            for _line in _lang_data.splitlines():
                if '=' in _line:
                    _key, _value = _line.split('=', 1)
                    _merged_lang[_key] = _value
        return '\n'.join([f"{_key}={_value}" for _key, _value in _merged_lang.items()])

    def _load_json_with_comments(self, _file):
        _file_content = _file.read().decode('latin-1')
        try:
            import json5 as _json5
            return _json5.loads(_file_content)
        except ValueError as e:
            _logging.error(f"Error parsing JSON with comments in file: {_file.name}: {e}")
            return None

    def _get_manifest_data(self, _file):
        try:
            with _zipfile.ZipFile(_file, 'r') as _pack_zip:
                if 'manifest.json' in _pack_zip.namelist():
                    with _pack_zip.open('manifest.json') as _manifest_file:
                        try:
                            # Read the manifest file content using latin-1
                            _manifest_content = _manifest_file.read().decode('latin-1')
                            # Remove block and line comments
                            _manifest_content_clean = _re.sub(r'/\*[\s\S]*?\*/|([^\\:]|^)//.*$', '', _manifest_content)
                            # Remove the "version" field
                            # This regex assumes that "version" is a JSON array of numbers and will match
                            # the key and its value (array). It works for the structure "version": [major, minor, patch]
                            _manifest_content_clean = _re.sub(r'"version"\s*:\s*\[[^]]*\]\s*,?', '', _manifest_content_clean)
                            # Optional: remove trailing commas before closing braces/brackets
                            _manifest_content_clean = _re.sub(r',\s*([}\]])', r'\1', _manifest_content_clean)
                            # Use a library that supports comments in JSON
                            try:
                                import json5 as json
                                _manifest_data = json.loads(_manifest_content_clean)
                            except ImportError:
                                _logging.warning("json5 library not installed, using standard json library.")
                                _manifest_data = _json.loads(_manifest_content)

                            return _manifest_data
                        except Exception as e:
                            _logging.error(f"Error reading or parsing manifest.json in file: {_file}: {e}")
                else:
                    _logging.error(f"manifest.json not found in file: {_file}")
        except Exception as e:
            _logging.error(f"Error opening file: {_file}: {e}")
        
        return None

    def _create_manifest(self):
        _bp_header_uuid = str(_uuid.uuid4())
        _rp_header_uuid = str(_uuid.uuid4())
        _bp_module_uuid = str(_uuid.uuid4())
        _rp_module_uuid = str(_uuid.uuid4())

        _manifest_behavior = {
            "format_version": 2,
            "header": {
                "description": "Modpack Created Using AutoBE : TheBedrockLab WeDidIt",
                "name": "AutoBE Behavior",
                "uuid": _bp_header_uuid,
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 2]
            },
            "modules": [
                {
                    "description": "Created Using AutoBE - TBL",
                    "type": "data",
                    "uuid": _bp_module_uuid,
                    "version": [1, 0, 0]
                },
                {
                    "description": "gametesting",
                    "language": "javascript",
                    "type": "script",
                    "uuid": "a96a2dd3-86e9-4f82-ae5f-a717282d3f1c",
                    "version": [1, 0, 0],
                    "entry": "scripts/TBL.js"
                }
            ],
            "capabilities": ["script_eval"],
            "dependencies": [
                {
                    "uuid": _rp_header_uuid,
                    "version": [1, 0, 0]
                },
                {
                    "module_name": "@minecraft/server",
                    "version": "1.12.0-beta"
                },
                {
                    "module_name": "@minecraft/server-ui",
                    "version": "1.2.0-beta"
                },
                {
                    "module_name": "@minecraft/server-gametest",
                    "version": "1.0.0-beta"
                }
            ],
            "metadata": {
                "authors": ["The Bedrock Labs"]
            }
        }

        _manifest_resource = {
            "format_version": 2,
            "header": {
                "description": "Modpack Created Using AutoBE : TheBedrockLab WeDidIt",
                "name": "AutoBE Resource",
                "uuid": _rp_header_uuid,
                "version": [1, 0, 0],
                "min_engine_version": [1, 21, 2]
            },
            "modules": [
                {
                    "description": "Created Using AutoBE - TBL",
                    "type": "resources",
                    "uuid": _rp_module_uuid,
                    "version": [1, 0, 0]
                }
            ],
            "dependencies": [
                {
                    "uuid": _bp_header_uuid,
                    "version": [1, 0, 0]
                }
            ],
            "metadata": {
                "authors": ["The Bedrock Labs"]
            }
        }

        _bp_path = _os.path.join(self._out_dir, "behavior_pack.zip")
        _rp_path = _os.path.join(self._out_dir, "resource_pack.zip")

        with _zipfile.ZipFile(_bp_path, 'a') as _bp_zip:
            _bp_zip.writestr("manifest.json", _json.dumps(_manifest_behavior, indent=2))

        with _zipfile.ZipFile(_rp_path, 'a') as _rp_zip:
            _rp_zip.writestr("manifest.json", _json.dumps(_manifest_resource, indent=2))
            
        _bp_new_path = _os.path.join(self._out_dir, "behavior_pack.mcpack")
        _shutil.move(_bp_path, _bp_new_path)

        _rp_new_path = _os.path.join(self._out_dir, "resource_pack.mcpack")
        _shutil.move(_rp_path, _rp_new_path)

        _messagebox.showinfo("Success", "Process 1/4 Completed Successfully!")

    def _move_tick_and_delete_functions(self):
        _functions_folder = _os.path.join(self._out_dir, "functions")
        _entities_folder = _os.path.join(self._out_dir, "entities")
        
        _bp_path = _os.path.join(self._out_dir, "behavior_pack.mcpack")
        _rp_path = _os.path.join(self._out_dir, "resource_pack.mcpack")

        _bp_functions_folder = "functions"
        _rp_functions_folder = f"{_bp_functions_folder}/"
        
        _bp_entities_folder = "entities"
        _rp_entities_folder = f"{_bp_entities_folder}/"

        _bp_tick_path = f"{_bp_functions_folder}/tick.json"
        _rp_tick_path = f"{_rp_functions_folder}tick.json"
        
        _bp_player_path = f"{_bp_entities_folder}/player.json"
        _rp_player_path = f"{_rp_entities_folder}player.json"

        try:
            # Move tick.json from resource pack to behavior pack
            with _zipfile.ZipFile(_rp_path, 'r') as _rp_zip:
                with _zipfile.ZipFile(_bp_path, 'a') as _bp_zip:
                    try:
                        _tick_data = _rp_zip.read(_rp_tick_path)
                        _bp_zip.writestr(_bp_tick_path, _tick_data)
                    except KeyError:
                        _logging.warning(f"'{_rp_tick_path}' not found in resource pack.")
                    
                    try:
                        _player_data = _rp_zip.read(_rp_player_path)
                        _bp_zip.writestr(_bp_player_path, _player_data)
                    except KeyError:
                        _logging.warning(f"'{_rp_player_path}' not found in resource pack.")

        except Exception as _e:
            _logging.error(f"An error occurred during the initial file operations: {_e}")

        try:
            # Extract and delete functions folder
            with _zipfile.ZipFile(_rp_path, 'a') as _rp_zip:
                for _file in list(_rp_zip.namelist()):
                    if _file.startswith(_rp_functions_folder):
                        try:
                            _rp_zip.extract(_file, self._out_dir)
                            _os.remove(_os.path.join(self._out_dir, _file))
                        except FileNotFoundError:
                            _logging.warning(f"File '{_file}' not found during extraction.")
                try:
                    _shutil.rmtree(_functions_folder)
                except FileNotFoundError:
                    _logging.warning(f"Folder '{_functions_folder}' not found during removal.")

        except Exception as _e:
            _logging.error(f"An error occurred while processing functions folder: {_e}")

        try:
            # Extract and delete entities folder
            with _zipfile.ZipFile(_rp_path, 'a') as _rp_zip:
                for _file in list(_rp_zip.namelist()):
                    if _file.startswith(_rp_entities_folder):
                        try:
                            _rp_zip.extract(_file, self._out_dir)
                            _os.remove(_os.path.join(self._out_dir, _file))
                        except FileNotFoundError:
                            _logging.warning(f"File '{_file}' not found during extraction.")
                try:
                    _shutil.rmtree(_entities_folder)
                except FileNotFoundError:
                    _logging.warning(f"Folder '{_entities_folder}' not found during removal.")

        except Exception as _e:
            _messagebox.showinfo("Error", f"An error occurred: {_e}")

    def _delete_manifest_files(self):
        _packs = ["behavior_pack.zip", "resource_pack.zip"]

        for _pack in _packs:
            _pack_path = _os.path.join(self._out_dir, _pack)
            _temp_pack_path = _os.path.join(self._out_dir, f"temp_{_pack}")

            try:
                with _zipfile.ZipFile(_pack_path, 'r') as _zip_read:
                    with _zipfile.ZipFile(_temp_pack_path, 'w') as _zip_write:
                        for _item in _zip_read.infolist():
                            if _item.filename not in ["manifest.json", "package.json", "contents.json", ".data", "package-lock.json", "signatures.json"]:
                                _data = _zip_read.read(_item.filename)
                                _zip_write.writestr(_item, _data)

                _os.remove(_pack_path)
                _os.rename(_temp_pack_path, _pack_path)

            except _zipfile.BadZipFile:
                _logging.error(f"Bad ZIP file: {_pack_path}", exc_info=True)
                _messagebox.showerror("Error", f"Bad ZIP file: {_pack_path}")
            except FileNotFoundError:
                _logging.error(f"File not found: {_pack_path}", exc_info=True)
                pass
            except Exception as _e:
                pass

    def _move_and_cleanup(self):
        _bp_path = _os.path.join(self._out_dir, "Behavior_packs", "scripts", "scripts")
        _mainjs_path = _os.path.join(self._out_dir, "Behavior_packs", "scripts", "TBL.js")
        _scriptswe_path = _os.path.join(self._out_dir, "scripts")

        try:
            _shutil.move(_bp_path, self._out_dir)
        except FileNotFoundError:
            print(f"Directory '{_bp_path}' does not exist.")

        try:
            _shutil.move(_mainjs_path, _scriptswe_path)
        except FileNotFoundError:
            print(f"File '{_mainjs_path}' does not exist.")

        try:
            _bp_path = _os.path.join(self._out_dir, "Behavior_packs")
            _shutil.rmtree(_bp_path)
        except FileNotFoundError:
            print(f"Directory '{_bp_path}' does not exist.")

    def _update_behavior_pack(self):
        _bp_path = _os.path.join(self._out_dir, "behavior_pack.mcpack")
        _scripts_folder = _os.path.join(self._out_dir, "scripts")

        if _os.path.exists(_bp_path):
            _temp_dir = _os.path.join(self._out_dir, "temp_unpack")
            _os.makedirs(_temp_dir, exist_ok=True)

            with _zipfile.ZipFile(_bp_path, 'r') as _zip_ref:
                _zip_ref.extractall(_temp_dir)

            _scripts_path_in_temp = _os.path.join(_temp_dir, "scripts")
            if _os.path.exists(_scripts_path_in_temp):
                _shutil.rmtree(_scripts_path_in_temp)
                
            _subpacks_path_in_temp = _os.path.join(_temp_dir, "subpacks")
            if _os.path.exists(_subpacks_path_in_temp):
                _shutil.rmtree(_subpacks_path_in_temp)

            _shutil.copytree(_scripts_folder, _scripts_path_in_temp)

            _new_bp_path = _os.path.join(self._out_dir, "behavior_pack.mcpack")
            with _zipfile.ZipFile(_new_bp_path, 'w') as _zip_ref:
                for _root, _dirs, _files in _os.walk(_temp_dir):
                    for _file in _files:
                        _file_path = _os.path.join(_root, _file)
                        _arcname = _os.path.relpath(_file_path, _temp_dir)
                        _zip_ref.write(_file_path, _arcname)

            _shutil.rmtree(_temp_dir)
            _shutil.rmtree(_scripts_folder)
            _messagebox.showinfo("Success", "Process 3/4 Completed Successfully!")
            _logging.info("Process 3/4 Completed Successfully!")
        else:
            _logging.error("behavior_pack.mcpack not found", exc_info=True)
            _messagebox.showwarning("Error", "behavior_pack.mcpack not found")

    def _merge_flipbook_textures(self, _selected_files):
        if not _selected_files:
            _logging.error("No .mcpack files selected", exc_info=True)
            _messagebox.showerror("Error", "Please select .mcpack files")
            return

        _merged_textures = []

        for _mcpack_file in _selected_files:
            try:
                with _zipfile.ZipFile(_mcpack_file, 'r') as _zip_ref:
                    try:
                        _texture_data = _zip_ref.read('textures/flipbook_textures.json').decode('latin-1')
                        _texture_data_lines = _texture_data.splitlines()
                        _filtered_texture_data = '\n'.join([_line for _line in _texture_data_lines if not _line.strip().startswith('//')])
                        _textures_json = _json.loads(_filtered_texture_data)
                        _merged_textures.extend(_textures_json)
                    except KeyError:
                        pass
            except Exception as _e:
                _logging.error(f"An error occurred while merging flipbook textures: {_e}", exc_info=True)

        _merged_zip_path = _os.path.join(self._out_dir, "flipbook_textures.zip")
        with _zipfile.ZipFile(_merged_zip_path, 'w') as _merged_zip:
            _merged_zip.writestr('flipbook_textures.json', _json.dumps(_merged_textures))

    def _merge_textures_list(self, _selected_files):
        if not _selected_files:
            _logging.error("No .mcpack files selected", exc_info=True)
            _messagebox.showerror("Error", "Please select .mcpack files")
            return

        _merged_textures = []

        for _mcpack_file in _selected_files:
            try:
                with _zipfile.ZipFile(_mcpack_file, 'r') as _zip_ref:
                    try:
                        _texture_data = _zip_ref.read('textures/textures_list.json').decode('latin-1')
                        _texture_data_lines = _texture_data.splitlines()
                        _filtered_texture_data = '\n'.join([_line for _line in _texture_data_lines if not _line.strip().startswith('//')])
                        _textures_json = _json.loads(_filtered_texture_data)
                        _merged_textures.extend(_textures_json)
                    except KeyError:
                        pass
            except Exception as _e:
                _logging.error(f"An error occurred while merging textures list: {_e}", exc_info=True)

        _merged_zip_path = _os.path.join(self._out_dir, "textures_list.zip")
        with _zipfile.ZipFile(_merged_zip_path, 'w') as _merged_zip:
            _merged_zip.writestr('textures_list.json', _json.dumps(_merged_textures))

    def _extract_and_delete_zip_files(self):
        _flipbook_zip_path = _os.path.join(self._out_dir, "flipbook_textures.zip")
        _textures_zip_path = _os.path.join(self._out_dir, "textures_list.zip")

        try:
            with _zipfile.ZipFile(_flipbook_zip_path, 'r') as _flipbook_zip:
                _flipbook_zip.extract('flipbook_textures.json', self._out_dir)
        except FileNotFoundError:
            pass

        try:
            with _zipfile.ZipFile(_textures_zip_path, 'r') as _textures_zip:
                _textures_zip.extract('textures_list.json', self._out_dir)
        except FileNotFoundError:
            pass

        try:
            _os.remove(_flipbook_zip_path)
        except FileNotFoundError:
            pass

        try:
            _os.remove(_textures_zip_path)
        except FileNotFoundError:
            pass

    def _move_to_resource_pack(self):
        _rp_path = _os.path.join(self._out_dir, "resource_pack.mcpack")
        _textures_folder_name = "textures"

        if not _os.path.exists(_rp_path):
            _logging.warning("resource_pack.mcpack not found in output directory", exc_info=True)
            _messagebox.showwarning("Warning", "resource_pack.mcpack not found in output directory")
            return

        try:
            _temp_dir = _os.path.join(self._out_dir, "temp_unpack_resource_pack")
            _os.makedirs(_temp_dir, exist_ok=True)
                
            with _zipfile.ZipFile(_rp_path, 'r') as _zip_ref:
                _zip_ref.extractall(_temp_dir)

            _functions_path_in_temp = _os.path.join(_temp_dir, "functions")
            if (_os.path.exists(_functions_path_in_temp)):
                _shutil.rmtree(_functions_path_in_temp)
                
            _entities_path_in_temp = _os.path.join(_temp_dir, "entities")
            if (_os.path.exists(_entities_path_in_temp)):
                _shutil.rmtree(_entities_path_in_temp)
                
            _subpacks_path_in_temp = _os.path.join(_temp_dir, "subpacks")
            if (_os.path.exists(_subpacks_path_in_temp)):
                _shutil.rmtree(_subpacks_path_in_temp)

            _textures_folder = _os.path.join(_temp_dir, _textures_folder_name)

            _flipbook_textures_source = _os.path.join(self._out_dir, "flipbook_textures.json")
            _flipbook_textures_dest = _os.path.join(_textures_folder, "flipbook_textures.json")
            _shutil.move(_flipbook_textures_source, _flipbook_textures_dest)

            _textures_list_source = _os.path.join(self._out_dir, "textures_list.json")
            _textures_list_dest = _os.path.join(_textures_folder, "textures_list.json")
            _shutil.move(_textures_list_source, _textures_list_dest)

            _new_rp_path = _os.path.join(self._out_dir, "updated_resource_pack.mcpack")
            with _zipfile.ZipFile(_new_rp_path, 'w') as _zip_ref:
                for _root, _dirs, _files in _os.walk(_temp_dir):
                    for _file in _files:
                        _file_path = _os.path.join(_root, _file)
                        _arcname = _os.path.relpath(_file_path, _temp_dir)
                        _zip_ref.write(_file_path, _arcname)

            _shutil.rmtree(_temp_dir)
            _shutil.move(_new_rp_path, _rp_path)
            _shutil.rmtree(_flipbook_textures_source)
            _shutil.rmtree(_textures_list_source)
            _messagebox.showinfo("Success", "Process 4/4 Completed Successfully!")
            _logging.info("Process 4/4 Completed Successfully!")

        except Exception as _e:
            pass
            
    def _show_help(self):
        _help_window = _tk.Toplevel(self._root)
        _help_window.title("Help")
        _help_window.geometry("800x800")
        _help_window.configure(bg='#0A0A0A')

        _help_text = """
        How To Use AutoBE?

         1. Add Files:
           - Click 'Add Files' to select .mcpack files (only) you want to merge.
           - You can select multiple files by holding down the Ctrl (Cmd on Mac) key while clicking.

         2. Remove Selected:
           - Select files from the list by clicking on them.
           - Click 'Remove Selected' to remove them from the list.

         3. Select Output Directory:
           - Click 'Browse' to choose the directory where the processed files will be saved.
           - Ensure you have write permissions for the selected directory.

         4. Start Process:
           - Click 'Start Process' to begin merging the selected .mcpack files.
           - The tool will create a resource pack and a behavior pack in the selected output directory.
           - You will see progress updates and logs in the log area.

         5. Preview Changes:
           - Will be changed or removed soon!
           
         6. Importing Packs:
           - After the Merging process, check your packs for any error's.
           - If none are seen continue with importing the packs.
           - Leave Feedback In YouTube & Discord.
           - If a mod does not work just remove it not all mods work together.

         Important Notes:
         - Make sure you have the right to use and modify the add-ons you are merging, if used for distribute.
         - The Bedrock Lab And Its Developers Are Not Responsible For Any Misuse Of This Tool.
         - Always comply with Mojang's guidelines and policies regarding the use of Minecraft and its content.
         - AutoBE is almost finished thank you for supporting us
         - Contact Us @TheBedrockLab@gmail.com

         For more help check the Discord Channel.

         Property Of TBL
        """

        _help_label = _tk.Label(_help_window, text=_help_text, bg='#0A0A0A', fg='#E1E1E1', font=("Helvetica", 12))
        _help_label.pack(padx=10, pady=10)

if __name__ == "__main__":
    _logging.basicConfig(level=_logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    _ctypes.windll.user32.ShowWindow(_ctypes.windll.kernel32.GetConsoleWindow(), 0)
    _root = _tk.Tk()
    _app = _App1(_root)
    _root.mainloop()
