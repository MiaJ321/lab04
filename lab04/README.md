# 基于大语言模型的智能需求建模

本项目基于大语言模型实现了CoCoME超市系统的智能需求建模。

## 任务内容

### 任务1：基于纯Restful API的智能化需求建模
使用纯Restful API方式调用大语言模型，生成CoCoME系统的需求模型。
- 设计Prompt以指导模型生成需求模型
- 定义输出格式为JSON结构
- 使用Python requests库发送请求并处理响应

### 任务2：基于OpenAI SDK的智能化需求建模
使用OpenAI SDK调用大语言模型，生成CoCoME系统的需求模型。
- 使用OpenAI Python SDK简化API调用
- 与任务1使用相同的Prompt和输出格式
- 处理并保存生成的需求模型

### 任务3：基于LLM Agent的智能化需求建模
使用OpenAI Agents实现MultiAgent Workflow，通过多个专业Agent协作完成需求建模。
- 定义多个专业Agent：需求分析、用例建模、系统顺序图建模、概念类图建模、模型集成和评估
- 设计Agent之间的协作流程
- 定义DSL格式规范化输出
- 实现外部工具支持Agent工作

## 目标模型
CoCoME（Common Component Modeling Example）超市系统，包含以下主要角色和功能：
- 角色：收银员、店长、系统管理员、顾客、供应商
- 主要功能：销售处理、库存管理、商品管理、顾客服务、供应商管理等

## 输入的Prompt
每个任务中，我们设计了不同的Prompt来引导模型生成需求模型：
- 系统Prompt：指导模型扮演需求分析师角色，并定义输出格式
- 用户Prompt：提供CoCoME系统的详细需求描述

## 输出格式定义
所有任务的输出均采用JSON格式，包含以下主要部分：
- 用例图：包含角色、用例及其关系
- 系统顺序图：展示用户与系统的交互
- 概念类图：包含系统中的类、属性和关系

## MultiAgent Workflow说明
任务3中实现的MultiAgent Workflow包含以下步骤：
1. 需求分析：由requirements_analyzer分析需求并提取关键信息
2. 用例建模：由use_case_modeler创建用例图
3. 系统顺序图建模：由sequence_diagram_modeler创建系统顺序图
4. 概念类图建模：由class_diagram_modeler创建概念类图
5. 模型集成：由model_integrator将各个模型集成为完整的需求模型
6. 模型评估：由model_evaluator评估需求模型的质量

## 环境配置
- Python 3.8+
- 依赖库：
  - requests
  - openai
  - openai-agents
  
## 使用方法
1. 安装依赖：`pip install requests openai openai-agents`
2. 运行任务1：`python task1_restful_api.py`
3. 运行任务2：`python task2_openai_sdk.py`
4. 运行任务3：`python task3_llm_agent.py`