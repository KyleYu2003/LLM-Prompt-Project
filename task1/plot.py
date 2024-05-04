import json
import matplotlib.pyplot as plt

with open("./data/case_study_result.json", encoding='utf-8') as f:
    data = json.load(f)

# 提取 x 和 y 数据
x = [key for key in data.keys()]
y = list(data.values())

# 创建柱状图
plt.figure(figsize=(8, 6))
plt.bar(x, y, color='gray')

plt.ylim(48, 50)

# 添加标题和标签
plt.title('Average Performance for Different Reward')
plt.xlabel('Reward')
plt.ylabel('Performance as number of correct answer')

# 显示图形
plt.show()