import os, shutil

def copy_to_public(source, destination):
    try:
        if not os.path.exists(source):
            raise Exception(f"Source directory does not exist: {source}")

        if os.path.exists(destination):
            print(f"Removing existing destination directory: {destination}")    
            shutil.rmtree(destination)
            
        print(f"Creating destination directory: {destination}")
        os.mkdir(destination)
        
        directory_list = os.listdir(source)

        for item in directory_list:
            
            source_path = os.path.join(source, item)
            destination_path = os.path.join(destination, item)

            if os.path.isfile(source_path):
                try:
                    print(f"Copying file: {source_path} to {destination_path}")
                    shutil.copy(source_path, destination_path)
                except Exception as e:
                    print(f"Error copying file {source_path}: {e}")

            elif os.path.isdir(source_path):
                try:
                    print(f"Processing directory: {source_path}")
                    copy_to_public(source_path, destination_path)
                except Exception as e:
                    print(f"Error processing directory {source_path}: {e}")
    
    except Exception as e:
        print(f"Error in copy_to_public: {e}")
        raise