import gym

# 建立環境，使用 render_mode 參數以便視覺化
env = gym.make("CartPole-v1", render_mode="human")
observation, info = env.reset(seed=42)

total_steps = 0  # 紀錄累計步數

# 定義固定策略函數
def fixed_policy(observation):
    # 這裡舉例一個簡單的策略：如果杆的角度小於 0，則向左移動；否則向右移動
    angle = observation[2]
    action = 0 if angle < 0 else 1
    return action

# 執行多個回合，直到達到目標步數
while True:
    env.render()  # 渲染環境（視覺化）

    action = fixed_policy(observation)  # 使用固定策略選擇動作
    observation, reward, terminated, truncated, info = env.step(action)
    total_steps += 1

    print('observation=', observation)

    # 檢查是否終止或截斷了當前回合
    if terminated or truncated:
        print(f"本回合共撐過 {total_steps} 步")
        if total_steps >= 50:
            print("達到目標步數，結束訓練。")
            break
        else:
            print("未達到目標步數，重置環境，開始新回合。")
            observation, info = env.reset()
            total_steps = 0  # 重置步數計數器，準備下一回合

env.close()  # 關閉環境
