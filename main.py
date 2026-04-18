from kirk import kirk

if __name__ == "__main__":
    for i in range(1, 5):
        print(f"Running level {i}...")
        kirk(i, "soft")
        kirk(i, "medium")
        kirk(i, "hard")
        kirk(i, "intermediate")
        kirk(i, "wet")
    