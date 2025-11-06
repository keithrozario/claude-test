from hello_world_package import sha256_hash


def main():
    data = b"hello world"
    hash_result = sha256_hash(data)
    print(f"SHA256 hash of '{data.decode()}': {hash_result}")


if __name__ == "__main__":
    main()
