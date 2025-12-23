import os

def check_itay_file():
    filename = "itay.txt"
    expected_content = "gg"
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"ERROR: {filename} does not exist")
        return False
    
    # Check file content
    with open(filename, 'r') as f:
        content = f.read().strip()
        if content != expected_content:
            print(f"ERROR: {filename} contains '{content}', expected '{expected_content}'")
            return False
    
    print(f"SUCCESS: {filename} exists with correct content '{expected_content}'")
    return True

if __name__ == "__main__":
    check_itay_file()
