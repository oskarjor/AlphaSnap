from utils.utils import all_subclasses

if __name__ == "__main__":
    import Card
    sub = all_subclasses(Card.Card)
    for s in sub:
        try:
            print(s().name)
        except:
            continue