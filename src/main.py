from storage import init_storage

def main ():
    if init_storage():
        print("storage initialized")
    else:
        print("storage not initialized")

if __name__ == "__main__":
    main()