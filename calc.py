

def calc_high_rate(path):
    rpath = "./res/" + path
    with open(rpath, "r") as f:
        data = f.readlines()

    nodes_num = [10, 22, 34, 46, 58]

    consensus_success_rates = [0, 0, 0, 0, 0]
    message_right_rates = [0, 0, 0, 0, 0]
    primary_node_error_rates = [0, 0, 0, 0, 0]

    count = 0
    for line in data:
        rates = line.strip().split()
        
        consensus_success_rates[count % 5] += float(rates[0])
        message_right_rates[count % 5] += float(rates[1])
        primary_node_error_rates[count % 5] += float(rates[2])
        count += 1

    # print(consensus_success_rates)
    # print(message_right_rates)
    # print(primary_node_error_rates)
    consensus_success_rate = [i/100 for i in consensus_success_rates]
    message_right_rate = [i/100 for i in message_right_rates]
    primary_node_error_rate = [i/100 for i in primary_node_error_rates]
    print(path)
    print(consensus_success_rate)
    print(message_right_rate)
    print(primary_node_error_rate)


def calc_low_rate(path):
    rpath = "./res1/" + path
    with open(rpath, "r") as f:
        data = f.readlines()

    nodes_num = [10, 22, 34, 46, 58]

    consensus_success_rates = [0, 0, 0, 0, 0]
    message_right_rates = [0, 0, 0, 0, 0]
    primary_node_error_rates = [0, 0, 0, 0, 0]

    count = 0
    for line in data:
        rates = line.strip().split()
        
        consensus_success_rates[count % 5] += float(rates[0])
        message_right_rates[count % 5] += float(rates[1])
        primary_node_error_rates[count % 5] += float(rates[2])
        count += 1

    # print(consensus_success_rates)
    # print(message_right_rates)
    # print(primary_node_error_rates)
    consensus_success_rate = [i/100 for i in consensus_success_rates]
    message_right_rate = [i/100 for i in message_right_rates]
    primary_node_error_rate = [i/100 for i in primary_node_error_rates]
    print(path)
    print(consensus_success_rate)
    print(message_right_rate)
    print(primary_node_error_rate)


def calc_rate_with_error(path):
    rpath = "./res_error1/" + path
    with open(rpath, "r") as f:
        data = f.readlines()

    error_rates = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2]

    consensus_success_rates = [0 for i in range(len(error_rates))]
    message_right_rates = [0 for i in range(len(error_rates))]
    primary_node_error_rates = [0 for i in range(len(error_rates))]

    count = 0
    for line in data:
        rates = line.strip().split()
        
        consensus_success_rates[count % 11] += float(rates[0])
        message_right_rates[count % 11] += float(rates[1])
        primary_node_error_rates[count % 11] += float(rates[2])
        count += 1

    # print(consensus_success_rates)
    # print(message_right_rates)
    # print(primary_node_error_rates)
    consensus_success_rate = [i/100 for i in consensus_success_rates]
    message_right_rate = [i/100 for i in message_right_rates]
    primary_node_error_rate = [i/100 for i in primary_node_error_rates]
    print(path)
    print(consensus_success_rate)
    print(message_right_rate)
    print(primary_node_error_rate)

all = ["PBFT.txt", "WPBFT.txt", "IWPBFT.txt"]
for path in all:

    calc_high_rate(path)
    # calc_low_rate(path)
    # calc_rate_with_error(path)

