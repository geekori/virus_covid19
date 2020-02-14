NORMAL = 0   # 正常人（未感染的人）
SUSPECTED = NORMAL + 1   # 有暴露感染风险的人
LATENCY = SUSPECTED + 1  # 处于潜伏期的人
CONFIRMED = LATENCY + 1  # 已经发病的人
FREEZE = CONFIRMED + 1   # 隔离治疗的人，禁止移动
DEATH = FREEZE + 1       # 已经死亡的人

