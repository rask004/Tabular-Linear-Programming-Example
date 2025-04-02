import csv
from collections import deque
import networkx as nx
from more_networkx import get_previous_depth_node, get_node_sequence_by_depth
import config


class LinearProblemData:
    def __init__(self):
        self.costs = {}
        self.x_params = set()
        self.y_params = set()


def get_linear_data_from_csv(filename:str, x_feature_column_name:str) -> LinearProblemData:
    data_obj = LinearProblemData()
    with open(filename) as fp:
        line = fp.readline()
    fieldnames = line.strip().split(',')
    for y in fieldnames[1:]:
        data_obj.y_params.add(y)
    with open(filename) as fp:
        reader = csv.DictReader(fp, fieldnames)
        next(reader)
        for row in reader:
            x = row[x_feature_column_name]
            data_obj.x_params.add(x)
            tmp_costs_ = {key:int(value) for key, value in row.items() if key != x_feature_column_name}
            data_obj.costs[x] = tmp_costs_
    return data_obj


def find_min_cost(linear_data: LinearProblemData) -> dict:
    X_PIVOT = 'X'
    Y_PIVOT = 'Y'
    g = nx.Graph()
    queue = deque()
    c = 1
    depth = 0
    x_params_seq = sorted(linear_data.x_params)
    y_params_seq = sorted(linear_data.y_params)
    max_depth = len(x_params_seq)
    pivot = X_PIVOT
    if len(y_params_seq) < len(x_params_seq):
        max_depth = len(y_params_seq)
        pivot = Y_PIVOT

    def get_x_y_pairs():
        if pivot == X_PIVOT:
            return ((x_params_seq[depth], y) for y in y_params_seq)
        else:
            return ((x, y_params_seq[depth]) for x in x_params_seq)

    node_name = config.START_NODE
    g.add_node(node_name, depth=depth, x=None, y=None, total_cost=0)
    
    for x, y in get_x_y_pairs():
        total_cost = linear_data.costs[x][y]
        new_name = str(c)
        node_data = {
            config.DATA_DEPTH_KEY: depth+1,
            config.DATA_X_KEY: x,
            config.DATA_Y_KEY: y,
            config.DATA_NUMERIC_KEY: total_cost
        }
        g.add_node(new_name, **node_data)
        g.add_edge(node_name, new_name)
        queue.append((new_name, depth+1, (x,), (y,), total_cost))
        c += 1

    while queue:
        #print(max_depth, queue)
        node_name, depth, used_x, used_y, total = queue.popleft()
        if depth >= max_depth:
            continue
        available_x = {x for x in x_params_seq if x not in used_x}
        available_y = {y for y in y_params_seq if y not in used_y}
        #print('   ', available_x, available_y)
        if not available_y or not available_x:
            continue
        pairs = [p for p in get_x_y_pairs()]
        for x, y in pairs:
            if not(x in available_x and y in available_y):
                continue
            new_name = str(c)
            new_total = total + linear_data.costs[x][y]
            new_used_x_ = list(used_x)
            new_used_x_.append(x)
            new_used_x_ = tuple(sorted(new_used_x_))
            new_used_y_ = list(used_y)
            new_used_y_.append(y)
            new_used_y_ = tuple(sorted(new_used_y_))
            node_data = {
                config.DATA_DEPTH_KEY: depth+1,
                config.DATA_X_KEY: x,
                config.DATA_Y_KEY: y,
                config.DATA_NUMERIC_KEY: new_total
                }   
            g.add_node(new_name, **node_data)
            g.add_edge(node_name, new_name)
            queue.append((str(c), depth + 1, new_used_x_, new_used_y_, new_total))
            c += 1

    end_nodes = [n for n in g.nodes(data=True) if n[-1][config.DATA_DEPTH_KEY] == max_depth]
    end_nodes = sorted(end_nodes, key=lambda n:n[-1][config.DATA_NUMERIC_KEY])
    min_cost_node = end_nodes[0][0]
    node_path = get_node_sequence_by_depth(g, min_cost_node, config.DATA_DEPTH_KEY, halt_node=config.START_NODE)
    results = {n[1][config.DATA_X_KEY]:n[1][config.DATA_Y_KEY] for p in node_path for n in g.nodes(data=True) if n[0] == p}
    results[config.DATA_NUMERIC_KEY] = g.nodes[min_cost_node][config.DATA_NUMERIC_KEY]
    return results


def user_interface(linear_data, result_data) -> None:
    x_params = sorted([x for x in linear_data.x_params])
    y_params = sorted([y for y in linear_data.y_params])
    print()
    print('  Linear Minimal Cost Problem')
    print('---------------------------------------------------')
    print('          |  {}  |  {}  |  {}  |  {}  |'.format(*y_params))
    print('---------------------------------------------------')
    for x_name in x_params:
        print(' {:<8} '.format(x_name), end='|')
        for y_name in y_params:
            print('  {:>5}  '.format(linear_data.costs[x_name][y_name]), end='|')
        print()
    print()
    print('Finding the lowest cost combination of each of the given things...')
    print()
    print()
    print('solution:')
    total = result_data[config.DATA_NUMERIC_KEY]
    for x in [x for x in result_data if x != config.DATA_NUMERIC_KEY]:
        y = result_data.get(x, None)
        cost = linear_data.costs[x].get(y, None)
        print('{:<8} --> {:<6}, cost = {}'.format(x, y, cost))
    print()
    print('total cost = ', total)
    print()


def main():
    linear_data = get_linear_data_from_csv(config.CSV_FILENAME, config.CSV_X_FEATURE_COLUMN)
    result_data = find_min_cost(linear_data)
    user_interface(linear_data, result_data)


if __name__=='__main__':
    main()