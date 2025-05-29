import random
def gen_wheels(core):
    return [sorted(random.sample(core,5)) for _ in range(10)]
