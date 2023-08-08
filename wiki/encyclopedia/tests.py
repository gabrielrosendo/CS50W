import os
import random
from django.test import TestCase

# Create your tests here.
path = os.listdir('wiki/entries')
num_files = len(path)
random_number = random.randint(0, num_files)

print(path[random_number])