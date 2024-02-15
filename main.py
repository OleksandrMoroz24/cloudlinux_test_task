import os
from collections import defaultdict

try:
    import magic  # Використовуйте для визначення типу файлу, якщо доступно

    magic_available = True
except ImportError:
    magic_available = False  # magic не доступний, буде використано розширення файлу


def scan_directory(directory, size_threshold, prefix=''):
    print(f"{prefix}{'|-- ' if prefix else ''}{os.path.basename(directory)}/")
    next_prefix = prefix + "    "
    total_size = 0
    file_types = defaultdict(lambda: {'count': 0, 'size': 0})
    large_files = []

    try:
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False):
                    dir_size, dir_file_types, dir_large_files = scan_directory(entry.path, size_threshold, next_prefix)
                    total_size += dir_size
                    for file_type, info in dir_file_types.items():
                        file_types[file_type]['count'] += info['count']
                        file_types[file_type]['size'] += info['size']
                    large_files.extend(dir_large_files)
                else:
                    try:
                        file_size = entry.stat(follow_symlinks=False).st_size
                        total_size += file_size

                        if magic_available:
                            file_type = magic.from_file(entry.path, mime=True)
                        else:
                            _, ext = os.path.splitext(entry.name)
                            file_type = ext.lower() or 'unknown'

                        file_types[file_type]['count'] += 1
                        file_types[file_type]['size'] += file_size

                        if file_size > size_threshold:
                            large_files.append((entry.path, file_size))

                        print(f"{next_prefix}{'|-- '}{entry.name} ({file_size} bytes)")

                    except Exception as e:
                        print(f"{next_prefix}{'|-- '}{entry.name} - Error: {e}")
    except PermissionError:
        print(f"{next_prefix}Permission Denied.")

    if prefix == '':  # Виведення підсумкової інформації лише для кореневої директорії
        print("\nSummary:")
        print(f"Total size of files: {total_size} bytes")
        for file_type, info in file_types.items():
            print(f"Type: {file_type}, Count: {info['count']}, Size: {info['size']} bytes")

        if large_files:
            print("\nLarge files:")
            for path, size in large_files:
                print(f"{path}: {size} bytes")

    return total_size, file_types, large_files  # Повертаємо зібрану інформацію


def analyze_permissions(directory):
    unusual_perms = []

    for root, dirs, files in os.walk(directory):
        for name in files + dirs:
            file_path = os.path.join(root, name)
            mode = os.stat(file_path).st_mode
            if not (mode & 0o777 in [0o644, 0o755]):
                unusual_perms.append((file_path, oct(mode)[-3:]))

    # Виведення файлів з незвичайними дозволами
    if unusual_perms:
        print("\nFiles and directories with unusual permissions:")
        for path, perms in unusual_perms:
            print(f"{path}: Permissions {perms}")


def interactive_mode():
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
                        input("Enter size threshold for files in bytes (0 for no threshold): ").strip())
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