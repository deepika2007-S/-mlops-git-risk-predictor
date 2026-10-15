def extremely_risky_nested_loops():
    # Adding lots of loops to spike the code complexity index!
    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    if a == b and c == d:
                        print("This is highly complex structural code!")
    return False
