import numpy as np

from base import move

###
import pickle

def export_data(name, data):
    try:
        if(name == 'p1'):
            f = open('./data/large_p1.txt', 'wb')
            pickle.dump(data, f)
            f.close()
        elif(name == 'p2'):
            f = open('./data/large_p2.txt', 'wb')
            pickle.dump(data, f)
            f.close()
    except:
        print("Export went wrong")

def update_data(name, state, act):
    global large_p1, large_p2
    try:
        if(name == 'p1'):
            large_p1[state] = act
        elif(name == 'p2'):
            large_p2[state] = act
    except:
        print("Update went wrong")


###

MAX_NUM_STEP_DICT = {
    'test': 200,
    'empty': 20,
    'small': 60 // 3,
    'medium': 120 // 3,
    'large': 1600 // 3,
}

def dict2list(d):
    return list(d.values())

def manhattanHeuristic(state, goal):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = state
    xy2 = goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


class Env():
    '''
    An environment consists of a set of speficied goals and a grid map.
    '''

    def __init__(self, goals, layout, map_name):
        self.env_name = map_name
        self.__goals = goals
        self.__layout = layout
        self.__reach_goal = np.zeros(len(goals))

    def get_goals(self):
        return self.__goals

    def get_reach_goal(self):
        return self.__reach_goal

    def is_feasible(self, curr_state, succ_state):
        '''
        Test if the successor state is feasible or not
        '''
        curr_profile = dict2list(curr_state)
        succ_profile = dict2list(succ_state)

        for pos in succ_profile:
            if pos[0] not in range(len(self.__layout)) or \
                    pos[1] not in range(len(self.__layout[0])) or \
                    self.__layout[pos] == 1:
                return False  # exceed the map

        for i in range(len(succ_profile)):
            for j in range(i + 1, len(succ_profile)):
                if succ_profile[i] == succ_profile[j]:
                    return False  # vertex collision
                elif succ_profile[i] == curr_profile[j] and \
                        succ_profile[j] == curr_profile[i]:
                    return False  # edge collision

        return True

    def transition(self, curr_state, action_profile):
        '''
        Make a transition based on the given action profile
        '''
        succ_state = dict()
        for name in self.__goals:
            succ_state[name] = move(curr_state[name],
                                    action_profile[name])

        succ_profile = dict2list(succ_state)

        # Agents go beyond the map or collide into a wall
        for pos in succ_profile:
            if pos[0] not in range(len(self.__layout)) or \
                    pos[1] not in range(len(self.__layout[0])) or \
                    self.__layout[pos] == 1:
                return None

        for i, name in enumerate(self.__goals):
            self.__reach_goal[i] = int(succ_state[name]
                                       == self.__goals[name])

        return succ_state

    def is_end(self):
        return np.all(self.__reach_goal == np.ones(len(self.__reach_goal)))


class Game():
    '''
    The main control flow of a one-shot multi-agent path finding.
    Input: a set of initial positions, a set of agents, a map, a set of goals.
    Output: path finding history, score
    '''

    def __init__(self, starts, agents, env):
        self.init_state = starts
        self.agents = agents
        self.env = env

    def run(self, max_score_p1, max_score_p2, large_p1, large_p2):
        state = self.init_state
        histry = [dict2list(state)]
        cnt = 0
        score = 0
        score_p1 = 0
        score_p2 = 0
        num = np.ones(len(self.agents))
        collision = None

        while True:
            print(f'T{cnt}: {state}')

            action_profile = dict()
            for agent in self.agents:
                try:
                    if agent.name == 'p1':
                        action = agent.large_get_action(state, large_p1)
                    elif agent.name == 'p2':
                        action = agent.large_get_action(state, large_p2)
                    
                except:
                    action = 'nil'
                print(f'{agent.name} moved: {action}')
                action_profile[agent.name] = action
                ###
                if(agent.name == 'p1'):
                    large_p1[state['p1']] = action
                elif(agent.name == 'p2'):
                    large_p2[state['p2']] = action
                ###

            succ_state = self.env.transition(state, action_profile)
            feasibility = self.env.is_feasible(state, succ_state)
            if not feasibility and collision is None:
                collision = cnt
                print('Infeasible trasition detected!')

            cnt += 1

            reach_goal = self.env.get_reach_goal()
            for i in range(len(self.agents)):
                if reach_goal[i] == 0:
                    num[i] += 1

            if np.sum(num) > MAX_NUM_STEP_DICT[self.env.env_name] * len(self.agents):
                print("Too many steps, see if you are in a dead/live lock!\n")
                score = 0
                score_p1 = -1 * manhattanHeuristic(state['p1'], (150, 125))
                score_p2 = -1 * manhattanHeuristic(state['p2'], (100, 175))
                if score_p1 > max_score_p1:
                    #export data
                    max_score_p1 = score_p1 
                    export_data('p1', large_p1)

                if score_p2 > max_score_p2:
                    max_score_p2 = score_p2
                    export_data('p2', large_p2)
                
                return histry, score, max_score_p1, max_score_p2

            histry.append(dict2list(succ_state))
            state = succ_state

            print('\t|\n\tV')
            if self.env.is_end():
                print('Goals reached!\n')
                break

        score = 100 - 100 * np.sum(num) / (MAX_NUM_STEP_DICT[self.env.env_name]
                                           * len(self.agents))

        score_p1 = 100 - 100 * num[0] / MAX_NUM_STEP_DICT[self.env.env_name]
        score_p2 = 100 - 100 * num[1] / MAX_NUM_STEP_DICT[self.env.env_name]
        if collision is not None:
            print(f'!!The earliest collision happened at T{collision}!!\n')
            score = -50

        if score_p1 > max_score_p1:
            max_score_p1 = score_p1
            export_data('p1', large_p1)

        if score_p2 > max_score_p2:
            max_score_p2 = score_p2
            export_data('p2', large_p2)


        print(num)
        return histry, score, max_score_p1, max_score_p2
