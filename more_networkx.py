from typing import Optional
import csv
from collections import deque
import networkx as nx


def get_previous_depth_node(graph:nx.Graph, node, depth_key:str) -> tuple[str, dict]:
    """Given a NetworkX graph and a particular node, find another node with a depth one less than
    the given node. It is assumd all nodes are assigned explicit data of their depth.
    graph     -- a non-directional graph created using the NetworkX package.
    node      -- a specific node which exists within the graph.
    depth_key -- a key referring to node data representing the depth of the node.
    returns   :  a tuple containing the new node found, and the data of the node.
                 if no node was found, returns a tuple of (None, {})."""
    nodes = []
    try:
        depth = graph.nodes[node][depth_key]
        nodes = [(x) for e in graph.edges(node) for x in e if x != node and graph.nodes[x][depth_key] == depth - 1]
    except KeyError:
        raise KeyError(f'Could not find node={node} in given graph, using:  graph.nodes[{repr(node)}]')
    finally:
        if nodes:
            node_name = nodes[0]
            return node_name, graph.nodes[node_name]
        return (None, {})


def get_node_sequence_by_depth(graph:nx.Graph, node, depth_key:str, halt_node:Optional[str]=None) -> list[str]:
    """Given a NetworkX graph, generate a list of nodes organised by decreasing depth. It is
    assumed that all nodes are assigned explicit data of their depth.
    Note that if a node is encountered without at least one edge to a suitable node, then the sequence
    will terminate before reaching the root node or halt_node.
    graph      -- a non-directional graph created using the NetworkX package.
    node       -- a specific node which exists within the graph, to start at.
    depth_key  -- a key referring to node data representing the depth of the node.
    halt_node  -- if not None, then the sequence will terminate early if this node is encountered.
    returns    :  a list of node names.
    """
    tmp_node = node
    node_path = [tmp_node]
    try:
        print()
        tmp_depth = graph.nodes[tmp_node][depth_key]
    except KeyError:
        raise KeyError(f'Could not find node={node} in given graph, using:  graph.nodes[{repr(node)}]')
    while tmp_depth > 0:
        tmp_node, _ = get_previous_depth_node(graph, tmp_node, depth_key)
        if tmp_node is None or halt_node is not None and tmp_node == halt_node:
            break
        tmp_depth -= 1
        node_path.append(tmp_node)
    return node_path
