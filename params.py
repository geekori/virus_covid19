class Params:
    success = False

    # 初始感染人数
    original_infected_count = 50

    # 病毒传播率
    broad_rate = 0.8

    # 病毒潜伏期，14天
    virus_latency = 140

    # 医院收治响应时间
    hospital_receive_time = 10

    # 医院床位
    hospital_bed_count = 100

    # 安全距离
    safe_distance = 2

    # 平均流动意向[-3,3]   值越大，流动意向越强
    average_flow_intention = 3

    # 城市总人口数量
    city_person_count = 5000

    # 病死率
    fatality_rate = 0.02

    # 死亡时间
    dead_time = 30
    # 死亡时间方差
    dead_variance = 30

    # 城市宽度
    city_width = 1100

    # 城市高度
    city_height = 800

    # 医院宽度（需要计算获得）
    hospial_width = 0

    # 城市中心x坐标
    city_center_x = 550

    # 城市中心y坐标
    city_center_y = 400

    # 用于计算城市中每个人随机位置的scale（用于正态分布）
    person_position_scale = 200

    current_time = 1  # 当前时间

