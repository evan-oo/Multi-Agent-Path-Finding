from base import (BaseAgent, action_dict, move, TIMEOUT)
from func_timeout import func_set_timeout
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
        if self.env.env_name == "small":
            if self.name == "p1":
                best_action = small_p1[game_state['p1']]
            else:
                best_action = small_p2[game_state['p2']]
        
            ###
            #if action[p1] change, here need to be updated
            ###
            action = {
                'p1': small_p1[game_state['p1']],
                'p2': small_p2[game_state['p2']]
                }
            if self.name == 'p1':
                # Reset p1_changed
                global p1_changed
                p1_changed = False
            
            # if p1 has changed to avoid conflict, p2 no need change
            if conflict_check(game_state, action) and (not p1_changed):
                action = conflict_avoid(game_state, action, avai_actions, self.name)
                
            best_action = action[self.name]
            
            #best_action = 'right'
        return best_action

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
    temp_action = action
    for act in avai_actions:
        temp_action[name] = act
        if (not conflict_check(game_state, temp_action)):
            if (name =='p1'):
                global p1_changed 
                p1_changed = True
            return temp_action
    return action
    


def deadlock_check(prev, curr):
    # previous state and current state
    if prev == curr:
        return True

p1_changed = False

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
