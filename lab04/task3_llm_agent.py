import asyncio
import json
from dataclasses import dataclass
from typing import List, Dict, Any, Literal, Optional
from agents import Agent, Runner, RunConfig, RunResult, function_tool
from openai import AsyncOpenAI
from agents import OpenAIProvider

# API配置
BASE_URL = "https://api.chatfire.cn/v1"
API_KEY = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"

# 创建OpenAI Provider
provider = OpenAIProvider(
    openai_client=AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY),
    use_responses=False,
)

# 定义DSL输出格式
@dataclass
class UseCaseDiagram:
    name: str
    actors: List[Dict[str, Any]]
    use_cases: List[Dict[str, Any]]

@dataclass
class SystemSequenceDiagram:
    name: str
    actor: str
    messages: List[Dict[str, Any]]

@dataclass
class ConceptClassDiagram:
    classes: List[Dict[str, Any]]
    relationships: List[Dict[str, Any]]

@dataclass
class RequirementsModel:
    use_case_diagram: UseCaseDiagram
    system_sequence_diagrams: List[SystemSequenceDiagram]
    concept_class_diagram: ConceptClassDiagram

# 定义外部工具
@function_tool
def get_cocome_requirements() -> str:
    """获取CoCoME系统需求"""
    return """
CoCoME是一个超市管理系统，主要包含以下功能：

角色：
1. 收银员(Cashier)：负责开关收银台和结算商品
2. 店长(StoreManager)：负责商品采购、价格设置以及开关店铺
3. 系统管理员(Administrator)：负责管理系统信息，包括店铺信息、收银台信息、收银员信息、商品信息、商品目录信息和供应商信息
4. 顾客(Customer)：可以浏览商品、将商品添加到购物车、结账和退货
5. 供应商(Supplier)：接受采购订单和推荐新商品

主要用例：
1. 处理销售(processSale)：收银员结算商品
2. 开关收银台(openCashDesk, closeCashDesk)：收银员开关收银台
3. 订购商品(orderProducts)：店长下采购订单
4. 接收订购商品(receiveOrderedProduct)：店长接收采购的商品
5. 查看库存报告(showStockReports)：店长查看库存报告
6. 更改价格(changePrice)：店长更改商品价格
7. 列出供应商(listSuppliers)：店长查看所有供应商
8. 开关店铺(openStore, closeStore)：店长开关店铺
9. 管理店铺(manageStore)：管理员管理店铺信息
10. 管理商品目录(manageProductCatalog)：管理员管理商品目录
11. 管理收银台(manageCashDesk)：管理员管理收银台信息
12. 管理收银员(manageCashier)：管理员管理收银员信息
13. 管理商品(manageItem)：管理员管理商品信息
14. 管理供应商(manageSupplier)：管理员管理供应商信息
15. 浏览商品(browseProducts)：顾客浏览商品
16. 添加商品到购物车(addProductsToCart)：顾客添加商品到购物车
17. 结账(checkOut)：顾客结账
18. 退货(returnProducts)：顾客退货
19. 接受采购订单(acceptPurchaseOrder)：供应商接受采购订单
20. 推荐新商品(recommendNewProducts)：供应商推荐新商品
21. 管理退货(manageReturn)：管理员管理退货
22. 管理监控状态(manageSurveillance)：管理员管理监控状态
23. 分析销售数据(analyzeSalesData)：管理员分析销售数据
"""

@function_tool
def save_model(model_json: str) -> str:
    """保存模型到文件"""
    try:
        model_data = json.loads(model_json)
        with open("task3_result.json", "w", encoding="utf-8") as f:
            json.dump(model_data, f, ensure_ascii=False, indent=2)
        return "模型已成功保存到task3_result.json"
    except Exception as e:
        return f"保存模型失败: {str(e)}"

# 定义Agent
requirements_analyzer = Agent(
    name="requirements_analyzer",
    model="gpt-4o",
    instructions="""
你是一个需求分析专家，负责分析系统需求并提取关键信息。
你的任务是分析CoCoME超市系统的需求，并提取所有角色、用例以及它们之间的关系。
请使用get_cocome_requirements工具获取系统需求。
输出应该包含所有角色及其描述，以及所有用例及其描述。
""",
    tools=[get_cocome_requirements],
)

use_case_modeler = Agent(
    name="use_case_modeler",
    model="gpt-4o",
    instructions="""
你是一个用例建模专家，负责创建系统的用例图。
基于需求分析结果，创建一个完整的用例图，包含所有角色、用例以及它们之间的关系（include, extend）。
输出应该是一个JSON格式的用例图，包含以下结构：
{
    "name": "系统名称",
    "actors": [
        {"name": "角色名称", "description": "角色描述"}
    ],
    "use_cases": [
        {"name": "用例名称", "description": "用例描述", "actor": "角色名称", "includes": ["包含的用例"], "extends": ["扩展的用例"]}
    ]
}
""",
)

sequence_diagram_modeler = Agent(
    name="sequence_diagram_modeler",
    model="gpt-4o",
    instructions="""
你是一个系统顺序图建模专家，负责创建系统的系统顺序图。
基于用例图，为主要用例创建系统顺序图，展示用户与系统的交互。
至少为以下用例创建系统顺序图：processSale, checkOut, returnProducts, manageReturn, acceptPurchaseOrder。
输出应该是一个JSON格式的系统顺序图列表，每个系统顺序图包含以下结构：
{
    "name": "顺序图名称",
    "actor": "角色名称",
    "messages": [
        {"type": "call", "from": "发送者", "to": "接收者", "message": "消息内容"},
        {"type": "return", "from": "发送者", "to": "接收者", "message": "返回内容"}
    ]
}
""",
)

class_diagram_modeler = Agent(
    name="class_diagram_modeler",
    model="gpt-4o",
    instructions="""
你是一个概念类图建模专家，负责创建系统的概念类图。
基于需求分析结果和用例图，识别系统中的主要类、属性、操作和关系。
输出应该是一个JSON格式的概念类图，包含以下结构：
{
    "classes": [
        {"name": "类名", "attributes": ["属性1", "属性2"], "operations": ["操作1", "操作2"]}
    ],
    "relationships": [
        {"type": "关系类型", "from": "源类", "to": "目标类", "multiplicity": "多重性"}
    ]
}
关系类型包括：association（关联）, aggregation（聚合）, composition（组合）, generalization（泛化）, dependency（依赖）
""",
)

model_integrator = Agent(
    name="model_integrator",
    model="gpt-4o",
    instructions="""
你是一个模型集成专家，负责将各个模型集成为一个完整的需求模型。
将用例图、系统顺序图和概念类图集成为一个完整的需求模型。
确保模型之间的一致性，如用例图中的角色和用例与系统顺序图中的角色和消息一致。
使用save_model工具保存最终模型。
输出应该是一个JSON格式的需求模型，包含以下结构：
{
    "use_case_diagram": {
        "name": "系统名称",
        "actors": [...],
        "use_cases": [...]
    },
    "system_sequence_diagrams": [...],
    "concept_class_diagram": {
        "classes": [...],
        "relationships": [...]
    }
}
""",
    tools=[save_model],
)

model_evaluator = Agent(
    name="model_evaluator",
    model="gpt-4o",
    instructions="""
你是一个模型评估专家，负责评估需求模型的质量。
评估模型的完整性、一致性和正确性。
检查是否所有需求都被正确建模，是否存在遗漏或错误。
提供改进建议。
输出评估结果，包括模型的优点、缺点和改进建议。
评估结果的格式为：
{
    "score": "pass/needs_improvement/fail",
    "feedback": "详细的评估意见",
    "improvement_suggestions": ["改进建议1", "改进建议2"]
}
""",
)

# 定义工作流
async def main():
    print("开始基于LLM Agent的智能化需求建模...")
    
    # 步骤1：需求分析
    print("步骤1：需求分析...")
    requirements_result = await Runner.run(
        requirements_analyzer,
        input="请分析CoCoME超市系统的需求",
        run_config=RunConfig(model_provider=provider)
    )
    requirements_output = requirements_result.final_output
    print("需求分析完成")
    
    # 步骤2：用例建模
    print("步骤2：用例建模...")
    use_case_result = await Runner.run(
        use_case_modeler,
        input=f"基于以下需求分析结果，创建用例图：\n{requirements_output}",
        run_config=RunConfig(model_provider=provider)
    )
    use_case_output = use_case_result.final_output
    print("用例建模完成")
    
    # 步骤3：系统顺序图建模
    print("步骤3：系统顺序图建模...")
    sequence_diagram_result = await Runner.run(
        sequence_diagram_modeler,
        input=f"基于以下用例图，创建系统顺序图：\n{use_case_output}",
        run_config=RunConfig(model_provider=provider)
    )
    sequence_diagram_output = sequence_diagram_result.final_output
    print("系统顺序图建模完成")
    
    # 步骤4：概念类图建模
    print("步骤4：概念类图建模...")
    class_diagram_result = await Runner.run(
        class_diagram_modeler,
        input=f"基于以下需求分析和用例图，创建概念类图：\n需求分析：{requirements_output}\n用例图：{use_case_output}",
        run_config=RunConfig(model_provider=provider)
    )
    class_diagram_output = class_diagram_result.final_output
    print("概念类图建模完成")
    
    # 步骤5：模型集成
    print("步骤5：模型集成...")
    integrator_result = await Runner.run(
        model_integrator,
        input=f"请集成以下模型：\n用例图：{use_case_output}\n系统顺序图：{sequence_diagram_output}\n概念类图：{class_diagram_output}",
        run_config=RunConfig(model_provider=provider)
    )
    integrated_model = integrator_result.final_output
    print("模型集成完成")
    
    # 步骤6：模型评估
    print("步骤6：模型评估...")
    evaluation_result = await Runner.run(
        model_evaluator,
        input=f"请评估以下需求模型：\n{integrated_model}",
        run_config=RunConfig(model_provider=provider)
    )
    evaluation = evaluation_result.final_output
    print("模型评估完成")
    
    print("任务3完成")
    return evaluation

if __name__ == "__main__":
    asyncio.run(main()) 