import subprocess
import threading
import os
import tkinter as tk
import customtkinter as ctk
import shutil


class BiocondaInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Bioconda Package Installer")
        self.geometry("800x600")
        self.resizable(True, True)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Tab View
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        # Add Tabs
        self.install_tab = self.tab_view.add("Install Package")
        self.installed_tab = self.tab_view.add("Installed Packages")
        self.compiler_tab = self.tab_view.add("Choose Compiler")

        # Set up Tabs
        self.setup_install_tab()
        self.setup_installed_tab()
        self.setup_compiler_tab()

        # Default Python Interpreter
        self.current_interpreter = shutil.which("python")  # Default to system Python

    def setup_install_tab(self):
        self.install_title_label = ctk.CTkLabel(
            self.install_tab, text="Bioconda Package Installer", font=("Arial", 24, "bold"), text_color="cyan"
        )
        self.install_title_label.pack(pady=15)

        self.search_frame = ctk.CTkFrame(self.install_tab, width=700, height=100)
        self.search_frame.pack(pady=10, padx=10, fill="x")

        self.search_entry = ctk.CTkEntry(
            self.search_frame, placeholder_text="Enter package name to search/install",
            width=500, font=("Arial", 14)
        )
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        self.search_button = ctk.CTkButton(
            self.search_frame, text="Search and Install", font=("Arial", 14),
            command=self.search_and_install
        )
        self.search_button.grid(row=0, column=1, padx=10, pady=10)

        self.output_frame = ctk.CTkFrame(self.install_tab, width=700, height=400)
        self.output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.output_textbox = ctk.CTkTextbox(self.output_frame, font=("Courier New", 12))
        self.output_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_installed_tab(self):
        self.installed_title_label = ctk.CTkLabel(
            self.installed_tab, text="Installed Packages", font=("Arial", 24, "bold"), text_color="cyan"
        )
        self.installed_title_label.pack(pady=15)

        self.button_frame = ctk.CTkFrame(self.installed_tab)
        self.button_frame.pack(pady=10)

        self.refresh_button = ctk.CTkButton(
            self.button_frame, text="Show Bioconda Packages", font=("Arial", 14), command=self.fetch_bioconda_packages
        )
        self.refresh_button.grid(row=0, column=0, padx=10)

        self.show_all_button = ctk.CTkButton(
            self.button_frame, text="Show All Packages", font=("Arial", 14), command=self.fetch_all_packages
        )
        self.show_all_button.grid(row=0, column=1, padx=10)

        self.installed_frame = ctk.CTkFrame(self.installed_tab, width=700, height=400)
        self.installed_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.installed_textbox = ctk.CTkTextbox(self.installed_frame, font=("Courier New", 12))
        self.installed_textbox.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_compiler_tab(self):
        self.compiler_title_label = ctk.CTkLabel(
            self.compiler_tab, text="Choose Python Interpreter", font=("Arial", 24, "bold"), text_color="cyan"
        )
        self.compiler_title_label.pack(pady=15)

        # Add a Listbox to display available compilers
        self.compiler_listbox = tk.Listbox(self.compiler_tab, font=("Courier New", 12), height=15)
        self.compiler_listbox.pack(padx=10, pady=10, fill="both", expand=True)

        # Refresh and Select Buttons
        self.refresh_button = ctk.CTkButton(
            self.compiler_tab, text="Refresh List", font=("Arial", 14), command=self.refresh_compiler_list
        )
        self.refresh_button.pack(pady=10)

        self.select_button = ctk.CTkButton(
            self.compiler_tab, text="Set Interpreter", font=("Arial", 14), command=self.set_selected_interpreter
        )
        self.select_button.pack(pady=10)

        self.compiler_output_textbox = ctk.CTkTextbox(self.compiler_tab, font=("Courier New", 12))
        self.compiler_output_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate the list on load
        self.refresh_compiler_list()

    def refresh_compiler_list(self):
        self.compiler_listbox.delete(0, "end")
        interpreters = self.find_all_python_interpreters()

        if interpreters:
            for interpreter in interpreters:
                self.compiler_listbox.insert("end", interpreter)
        else:
            self.compiler_output_textbox.insert("end", "No Python interpreters found.\n", "error")

    def set_selected_interpreter(self):
        selected_index = self.compiler_listbox.curselection()

        if not selected_index:
            self.compiler_output_textbox.insert("end", "No interpreter selected.\n", "error")
            return

        selected_interpreter = self.compiler_listbox.get(selected_index[0])
        self.current_interpreter = selected_interpreter
        self.compiler_output_textbox.insert("end", f"Selected interpreter: {selected_interpreter}\n", "success")
        self.compiler_output_textbox.see("end")

    def find_all_python_interpreters(self):
        paths = os.environ["PATH"].split(os.pathsep)
        interpreters = []

        for path in paths:
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.startswith("python") and os.access(os.path.join(path, file), os.X_OK):
                        interpreters.append(os.path.join(path, file))

        return sorted(interpreters)

    def search_and_install(self):
        package_name = self.search_entry.get().strip()

        if not package_name:
            self.output_textbox.insert("end", "Please enter a package name.\n", "error")
            return

        self.output_textbox.insert("end", f"Searching and installing package: {package_name}...\n")
        self.output_textbox.see("end")

        threading.Thread(target=self.install_package, args=(package_name,), daemon=True).start()

    def install_package(self, package_name):
        try:
            process = subprocess.Popen(
                [self.current_interpreter, "-m", "conda", "install", "-c", "bioconda", package_name, "-y"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            for line in iter(process.stdout.readline, ''):
                self.update_output_textbox(line)
                
            process.stdout.close()
            process.wait()

            if process.returncode == 0:
                self.update_output_textbox(f"Package '{package_name}' installed successfully.\n")
            else:
                error_msg = process.stderr.read()
                self.update_output_textbox(f"Failed to install '{package_name}'.\nError: {error_msg}\n")

        except Exception as e:
            self.update_output_textbox(f"An error occurred: {str(e)}\n")

    def update_output_textbox(self, text):
        # Use after() for thread-safe GUI update
        self.output_textbox.after(0, self.output_textbox.insert, "end", text)
        self.output_textbox.after(0, self.output_textbox.see, "end")

    def fetch_bioconda_packages(self):
        # This method will fetch the list of installed Bioconda packages
        self.installed_textbox.delete(1.0, "end")  # Clear the current list
        try:
            process = subprocess.Popen(
                ["conda", "list", "-c", "bioconda"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            for line in iter(process.stdout.readline, ''):
                self.update_installed_textbox(line)

            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                error_msg = process.stderr.read()
                self.update_installed_textbox(f"Error fetching Bioconda packages: {error_msg}\n")

        except Exception as e:
            self.update_installed_textbox(f"An error occurred: {str(e)}\n")

    def update_installed_textbox(self, text):
        # Update the textbox in a thread-safe manner
        self.installed_textbox.after(0, self.installed_textbox.insert, "end", text)
        self.installed_textbox.after(0, self.installed_textbox.see, "end")

    def fetch_all_packages(self):
        self.installed_textbox.delete(1.0, "end")
        try:
            process = subprocess.Popen(
                ["conda", "list"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            for line in iter(process.stdout.readline, ''):
                self.update_installed_textbox(line)

            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                error_msg = process.stderr.read()
                self.update_installed_textbox(f"Error fetching all packages: {error_msg}\n")

        except Exception as e:
            self.update_installed_textbox(f"An error occurred: {str(e)}\n")


if __name__ == "__main__":
    app = BiocondaInstallerApp()
    app.mainloop()

