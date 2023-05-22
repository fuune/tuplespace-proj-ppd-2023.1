import linsimpy
tse = linsimpy.TupleSpaceEnvironment()
print()

def producer():
    yield tse.timeout(1)
    print(f"(1, 2) added at time {tse.now}")
    yield tse.out((1, 2))

    yield tse.timeout(1)
    print(f"('three', 4) added at time {tse.now}")
    yield tse.out(('three', 4))

    return 'process can return something'

def consumer():
    val = yield tse.in_(('three', int))
    print(f"{val} removed at time {tse.now}")

    val = yield tse.in_((object, 2))
    print(f"{val} removed at time {tse.now}")

tse.eval(('producer_process', producer()))
tse.eval(('consumer_process', consumer()))
tse.run()
assert tse.now == 2
print(tse.items)

####################################################

