#!/usr/bin/env python3 

import random

for _ in range(10000):
    num_count = random.randint(100, 200)
    print(" ".join(str(random.randrange(-10000, 10000)) for _ in range(num_count)))
    
