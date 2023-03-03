# importing the required module
import timeit

# code snippet to be executed only once
# before the stmt parameter in timeit
mysetup = "import numpy as np"

# code snippet whose execution time
# is to be measured
mycode = '''
dict = {}
for i in range(10000):
    point_tuple = (90,78)
    distance = np.linalg.norm(np.array((200,300)) - np.array((312,678)))
    data = {point_tuple: distance}
    dict.update(data)
    
'''

# timeit statement
exec_time = timeit.timeit(stmt=mycode, setup=mysetup, number=1) * 10**3
print(f"The time of execution of above program is : {exec_time:.03f}ms")
