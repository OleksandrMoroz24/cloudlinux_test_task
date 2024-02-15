import os
from collections import defaultdict

try:
    import magic  # for inspecting type of files

    magic_available = True
except ImportError:
    magic_available = False  # magic not available, use file extension


def scan_directory(
        directory: str,
        size_threshold: int,
        prefix=""
) -> tuple:
    """
        Recursively scans a directory, printing its structure and summarizing file types and sizes.

        Args:
            directory (str): The path to the directory to scan.
            size_threshold (int): The size threshold in bytes for identifying large files.
            prefix (str): A prefix used for indentation to represent the structure visually.

        Returns:
            tuple: A tuple containing the total size of files, a dictionary of file types with their counts and sizes, and a list of large files.
    """
    print(f"{prefix}{'|-- ' if prefix else ''}{os.path.basename(directory)}/")
    next_prefix = prefix + "    "
    total_size = 0
    file_types = defaultdict(lambda: {"count": 0, "size": 0})
    large_files = []

    try:
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False):
                    dir_size, dir_file_types, dir_large_files = scan_directory(
                        entry.path, size_threshold, next_prefix
                    )
                    total_size += dir_size
                    for file_type, info in dir_file_types.items():
                        file_types[file_type]["count"] += info["count"]
                        file_types[file_type]["size"] += info["size"]
                    large_files.extend(dir_large_files)
                else:
                    try:
                        file_size = entry.stat(follow_symlinks=False).st_size
                        total_size += file_size

                        if magic_available:
                            file_type = magic.from_file(entry.path, mime=True)
                        else:
                            _, ext = os.path.splitext(entry.name)
                            file_type = ext.lower() or "unknown"

                        file_types[file_type]["count"] += 1
                        file_types[file_type]["size"] += file_size

                        if file_size > size_threshold:
                            large_files.append((entry.path, file_size))

                        print(f"{next_prefix}{'|-- '}{entry.name} ({file_size} bytes)")

                    except Exception as e:
                        print(f"{next_prefix}{'|-- '}{entry.name} - Error: {e}")
    except PermissionError:
        print(f"{next_prefix}Permission Denied.")

    if prefix == "":  # Displaying summary information only for the root directory
        print("\nSummary:")
        print(f"Total size of files: {total_size} bytes")
        for file_type, info in file_types.items():
            print(
                f"Type: {file_type}, Count: {info['count']}, Size: {info['size']} bytes"
            )

        if large_files:
            print("\nLarge files:")
            for path, size in large_files:
                print(f"{path}: {size} bytes")

    return total_size, file_types, large_files  # return all collected information


def analyze_permissions(directory: str) -> None:
    """
        Analyzes and prints files and directories within the given directory that have unusual permissions.

        Unusual permissions are defined as not being either 644 or 755.

        Args:
            directory (str): The path to the directory to analyze for unusual permissions.

        This function does not return anything but prints out the paths and permissions of files and directories with unusual permissions.
    """
    unusual_perms = []

    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            file_path = os.path.join(root, name)
            mode = os.stat(file_path).st_mode
            if not (mode & 0o777 in [0o644, 0o755]):   # filtering permissions, usual permissions is 644 and 755
                unusual_perms.append((file_path, oct(mode)[-3:]))

    # print files with unusual permissions
    if unusual_perms:
        print("\nFiles and directories with unusual permissions:")
        for path, perms in unusual_perms:
            print(f"{path}: Permissions {perms}")


def interactive_mode():
    """
    Provides an interactive command line interface for the user to choose between scanning a directory, analyzing file permissions, or exiting the program.

    The user can specify the directory to scan or analyze and set a size threshold for identifying large files during the scan.

    This function loops until the user chooses to exit.
    """
    while True:
        command = input("\nEnter command (scan, perms, exit): ").strip().lower()
        if command == "exit":
            break
        elif command in ["scan", "perms"]:
            directory = input("Enter directory path: ").strip()
            if not os.path.isdir(directory):
                print("Invalid directory path")
                continue

            if command == "scan":
                try:
                    size_threshold = int(
                        input(
                            "Enter size threshold for files in bytes (0 for no threshold): "
                        ).strip()
                    )
                except ValueError:
                    print("Invalid size threshold, setting to 0")
                    size_threshold = 0
                scan_directory(directory, size_threshold)
            elif command == "perms":
                analyze_permissions(directory)
        else:
            print("Unknown command")


if __name__ == "__main__":
    interactive_mode()
