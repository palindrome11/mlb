
import argparse
import hashlib
import os

def files_match(p1, p2):
    if os.stat(p1).st_size != os.stat(p2).st_size:
        return False
    return file_checksum(p1) == file_checksum(p2)

def file_checksum(path, algo='sha256'):
    h = hashlib.new(algo)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare two files by size and checksum')
    parser.add_argument('file1', help='first file to compare')
    parser.add_argument('file2', help='second file to compare')
    parser.add_argument('--verbose', '-v', action='store_true', help='show checksums')
    args = parser.parse_args()

    if args.verbose:
        print(f"{args.file1}: {file_checksum(args.file1)}")
        print(f"{args.file2}: {file_checksum(args.file2)}")

    print("MATCH" if files_match(args.file1, args.file2) else "DIFFER")