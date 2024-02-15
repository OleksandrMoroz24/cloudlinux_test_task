## Program Description

This program provides a suite of tools for analyzing the file system structure within a specified directory. It features an interactive command-line interface that allows users to scan directories, identify large files, and analyze file permissions.

### Features

- **Directory Scanning:** Recursively scans a specified directory, printing out its structure in a tree-like format. It provides a visual representation of the directory hierarchy, including all subdirectories and files.

- **File Type and Size Summary:** Summarizes the types of files within the scanned directory, counting the occurrences of each file type and calculating the total size of files grouped by type. This feature helps in identifying the composition of the directory in terms of file types and sizes.

- **Large File Identification:** Allows users to specify a size threshold and identifies all files exceeding this threshold. This is particularly useful for finding large files that may be consuming significant disk space.

- **Permission Analysis:** Analyzes and reports files and directories with "unusual" permissions. By default, it flags any permissions other than 644 (read and write for the owner, read for others) for files and 755 (read, write, and execute for the owner, read and execute for others) for directories as unusual.

- **Interactive Command Line Interface:** Users can easily navigate the program's features through simple commands, making it accessible for both experienced and novice users.

### Technologies Used

- Python 3: The core programming language used to develop the program.
- `os` and `collections` modules: Utilized for navigating the file system and organizing data.
- `magic` library (optional): Employed for inspecting file types more accurately than relying solely on file extensions. If `magic` is not available, the program gracefully falls back to using file extensions.


## Project Setup and Running Guide

### Prerequisites

Ensure you have the following installed on your Linux system:
- Git
- Python 3
- pip (Python package manager)

### Installation

#### 1. Install Git

If you haven't installed Git yet, open your terminal and run:

```bash
sudo apt-get update
sudo apt-get install git
```

This command is for Debian/Ubuntu-based distributions. For other distributions, please use the package manager specific to your Linux distribution (e.g., `yum` for CentOS or `dnf` for Fedora).

#### 2. Clone the Project Repository

Navigate to the directory where you want to clone the project and run:

```bash
git clone https://github.com/OleksandrMoroz24/cloudlinux_test_task.git
```

#### 3. Set Up a Virtual Environment

Navigate into the project directory:

```bash
cd cloudlinux_test_task
```

Create a virtual environment to isolate the project dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Linux or macOS:

```bash
source venv/bin/activate
```

#### 4. Install Project Dependencies

With the virtual environment activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

### Running the Project

Execute the main script or start the project as instructed in the project's documentation. For example, if the entry point is a Python script:

```bash
python main.py
```

### Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment by running:

```bash
deactivate
```

This will return you to the global Python environment.

## Example of usage
### scan command
![image](https://github.com/OleksandrMoroz24/cloudlinux_test_task/assets/140017557/329b8551-a4cb-4ca4-8cca-d98435f377b0)
![image](https://github.com/OleksandrMoroz24/cloudlinux_test_task/assets/140017557/86ed064c-90c8-414e-8def-e32740a4d93a)
![image](https://github.com/OleksandrMoroz24/cloudlinux_test_task/assets/140017557/1b894a78-a7d0-426c-ac3b-fee5c6007891)
### perms command



