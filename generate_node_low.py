import random

def generate_nodes(num):
    while True:
        nodes = []
        
        # if num > 40:
        #     base_count_1 = num // 2
        #     # for i in range(base_count_1):
        #     r = 0
        #     while r < base_count_1:
        #         a = random.uniform(0, 0.1)
        #         if a!= 1.0 and a>=0.005:
        #             nodes.append(round(a, 2))
        #             r += 1
            
        #     base_count_2 = num // 4
        #     for i in range(base_count_2):
        #         a = random.uniform(0.1, 0.2)
        #         nodes.append(round(a, 2))
            
        #     for i in range(num - base_count_1 - base_count_2):
        #         a = random.uniform(0.2, 0.8)
        #         nodes.append(round(a, 2))
        # else:
        #     base_count = num // 2
        #     r = 0
        #     while r < base_count:
        #     # for i in range(base_count):
        #         a = random.uniform(0, 0.1)
        #         if a!= 1.0 and a>=0.005:
        #             nodes.append(round(a, 2))
        #             r += 1
            
        #     for i in range(num - base_count):
        #         a = random.uniform(0.1, 0.8)
        #         nodes.append(round(a, 2))

        base_count = num // 4
        r = 0
        while r < base_count:
        # for i in range(base_count):
            a = random.uniform(0, 0.1)
            if a!= 1.0 and a>=0.005:
                nodes.append(round(a, 2))
                r += 1
        
        for i in range(num - base_count):
            a = random.uniform(0.1, 0.8)
            nodes.append(round(a, 2))
        
        nodes.sort()
        normal_note_rates = [1-x for x in nodes]
        weights = [y/sum(normal_note_rates) for y in normal_note_rates]
        up = 0
        down = 0
        for j in range(len(normal_note_rates)):
            up = up + normal_note_rates[j]**3
            down = down + normal_note_rates[j]
        E = up/down
        if(E > 2/3):
            # print(len(similarity) - i)
            # print(E)
            # print(len(weights))
            return weights, nodes
        

def start_run():
    nodes_num = [10, 22, 34, 46, 58]
    # nodes_num = [10]
    for i in nodes_num:
        weights, nodes = generate_nodes(i)
        # print(weights)
        # print(nodes)
        with open("./node/nodes_low.txt", "a") as f:
            f.write(str(nodes)+"\n")

if __name__ == "__main__":
    for i in range(100):
        if i % 10 == 0:
            print(i)
        start_run()
        