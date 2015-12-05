import swing_copter
import math
import random
from state_tree_node import StateTreeNode
import copy

num_charges = 20
max_charge_depth = 10000

def select(node):
	if node.visits == 0:
		return node
	score = 0
	for i in range(len(node.children)):
		if node.children[i] == None:
			continue
		if node.children[i].visits == 0:
			return node.children[i]
		new_score = selectfn(node.children[i])
		if new_score > score:
			score = new_score
			result = node.children[i]
	return select(result)

def selectfn(node):
	return node.utility + math.sqrt( 2 * math.log(node.parent.visits) / node.visits )

def expand(root, node):
	actions = node.game_state.get_actions()
	for i in range(len(actions)):
		new_state = node.game_state.get_next_state(actions[i], create_walls=False)
		new_node = StateTreeNode(new_state, parent = node)
		node.children[i] = new_node

def get_reward(game_state):
	return game_state.frame_count

def simulate(node):
	state = copy.deepcopy(node.game_state)
	depth = 0
	while not state.game_over and depth < max_charge_depth:
		action = random.random() > 0.5
		state.update_state(action, create_walls=False)
		depth += 1
	return get_reward(state)

def backpropagate(node, score):
	node.visits += 1
	node.utility += score
	if node.parent:
		backpropagate(node.parent, score)

def get_MCTS_action(game_state):
	actions = game_state.get_actions()
	if len(actions) == 1:
		return actions[0]

	root = StateTreeNode(game_state)
	for i in xrange(num_charges):
		node = select(root)
		expand(root, node)
		score = simulate(node)
		backpropagate(node, score)

	best_action = None
	best_score = -1
	for i in range(len(root.children)):
		action_score = root.children[i].utility / root.children[i].visits
		if action_score > best_score:
			best_action = actions[i]
			best_score = action_score
	return best_action