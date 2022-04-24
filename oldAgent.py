from base import (BaseAgent, action_dict, move,
                  set_timeout, after_timeout, TIMEOUT)

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

    @set_timeout(TIMEOUT, after_timeout)
    def get_action(self, game_state):
        """
        # Step 1. figure out what is accessible
        obs = self.observe(game_state)
        avai_actions = self.get_avai_actions(game_state)
        goal = self.env.get_goals()[self.name]

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
        
        if self.env.env_name == 'small':
            if self.name == 'p1':
                best_action = actionP1[game_state]
            else:
                best_action = actionP2[game_state]
        """
        best_action = action_dict['right']
        return best_action


actionP1 = {
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

actionP2 = {
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
