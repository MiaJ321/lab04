import requests
import json
import os

# API配置
BASE_URL = "https://api.chatfire.cn/v1"
API_KEY = "sk-zO8exlBicZh7nJeZn5GuC5X9SPuVrZzXoGyOW0i9BFvN62ON"

# 设计Prompt
system_prompt = """
你是一个专业的需求分析师，擅长将自然语言需求转换为UML模型。
请基于我提供的CoCoME超市系统需求，生成以下UML模型：
1. 用例图：包含所有角色和用例，以及用例之间的关系（include, extend）
2. 系统顺序图：为主要用例生成系统顺序图，展示用户与系统的交互
3. 概念类图：识别系统中的主要类、属性和关系

请以JSON格式输出结果，包含以下结构：
{
    "use_case_diagram": {
        "actors": [
            {"name": "ActorName", "description": "Actor description"}
        ],
        "use_cases": [
            {"name": "UseCaseName", "description": "UseCase description", "actor": "ActorName", "includes": [], "extends": []}
        ]
    },
    "system_sequence_diagrams": [
        {
            "name": "SSDName",
            "actor": "ActorName",
            "messages": [
                {"type": "call", "from": "Actor", "to": "System", "message": "message content"},
                {"type": "return", "from": "System", "to": "Actor", "message": "return content"}
            ]
        }
    ],
    "concept_class_diagram": {
        "classes": [
            {"name": "ClassName", "attributes": ["attribute1", "attribute2"], "operations": ["operation1", "operation2"]},
        ],
        "relationships": [
            {"type": "association", "from": "Class1", "to": "Class2", "multiplicity": "1..*"}
        ]
    }
}
"""

# CoCoME系统需求
user_prompt = """
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

请基于上述需求，生成UML模型。
"""

# 发送请求到API
def call_openai_api(system_prompt, user_prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

# 保存结果到文件
def save_result(response, filename):
    if response and 'choices' in response:
        content = response['choices'][0]['message']['content']
        
        # 尝试解析JSON
        try:
            json_content = json.loads(content)
            with open(f"{filename}.json", "w", encoding="utf-8") as f:
                json.dump(json_content, f, ensure_ascii=False, indent=2)
            print(f"结果已保存到 {filename}.json")
        except json.JSONDecodeError:
            # 如果不是有效的JSON，则保存为文本
            with open(f"{filename}.txt", "w", encoding="utf-8") as f:
                f.write(content)
            print(f"结果已保存到 {filename}.txt")
    else:
        print("没有有效的响应内容")

# 主函数
def main():
    print("开始基于Restful API的智能化需求建模...")
    response = call_openai_api(system_prompt, user_prompt)
    save_result(response, "task1_result")
    print("任务1完成")

if __name__ == "__main__":
    main() 