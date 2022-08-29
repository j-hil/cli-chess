from itertools import product

if __name__ == "__main__":
    for i, j in product(range(8), repeat=2):
        if j ==7:
            end = "\n" if i !=2  else "       CLI CHESS :) - coming soon\n"
        else:
            end = ""
        print("##" if (i + j) % 2 == 0 else "  ", end=end)
