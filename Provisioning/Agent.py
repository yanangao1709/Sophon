from Config import AgentConfig
from Provisioning import ExperienceMemory
from Provisioning import MyDQN
import torch
import torch.optim as optim
from torch.autograd import Variable
import numpy as np
import random
from Config import AgentConfig, QNConfig
import pylab


class Agent():
    def __init__(self, agent_id, LoadModel):
        self.agent_id = agent_id
        self.load_model = LoadModel
        self.obs_size = AgentConfig.obs_size
        self.action_size = AgentConfig.act_size
        self.epsilon = AgentConfig.epsilon

        # create prioritized replay memory using SumTree
        self.memory = ExperienceMemory.Memory(AgentConfig.memory_size)

        # create main model and target model
        self.model = MyDQN.MyDQN(self.obs_size, self.action_size)
        self.target_model = MyDQN.MyDQN(self.obs_size, self.action_size)
        self.optimizer = optim.Adam(self.model.parameters(), lr=AgentConfig.learning_rate)

        # initialize target model
        self.update_target_model()

        if self.load_model:
            self.model = torch.load('./save_model/cartpole_dqn')

        # 绘图
        self.losses = []
        self.times = 0
        self.times_list = []

    # after some time interval update the target model to be same with model
    def update_target_model(self):
        self.target_model.load_state_dict(self.model.state_dict())

    # get action from model using epsilon-greedy policy
    def get_action(self, state):
        actions = [0 for r in range(QNConfig.request_pool_len)]
        if np.random.rand() <= self.epsilon:
            for r in range(QNConfig.request_pool_len):
                actions[r] = random.randrange(self.action_size)
        else:
            state = torch.from_numpy(np.array(state))
            state = Variable(state).float().cpu()
            q_value = self.model(state)
            for r in range(QNConfig.request_pool_len):
                _, action = torch.max(q_value[r], 0)
                actions[r] = int(action)
        return actions

    # save sample (error,<s,a,r,s'>) to the replay memory
    def append_sample(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)

    # pick samples from prioritized replay memory (with batch_size)
    def train_model(self, done , ep):
        if self.epsilon > AgentConfig.epsilon_min:
            self.epsilon -= AgentConfig.epsilon_decay

        states, actions, rewards, next_states, dones = self.memory.sample(AgentConfig.batch_size)

        # Q function of current state
        states = torch.Tensor(states)
        states = Variable(states).float()
        pred = self.model(states)
        action_tensor = torch.tensor(actions).permute(1,0)

        # pred = torch.sum(pred.mul(Variable(one_hot_action)), dim=1)

        # Q function of next state
        next_states = torch.Tensor(next_states)
        next_states = Variable(next_states).float()
        next_pred = self.target_model(next_states)
        rewards = torch.FloatTensor(rewards)

        pred_actions = []
        pred_next_actions = []
        for r in range(QNConfig.request_pool_len):
            pred_actions.append(torch.gather(pred[r], dim=1, index=action_tensor[r].unsqueeze(-1)).squeeze())
            pred_next_actions.append(next_pred[r].max(dim=1)[0])
        pred_actions_mean = torch.mean(torch.stack(pred_actions, dim=0), dim=0)
        pred_next_actions_mean = torch.mean(torch.stack(pred_next_actions, dim=0), dim=0)

        # Q Learning: get maximum Q value at s' from target model
        target = rewards + AgentConfig.discount_factor * pred_next_actions_mean
        target = Variable(target)

        # errors = pred_actions_mean - target
        # loss = torch.tensor((errors ** 2).sum())

        self.optimizer.zero_grad()

        # MSE Loss function
        loss = (torch.nn.functional.mse_loss(pred_actions_mean, target)).mean()
        loss.backward()
        self.losses.append(loss.data)
        self.times_list.append(self.times)
        self.times += 1
        if done:
            pylab.plot(self.times_list, self.losses, 'b')
            pylab.savefig("./save_graph/loss/loss_" + str(self.agent_id) + ".png")
            pylab.close()

        # and train
        self.optimizer.step()


