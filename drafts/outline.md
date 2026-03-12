# 大纲

## Introduction

fig-teaser
修改：
1. the robot 改为 I
2. 听觉声音锥体
3. 从各个锥体冒出"I hear ..., I should ..."的思考框

## Related Work

## Dataset

table-task
跟几种任务对比，突出我们任务的挑战性和价值。

table-dataset
介绍4个难度的细节和统计性指标

fig-habitat-avh
仿真示意图，展示几个任务场景

## Method

table-definition
定义术语和符号

fig-method
修改：
1. 术语要对齐
2. ...

按感知-建图-规划的顺序介绍方法，突出我们方法的创新点和优势。

?fig-data-structure
展示各层实体的数据结构和更新方式。
算了不加了，太细节了。

## Experiments

更多中间结果

指标：要不要加入各个模块的性能指标（如声源定位误差、信息增益等）

table-performance
在L1-L4上展示我们方法和几个baseline的性能对比

table-ablation-sim

fig-qualitative-sim

table-performance-real

fig-qualitative-real

## Conclusion

---

## 随想

亮点：
社交导航对声音充耳不闻，视听导航又仅仅把声音当做目标或干扰。
社交导航需要像对待视觉一样对待声音（不仅要从视觉理解人类，还要从听觉上理解，进而做出更符合社交礼仪的行动），视听导航要考虑社交属性，不仅要把声音当做一个重要的环境线索，还要把它当做一个动态的、具有时空关联性的风险因素（要避开的虚拟墙，如谈话、脚步）。

1. 主动搜索：针对听觉感知的不确定性，利用视觉和场景语义与结构信息作为先验，进行贝叶斯推理。


静态实体锚定。也要上概率，不能一锤定音：
引入基于稀疏信念得分的锚定机制 (Sparse Belief Anchoring)，解决单帧 DoA 误差和语义特征噪声导致的“错误锚定”或“频繁闪烁”问题。
与主动搜索的 Dense Belief Map 遥相呼应。一个是针对未知位置的连续空间概率搜索，一个是针对已知实体的离散空间概率确认，构成了完整的贝叶斯视听融合体系。
