import base64
import os


def decode_filename(filename):
    # try to decode the filename as base64
    try:
        decoded = base64.b64decode(filename).decode()
        return decoded
    except:
        # if decoding fails, return the original filename
        return filename


# specify the directory to scan
directory = "C:/Users/Administrator/Desktop/printTemplate/"

# loop through all subdirectories and files in the directory
for root, dirs, files in os.walk(directory):
    for filename in files:
        # get the full path of the file
        filepath = os.path.join(root, filename)
        # get the new filename by calling the decode function
        new_filename = decode_filename(filename)
        # if the new filename is different from the original one, rename the file
        if new_filename != filename:
            # get the new full path of the file
            new_filepath = os.path.join(root, new_filename)
            # try to rename the file
            try:
                os.rename(filepath, new_filepath)
            except OSError as e:
                # handle possible errors
                print(f"Failed to rename {filepath} to {new_filepath}: {e}")
