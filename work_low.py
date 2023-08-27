import random


def PBFT_prepare_consensus(nodes, primary_node_id):
    prepare_nodes = []
    primary_node_wrong = False
    f = (len(nodes) - 1) // 3
    for i in range(len(nodes)):
        error = random.randint(0, 1)
        if error == 0:
            prepare_nodes.append(i)
        else:
            x = random.uniform(0, 1)
            if x > nodes[i]:
                prepare_nodes.append(i)
            elif x <= nodes[i] and i == primary_node_id:
                primary_node_wrong = True
    return len(prepare_nodes) >= (2*f+1), len(prepare_nodes), primary_node_wrong
    
def PBFT_commit_consensus(nodes, primary_node_id):
    commit_nodes = []
    primary_node_wrong = False
    f = (len(nodes) - 1) // 3
    for i in range(len(nodes)):
        error = random.randint(0, 1)
        if error == 0:
            commit_nodes.append(i)
        else:
            x = random.uniform(0, 1)
            if x > nodes[i]:
                commit_nodes.append(i)
            elif x <= nodes[i] and i == primary_node_id:
                primary_node_wrong = True
    return len(commit_nodes) >= (2*f+1), len(commit_nodes), primary_node_wrong

def PBFT_run_consensus(nodes):
    all_round = 10000
    correct_round = 0
    all_prepare_count = 0
    all_commit_count = 0
    primary_node_wrong_round = 0
    primary_node_id = 0
    for i in range(all_round):
        prepare_res, prepare_count, primary_node_wrong = PBFT_prepare_consensus(nodes, primary_node_id)
        
        if primary_node_wrong == True:
            primary_node_wrong_round += 1
            primary_node_id = (primary_node_id + 1) % len(nodes)
            continue

        if prepare_res == True:
            commit_res, commit_count, primary_node_wrong = PBFT_commit_consensus(nodes, primary_node_id)

            if primary_node_wrong == True:
                primary_node_wrong_round += 1
                primary_node_id = (primary_node_id + 1) % len(nodes)
                continue

            if commit_res == True:
                correct_round += 1
                all_prepare_count += prepare_count
                all_commit_count += commit_count
    
    PBFT_consensus_success_rate = correct_round / all_round
    PBFT_message_right_rate = (all_prepare_count + all_commit_count) / (correct_round * len(nodes) *2)
    PBFT_primary_node_error_rate = primary_node_wrong_round / all_round
    # print("PBFT 共识成功率: ", PBFT_consensus_success_rate)
    # print("PBFT 消息正确率: ", PBFT_message_right_rate)
    # print("PBFT 主节点出错率: ", PBFT_primary_node_error_rate)

    with open(r"./res1/PBFT.txt", "a") as f:
        f.write(str(PBFT_consensus_success_rate) + " " + str(PBFT_message_right_rate) + " " + str(PBFT_primary_node_error_rate) + "\n")



def WPBFT_prepare_consensus(nodes, weights, primary_node_id):
    prepare_nodes = []
    primary_node_wrong = False
    f = (len(nodes) - 1) // 3
    for i in range(len(nodes)):
        error = random.randint(0, 1)
        if error == 0:
            prepare_nodes.append(i)
        else:
            x = random.uniform(0, 1)
            if x > nodes[i]:
                prepare_nodes.append(i)
            elif x <= nodes[i] and i == primary_node_id:
                primary_node_wrong = True
    all_weight = 0
    for i in prepare_nodes:
        all_weight += weights[i]
    return all_weight >= (2*f+1)/(3*f+1), len(prepare_nodes), prepare_nodes, primary_node_wrong

def WPBFT_commit_consensus(nodes, weights, primary_node_id):
    commit_nodes = []
    primary_node_wrong = False
    f = (len(nodes) - 1) // 3
    for i in range(len(nodes)):
        error = random.randint(0, 1)
        if error == 0:
            commit_nodes.append(i)
        else:
            x = random.uniform(0, 1)
            if x > nodes[i]:
                commit_nodes.append(i)
            elif x <= nodes[i] and i == primary_node_id:
                primary_node_wrong = True
    all_weight = 0
    for i in commit_nodes:
        all_weight += weights[i]
    return all_weight >= (2*f+1)/(3*f+1), len(commit_nodes), commit_nodes, primary_node_wrong

def WPBFT_run_consensus(nodes, weights):
    all_round = 10000
    correct_round = 0
    all_prepare_count = 0
    all_commit_count = 0
    primary_node_wrong_round = 0
    primary_node_id = 0

    for i in range(all_round):
        prepare_res, prepare_count, prepare_nodes, primary_node_wrong = WPBFT_prepare_consensus(nodes, weights, primary_node_id)
        
        if primary_node_wrong == True:
            primary_node_wrong_round += 1
            primary_node_id, weights = WPBFT_get_next_primary_id(primary_node_id, weights)
            
            continue
        
        if prepare_res == True:
            commit_res, commit_count, commit_nodes, primary_node_wrong = WPBFT_commit_consensus(nodes, weights, primary_node_id)
            
            if primary_node_wrong == True:
                primary_node_wrong_round += 1
                primary_node_id, weights = WPBFT_get_next_primary_id(primary_node_id, weights)
                continue
            
            if commit_res == True:
                correct_round += 1
                all_prepare_count += prepare_count
                all_commit_count += commit_count

                weights = WPBFT_update_weights(weights, nodes, prepare_nodes, commit_nodes)
            else:
                commit_nodes = []
        else:
            prepare_nodes = []
            commit_nodes = []
        
    
    WPBFT_consensus_success_rate = correct_round / all_round
    WPBFT_message_right_rate = (all_prepare_count + all_commit_count) / (correct_round * len(nodes) *2)
    WPBFT_primary_node_error_rate = primary_node_wrong_round / all_round
    # print("IWPBFT 共识成功率: ", IWPBFT_consensus_success_rate)
    # print("IWPBFT 消息正确率: ", IWPBFT_message_right_rate)
    # print("IWPBFT 主节点出错率: ", IWPBFT_primary_node_error_rate)

    with open(r"./res1/WPBFT.txt", "a") as f:
        f.write(str(WPBFT_consensus_success_rate) + " " + str(WPBFT_message_right_rate) + " " + str(WPBFT_primary_node_error_rate) + "\n")

def WPBFT_update_weights(weights, nodes, prepare_nodes, commit_nodes):
    tmp = weights
    wrong_node = []
    for i in range(len(nodes)):
        if (i in prepare_nodes) and (i in commit_nodes):
            continue
        else:
            wrong_node.append(i)
    for i in range(len(nodes)):
        if i not in wrong_node:
            tmp[i] = weights[i] + (len(weights) - len(wrong_node)) / len(weights) * (1 - weights[i])
        else:
            tmp[i] = weights[i] - (len(weights) - len(wrong_node)) / len(weights) * weights[i]
    weights = [i/sum(tmp) for i in tmp]
    return weights

def WPBFT_get_next_primary_id(primary_node_id, weights):
    next_id = 0
    max_weight = 0
    for i in range(len(weights)):
        if i != primary_node_id:
            if weights[i] > max_weight:
                max_weight = weights[i]
                next_id = i
    tmp = weights
    deducted_weight = weights[primary_node_id] * 0.5
    for i in range(len(weights)):
        if i == primary_node_id:
            tmp[i] = weights[i] * 0.5
        else:
            tmp[i] += deducted_weight/(len(weights)-1)
        
    new_weights = tmp
    return next_id, new_weights



def IWPBFT_prepare_consensus(nodes, weights, primary_node_id):
    prepare_nodes = []
    primary_node_wrong = False
    f = (len(nodes) - 1) // 3
    for i in range(len(nodes)):
        error = random.randint(0, 1)
        if error == 0:
            prepare_nodes.append(i)
        else:
            x = random.uniform(0, 1)
            if x > nodes[i]:
                prepare_nodes.append(i)
            elif x <= nodes[i] and i == primary_node_id:
                primary_node_wrong = True
    all_weight = 0
    for i in prepare_nodes:
        all_weight += weights[i]
    return all_weight >= (2*f+1)/(3*f+1), len(prepare_nodes), prepare_nodes, primary_node_wrong

def IWPBFT_commit_consensus(nodes, weights, primary_node_id):
    commit_nodes = []
    primary_node_wrong = False
    f = (len(nodes) - 1) // 3
    for i in range(len(nodes)):
        error = random.randint(0, 1)
        if error == 0:
            commit_nodes.append(i)
        else:
            x = random.uniform(0, 1)
            if x > nodes[i]:
                commit_nodes.append(i)
            elif x <= nodes[i] and i == primary_node_id:
                primary_node_wrong = True
    all_weight = 0
    for i in commit_nodes:
        all_weight += weights[i]
    return all_weight >= (2*f+1)/(3*f+1), len(commit_nodes), commit_nodes, primary_node_wrong

def IWPBFT_get_next_primary_id(primary_node_id, weights):
    next_id = 0
    max_weight = 0
    for i in range(len(weights)):
        if i != primary_node_id:
            if weights[i] > max_weight:
                max_weight = weights[i]
                next_id = i
    tmp = weights
    tmp[primary_node_id] = tmp[primary_node_id] * 0.1
    new_weights = [i/sum(tmp) for i in tmp]
    return next_id, new_weights

def IWPBFT_run_consensus(nodes, weights):
    all_round = 10000
    correct_round = 0
    all_prepare_count = 0
    all_commit_count = 0
    primary_node_wrong_round = 0
    primary_node_id = 0

    for i in range(all_round):
        prepare_res, prepare_count, prepare_nodes, primary_node_wrong = IWPBFT_prepare_consensus(nodes, weights, primary_node_id)
        
        if primary_node_wrong == True:
            primary_node_wrong_round += 1
            primary_node_id, weights = IWPBFT_get_next_primary_id(primary_node_id, weights)
            
            continue
        
        if prepare_res == True:
            commit_res, commit_count, commit_nodes, primary_node_wrong = IWPBFT_commit_consensus(nodes, weights, primary_node_id)
            
            if primary_node_wrong == True:
                primary_node_wrong_round += 1
                primary_node_id, weights = IWPBFT_get_next_primary_id(primary_node_id, weights)
                continue
            
            if commit_res == True:
                correct_round += 1
                all_prepare_count += prepare_count
                all_commit_count += commit_count

                weights = IWPBFT_update_weights(weights, nodes, prepare_nodes, commit_nodes)
            else:
                commit_nodes = []
        else:
            prepare_nodes = []
            commit_nodes = []
        
    
    IWPBFT_consensus_success_rate = correct_round / all_round
    IWPBFT_message_right_rate = (all_prepare_count + all_commit_count) / (correct_round * len(nodes) *2)
    IWPBFT_primary_node_error_rate = primary_node_wrong_round / all_round
    # print("IWPBFT 共识成功率: ", IWPBFT_consensus_success_rate)
    # print("IWPBFT 消息正确率: ", IWPBFT_message_right_rate)
    # print("IWPBFT 主节点出错率: ", IWPBFT_primary_node_error_rate)

    with open(r"./res1/IWPBFT.txt", "a") as f:
        f.write(str(IWPBFT_consensus_success_rate) + " " + str(IWPBFT_message_right_rate) + " " + str(IWPBFT_primary_node_error_rate) + "\n")

def IWPBFT_update_weights(weights, nodes, prepare_nodes, commit_nodes):
    average = 1 / len(weights)
    bsae_point = average * average
    tmp = weights
    wrong_node = []
    for i in range(len(nodes)):
        if (i in prepare_nodes) and (i in commit_nodes):
            continue
        else:
            wrong_node.append(i)
    for i in range(len(nodes)):
        if i not in wrong_node:
            if weights[i] > average + bsae_point:
                level = (weights[i] - average - bsae_point) // bsae_point
                coefficient = 1 - min(0.3, 0.1 * (level))
            elif weights[i] < average - bsae_point:
                level = (average - bsae_point - weights[i]) // bsae_point
                coefficient = min(0.5, 0.1 * (level)) + 1
            else:
                coefficient = 1
            tmp[i] = weights[i] + bsae_point * coefficient
        else:
            tmp[i] = weights[i] - (len(weights) - len(wrong_node)) / len(weights) * weights[i]
    weights = [i/sum(tmp) for i in tmp]
    return weights

def calc_weights(nodes):
    nodes.sort()
    normal_note_rates = [1-x for x in nodes]
    weights = [y/sum(normal_note_rates) for y in normal_note_rates]
    up = 0
    down = 0
    for j in range(len(normal_note_rates)):
        up = up + normal_note_rates[j]**3
        down = down + normal_note_rates[j]
    E = up/down
    assert E > 2/3
    return weights

def start_run():
    nodes_num = [10, 22, 34, 46, 58]
    with open("./node/nodes_low.txt", "r") as f:
            data = f.readlines()
    # nodes_num = [10]
    count = 0
    for line in data:
        nodes = eval(line.strip())
        assert len(nodes) == nodes_num[count % 5]
        weights = calc_weights(nodes)

        IWPBFT_nodes = nodes.copy()
        IWPBFT_run_consensus(IWPBFT_nodes, weights)

        WPBFT_nodes = nodes.copy()
        WPBFT_run_consensus(WPBFT_nodes, weights)

        PBFT_nodes = nodes.copy()
        random.shuffle(PBFT_nodes)
        PBFT_run_consensus(PBFT_nodes)

        count += 1


if __name__ == "__main__":
    start_run()
        
