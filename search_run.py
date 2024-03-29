from agent import MyAgent
#from game import Env, Game
#from rl_game import Env, 
from game import Env
from animator import Animation

import argparse
import os
import sys
from copy import deepcopy

import numpy as np

####
from base import move
import pickle
i = 0

class Args():
    def __init__(self):
        #self.agents = ['p1', 'p2']
        self.agents = ['p2']
        self.map = 'large'
        #self.goals = {'p1': (150, 125), 'p2': (100, 175)}
        self.goals = {'p2': (100, 175)}
        self.vis = False
        self.eval = False
        self.save = None

def get_starts_rl(agents):
    # initial states for agents
    global i
    # Round Number
    if i > 1000:
        print('Program terminates')
        return None, None, None
    starts = {'p1': (96, 109), 'p2': (79, 189)}
    print(f'Round No. : {i}')
    p1_dict, p2_dict = import_data()
    i += 1
    return starts, p1_dict, p2_dict

def import_data():
    try:
        f1 = open('./data/search_large.txt', 'rb')
        search_large = pickle.load(f1)
        f1.close()
        return search_large
    except:
        print("import_data went wrong")

'''
search_large = {
    'p1':{
        (150, 125): 'nil'
    },
    'p2': {
        (100, 175): 'nil'
    }
}
'''
def search(agent, state):
    if agent.env.is_feasible(state, state):
        state_list = list()
        avai_actions = agent.get_avai_actions(state)
        avai_actions.remove('nil')
        for act in avai_actions:
            if act == 'up':
                if search_large[agent.name].get(move(state[agent.name], 'up')):
                    continue
                else:
                    search_large[agent.name][move(state[agent.name], 'up')] = 'down'
                    state_list.append(move(state[agent.name], 'up'))
            elif act == 'down':
                if search_large[agent.name].get(move(state[agent.name], 'down')):
                    continue
                else:
                    search_large[agent.name][move(state[agent.name], 'down')] = 'up'
                    state_list.append(move(state[agent.name], 'down'))
            elif act == 'left':
                if search_large[agent.name].get(move(state[agent.name], 'left')):
                    continue
                else:
                    search_large[agent.name][move(state[agent.name], 'left')] = 'right'
                    state_list.append(move(state[agent.name], 'left'))
            elif act == 'right':
                if search_large[agent.name].get(move(state[agent.name], 'right')):
                    continue
                else:
                    search_large[agent.name][move(state[agent.name], 'right')] = 'left'
                    state_list.append(move(state[agent.name], 'right'))
        #return state_list
    return state_list
                    
def export_data(data):
    try:
        f = open('./data/search_large.txt', 'wb')
        pickle.dump(data, f)
        f.close()
    except:
        print("Export went wrong")
####    


def parse_map_from_file(map_config):
    PREFIX = 'maps/'
    POSTFIX = '.map'
    if not os.path.exists(PREFIX + map_config + POSTFIX):
        raise ValueError('Map config does not exist!')
    layout = []
    with open(PREFIX + map_config + POSTFIX, 'r') as f:
        line = f.readline()
        while line:
            if line.startswith('#'):
                pass
            else:
                row = []
                for char in line:
                    if char == '.':
                        row.append(0)
                    elif char == '@':
                        row.append(1)
                    else:
                        continue
                layout.append(row)
            line = f.readline()
    return np.array(layout)


def parse_goals(goals):
    goal_dict = dict()
    for i, goal in enumerate(goals):
        goal_dict[f'p{i + 1}'] = eval(goal.replace('_', ','))
    return goal_dict


def get_args():
    """
    parser = argparse.ArgumentParser(
        description='Multi-Agent Path Finding Term Project.'
    )

    parser.add_argument('--agents', dest='agents', type=str, nargs='+',
                        help='Specify a list of agent names')
    parser.add_argument('--map', dest='map', type=str,
                        help='Specify a map')
    parser.add_argument('--goals', dest='goals', type=str, nargs='+',
                        help='Specify the goals for each agent,'
                             'e.g. 2_0 0_2')
    parser.add_argument('--vis', dest='vis', action='store_true',
                        help='Visulize the process')
    parser.add_argument('--save', dest='save', type=str,
                        help='Specify the path to save the animation vedio')
    parser.add_argument('--eval', dest='eval', action='store_true',
                        help='Do evaluation')

    args = parser.parse_args()
    """
    args = Args()
    map_name = args.map
    args.map = parse_map_from_file(args.map)

    #args.goals = parse_goals(args.goals)

    return args, map_name


def show_args(args):
    args = vars(args)
    for key in args:
        print(f'{key.upper()}:')
        print(args[key])
        print('-------------\n')


def get_starts(agents):
    starts = dict()
    for name in agents:
        char = input(f'Specify an initial position for agent {name}: ')
        if char.lower() == 'n':
            print('Program terminates')
            return None
        starts[name] = eval(char.replace(' ', ','))
    return starts

search_large = import_data()

if __name__ == '__main__':
    args, map_name = get_args()
    max_score_p1 = 0
    max_score_p2 = 0
    #search_large = import_data()
    

    if not args.eval:
        show_args(args)

        env = Env(args.goals, args.map, map_name)
        

        agents = []
        for name in args.agents:
            agents.append(MyAgent(name, deepcopy(env)))   

        for agent in agents:
            #print('fuck you') 
            state_list = search(agent, agent.env.get_goals())
            temp_list = state_list.copy()
            #print(f'temp_list: {temp_list}')
            while temp_list:
                temp_list.clear()
                for i in state_list:
                    l = search(agent,{'p2': i})
                    #print(f'l: {l}')
                    temp_list.extend(l)
                #print(f'temp_list: {temp_list}')
                state_list.clear()
                state_list = temp_list.copy()
            
        
        export_data(search_large)


        """
        starts, large_p1, large_p2 = get_starts_rl(args.agents)

        while starts:
            print('\nSTARTS:')
            print(starts)
            print('-------------\n')

            game = Game(starts, agents, deepcopy(env))
            history, score, max_score_p1, max_score_p2 = game.run(max_score_p1, max_score_p2, large_p1, large_p2)
            print(f'==> Score: {score}\n')
            print(f'==> p1 Max Score: {max_score_p1}\n')
            print(f'==> p2 Max Score: {max_score_p2}\n')

            if args.vis:
                animator = Animation(args.agents,
                                     args.map,
                                     list(starts.values()),
                                     list(args.goals.values()),
                                     history)
                animator.show()
                if args.save:
                    animator.save(file_name=f'recording/{args.save}',
                                  speed=100)

            starts, large_p1, large_p2 = get_starts_rl(args.agents)
        """
    else:
        print('error')
        """
        stdout_fd = sys.stdout
        sys.stdout = open("eval.log", "w")

        NUM_ROUNDS = {
            'test': 20,
            'empty': 10,
            'small': 10,
            'medium': 20,
            'large': 30,
        }
        env = Env(args.goals, args.map, map_name)
        agents = []
        for name in args.agents:
            agents.append(MyAgent(name, deepcopy(env)))

        num_rounds = NUM_ROUNDS[map_name]
        score_list = []
        i = 0
        while i < num_rounds:
            initials = np.random.choice(range(len(args.map)),
                                        size=(len(agents), 2),
                                        replace=False)
            # print(initials)
            invalid = False
            for pos in initials:
                # print(tuple(pos), args.map[tuple(pos)])
                if args.map[tuple(pos)] == 1:
                    invalid = True
                    break
                if map_name == 'large' and pos[0] > 110 and pos[1] < 75:
                    invalid = True
                    break
            if invalid:
                continue

            starts = dict()
            for k in range(len(agents)):
                starts[agents[k].name] = tuple(initials[k])
            game = Game(starts, agents, env)
            history, score = game.run()
            score_list.append(score)
            i += 1

        sys.stdout = stdout_fd
        print(score_list)
        print(np.mean(score_list))
        """