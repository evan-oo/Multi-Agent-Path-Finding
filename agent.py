from base import (BaseAgent, action_dict, move, TIMEOUT)
from func_timeout import func_set_timeout
import json, pickle
import numpy as np

##################################################################################
# Here is a demo agent.                                                          #
# You can implement any helper functions.                                        #
# You must not remove the set_timeout restriction.                               #
# You can start your code any where but only the get_action() will be evaluated. #
##################################################################################

class MyAgent(BaseAgent):
    def get_avai_actions(self, game_state):
        avai_actions = []
        for action in action_dict:
            fake_action_profile = dict()
            for name in game_state:
                if name == self.name:
                    fake_action_profile[name] = action
                else:
                    fake_action_profile[name] = 'nil'
            succ_state = self.env.transition(game_state, fake_action_profile)
            if succ_state:
                avai_actions.append(action)
        return avai_actions
    @func_set_timeout(TIMEOUT)
    def get_action(self, game_state):
        
        # Step 1. figure out what is accessible
        obs = self.observe(game_state)
        avai_actions = self.get_avai_actions(game_state)
        goal = self.env.get_goals()[self.name]
        """
        # Step 2. production system or any rule-based system
        min_dist = 999999
        best_action = None
        for action in avai_actions:
            succ = move(obs[0], action)
            if succ in obs[1:]:
                continue
            else:
                dist = (goal[0] - succ[0]) ** 2 + (goal[1] - succ[1]) ** 2
                if dist <= min_dist:
                    min_dist = dist
                    best_action = action
        # TODO: you may want to start here
        # Feel free erase all the demo code above
        """
        print(f'game_state: {game_state}')
        global p1_changed
        
        if self.env.env_name == "small":
            
            action = {
                'p1': small_p1[game_state['p1']],
                'p2': small_p2[game_state['p2']]
                }
            if self.name == 'p1':
                # Reset p1_changed
                p1_changed = False
            
            # if p1 has changed to avoid conflict, p2 no need change
            if conflict_check(game_state, action) and (not p1_changed):
                action = conflict_avoid(game_state, action, avai_actions, self.name)
                
            best_action = action[self.name]
            
        elif self.env.env_name == 'medium':
            action = {
                'p1': medium_p1[game_state['p1']],
                'p2': medium_p2[game_state['p2']]
                }
            if self.name == 'p1':
                # Reset p1_changed
                p1_changed = False
            
            # if p1 has changed to avoid conflict, p2 no need change
            if conflict_check(game_state, action) and (not p1_changed):
                action = conflict_avoid(game_state, action, avai_actions, self.name)
                
            best_action = action[self.name]
        elif self.env.env_name == 'large':
            search_large = get_large_data()
            if search_large[self.name].get(game_state[self.name]):
                best_action = search_large[self.name][game_state[self.name]]
                
            
            
            #best_action = action[self.name]
        
        return best_action

    def large_get_action(self, game_state, data):
        # Step 1. figure out what is accessible
        #obs = self.observe(game_state)
        avai_actions = self.get_avai_actions(game_state)
        goal = self.env.get_goals()[self.name]
        print(f'game_state: {game_state}')
        if self.env.env_name == 'large':
            if self.name == 'p1':
                if data.get(game_state['p1']):
                    if np.random.rand() > 0.2:
                        best_action = data[game_state['p1']]
                    else:
                        #best_action = avai_actions[np.random.randint(len(avai_actions))]
                        best_action = random_move(game_state['p1'], goal, avai_actions)
                else:
                    #best_action = avai_actions[np.random.randint(len(avai_actions))]
                    best_action = random_move(game_state['p1'], goal, avai_actions)
            elif self.name == 'p2':
                if data.get(game_state['p2']):
                    if np.random.rand() > 0.2:
                        best_action = data[game_state['p2']]
                    else:
                        #best_action = avai_actions[np.random.randint(len(avai_actions))]
                        best_action = random_move(game_state['p2'], goal, avai_actions)
                else:
                    #best_action = avai_actions[np.random.randint(len(avai_actions))]
                    best_action = random_move(game_state['p2'], goal, avai_actions)
    
        return best_action
    
    
def random_move(state, goal, avai_actions):
    #state = game_state[self.name]
    #goal = self.env.get_goals()[self.name]
    #avai_actions = self.get_avai_actions(game_state)
    avai_actions.remove('nil')
    diff_x = goal[0] - state[0]
    x = 'nil'
    if diff_x > 0:
        x = 'down'
    else:
        x = 'up'
    diff_y = goal[1] - state[1]
    y = 'nil'
    if diff_y > 0:
        y = 'right'
    else:
        y = 'left'
    r = np.random.rand()
    action = 'nil'
    if abs(diff_x) > abs(diff_y):
        if (x in avai_actions) and r > 0.8:
            action = 'down' if diff_x > 0 else 'up'
        elif (y in avai_actions) and r > 0.7:
            action = 'right' if diff_y > 0 else 'left'
        else:
            action = avai_actions[np.random.randint(len(avai_actions))]
    else:
        if (y in avai_actions) and r > 0.8:
            action = 'right' if diff_y > 0 else 'left'
        elif (x in avai_actions) and r > 0.7:
            action = 'down' if diff_x > 0 else 'up'
        else:
            action = avai_actions[np.random.randint(len(avai_actions))]
    return action
            

def conflict_check(game_state, action):
    # game_state dict and action dict
    # go to same block 
    if move(game_state['p1'],action['p1']) == move(game_state['p2'],action['p2']):
       return True
    #swap block
    if move(game_state['p1'],action['p1']) == game_state['p2'] and move(game_state['p2'], action['p2']) == game_state['p1']:
       return True
    return False

def conflict_avoid(game_state, action, avai_actions, name):
    #game_state dict, action dict, agent's avai_actions and agent's name
    # return alternative action with no conflict or return same action
    global p1_changed
    temp_action = action
    for act in avai_actions:
        if(act == 'nil'):
            continue
        temp_action[name] = act
        if (not conflict_check(game_state, temp_action)):
            if (name =='p1'):
                p1_changed = True
            return temp_action
    return action
    


def deadlock_check(prev, curr):
    # previous state and current state
    if prev == curr:
        return True
    
def get_large_data():
    try:
        
        f = open('./data/search_large.txt', 'rb')
        data = pickle.load(f)
        f.close()
        return data
    except:
        print("Export went wrong")


small_p1 = {
    (1,1): 'right',
    (1,2): 'right',
    (1,3): 'right',
    (1,4): 'right',
    (1,5): 'down',
    (1,6): 'left',
    (2,1): 'up',
    (2,2): 'right',
    (2,3): 'right',
    (2,4): 'right',
    (2,5): 'down',
    (2,6): 'left',
    (3,1): 'down',
    (3,2): 'right',
    (3,3): 'down',
    (3,4): 'right',
    (3,5): 'down',
    (3,6): 'left',
    (4,1): 'down',
    (4,2): 'right',
    (4,3): 'right',
    (4,4): 'right',
    (4,5): 'down',
    (4,6): 'left',
    (5,1): 'down',
    (5,2): 'down',
    (5,3): 'down',
    (5,4): 'right',
    (5,5): 'nil',
    (5,6): 'left',
    (6,1): 'right',
    (6,2): 'right',
    (6,3): 'right',
    (6,4): 'right',
    (6,5): 'up',
    (6,6): 'left'
}

small_p2 = {
    (1,1): 'right',
    (1,2): 'right',
    (1,3): 'down',
    (1,4): 'down',
    (1,5): 'left',
    (1,6): 'left',
    (2,1): 'down',
    (2,2): 'right',
    (2,3): 'down',
    (2,4): 'left',
    (2,5): 'left',
    (2,6): 'left',
    (3,1): 'right',
    (3,2): 'right',
    (3,3): 'nil',
    (3,4): 'right',
    (3,5): 'down',
    (3,6): 'left',
    (4,1): 'up',
    (4,2): 'right',
    (4,3): 'up',
    (4,4): 'left',
    (4,5): 'left',
    (4,6): 'left',
    (5,1): 'right',
    (5,2): 'right',
    (5,3): 'up',
    (5,4): 'right',
    (5,5): 'up',
    (5,6): 'left',
    (6,1): 'right',
    (6,2): 'right',
    (6,3): 'up',
    (6,4): 'left',
    (6,5): 'left',
    (6,6): 'left'
}

medium_p1 = {
    (1,1): 'down',
    (1,2): 'down',
    (1,3): 'down',
    (1,4): 'down',
    (1,5): 'down',
    (1,6): 'down',
    (1,7): 'down',
    (1,8): 'down',
    (1,9): 'down',
    (1,10): 'down',
    (1,11): 'down',
    (1,12): 'down',
    (1,13): 'down',
    (1,14): 'down',
    (1,15): 'down',
    (1,16): 'down',
    (2,1): 'down',
    (2,2): 'down',
    (2,3): 'down',
    (2,4): 'down',
    (2,5): 'left',
    (2,6): 'left',
    (2,7): 'left',
    (2,8): 'left',
    (2,9): 'left',
    (2,10): 'down',
    (2,11): 'down',
    (2,12): 'down',
    (2,13): 'down',
    (2,14): 'down',
    (2,15): 'down',
    (2,16): 'down',
    (3,1): 'down',
    (3,2): 'down',
    (3,3): 'down',
    (3,4): 'down',
    (3,5): 'left',
    (3,6): 'left',
    (3,7): 'down',
    (3,8): 'down',
    (3,9): 'down',
    (3,10): 'down',
    (3,11): 'down',
    (3,12): 'down',
    (3,13): 'down',
    (3,14): 'down',
    (3,15): 'down',
    (3,16): 'down',
    (4,1): 'down',
    (4,2): 'down',
    (4,3): 'down',
    (4,4): 'down',
    (4,5): 'left',
    (4,6): 'left',
    (4,7): 'down',
    (4,8): 'right',
    (4,9): 'right',
    (4,10): 'down',
    (4,11): 'down',
    (4,12): 'down',
    (4,13): 'down',
    (4,14): 'down',
    (4,15): 'down',
    (4,16): 'down',
    (5,1): 'down',
    (5,2): 'down',
    (5,3): 'down',
    (5,4): 'down',
    (5,5): 'left',
    (5,6): 'left',
    (5,7): 'left',
    (5,8): 'right',
    (5,9): 'right',
    (5,10): 'down',
    (5,11): 'down',
    (5,12): 'down',
    (5,13): 'down',
    (5,14): 'down',
    (5,15): 'down',
    (5,16): 'down',
    (6,1): 'down',
    (6,2): 'down',
    (6,3): 'down',
    (6,4): 'down',
    (6,5): 'down',
    (6,6): 'down',
    (6,7): 'down',
    (6,8): 'down',
    (6,9): 'down',
    (6,10): 'down',
    (6,11): 'down',
    (6,12): 'down',
    (6,13): 'down',
    (6,14): 'down',
    (6,15): 'down',
    (6,16): 'down',
    (7,1): 'down',
    (7,2): 'down',
    (7,3): 'down',
    (7,4): 'down',
    (7,5): 'down',
    (7,6): 'down',
    (7,7): 'left',
    (7,8): 'left',
    (7,9): 'left',
    (7,10): 'down',
    (7,11): 'down',
    (7,12): 'down',
    (7,13): 'down',
    (7,14): 'down',
    (7,15): 'down',
    (7,16): 'down',
    (8,1): 'down',
    (8,2): 'down',
    (8,3): 'down',
    (8,4): 'down',
    (8,5): 'down',
    (8,6): 'down',
    (8,7): 'down',
    (8,8): 'down',
    (8,9): 'down',
    (8,10): 'down',
    (8,11): 'down',
    (8,12): 'down',
    (8,13): 'down',
    (8,14): 'down',
    (8,15): 'down',
    (8,16): 'down',
    (9,1): 'right',
    (9,2): 'right',
    (9,3): 'right',
    (9,4): 'right',
    (9,5): 'right',
    (9,6): 'right',
    (9,7): 'nil',
    (9,8): 'left',
    (9,9): 'down',
    (9,10): 'down',
    (9,11): 'down',
    (9,12): 'down',
    (9,13): 'left',
    (9,14): 'left',
    (9,15): 'left',
    (9,16): 'left',
    (10,1): 'up',
    (10,2): 'up',
    (10,3): 'up',
    (10,4): 'up',
    (10,5): 'up',
    (10,6): 'up',
    (10,7): 'up',
    (10,8): 'up',
    (10,9): 'left',
    (10,10): 'left',
    (10,11): 'left',
    (10,12): 'left',
    (10,13): 'down',
    (10,14): 'up',
    (10,15): 'up',
    (10,16): 'up',
    (11,1): 'up',
    (11,2): 'up',
    (11,3): 'up',
    (11,4): 'up',
    (11,5): 'up',
    (11,6): 'up',
    (11,7): 'up',
    (11,8): 'up',
    (11,9): 'up',
    (11,10): 'up',
    (11,11): 'up',
    (11,12): 'up',
    (11,13): 'left',
    (11,14): 'left',
    (11,15): 'left',
    (11,16): 'left',
    (12,1): 'up',
    (12,2): 'up',
    (12,3): 'up',
    (12,4): 'right',
    (12,5): 'right',
    (12,6): 'up',
    (12,7): 'up',
    (12,8): 'up',
    (12,9): 'up',
    (12,10): 'up',
    (12,11): 'up',
    (12,12): 'up',
    (12,13): 'up',
    (12,14): 'up',
    (12,15): 'up',
    (12,16): 'up',
    (13,1): 'up',
    (13,2): 'up',
    (13,3): 'up',
    (13,4): 'up',
    (13,5): 'up',
    (13,6): 'up',
    (13,7): 'up',
    (13,8): 'up',
    (13,9): 'up',
    (13,10): 'up',
    (13,11): 'up',
    (13,12): 'up',
    (13,13): 'up',
    (13,14): 'up',
    (13,15): 'up',
    (13,16): 'up',
    (14,1): 'right',
    (14,2): 'right',
    (14,3): 'right',
    (14,4): 'up',
    (14,5): 'up',
    (14,6): 'up',
    (14,7): 'up',
    (14,8): 'up',
    (14,9): 'up',
    (14,10): 'up',
    (14,11): 'up',
    (14,12): 'right',
    (14,13): 'up',
    (14,14): 'up',
    (14,15): 'up',
    (14,16): 'up',
    (15,1): 'up',
    (15,2): 'up',
    (15,3): 'up',
    (15,4): 'up',
    (15,5): 'up',
    (15,6): 'up',
    (15,7): 'up',
    (15,8): 'up',
    (15,9): 'up',
    (15,10): 'up',
    (15,11): 'left',
    (15,12): 'left',
    (15,13): 'up',
    (15,14): 'up',
    (15,15): 'up',
    (15,16): 'left',
    (16,1): 'up',
    (16,2): 'up',
    (16,3): 'up',
    (16,4): 'up',
    (16,5): 'up',
    (16,6): 'right',
    (16,7): 'up',
    (16,8): 'up',
    (16,9): 'up',
    (16,10): 'up',
    (16,11): 'up',
    (16,12): 'up',
    (16,13): 'up',
    (16,14): 'up',
    (16,15): 'up',
    (16,16): 'up'
}


medium_p2 = {
    (1,1): 'down',
    (1,2): 'down',
    (1,3): 'down',
    (1,4): 'down',
    (1,5): 'down',
    (1,6): 'down',
    (1,7): 'down',
    (1,8): 'down',
    (1,9): 'down',
    (1,10): 'down',
    (1,11): 'down',
    (1,12): 'down',
    (1,13): 'down',
    (1,14): 'down',
    (1,15): 'down',
    (1,16): 'down',
    (2,1): 'down',
    (2,2): 'down',
    (2,3): 'down',
    (2,4): 'down',
    (2,5): 'down',
    (2,6): 'down',
    (2,7): 'left',
    (2,8): 'right',
    (2,9): 'right',
    (2,10): 'down',
    (2,11): 'down',
    (2,12): 'down',
    (2,13): 'down',
    (2,14): 'down',
    (2,15): 'down',
    (2,16): 'down',
    (3,1): 'down',
    (3,2): 'down',
    (3,3): 'down',
    (3,4): 'down',
    (3,5): 'down',
    (3,6): 'down',
    (3,7): 'down',
    (3,8): 'down',
    (3,9): 'down',
    (3,10): 'down',
    (3,11): 'down',
    (3,12): 'down',
    (3,13): 'left',
    (3,14): 'left',
    (3,15): 'left',
    (3,16): 'left',
    (4,1): 'down',
    (4,2): 'down',
    (4,3): 'down',
    (4,4): 'down',
    (4,5): 'down',
    (4,6): 'down',
    (4,7): 'down',
    (4,8): 'right',
    (4,9): 'down',
    (4,10): 'down',
    (4,11): 'down',
    (4,12): 'down',
    (4,13): 'down',
    (4,14): 'up',
    (4,15): 'up',
    (4,16): 'up',
    (5,1): 'right',
    (5,2): 'right',
    (5,3): 'right',
    (5,4): 'right',
    (5,5): 'right',
    (5,6): 'right',
    (5,7): 'right',
    (5,8): 'right',
    (5,9): 'nil',
    (5,10): 'left',
    (5,11): 'left',
    (5,12): 'left',
    (5,13): 'down',
    (5,14): 'down',
    (5,15): 'down',
    (5,16): 'down',
    (6,1): 'up',
    (6,2): 'up',
    (6,3): 'up',
    (6,4): 'up',
    (6,5): 'up',
    (6,6): 'up',
    (6,7): 'up',
    (6,8): 'up',
    (6,9): 'up',
    (6,10): 'up',
    (6,11): 'up',
    (6,12): 'up',
    (6,13): 'left',
    (6,14): 'left',
    (6,15): 'left',
    (6,16): 'left',
    (7,1): 'up',
    (7,2): 'up',
    (7,3): 'up',
    (7,4): 'up',
    (7,5): 'right',
    (7,6): 'right',
    (7,7): 'right',
    (7,8): 'right',
    (7,9): 'right',
    (7,10): 'up',
    (7,11): 'up',
    (7,12): 'up',
    (7,13): 'up',
    (7,14): 'up',
    (7,15): 'up',
    (7,16): 'up',
    (8,1): 'up',
    (8,2): 'up',
    (8,3): 'up',
    (8,4): 'up',
    (8,5): 'up',
    (8,6): 'up',
    (8,7): 'up',
    (8,8): 'up',
    (8,9): 'up',
    (8,10): 'up',
    (8,11): 'up',
    (8,12): 'up',
    (8,13): 'up',
    (8,14): 'up',
    (8,15): 'up',
    (8,16): 'up',
    (9,1): 'up',
    (9,2): 'up',
    (9,3): 'up',
    (9,4): 'up',
    (9,5): 'up',
    (9,6): 'up',
    (9,7): 'down',
    (9,8): 'down',
    (9,9): 'up',
    (9,10): 'up',
    (9,11): 'up',
    (9,12): 'up',
    (9,13): 'up',
    (9,14): 'up',
    (9,15): 'up',
    (9,16): 'up',
    (10,1): 'up',
    (10,2): 'up',
    (10,3): 'up',
    (10,4): 'up',
    (10,5): 'up',
    (10,6): 'up',
    (10,7): 'right',
    (10,8): 'right',
    (10,9): 'right',
    (10,10): 'up',
    (10,11): 'up',
    (10,12): 'up',
    (10,13): 'up',
    (10,14): 'up',
    (10,15): 'up',
    (10,16): 'up',
    (11,1): 'up',
    (11,2): 'up',
    (11,3): 'up',
    (11,4): 'up',
    (11,5): 'up',
    (11,6): 'up',
    (11,7): 'up',
    (11,8): 'up',
    (11,9): 'up',
    (11,10): 'up',
    (11,11): 'up',
    (11,12): 'up',
    (11,13): 'left',
    (11,14): 'up',
    (11,15): 'up',
    (11,16): 'up',
    (12,1): 'up',
    (12,2): 'up',
    (12,3): 'up',
    (12,4): 'right',
    (12,5): 'right',
    (12,6): 'up',
    (12,7): 'up',
    (12,8): 'up',
    (12,9): 'up',
    (12,10): 'up',
    (12,11): 'up',
    (12,12): 'up',
    (12,13): 'up',
    (12,14): 'up',
    (12,15): 'up',
    (12,16): 'up',
    (13,1): 'up',
    (13,2): 'up',
    (13,3): 'up',
    (13,4): 'up',
    (13,5): 'up',
    (13,6): 'up',
    (13,7): 'up',
    (13,8): 'up',
    (13,9): 'up',
    (13,10): 'up',
    (13,11): 'up',
    (13,12): 'up',
    (13,13): 'up',
    (13,14): 'up',
    (13,15): 'up',
    (13,16): 'up',
    (14,1): 'right',
    (14,2): 'right',
    (14,3): 'right',
    (14,4): 'up',
    (14,5): 'up',
    (14,6): 'up',
    (14,7): 'up',
    (14,8): 'up',
    (14,9): 'up',
    (14,10): 'up',
    (14,11): 'up',
    (14,12): 'right',
    (14,13): 'up',
    (14,14): 'up',
    (14,15): 'up',
    (14,16): 'up',
    (15,1): 'up',
    (15,2): 'up',
    (15,3): 'up',
    (15,4): 'up',
    (15,5): 'up',
    (15,6): 'up',
    (15,7): 'up',
    (15,8): 'up',
    (15,9): 'up',
    (15,10): 'up',
    (15,11): 'left',
    (15,12): 'left',
    (15,13): 'up',
    (15,14): 'up',
    (15,15): 'up',
    (15,16): 'left',
    (16,1): 'up',
    (16,2): 'up',
    (16,3): 'up',
    (16,4): 'up',
    (16,5): 'up',
    (16,6): 'right',
    (16,7): 'up',
    (16,8): 'up',
    (16,9): 'up',
    (16,10): 'up',
    (16,11): 'up',
    (16,12): 'up',
    (16,13): 'up',
    (16,14): 'up',
    (16,15): 'up',
    (16,16): 'up'
}