import streamlit as st
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import sys

# ============================================
# 配置页面
# ============================================
st.set_page_config(
    page_title="DVF 数据分析平台",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# 多语言支持
# ============================================
LANGUAGES = {
    'zh': {
        'app_title': '🏠 DVF 房地产交易数据分析平台',
        'db_config': '⚙️ 数据库配置',
        'db_settings': '🔧 数据库连接设置',
        'db_tip': '💡 **提示**: 可以使用 root 用户，不需要创建 userP6',
        'host': '主机地址',
        'host_help': 'MySQL 服务器地址（localhost 表示本地连接）',
        'user': '用户名',
        'user_help': 'MySQL 用户名（可以使用 root 或其他现有用户）',
        'password': '密码',
        'password_help': 'MySQL 密码（root 用户的密码）',
        'database': '数据库名',
        'database_help': '要连接的数据库名称',
        'database_label': '数据库',
        'analysis_selection': '📊 分析问题选择',
        'select_question': '选择要查看的分析问题：',
        'select_question_label': '选择问题：',
        'db_status_check': '🔍 数据库状态检查',
        'db_connected': '✅ 数据库连接成功',
        'tip_chart': '💡 提示：点击图表可以缩放、平移和下载',
        'data_source': '数据来源',
        'view_data': '📊 查看数据',
        'data_summary': '数据摘要',
        'raw_data': '📋 查看原始数据',
        'database': '数据库',
        'rows': '行',
        # 错误信息
        'db_auth_failed': '❌ **数据库认证失败！**',
        'db_not_found': '❌ **数据库不存在！**',
        'db_connect_failed': '❌ **无法连接到 MySQL 服务器！**',
        'query_error': '❌ 查询执行错误',
        'empty_result': '⚠️ 查询返回空结果！',
        'table_empty': '表为空',
        'table_not_found': '表不存在或无法访问',
        'check_db_error': '检查数据库状态时出错',
        # 诊断步骤
        'diagnostic_steps': '🔍 诊断步骤',
        'check_mysql_service': '检查 MySQL 服务是否运行',
        'verify_connection': '验证数据库连接信息',
        'check_permissions': '检查用户权限',
        'confirm_db_created': '确认数据库已创建',
        # 可能的原因
        'possible_reasons': '可能的原因：',
        'username_password_wrong': '用户名或密码错误',
        'user_not_exists': '用户不存在',
        'no_access': '用户没有访问权限',
        'service_not_running': 'MySQL 服务未启动',
        'host_port_wrong': '主机地址或端口错误',
        # 解决方法
        'solutions': '解决方法：',
        'check_credentials': '检查用户名和密码是否正确',
        'confirm_mysql_running': '确认 MySQL 服务正在运行',
        'test_connection': '使用 MySQL Workbench 或命令行测试连接',
        'create_user': '如果需要创建用户，运行：',
        'check_service': '检查 MySQL 服务是否运行',
        'check_firewall': '检查防火墙设置',
        # 数据相关
        'data_points': '数据点数',
        'correlation': '相关系数',
        'avg_area': '平均面积',
        'avg_price': '平均价格',
        'table_exists': '表存在',
        'total_rows': '表中的总行数',
        'no_data_rows': '有数据的行数',
        'view_query': '🔍 查看查询语句',
        'possible_causes': '可能的原因：',
        'no_data_in_db': '数据库中没有数据（表是空的）',
        'data_not_imported': '数据还没有导入到数据库中',
        'table_mismatch': '表结构不匹配或表不存在',
        'solution_check_data': '检查数据库是否有数据',
        'solution_import_data': '如果没有数据，需要先运行 `create_tab.sql` 导入数据',
        # Q11 相关
        'analysis_purpose': '📊 分析目的',
        'analysis_description': '这个分析旨在探索**房产建筑面积**与**房产价值**之间的相关性关系。',
        'research_questions': '研究问题：',
        'research_q1': '面积越大的房产，价格是否越高？',
        'research_q2': '面积和价格之间是否存在线性关系？',
        'research_q3': '这种关系的强度如何？',
        'expected_results': '预期结果：',
        'expected_strong': '如果相关性强（r > 0.7）：面积是价格的主要决定因素',
        'expected_weak': '如果相关性弱（r < 0.3）：价格更多受其他因素影响（位置、房产类型、年份等）',
        'overall_correlation': '📈 整体相关性分析',
        'correlation_explanation': '🔍 相关性解释',
        'weak_correlation': '相关性较弱',
        'medium_correlation': '中等相关性',
        'strong_correlation': '强相关性',
        'what_does_this_mean': '这意味着什么？',
        'weak_explanation': '面积和价格之间的**线性关系不明显**',
        'weak_explanation2': '仅凭面积无法很好地预测价格',
        'weak_explanation3': '价格更多受其他因素影响',
        'why_horizontal': '为什么趋势线是水平的？',
        'horizontal_explanation': '当相关性很弱时，趋势线会接近数据的平均值，看起来几乎是水平的。这说明：',
        'horizontal_explanation2': '不同面积的房产价格差异很大',
        'horizontal_explanation3': '面积不是价格的主要决定因素',
        'medium_explanation': '面积和价格之间存在**一定的线性关系**',
        'medium_explanation2': '面积可以部分解释价格变化',
        'medium_explanation3': '但仍有其他重要因素影响价格',
        'strong_explanation': '面积和价格之间存在**明显的线性关系**',
        'strong_explanation2': '面积是价格的主要决定因素之一',
        'strong_explanation3': '可以用面积来预测价格（有一定准确性）',
        'by_property_type': '🏠 按房产类型分析',
        'property_type': '房产类型',
        'type_correlation_note': '不同房产类型的相关性可能不同。下面图表中不同颜色代表不同房产类型。',
        'scatter_plot': '📊 散点图',
        'overall_trendline': '整体趋势线',
        'type_trendline': '趋势线',
        'trendline_note': '不同颜色代表不同的房产类型。红色虚线是整体数据的趋势线。只为相关性较强（|r| ≥ 0.3）的类型显示单独的趋势线。',
        'trendline_note_weak': '不同颜色代表不同的房产类型。由于整体相关性较弱（|r| < 0.3），未显示趋势线。',
        'trendline_note_simple': '**红色虚线**是线性回归趋势线，显示面积和价格之间的线性关系。',
        'trendline_note_no': '由于相关性较弱（|r| < 0.3），未显示趋势线，因为线性关系不明显。',
        'correlation_coefficient': '整体相关系数 r',
        # Q1 相关
        'q1_analysis_purpose': '📊 分析目的',
        'q1_analysis_description': '这个分析旨在探索**房地产交易数量**的**时间趋势**，了解市场的活跃程度和周期性变化。',
        'q1_research_questions': '研究问题：',
        'q1_research_q1': '交易数量是否随时间增长或下降？',
        'q1_research_q2': '是否存在明显的季节性模式？',
        'q1_research_q3': '哪些月份交易最活跃？',
        'q1_expected_results': '预期结果：',
        'q1_expected_trend': '通过观察交易数量的变化趋势，可以了解房地产市场的整体活跃度和周期性规律。',
        'q1_expected_seasonal': '如果存在季节性模式，可以帮助预测未来交易量的变化。',
        'q1_key_insights': '关键洞察：',
        'q1_insight1': '交易数量的变化反映了市场供需关系和投资者信心',
        'q1_insight2': '季节性模式可能受节假日、政策调整等因素影响',
        'q1_insight3': '长期趋势可以帮助判断市场的发展方向',
        # Q1 统计相关
        'q1_statistics': '📈 数据统计',
        'q1_total_transactions': '总交易数',
        'q1_avg_per_month': '月均交易数',
        'q1_most_active_month': '最活跃月份',
        'q1_trend_chart': '📊 趋势图',
        'q1_title': 'Q1: 每月交易数量变化',
        # Q2 相关
        'q2_analysis_purpose': '📊 分析目的',
        'q2_analysis_description': '这个分析旨在了解不同**价格区间**的房产分布情况，识别市场的主要价格段。',
        'q2_research_questions': '研究问题：',
        'q2_research_q1': '哪个价格区间的交易最多？',
        'q2_research_q2': '价格分布是否呈现特定模式？',
        'q2_research_q3': '高端和低端市场的比例如何？',
        'q2_expected_results': '预期结果：',
        'q2_expected_distribution': '价格分布可以帮助识别市场的主要需求区间，了解不同价位房产的市场表现。',
        'q2_expected_segments': '通过分析价格区间分布，可以了解市场的价格结构和消费者购买力。',
        'q2_key_insights': '关键洞察：',
        'q2_insight1': '价格分布反映了市场的供需平衡和消费者购买力',
        'q2_insight2': '主要价格区间可能反映当地的经济水平和市场特征',
        'q2_insight3': '价格区间的集中度可以揭示市场的价格偏好',
        'q2_statistics': '📈 数据统计',
        'q2_total_mutations': '总交易数',
        'q2_price_ranges': '价格区间数',
        'q2_most_common_range': '最常见区间',
        'q2_avg_per_range': '区间平均交易数',
        'q2_distribution_chart': '📊 价格分布图',
        'q2_title': 'Q2: 价格区间分布',
        # Q3 相关
        'q3_analysis_purpose': '📊 分析目的',
        'q3_analysis_description': '这个分析旨在比较不同**交易类型**（如买卖、交换等）的平均价格，了解交易类型对价格的影响。',
        'q3_research_questions': '研究问题：',
        'q3_research_q1': '哪种交易类型的平均价格最高？',
        'q3_research_q2': '不同交易类型之间的价格差异有多大？',
        'q3_research_q3': '交易类型是否影响房产价值？',
        'q3_expected_results': '预期结果：',
        'q3_expected_difference': '不同交易类型的价格差异可能反映市场行为、税收政策或交易动机的差异。',
        'q3_expected_impact': '了解交易类型对价格的影响有助于理解市场机制和交易特征。',
        'q3_key_insights': '关键洞察：',
        'q3_insight1': '交易类型可能反映不同的交易动机和市场条件',
        'q3_insight2': '价格差异可能受税收政策、交易成本等因素影响',
        'q3_insight3': '某些交易类型可能更适合特定价格区间的房产',
        'q3_statistics': '📈 数据统计',
        'q3_transaction_types': '交易类型数',
        'q3_highest_avg_price': '最高平均价格',
        'q3_lowest_avg_price': '最低平均价格',
        'q3_price_difference': '价格差异',
        'q3_comparison_chart': '📊 价格对比图',
        'q3_title': 'Q3: 按交易类型的平均价格',
        # Q4 相关
        'q4_analysis_purpose': '📊 分析目的',
        'q4_analysis_description': '这个分析旨在了解市场中不同**房产类型**（公寓、别墅等）的分布比例。',
        'q4_research_questions': '研究问题：',
        'q4_research_q1': '哪种房产类型最常见？',
        'q4_research_q2': '不同类型房产的市场份额如何？',
        'q4_research_q3': '市场是否偏向某种特定类型？',
        'q4_expected_results': '预期结果：',
        'q4_expected_distribution': '房产类型的分布反映了市场需求和供应结构，有助于理解市场特征。',
        'q4_expected_market': '了解房产类型分布可以帮助识别市场的主要供应类型和需求偏好。',
        'q4_key_insights': '关键洞察：',
        'q4_insight1': '房产类型分布反映了市场需求和供应结构',
        'q4_insight2': '不同类型的比例可能受地理位置、城市规划等因素影响',
        'q4_insight3': '市场类型分布可以帮助理解当地房地产市场特征',
        'q4_statistics': '📈 数据统计',
        'q4_total_properties': '总房产数',
        'q4_property_types': '房产类型数',
        'q4_most_common_type': '最常见类型',
        'q4_distribution_chart': '📊 类型分布图',
        'q4_title': 'Q4: 房产类型分布',
        # Q5 相关
        'q5_analysis_purpose': '📊 分析目的',
        'q5_analysis_description': '这个分析旨在计算**每平方米的平均价格**，比较不同房产类型的单位价格差异。',
        'q5_research_questions': '研究问题：',
        'q5_research_q1': '哪种房产类型的单价最高？',
        'q5_research_q2': '不同类型房产的性价比如何？',
        'q5_research_q3': '单价差异是否合理？',
        'q5_expected_results': '预期结果：',
        'q5_expected_price': '单价分析可以帮助评估不同房产类型的价值，是投资决策的重要参考指标。',
        'q5_expected_comparison': '通过比较单价，可以了解不同类型房产的价值定位和投资潜力。',
        'q5_key_insights': '关键洞察：',
        'q5_insight1': '单价是评估房产价值的重要指标，反映了单位面积的价值',
        'q5_insight2': '不同房产类型的单价差异可能受位置、质量、需求等因素影响',
        'q5_insight3': '单价分析有助于理解不同类型房产的投资价值和市场定位',
        'q5_statistics': '📈 数据统计',
        'q5_property_types': '房产类型数',
        'q5_highest_price_m2': '最高单价',
        'q5_lowest_price_m2': '最低单价',
        'q5_avg_price_m2': '平均单价',
        'q5_price_comparison_chart': '📊 单价对比图',
        'q5_title': 'Q5: 每平方米价格（按类型）',
        # Q6 相关
        'q6_analysis_purpose': '📊 分析目的',
        'q6_analysis_description': '这个分析旨在分析房产的**房间数分布**，了解市场主流房型。',
        'q6_research_questions': '研究问题：',
        'q6_research_q1': '几居室的房产最常见？',
        'q6_research_q2': '房间数分布是否呈现特定模式？',
        'q6_research_q3': '市场偏好哪种房型？',
        'q6_expected_results': '预期结果：',
        'q6_expected_distribution': '房间数分布反映了市场需求和家庭结构，有助于理解购房者的偏好。',
        'q6_expected_market': '了解主流房型可以帮助理解市场的实际需求和供应结构。',
        'q6_key_insights': '关键洞察：',
        'q6_insight1': '房间数分布反映了市场需求和家庭结构',
        'q6_insight2': '不同房间数的房产可能面向不同的目标群体（单身、家庭等）',
        'q6_insight3': '主流房型可能反映当地的人口结构和生活方式',
        'q6_statistics': '📈 数据统计',
        'q6_total_properties': '总房产数',
        'q6_room_count_range': '房间数范围',
        'q6_most_common_rooms': '最常见房间数',
        'q6_avg_rooms': '平均房间数',
        'q6_distribution_chart': '📊 房间数分布图',
        'q6_title': 'Q6: 房间数分布',
        # Q7 相关
        'q7_analysis_purpose': '📊 分析目的',
        'q7_analysis_description': '这个分析旨在识别**交易量最大的城市**，了解房地产市场的热点区域。',
        'q7_research_questions': '研究问题：',
        'q7_research_q1': '哪些城市的交易最活跃？',
        'q7_research_q2': '交易量是否集中在某些城市？',
        'q7_research_q3': '城市间的交易量差异如何？',
        'q7_expected_results': '预期结果：',
        'q7_expected_ranking': '交易量排名可以帮助识别市场热点，了解不同城市的房地产活跃度。',
        'q7_expected_concentration': '交易量的集中度可能反映城市的经济活力和房地产市场的发展水平。',
        'q7_key_insights': '关键洞察：',
        'q7_insight1': '交易量排名反映了不同城市的房地产市场活跃度',
        'q7_insight2': '交易量集中的城市可能是经济中心或发展热点',
        'q7_insight3': '城市间的交易量差异可能反映经济发展水平和人口流动',
        'q7_statistics': '📈 数据统计',
        'q7_total_transactions': '总交易数',
        'q7_cities_shown': '显示城市数',
        'q7_most_active_city': '最活跃城市',
        'q7_top_city_transactions': '最高城市交易数',
        'q7_ranking_chart': '📊 城市排名图',
        'q7_title': 'Q7: 交易量Top10城市',
        # Q8 相关
        'q8_analysis_purpose': '📊 分析目的',
        'q8_analysis_description': '这个分析旨在比较不同**省份**的平均房产价格，了解地区间的价格差异。',
        'q8_research_questions': '研究问题：',
        'q8_research_q1': '哪个省份的平均价格最高？',
        'q8_research_q2': '地区间的价格差异有多大？',
        'q8_research_q3': '价格分布是否呈现地理规律？',
        'q8_expected_results': '预期结果：',
        'q8_expected_difference': '省份间的价格差异反映了经济发展水平、地理位置和市场需求的不同。',
        'q8_expected_pattern': '价格分布可能呈现明显的地理规律，如大城市价格较高。',
        'q8_key_insights': '关键洞察：',
        'q8_insight1': '省份间的价格差异反映了经济发展水平和地理位置的影响',
        'q8_insight2': '价格差异可能受城市规模、经济活力、地理位置等因素影响',
        'q8_insight3': '了解地区价格差异有助于理解房地产市场的区域特征',
        'q8_statistics': '📈 数据统计',
        'q8_departments': '省份数',
        'q8_highest_avg_price': '最高平均价格',
        'q8_lowest_avg_price': '最低平均价格',
        'q8_price_range': '价格范围',
        'q8_comparison_chart': '📊 省份价格对比图',
        'q8_title': 'Q8: 各省平均价格',
        # Q9 相关
        'q9_analysis_purpose': '📊 分析目的',
        'q9_analysis_description': '这个分析旨在分析不同**邮政编码区域**的交易量，识别高活跃度的具体区域。',
        'q9_research_questions': '研究问题：',
        'q9_research_q1': '哪些邮政编码区域的交易最频繁？',
        'q9_research_q2': '交易量是否集中在特定区域？',
        'q9_research_q3': '区域间的活跃度差异如何？',
        'q9_expected_results': '预期结果：',
        'q9_expected_analysis': '邮政编码级别的分析可以更精确地识别市场热点，了解微观市场的活跃程度。',
        'q9_expected_precision': '邮政编码分析可以提供比城市级别更细粒度的市场洞察。',
        'q9_key_insights': '关键洞察：',
        'q9_insight1': '邮政编码级别的分析可以识别具体的市场热点区域',
        'q9_insight2': '交易量集中的区域可能是商业中心、住宅区或发展新区',
        'q9_insight3': '区域活跃度差异可能反映地理位置、交通便利性等因素',
        'q9_statistics': '📈 数据统计',
        'q9_postal_codes_shown': '显示邮政编码数',
        'q9_total_transactions': '总交易数',
        'q9_most_active_code': '最活跃邮政编码',
        'q9_top_code_transactions': '最高区域交易数',
        'q9_ranking_chart': '📊 邮政编码排名图',
        'q9_title': 'Q9: 邮政编码交易量Top15',
        # Q10 相关
        'q10_analysis_purpose': '📊 分析目的',
        'q10_analysis_description': '这个分析旨在分析房产**建筑面积的分布情况**，了解市场主流面积范围。',
        'q10_research_questions': '研究问题：',
        'q10_research_q1': '哪个面积区间的房产最多？',
        'q10_research_q2': '面积分布是否呈现特定模式？',
        'q10_research_q3': '市场偏好哪种面积的房产？',
        'q10_expected_results': '预期结果：',
        'q10_expected_distribution': '面积分布反映了市场需求和购房者的实际需求，有助于理解市场特征。',
        'q10_expected_market': '了解主流面积范围可以帮助理解市场的实际需求和供应结构。',
        'q10_key_insights': '关键洞察：',
        'q10_insight1': '面积分布反映了市场需求和购房者的实际需求',
        'q10_insight2': '不同面积区间的房产可能面向不同的目标群体',
        'q10_insight3': '主流面积范围可能反映当地的生活水平和居住习惯',
        'q10_statistics': '📈 数据统计',
        'q10_total_properties': '总房产数',
        'q10_surface_ranges': '面积区间数',
        'q10_most_common_range': '最常见区间',
        'q10_avg_surface': '平均面积',
        'q10_distribution_chart': '📊 面积分布图',
        'q10_title': 'Q10: 建筑面积分布',
        # Q11 相关（Q11没有单独的title，使用通用键）
        'q11_title': 'Q11: 面积与价格相关性',
        # Q12 相关
        'q12_analysis_purpose': '📊 分析目的',
        'q12_analysis_description': '这个分析旨在比较不同**土地性质**（如住宅、商业等）的平均土地面积。',
        'q12_research_questions': '研究问题：',
        'q12_research_q1': '哪种土地性质的平均面积最大？',
        'q12_research_q2': '不同性质土地的面积差异如何？',
        'q12_research_q3': '土地性质是否影响面积大小？',
        'q12_expected_results': '预期结果：',
        'q12_expected_difference': '不同土地性质的平均面积差异反映了用途和规划的不同要求。',
        'q12_expected_usage': '了解不同土地性质的平均面积有助于理解土地利用模式和规划特征。',
        'q12_key_insights': '关键洞察：',
        'q12_insight1': '土地性质反映了不同的用途和规划要求',
        'q12_insight2': '不同性质的土地面积差异可能受规划政策、用途需求等因素影响',
        'q12_insight3': '平均面积分析有助于理解土地利用效率和规划特征',
        'q12_statistics': '📈 数据统计',
        'q12_land_types': '土地性质数',
        'q12_largest_avg_area': '最大平均面积',
        'q12_smallest_avg_area': '最小平均面积',
        'q12_area_range': '面积范围',
        'q12_comparison_chart': '📊 土地面积对比图',
        'q12_title': 'Q12: 土地性质平均面积',
        # Q13 相关
        'q13_analysis_purpose': '📊 分析目的',
        'q13_analysis_description': '这个分析旨在分析**平均价格的时间趋势**，了解市场价格的波动情况。',
        'q13_research_questions': '研究问题：',
        'q13_research_q1': '平均价格是否随时间变化？',
        'q13_research_q2': '是否存在价格上涨或下降的趋势？',
        'q13_research_q3': '价格波动是否有规律？',
        'q13_expected_results': '预期结果：',
        'q13_expected_trend': '价格趋势分析可以帮助了解市场走势，是投资和决策的重要参考。',
        'q13_expected_volatility': '价格波动可能反映市场供需变化、经济周期等因素的影响。',
        'q13_key_insights': '关键洞察：',
        'q13_insight1': '价格趋势反映了市场的供需关系和投资者预期',
        'q13_insight2': '价格波动可能受经济周期、政策调整、市场情绪等因素影响',
        'q13_insight3': '长期价格趋势可以帮助判断市场的发展方向和投资时机',
        'q13_statistics': '📈 数据统计',
        'q13_months': '月份数',
        'q13_highest_avg_price': '最高平均价格',
        'q13_lowest_avg_price': '最低平均价格',
        'q13_current_avg_price': '当前平均价格',
        'q13_trend_chart': '📊 价格趋势图',
        'q13_title': 'Q13: 月度平均价格变化',
        # Q14 相关
        'q14_analysis_purpose': '📊 分析目的',
        'q14_analysis_description': '这个分析旨在比较不同**房产类型**的价格统计（平均、最低、最高），全面了解价格分布。',
        'q14_research_questions': '研究问题：',
        'q14_research_q1': '哪种房产类型的平均价格最高？',
        'q14_research_q2': '价格范围（最低到最高）差异如何？',
        'q14_research_q3': '不同类型的价格波动性如何？',
        'q14_expected_results': '预期结果：',
        'q14_expected_comparison': '价格对比可以帮助评估不同房产类型的价值区间，了解市场的价格结构。',
        'q14_expected_range': '价格范围分析可以揭示不同类型房产的价格波动性和市场多样性。',
        'q14_key_insights': '关键洞察：',
        'q14_insight1': '价格统计反映了不同类型房产的价值定位和市场表现',
        'q14_insight2': '价格范围差异可能反映市场多样性、供需关系等因素',
        'q14_insight3': '了解价格统计有助于理解不同类型房产的投资价值和风险',
        'q14_statistics': '📈 数据统计',
        'q14_property_types': '房产类型数',
        'q14_highest_avg': '最高平均价格',
        'q14_largest_range': '最大价格范围',
        'q14_price_comparison_chart': '📊 价格对比图',
        'q14_title': 'Q14: 房产类型价格对比',
        # Q15 相关
        'q15_analysis_purpose': '📊 分析目的',
        'q15_analysis_description': '这个分析旨在对比**房屋和公寓**的价格分布，了解两种主要房产类型的价格差异。',
        'q15_research_questions': '研究问题：',
        'q15_research_q1': '房屋和公寓的价格分布有何不同？',
        'q15_research_q2': '哪种类型的价格更高？',
        'q15_research_q3': '价格分布是否呈现不同模式？',
        'q15_expected_results': '预期结果：',
        'q15_expected_comparison': '房屋和公寓的价格对比可以帮助理解不同类型房产的市场定位和价值差异。',
        'q15_expected_distribution': '价格分布模式可能反映不同类型房产的目标群体和市场特征。',
        'q15_key_insights': '关键洞察：',
        'q15_insight1': '房屋和公寓的价格分布反映了不同的市场定位和目标群体',
        'q15_insight2': '价格差异可能受位置、面积、质量、需求等因素影响',
        'q15_insight3': '了解价格分布有助于理解不同类型房产的投资价值和市场特征',
        'q15_statistics': '📈 数据统计',
        'q15_total_properties': '总房产数',
        'q15_houses': '房屋数',
        'q15_apartments': '公寓数',
        'q15_house_median': '房屋中位数价格',
        'q15_apartment_median': '公寓中位数价格',
        'q15_distribution_chart': '📊 价格分布对比图',
        'q15_title': 'Q15: 房屋vs公寓价格分布',
        # Q16 相关
        'q16_analysis_purpose': '📊 分析目的',
        'q16_analysis_description': '这个分析旨在计算**土地面积与建筑面积的比值**，了解不同城市的土地利用情况。',
        'q16_research_questions': '研究问题：',
        'q16_research_q1': '哪些城市的土地/建筑面积比最高？',
        'q16_research_q2': '比值差异反映了什么？',
        'q16_research_q3': '土地利用效率如何？',
        'q16_expected_results': '预期结果：',
        'q16_expected_ratio': '土地/建筑面积比反映了土地利用密度，比值高的地区可能有更多的土地空间。',
        'q16_expected_efficiency': '了解土地利用比例有助于理解不同城市的规划特征和开发模式。',
        'q16_key_insights': '关键洞察：',
        'q16_insight1': '土地/建筑面积比反映了土地利用密度和开发强度',
        'q16_insight2': '比值高的地区可能有更多的土地空间，适合低密度开发',
        'q16_insight3': '比值差异可能反映城市规划政策、土地供应等因素',
        'q16_statistics': '📈 数据统计',
        'q16_cities_shown': '显示城市数',
        'q16_highest_ratio': '最高比值',
        'q16_lowest_ratio': '最低比值',
        'q16_avg_ratio': '平均比值',
        'q16_ranking_chart': '📊 比值排名图',
        'q16_title': 'Q16: 土地/建筑面积比Top10',
        # Q17 相关
        'q17_analysis_purpose': '📊 分析目的',
        'q17_analysis_description': '这个分析旨在分析**每笔交易包含的房产数量**，了解交易的复杂性。',
        'q17_research_questions': '研究问题：',
        'q17_research_q1': '大多数交易包含几个房产？',
        'q17_research_q2': '单笔交易多房产的情况是否常见？',
        'q17_research_q3': '交易复杂度分布如何？',
        'q17_expected_results': '预期结果：',
        'q17_expected_complexity': '每笔交易的房产数量反映了交易的复杂程度，可能影响交易流程和价格。',
        'q17_expected_pattern': '了解交易复杂度分布有助于理解市场的交易模式和特征。',
        'q17_key_insights': '关键洞察：',
        'q17_insight1': '交易复杂度反映了市场的交易模式和特征',
        'q17_insight2': '多房产交易可能涉及批量交易、投资组合等特殊情况',
        'q17_insight3': '交易复杂度可能影响交易流程、价格谈判等因素',
        'q17_statistics': '📈 数据统计',
        'q17_total_transactions': '总交易数',
        'q17_most_common_count': '最常见房产数',
        'q17_max_properties': '单笔最大房产数',
        'q17_avg_properties': '平均房产数',
        'q17_distribution_chart': '📊 交易复杂度分布图',
        'q17_title': 'Q17: 每笔交易的房产数量',
        # Q18 相关
        'q18_analysis_purpose': '📊 分析目的',
        'q18_analysis_description': '这个分析旨在统计**有土地和无土地房产的数量**，了解不同房产类型的特征。',
        'q18_research_questions': '研究问题：',
        'q18_research_q1': '哪种房产类型更可能有土地？',
        'q18_research_q2': '有土地和无土地房产的比例如何？',
        'q18_research_q3': '土地是否影响房产类型？',
        'q18_expected_results': '预期结果：',
        'q18_expected_characteristics': '土地拥有情况反映了房产的完整性和价值，是房产特征的重要指标。',
        'q18_expected_distribution': '了解土地分布有助于理解不同类型房产的特征和市场定位。',
        'q18_key_insights': '关键洞察：',
        'q18_insight1': '土地拥有情况反映了房产的完整性和价值',
        'q18_insight2': '不同房产类型的土地拥有率可能差异很大',
        'q18_insight3': '土地是房产价值的重要组成部分，影响市场定位',
        'q18_statistics': '📈 数据统计',
        'q18_property_types': '房产类型数',
        'q18_total_with_land': '有土地总数',
        'q18_total_without_land': '无土地总数',
        'q18_land_ownership_rate': '土地拥有率',
        'q18_comparison_chart': '📊 土地拥有情况对比图',
        'q18_title': 'Q18: 有/无土地房产统计',
        # Q19 相关
        'q19_analysis_purpose': '📊 分析目的',
        'q19_analysis_description': '这个分析旨在分析**一周中不同日期的交易分布**，了解交易的时间模式。',
        'q19_research_questions': '研究问题：',
        'q19_research_q1': '一周中哪天的交易最多？',
        'q19_research_q2': '是否存在工作日和周末的差异？',
        'q19_research_q3': '交易时间是否有规律？',
        'q19_expected_results': '预期结果：',
        'q19_expected_pattern': '交易日期分布可能反映市场行为模式，如工作日交易更活跃等。',
        'q19_expected_behavior': '了解交易时间模式有助于理解市场运作规律和交易习惯。',
        'q19_key_insights': '关键洞察：',
        'q19_insight1': '交易日期分布反映了市场行为模式和工作习惯',
        'q19_insight2': '工作日和周末的交易量差异可能反映市场运作规律',
        'q19_insight3': '交易时间模式可能受法律程序、办公时间等因素影响',
        'q19_statistics': '📈 数据统计',
        'q19_total_transactions': '总交易数',
        'q19_most_active_day': '最活跃日期',
        'q19_least_active_day': '最不活跃日期',
        'q19_weekday_avg': '工作日平均',
        'q19_distribution_chart': '📊 日期分布图',
        'q19_title': 'Q19: 一周交易分布',
        # Q20 相关
        'q20_analysis_purpose': '📊 分析目的',
        'q20_analysis_description': '这个分析旨在分析**每周的交易量和交易总额**，了解市场的周度变化趋势。',
        'q20_research_questions': '研究问题：',
        'q20_research_q1': '交易量和交易总额是否同步变化？',
        'q20_research_q2': '是否存在周期性模式？',
        'q20_research_q3': '市场活跃度如何波动？',
        'q20_expected_results': '预期结果：',
        'q20_expected_analysis': '周度分析可以帮助识别市场的短期趋势和周期性规律。',
        'q20_expected_trends': '交易量和交易总额的变化趋势可以反映市场的整体活跃度和价值变化。',
        'q20_key_insights': '关键洞察：',
        'q20_insight1': '周度分析可以揭示市场的短期趋势和周期性规律',
        'q20_insight2': '交易量和交易总额的同步性反映市场的整体活跃度',
        'q20_insight3': '周期性模式可能受季节性因素、市场事件等影响',
        'q20_statistics': '📈 数据统计',
        'q20_weeks': '周数',
        'q20_total_transactions': '总交易数',
        'q20_total_volume': '总交易额',
        'q20_avg_transactions_per_week': '周均交易数',
        'q20_avg_volume_per_week': '周均交易额',
        'q20_trend_chart': '📊 周度趋势图',
        'q20_title': 'Q20: 周交易量分析',
    },
    'fr': {
        'app_title': '🏠 Plateforme d\'analyse des données DVF',
        'db_config': '⚙️ Configuration de la base de données',
        'db_settings': '🔧 Paramètres de connexion',
        'db_tip': '💡 **Astuce**: Vous pouvez utiliser l\'utilisateur root, pas besoin de créer userP6',
        'host': 'Adresse du serveur',
        'host_help': 'Adresse du serveur MySQL (localhost signifie connexion locale)',
        'user': 'Nom d\'utilisateur',
        'user_help': 'Nom d\'utilisateur MySQL (vous pouvez utiliser root ou un autre utilisateur existant)',
        'password': 'Mot de passe',
        'password_help': 'Mot de passe MySQL (mot de passe de l\'utilisateur root)',
        'database': 'Nom de la base de données',
        'database_help': 'Nom de la base de données à connecter',
        'analysis_selection': '📊 Sélection des questions d\'analyse',
        'select_question': 'Sélectionnez la question d\'analyse à visualiser :',
        'select_question_label': 'Sélectionner une question :',
        'db_status_check': '🔍 Vérification de l\'état de la base de données',
        'db_connected': '✅ Connexion à la base de données réussie',
        'tip_chart': '💡 Astuce : Cliquez sur le graphique pour zoomer, déplacer et télécharger',
        'data_source': 'Source des données',
        'view_data': '📊 Voir les données',
        'data_summary': 'Résumé des données',
        'raw_data': '📋 Voir les données brutes',
        'database': 'Base de données',
        'rows': 'lignes',
        # 错误信息
        'db_auth_failed': '❌ **Échec de l\'authentification de la base de données !**',
        'db_not_found': '❌ **Base de données introuvable !**',
        'db_connect_failed': '❌ **Impossible de se connecter au serveur MySQL !**',
        'query_error': '❌ Erreur d\'exécution de la requête',
        'empty_result': '⚠️ La requête a retourné un résultat vide !',
        'table_empty': 'table vide',
        'table_not_found': 'Table inexistante ou inaccessible',
        'check_db_error': 'Erreur lors de la vérification de l\'état de la base de données',
        # 诊断步骤
        'diagnostic_steps': '🔍 Étapes de diagnostic',
        'check_mysql_service': 'Vérifier si le service MySQL est en cours d\'exécution',
        'verify_connection': 'Vérifier les informations de connexion à la base de données',
        'check_permissions': 'Vérifier les permissions de l\'utilisateur',
        'confirm_db_created': 'Confirmer que la base de données a été créée',
        # 可能的原因
        'possible_reasons': 'Raisons possibles :',
        'username_password_wrong': 'Nom d\'utilisateur ou mot de passe incorrect',
        'user_not_exists': 'L\'utilisateur n\'existe pas',
        'no_access': 'L\'utilisateur n\'a pas les droits d\'accès',
        'service_not_running': 'Le service MySQL n\'est pas démarré',
        'host_port_wrong': 'Adresse du serveur ou port incorrect',
        # 解决方法
        'solutions': 'Solutions :',
        'check_credentials': 'Vérifier que le nom d\'utilisateur et le mot de passe sont corrects',
        'confirm_mysql_running': 'Confirmer que le service MySQL est en cours d\'exécution',
        'test_connection': 'Tester la connexion avec MySQL Workbench ou la ligne de commande',
        'create_user': 'Si vous devez créer un utilisateur, exécutez :',
        'check_service': 'Vérifier si le service MySQL est en cours d\'exécution',
        'check_firewall': 'Vérifier les paramètres du pare-feu',
        # 数据相关
        'data_points': 'Nombre de points de données',
        'correlation': 'Coefficient de corrélation',
        'avg_area': 'Surface moyenne',
        'avg_price': 'Prix moyen',
        'table_exists': 'Table existe',
        'total_rows': 'Nombre total de lignes dans la table',
        'no_data_rows': 'Nombre de lignes avec données',
        'view_query': '🔍 Voir la requête SQL',
        'possible_causes': 'Causes possibles :',
        'no_data_in_db': 'Aucune donnée dans la base de données (table vide)',
        'data_not_imported': 'Les données n\'ont pas encore été importées dans la base de données',
        'table_mismatch': 'Structure de table incompatible ou table inexistante',
        'solution_check_data': 'Vérifier s\'il y a des données dans la base de données',
        'solution_import_data': 'S\'il n\'y a pas de données, exécutez d\'abord `create_tab.sql` pour importer les données',
        # Q11 相关
        'analysis_purpose': '📊 Objectif de l\'analyse',
        'analysis_description': 'Cette analyse vise à explorer la corrélation entre la **surface bâtie** et la **valeur foncière** des biens immobiliers.',
        'research_questions': 'Questions de recherche :',
        'research_q1': 'Les biens avec une plus grande surface ont-ils un prix plus élevé ?',
        'research_q2': 'Existe-t-il une relation linéaire entre la surface et le prix ?',
        'research_q3': 'Quelle est la force de cette relation ?',
        'expected_results': 'Résultats attendus :',
        'expected_strong': 'Si la corrélation est forte (r > 0.7) : la surface est un facteur déterminant majeur du prix',
        'expected_weak': 'Si la corrélation est faible (r < 0.3) : le prix est davantage influencé par d\'autres facteurs (emplacement, type de bien, année, etc.)',
        'overall_correlation': '📈 Analyse de corrélation globale',
        'correlation_explanation': '🔍 Explication de la corrélation',
        'weak_correlation': 'Corrélation faible',
        'medium_correlation': 'Corrélation modérée',
        'strong_correlation': 'Corrélation forte',
        'what_does_this_mean': 'Qu\'est-ce que cela signifie ?',
        'weak_explanation': 'La **relation linéaire** entre la surface et le prix n\'est pas évidente',
        'weak_explanation2': 'La surface seule ne permet pas de bien prédire le prix',
        'weak_explanation3': 'Le prix est davantage influencé par d\'autres facteurs',
        'why_horizontal': 'Pourquoi la ligne de tendance est-elle horizontale ?',
        'horizontal_explanation': 'Lorsque la corrélation est très faible, la ligne de tendance se rapproche de la moyenne des données, ce qui la rend presque horizontale. Cela indique que :',
        'horizontal_explanation2': 'Les prix des biens varient considérablement pour différentes surfaces',
        'horizontal_explanation3': 'La surface n\'est pas un facteur déterminant majeur du prix',
        'medium_explanation': 'Il existe une **certaine relation linéaire** entre la surface et le prix',
        'medium_explanation2': 'La surface peut partiellement expliquer les variations de prix',
        'medium_explanation3': 'Mais d\'autres facteurs importants influencent encore le prix',
        'strong_explanation': 'Il existe une **relation linéaire évidente** entre la surface et le prix',
        'strong_explanation2': 'La surface est l\'un des facteurs déterminants majeurs du prix',
        'strong_explanation3': 'On peut utiliser la surface pour prédire le prix (avec une certaine précision)',
        'by_property_type': '🏠 Analyse par type de bien',
        'property_type': 'Type de bien',
        'type_correlation_note': 'La corrélation peut différer selon le type de bien. Dans le graphique ci-dessous, différentes couleurs représentent différents types de biens.',
        'scatter_plot': '📊 Nuage de points',
        'overall_trendline': 'Ligne de tendance globale',
        'type_trendline': 'Ligne de tendance',
        'trendline_note': 'Différentes couleurs représentent différents types de biens. La ligne rouge en pointillés est la ligne de tendance pour toutes les données. Seuls les types avec une corrélation suffisamment forte (|r| ≥ 0.3) affichent leur propre ligne de tendance.',
        'trendline_note_weak': 'Différentes couleurs représentent différents types de biens. Comme la corrélation globale est faible (|r| < 0.3), aucune ligne de tendance n\'est affichée.',
        'trendline_note_simple': 'La **ligne rouge en pointillés** est la ligne de régression linéaire, montrant la relation linéaire entre la surface et le prix.',
        'trendline_note_no': 'Comme la corrélation est faible (|r| < 0.3), aucune ligne de tendance n\'est affichée car la relation linéaire n\'est pas évidente.',
        'correlation_coefficient': 'Coefficient de corrélation global r',
        # Q1 相关
        'q1_analysis_purpose': '📊 Objectif de l\'analyse',
        'q1_analysis_description': 'Cette analyse vise à explorer les **tendances temporelles** du **nombre de transactions immobilières** pour comprendre le niveau d\'activité du marché et les variations cycliques.',
        'q1_research_questions': 'Questions de recherche :',
        'q1_research_q1': 'Le nombre de transactions augmente-t-il ou diminue-t-il dans le temps ?',
        'q1_research_q2': 'Y a-t-il des modèles saisonniers évidents ?',
        'q1_research_q3': 'Quels mois sont les plus actifs en transactions ?',
        'q1_expected_results': 'Résultats attendus :',
        'q1_expected_trend': 'L\'observation des tendances du nombre de transactions permet de comprendre l\'activité globale du marché immobilier et les régularités cycliques.',
        'q1_expected_seasonal': 'S\'il existe des modèles saisonniers, cela peut aider à prédire les variations futures du volume de transactions.',
        'q1_key_insights': 'Insights clés :',
        'q1_insight1': 'Les variations du nombre de transactions reflètent la relation offre-demande et la confiance des investisseurs',
        'q1_insight2': 'Les modèles saisonniers peuvent être influencés par les jours fériés, les ajustements politiques, etc.',
        'q1_insight3': 'Les tendances à long terme aident à juger la direction du développement du marché',
        # Q1 统计相关
        'q1_statistics': '📈 Statistiques',
        'q1_total_transactions': 'Total transactions',
        'q1_avg_per_month': 'Moyenne mensuelle',
        'q1_most_active_month': 'Mois le plus actif',
        'q1_trend_chart': '📊 Graphique de tendance',
        'q1_title': 'Q1: Évolution du nombre de mutations par mois',
        # Q2 相关
        'q2_analysis_purpose': '📊 Objectif de l\'analyse',
        'q2_analysis_description': 'Cette analyse vise à comprendre la distribution des biens immobiliers dans différentes **tranches de prix** pour identifier les segments principaux du marché.',
        'q2_research_questions': 'Questions de recherche :',
        'q2_research_q1': 'Quelle tranche de prix a le plus de transactions ?',
        'q2_research_q2': 'La distribution des prix présente-t-elle un modèle spécifique ?',
        'q2_research_q3': 'Quelle est la proportion entre marché haut de gamme et bas de gamme ?',
        'q2_expected_results': 'Résultats attendus :',
        'q2_expected_distribution': 'La distribution des prix aide à identifier les segments de demande principaux et à comprendre la performance du marché à différents niveaux de prix.',
        'q2_expected_segments': 'L\'analyse de la distribution par tranches de prix permet de comprendre la structure des prix et le pouvoir d\'achat des consommateurs.',
        'q2_key_insights': 'Insights clés :',
        'q2_insight1': 'La distribution des prix reflète l\'équilibre offre-demande et le pouvoir d\'achat des consommateurs',
        'q2_insight2': 'Les tranches de prix principales peuvent refléter le niveau économique local et les caractéristiques du marché',
        'q2_insight3': 'La concentration des tranches de prix peut révéler les préférences de prix du marché',
        'q2_statistics': '📈 Statistiques',
        'q2_total_mutations': 'Total transactions',
        'q2_price_ranges': 'Nombre de tranches',
        'q2_most_common_range': 'Tranche la plus courante',
        'q2_avg_per_range': 'Moyenne par tranche',
        'q2_distribution_chart': '📊 Graphique de distribution',
        'q2_title': 'Q2: Distribution des valeurs foncières par tranche',
        # Q3 相关
        'q3_analysis_purpose': '📊 Objectif de l\'analyse',
        'q3_analysis_description': 'Cette analyse vise à comparer les prix moyens par **type de transaction** (vente, échange, etc.) pour comprendre l\'impact du type de transaction sur le prix.',
        'q3_research_questions': 'Questions de recherche :',
        'q3_research_q1': 'Quel type de transaction a le prix moyen le plus élevé ?',
        'q3_research_q2': 'Quelle est l\'ampleur des différences de prix entre types de transactions ?',
        'q3_research_q3': 'Le type de transaction influence-t-il la valeur du bien ?',
        'q3_expected_results': 'Résultats attendus :',
        'q3_expected_difference': 'Les différences de prix entre types de transactions peuvent refléter des différences de comportement du marché, de politique fiscale ou de motivation de transaction.',
        'q3_expected_impact': 'Comprendre l\'impact du type de transaction sur le prix aide à comprendre les mécanismes du marché et les caractéristiques des transactions.',
        'q3_key_insights': 'Insights clés :',
        'q3_insight1': 'Le type de transaction peut refléter différentes motivations et conditions de marché',
        'q3_insight2': 'Les différences de prix peuvent être influencées par la politique fiscale, les coûts de transaction, etc.',
        'q3_insight3': 'Certains types de transactions peuvent être plus adaptés à des tranches de prix spécifiques',
        'q3_statistics': '📈 Statistiques',
        'q3_transaction_types': 'Nombre de types',
        'q3_highest_avg_price': 'Prix moyen le plus élevé',
        'q3_lowest_avg_price': 'Prix moyen le plus bas',
        'q3_price_difference': 'Différence de prix',
        'q3_comparison_chart': '📊 Graphique de comparaison',
        'q3_title': 'Q3: Valeur foncière moyenne par nature de mutation',
        # Q4 相关
        'q4_analysis_purpose': '📊 Objectif de l\'analyse',
        'q4_analysis_description': 'Cette analyse vise à comprendre la distribution proportionnelle des différents **types de biens** (appartements, maisons, etc.) sur le marché.',
        'q4_research_questions': 'Questions de recherche :',
        'q4_research_q1': 'Quel type de bien est le plus courant ?',
        'q4_research_q2': 'Quelle est la part de marché de chaque type de bien ?',
        'q4_research_q3': 'Le marché est-il orienté vers un type spécifique ?',
        'q4_expected_results': 'Résultats attendus :',
        'q4_expected_distribution': 'La distribution des types de biens reflète la structure de la demande et de l\'offre du marché, aidant à comprendre les caractéristiques du marché.',
        'q4_expected_market': 'Comprendre la distribution des types de biens aide à identifier les principaux types d\'offre et les préférences de demande du marché.',
        'q4_key_insights': 'Insights clés :',
        'q4_insight1': 'La distribution des types de biens reflète la structure de la demande et de l\'offre du marché',
        'q4_insight2': 'La proportion des différents types peut être influencée par l\'emplacement géographique, la planification urbaine, etc.',
        'q4_insight3': 'La distribution des types de marché aide à comprendre les caractéristiques du marché immobilier local',
        'q4_statistics': '📈 Statistiques',
        'q4_total_properties': 'Total biens',
        'q4_property_types': 'Nombre de types',
        'q4_most_common_type': 'Type le plus courant',
        'q4_distribution_chart': '📊 Graphique de distribution',
        'q4_title': 'Q4: Répartition des biens par type de local',
        # Q5 相关
        'q5_analysis_purpose': '📊 Objectif de l\'analyse',
        'q5_analysis_description': 'Cette analyse vise à calculer le **prix moyen au m²** et comparer les différences de prix unitaire entre différents types de biens.',
        'q5_research_questions': 'Questions de recherche :',
        'q5_research_q1': 'Quel type de bien a le prix unitaire le plus élevé ?',
        'q5_research_q2': 'Quel est le rapport qualité-prix des différents types de biens ?',
        'q5_research_q3': 'Les différences de prix unitaire sont-elles raisonnables ?',
        'q5_expected_results': 'Résultats attendus :',
        'q5_expected_price': 'L\'analyse du prix unitaire aide à évaluer la valeur des différents types de biens et constitue une référence importante pour les décisions d\'investissement.',
        'q5_expected_comparison': 'En comparant les prix unitaires, on peut comprendre le positionnement de valeur et le potentiel d\'investissement des différents types de biens.',
        'q5_key_insights': 'Insights clés :',
        'q5_insight1': 'Le prix unitaire est un indicateur important pour évaluer la valeur des biens, reflétant la valeur par unité de surface',
        'q5_insight2': 'Les différences de prix unitaire entre types de biens peuvent être influencées par l\'emplacement, la qualité, la demande, etc.',
        'q5_insight3': 'L\'analyse du prix unitaire aide à comprendre la valeur d\'investissement et le positionnement du marché des différents types de biens',
        'q5_statistics': '📈 Statistiques',
        'q5_property_types': 'Nombre de types',
        'q5_highest_price_m2': 'Prix unitaire le plus élevé',
        'q5_lowest_price_m2': 'Prix unitaire le plus bas',
        'q5_avg_price_m2': 'Prix unitaire moyen',
        'q5_price_comparison_chart': '📊 Graphique de comparaison des prix',
        'q5_title': 'Q5: Prix moyen au m² par type de local',
        # Q6 相关
        'q6_analysis_purpose': '📊 Objectif de l\'analyse',
        'q6_analysis_description': 'Cette analyse vise à analyser la **distribution du nombre de pièces** pour comprendre les types de logements dominants sur le marché.',
        'q6_research_questions': 'Questions de recherche :',
        'q6_research_q1': 'Combien de pièces sont les plus courantes ?',
        'q6_research_q2': 'La distribution du nombre de pièces présente-t-elle un modèle spécifique ?',
        'q6_research_q3': 'Quelle est la préférence du marché ?',
        'q6_expected_results': 'Résultats attendus :',
        'q6_expected_distribution': 'La distribution du nombre de pièces reflète la demande du marché et la structure familiale, aidant à comprendre les préférences des acheteurs.',
        'q6_expected_market': 'Comprendre les types de logements dominants aide à comprendre la demande réelle et la structure de l\'offre du marché.',
        'q6_key_insights': 'Insights clés :',
        'q6_insight1': 'La distribution du nombre de pièces reflète la demande du marché et la structure familiale',
        'q6_insight2': 'Les biens avec différents nombres de pièces peuvent cibler différents groupes (célibataires, familles, etc.)',
        'q6_insight3': 'Les types de logements dominants peuvent refléter la structure démographique et le mode de vie local',
        'q6_statistics': '📈 Statistiques',
        'q6_total_properties': 'Total biens',
        'q6_room_count_range': 'Plage de pièces',
        'q6_most_common_rooms': 'Nombre de pièces le plus courant',
        'q6_avg_rooms': 'Nombre moyen de pièces',
        'q6_distribution_chart': '📊 Graphique de distribution',
        'q6_title': 'Q6: Distribution du nombre de pièces principales',
        # Q7 相关
        'q7_analysis_purpose': '📊 Objectif de l\'analyse',
        'q7_analysis_description': 'Cette analyse vise à identifier les **villes avec le plus grand volume de transactions** pour comprendre les zones chaudes du marché immobilier.',
        'q7_research_questions': 'Questions de recherche :',
        'q7_research_q1': 'Quelles villes sont les plus actives en transactions ?',
        'q7_research_q2': 'Les transactions sont-elles concentrées dans certaines villes ?',
        'q7_research_q3': 'Quelle est la différence de volume entre les villes ?',
        'q7_expected_results': 'Résultats attendus :',
        'q7_expected_ranking': 'Le classement du volume de transactions aide à identifier les points chauds du marché et à comprendre l\'activité immobilière de différentes villes.',
        'q7_expected_concentration': 'La concentration du volume de transactions peut refléter la vitalité économique et le niveau de développement du marché immobilier des villes.',
        'q7_key_insights': 'Insights clés :',
        'q7_insight1': 'Le classement du volume de transactions reflète l\'activité du marché immobilier de différentes villes',
        'q7_insight2': 'Les villes avec une concentration élevée de transactions peuvent être des centres économiques ou des points chauds de développement',
        'q7_insight3': 'Les différences de volume entre villes peuvent refléter le niveau de développement économique et la mobilité de la population',
        'q7_statistics': '📈 Statistiques',
        'q7_total_transactions': 'Total transactions',
        'q7_cities_shown': 'Nombre de villes affichées',
        'q7_most_active_city': 'Ville la plus active',
        'q7_top_city_transactions': 'Transactions de la ville en tête',
        'q7_ranking_chart': '📊 Graphique de classement',
        'q7_title': 'Q7: Top 10 des communes par nombre de transactions',
        # Q8 相关
        'q8_analysis_purpose': '📊 Objectif de l\'analyse',
        'q8_analysis_description': 'Cette analyse vise à comparer les prix moyens des biens immobiliers par **département** pour comprendre les différences de prix entre régions.',
        'q8_research_questions': 'Questions de recherche :',
        'q8_research_q1': 'Quel département a le prix moyen le plus élevé ?',
        'q8_research_q2': 'Quelle est l\'ampleur des différences de prix entre régions ?',
        'q8_research_q3': 'La distribution des prix présente-t-elle une régularité géographique ?',
        'q8_expected_results': 'Résultats attendus :',
        'q8_expected_difference': 'Les différences de prix entre départements reflètent les différents niveaux de développement économique, emplacements géographiques et demandes du marché.',
        'q8_expected_pattern': 'La distribution des prix peut présenter des régularités géographiques évidentes, comme des prix plus élevés dans les grandes villes.',
        'q8_key_insights': 'Insights clés :',
        'q8_insight1': 'Les différences de prix entre départements reflètent l\'influence du niveau de développement économique et de l\'emplacement géographique',
        'q8_insight2': 'Les différences de prix peuvent être influencées par la taille de la ville, la vitalité économique, l\'emplacement géographique, etc.',
        'q8_insight3': 'Comprendre les différences de prix régionales aide à comprendre les caractéristiques régionales du marché immobilier',
        'q8_statistics': '📈 Statistiques',
        'q8_departments': 'Nombre de départements',
        'q8_highest_avg_price': 'Prix moyen le plus élevé',
        'q8_lowest_avg_price': 'Prix moyen le plus bas',
        'q8_price_range': 'Plage de prix',
        'q8_comparison_chart': '📊 Graphique de comparaison',
        'q8_title': 'Q8: Valeur foncière moyenne par département',
        # Q9 相关
        'q9_analysis_purpose': '📊 Objectif de l\'analyse',
        'q9_analysis_description': 'Cette analyse vise à analyser le volume de transactions par **code postal** pour identifier les zones spécifiques à forte activité.',
        'q9_research_questions': 'Questions de recherche :',
        'q9_research_q1': 'Quels codes postaux ont les transactions les plus fréquentes ?',
        'q9_research_q2': 'Les transactions sont-elles concentrées dans des zones spécifiques ?',
        'q9_research_q3': 'Quelle est la différence d\'activité entre les zones ?',
        'q9_expected_results': 'Résultats attendus :',
        'q9_expected_analysis': 'L\'analyse au niveau du code postal peut identifier plus précisément les points chauds du marché et comprendre l\'activité des micro-marchés.',
        'q9_expected_precision': 'L\'analyse par code postal peut fournir des insights de marché plus granulaires qu\'au niveau de la ville.',
        'q9_key_insights': 'Insights clés :',
        'q9_insight1': 'L\'analyse au niveau du code postal peut identifier des zones spécifiques de points chauds du marché',
        'q9_insight2': 'Les zones avec une concentration élevée de transactions peuvent être des centres commerciaux, des zones résidentielles ou de nouveaux quartiers en développement',
        'q9_insight3': 'Les différences d\'activité entre zones peuvent refléter des facteurs tels que l\'emplacement géographique, la commodité des transports, etc.',
        'q9_statistics': '📈 Statistiques',
        'q9_postal_codes_shown': 'Nombre de codes postaux affichés',
        'q9_total_transactions': 'Total transactions',
        'q9_most_active_code': 'Code postal le plus actif',
        'q9_top_code_transactions': 'Transactions de la zone en tête',
        'q9_ranking_chart': '📊 Graphique de classement',
        'q9_title': 'Q9: Top 15 des codes postaux par nombre de transactions',
        # Q10 相关
        'q10_analysis_purpose': '📊 Objectif de l\'analyse',
        'q10_analysis_description': 'Cette analyse vise à analyser la **distribution des surfaces bâties** pour comprendre les gammes de surface dominantes sur le marché.',
        'q10_research_questions': 'Questions de recherche :',
        'q10_research_q1': 'Quelle tranche de surface a le plus de biens ?',
        'q10_research_q2': 'La distribution des surfaces présente-t-elle un modèle spécifique ?',
        'q10_research_q3': 'Quelle surface le marché préfère-t-il ?',
        'q10_expected_results': 'Résultats attendus :',
        'q10_expected_distribution': 'La distribution des surfaces reflète la demande du marché et les besoins réels des acheteurs, aidant à comprendre les caractéristiques du marché.',
        'q10_expected_market': 'Comprendre les gammes de surface dominantes aide à comprendre la demande réelle et la structure de l\'offre du marché.',
        'q10_key_insights': 'Insights clés :',
        'q10_insight1': 'La distribution des surfaces reflète la demande du marché et les besoins réels des acheteurs',
        'q10_insight2': 'Les biens dans différentes tranches de surface peuvent cibler différents groupes cibles',
        'q10_insight3': 'Les gammes de surface dominantes peuvent refléter le niveau de vie local et les habitudes de vie',
        'q10_statistics': '📈 Statistiques',
        'q10_total_properties': 'Total biens',
        'q10_surface_ranges': 'Nombre de tranches',
        'q10_most_common_range': 'Tranche la plus courante',
        'q10_avg_surface': 'Surface moyenne',
        'q10_distribution_chart': '📊 Graphique de distribution',
        'q10_title': 'Q10: Distribution des surfaces bâties',
        # Q11 相关
        'q11_title': 'Q11: Corrélation surface bâtie vs valeur foncière',
        # Q12 相关
        'q12_analysis_purpose': '📊 Objectif de l\'analyse',
        'q12_analysis_description': 'Cette analyse vise à comparer les surfaces moyennes des terrains par **nature de culture** (résidentiel, commercial, etc.).',
        'q12_research_questions': 'Questions de recherche :',
        'q12_research_q1': 'Quelle nature de culture a la surface moyenne la plus grande ?',
        'q12_research_q2': 'Quelle est la différence de surface entre les différentes natures ?',
        'q12_research_q3': 'La nature de culture influence-t-elle la taille de la surface ?',
        'q12_expected_results': 'Résultats attendus :',
        'q12_expected_difference': 'Les différences de surface moyenne entre natures de culture reflètent les différents besoins d\'utilisation et de planification.',
        'q12_expected_usage': 'Comprendre les surfaces moyennes par nature de culture aide à comprendre les modèles d\'utilisation des terres et les caractéristiques de planification.',
        'q12_key_insights': 'Insights clés :',
        'q12_insight1': 'La nature de culture reflète différents usages et exigences de planification',
        'q12_insight2': 'Les différences de surface entre natures peuvent être influencées par les politiques de planification, les besoins d\'usage, etc.',
        'q12_insight3': 'L\'analyse de la surface moyenne aide à comprendre l\'efficacité d\'utilisation des terres et les caractéristiques de planification',
        'q12_statistics': '📈 Statistiques',
        'q12_land_types': 'Nombre de natures',
        'q12_largest_avg_area': 'Surface moyenne la plus grande',
        'q12_smallest_avg_area': 'Surface moyenne la plus petite',
        'q12_area_range': 'Plage de surface',
        'q12_comparison_chart': '📊 Graphique de comparaison',
        'q12_title': 'Q12: Surface terrain moyenne par nature de culture',
        # Q13 相关
        'q13_analysis_purpose': '📊 Objectif de l\'analyse',
        'q13_analysis_description': 'Cette analyse vise à analyser les **tendances temporelles des prix moyens** pour comprendre les fluctuations du marché.',
        'q13_research_questions': 'Questions de recherche :',
        'q13_research_q1': 'Le prix moyen change-t-il dans le temps ?',
        'q13_research_q2': 'Y a-t-il une tendance à la hausse ou à la baisse des prix ?',
        'q13_research_q3': 'Les fluctuations de prix ont-elles une régularité ?',
        'q13_expected_results': 'Résultats attendus :',
        'q13_expected_trend': 'L\'analyse des tendances de prix aide à comprendre l\'évolution du marché et constitue une référence importante pour l\'investissement et les décisions.',
        'q13_expected_volatility': 'Les fluctuations de prix peuvent refléter l\'influence de changements d\'offre-demande, de cycles économiques et d\'autres facteurs.',
        'q13_key_insights': 'Insights clés :',
        'q13_insight1': 'Les tendances de prix reflètent la relation offre-demande et les attentes des investisseurs',
        'q13_insight2': 'Les fluctuations de prix peuvent être influencées par les cycles économiques, les ajustements politiques, la sentiment du marché, etc.',
        'q13_insight3': 'Les tendances de prix à long terme aident à juger la direction du développement du marché et le timing d\'investissement',
        'q13_statistics': '📈 Statistiques',
        'q13_months': 'Nombre de mois',
        'q13_highest_avg_price': 'Prix moyen le plus élevé',
        'q13_lowest_avg_price': 'Prix moyen le plus bas',
        'q13_current_avg_price': 'Prix moyen actuel',
        'q13_trend_chart': '📊 Graphique de tendance',
        'q13_title': 'Q13: Évolution du prix moyen mensuel',
        # Q14 相关
        'q14_analysis_purpose': '📊 Objectif de l\'analyse',
        'q14_analysis_description': 'Cette analyse vise à comparer les statistiques de prix (moyen, minimum, maximum) par **type de bien** pour comprendre globalement la distribution des prix.',
        'q14_research_questions': 'Questions de recherche :',
        'q14_research_q1': 'Quel type de bien a le prix moyen le plus élevé ?',
        'q14_research_q2': 'Quelle est la différence de fourchette de prix (minimum à maximum) ?',
        'q14_research_q3': 'Quelle est la volatilité des prix par type ?',
        'q14_expected_results': 'Résultats attendus :',
        'q14_expected_comparison': 'La comparaison des prix aide à évaluer les fourchettes de valeur des différents types de biens et à comprendre la structure des prix du marché.',
        'q14_expected_range': 'L\'analyse de la fourchette de prix peut révéler la volatilité des prix et la diversité du marché pour différents types de biens.',
        'q14_key_insights': 'Insights clés :',
        'q14_insight1': 'Les statistiques de prix reflètent le positionnement de valeur et la performance du marché des différents types de biens',
        'q14_insight2': 'Les différences de fourchette de prix peuvent refléter la diversité du marché, la relation offre-demande et d\'autres facteurs',
        'q14_insight3': 'Comprendre les statistiques de prix aide à comprendre la valeur d\'investissement et les risques des différents types de biens',
        'q14_statistics': '📈 Statistiques',
        'q14_property_types': 'Nombre de types',
        'q14_highest_avg': 'Prix moyen le plus élevé',
        'q14_largest_range': 'Fourchette de prix la plus large',
        'q14_price_comparison_chart': '📊 Graphique de comparaison',
        'q14_title': 'Q14: Comparaison des prix par type de bien',
        # Q15 相关
        'q15_analysis_purpose': '📊 Objectif de l\'analyse',
        'q15_analysis_description': 'Cette analyse vise à comparer la distribution des prix des **maisons et des appartements** pour comprendre les différences de prix entre les deux principaux types de biens.',
        'q15_research_questions': 'Questions de recherche :',
        'q15_research_q1': 'Quelle est la différence de distribution des prix entre maisons et appartements ?',
        'q15_research_q2': 'Quel type a le prix le plus élevé ?',
        'q15_research_q3': 'Les distributions de prix présentent-elles des modèles différents ?',
        'q15_expected_results': 'Résultats attendus :',
        'q15_expected_comparison': 'La comparaison des prix des maisons et des appartements aide à comprendre le positionnement du marché et les différences de valeur entre différents types de biens.',
        'q15_expected_distribution': 'Les modèles de distribution des prix peuvent refléter les groupes cibles et les caractéristiques du marché des différents types de biens.',
        'q15_key_insights': 'Insights clés :',
        'q15_insight1': 'La distribution des prix des maisons et des appartements reflète différents positionnements de marché et groupes cibles',
        'q15_insight2': 'Les différences de prix peuvent être influencées par l\'emplacement, la surface, la qualité, la demande et d\'autres facteurs',
        'q15_insight3': 'Comprendre la distribution des prix aide à comprendre la valeur d\'investissement et les caractéristiques du marché des différents types de biens',
        'q15_statistics': '📈 Statistiques',
        'q15_total_properties': 'Total biens',
        'q15_houses': 'Nombre de maisons',
        'q15_apartments': 'Nombre d\'appartements',
        'q15_house_median': 'Prix médian des maisons',
        'q15_apartment_median': 'Prix médian des appartements',
        'q15_distribution_chart': '📊 Graphique de distribution',
        'q15_title': 'Q15: Distribution des prix - Maisons vs Appartements',
        # Q16 相关
        'q16_analysis_purpose': '📊 Objectif de l\'analyse',
        'q16_analysis_description': 'Cette analyse vise à calculer le **ratio entre surface de terrain et surface bâtie** pour comprendre l\'utilisation des terres dans différentes villes.',
        'q16_research_questions': 'Questions de recherche :',
        'q16_research_q1': 'Quelles villes ont le ratio terrain/bâti le plus élevé ?',
        'q16_research_q2': 'Que reflètent les différences de ratio ?',
        'q16_research_q3': 'Quelle est l\'efficacité d\'utilisation des terres ?',
        'q16_expected_results': 'Résultats attendus :',
        'q16_expected_ratio': 'Le ratio terrain/bâti reflète la densité d\'utilisation des terres, les zones avec un ratio élevé peuvent avoir plus d\'espace de terrain.',
        'q16_expected_efficiency': 'Comprendre les ratios d\'utilisation des terres aide à comprendre les caractéristiques de planification et les modèles de développement de différentes villes.',
        'q16_key_insights': 'Insights clés :',
        'q16_insight1': 'Le ratio terrain/bâti reflète la densité d\'utilisation des terres et l\'intensité de développement',
        'q16_insight2': 'Les zones avec un ratio élevé peuvent avoir plus d\'espace de terrain, adaptées au développement à faible densité',
        'q16_insight3': 'Les différences de ratio peuvent refléter les politiques de planification urbaine, l\'approvisionnement en terres et d\'autres facteurs',
        'q16_statistics': '📈 Statistiques',
        'q16_cities_shown': 'Nombre de villes affichées',
        'q16_highest_ratio': 'Ratio le plus élevé',
        'q16_lowest_ratio': 'Ratio le plus bas',
        'q16_avg_ratio': 'Ratio moyen',
        'q16_ranking_chart': '📊 Graphique de classement',
        'q16_title': 'Q16: Ratio surface terrain/surface bâtie par commune',
        # Q17 相关
        'q17_analysis_purpose': '📊 Objectif de l\'analyse',
        'q17_analysis_description': 'Cette analyse vise à analyser le **nombre de biens par transaction** pour comprendre la complexité des transactions.',
        'q17_research_questions': 'Questions de recherche :',
        'q17_research_q1': 'Combien de biens contient la plupart des transactions ?',
        'q17_research_q2': 'Les transactions multi-biens sont-elles courantes ?',
        'q17_research_q3': 'Quelle est la distribution de la complexité des transactions ?',
        'q17_expected_results': 'Résultats attendus :',
        'q17_expected_complexity': 'Le nombre de biens par transaction reflète le degré de complexité de la transaction, ce qui peut affecter le processus et le prix de la transaction.',
        'q17_expected_pattern': 'Comprendre la distribution de la complexité des transactions aide à comprendre les modèles et caractéristiques des transactions du marché.',
        'q17_key_insights': 'Insights clés :',
        'q17_insight1': 'La complexité des transactions reflète les modèles et caractéristiques des transactions du marché',
        'q17_insight2': 'Les transactions multi-biens peuvent impliquer des transactions groupées, des portefeuilles d\'investissement et d\'autres situations spéciales',
        'q17_insight3': 'La complexité des transactions peut affecter le processus de transaction, la négociation des prix et d\'autres facteurs',
        'q17_statistics': '📈 Statistiques',
        'q17_total_transactions': 'Total transactions',
        'q17_most_common_count': 'Nombre de biens le plus courant',
        'q17_max_properties': 'Nombre maximum de biens par transaction',
        'q17_avg_properties': 'Nombre moyen de biens',
        'q17_distribution_chart': '📊 Graphique de distribution',
        'q17_title': 'Q17: Nombre de biens par transaction',
        # Q18 相关
        'q18_analysis_purpose': '📊 Objectif de l\'analyse',
        'q18_analysis_description': 'Cette analyse vise à statistiquer le **nombre de biens avec et sans terrain** pour comprendre les caractéristiques des différents types de biens.',
        'q18_research_questions': 'Questions de recherche :',
        'q18_research_q1': 'Quel type de bien est plus susceptible d\'avoir un terrain ?',
        'q18_research_q2': 'Quelle est la proportion entre biens avec et sans terrain ?',
        'q18_research_q3': 'Le terrain influence-t-il le type de bien ?',
        'q18_expected_results': 'Résultats attendus :',
        'q18_expected_characteristics': 'La possession de terrain reflète l\'intégralité et la valeur du bien, c\'est un indicateur important des caractéristiques du bien.',
        'q18_expected_distribution': 'Comprendre la distribution des terrains aide à comprendre les caractéristiques et le positionnement du marché des différents types de biens.',
        'q18_key_insights': 'Insights clés :',
        'q18_insight1': 'La possession de terrain reflète l\'intégralité et la valeur du bien',
        'q18_insight2': 'Le taux de possession de terrain peut varier considérablement selon le type de bien',
        'q18_insight3': 'Le terrain est une composante importante de la valeur du bien, influençant le positionnement du marché',
        'q18_statistics': '📈 Statistiques',
        'q18_property_types': 'Nombre de types',
        'q18_total_with_land': 'Total avec terrain',
        'q18_total_without_land': 'Total sans terrain',
        'q18_land_ownership_rate': 'Taux de possession de terrain',
        'q18_comparison_chart': '📊 Graphique de comparaison',
        'q18_title': 'Q18: Biens avec/sans terrain par type',
        # Q19 相关
        'q19_analysis_purpose': '📊 Objectif de l\'analyse',
        'q19_analysis_description': 'Cette analyse vise à analyser la **distribution des transactions par jour de la semaine** pour comprendre les modèles temporels des transactions.',
        'q19_research_questions': 'Questions de recherche :',
        'q19_research_q1': 'Quel jour de la semaine a le plus de transactions ?',
        'q19_research_q2': 'Y a-t-il une différence entre jours ouvrables et week-end ?',
        'q19_research_q3': 'Le temps des transactions a-t-il une régularité ?',
        'q19_expected_results': 'Résultats attendus :',
        'q19_expected_pattern': 'La distribution des dates de transaction peut refléter les modèles de comportement du marché, comme une activité plus élevée les jours ouvrables.',
        'q19_expected_behavior': 'Comprendre les modèles temporels des transactions aide à comprendre les régularités de fonctionnement du marché et les habitudes de transaction.',
        'q19_key_insights': 'Insights clés :',
        'q19_insight1': 'La distribution des dates de transaction reflète les modèles de comportement du marché et les habitudes de travail',
        'q19_insight2': 'Les différences de volume de transactions entre jours ouvrables et week-end peuvent refléter les régularités de fonctionnement du marché',
        'q19_insight3': 'Les modèles temporels des transactions peuvent être influencés par les procédures légales, les heures de bureau et d\'autres facteurs',
        'q19_statistics': '📈 Statistiques',
        'q19_total_transactions': 'Total transactions',
        'q19_most_active_day': 'Jour le plus actif',
        'q19_least_active_day': 'Jour le moins actif',
        'q19_weekday_avg': 'Moyenne des jours ouvrables',
        'q19_distribution_chart': '📊 Graphique de distribution',
        'q19_title': 'Q19: Transactions par jour de la semaine',
        # Q20 相关
        'q20_analysis_purpose': '📊 Objectif de l\'analyse',
        'q20_analysis_description': 'Cette analyse vise à analyser le **volume et le montant total des transactions par semaine** pour comprendre les tendances de changement hebdomadaire du marché.',
        'q20_research_questions': 'Questions de recherche :',
        'q20_research_q1': 'Le volume et le montant total des transactions changent-ils de manière synchrone ?',
        'q20_research_q2': 'Y a-t-il des modèles cycliques ?',
        'q20_research_q3': 'Comment l\'activité du marché fluctue-t-elle ?',
        'q20_expected_results': 'Résultats attendus :',
        'q20_expected_analysis': 'L\'analyse hebdomadaire aide à identifier les tendances à court terme et les régularités cycliques du marché.',
        'q20_expected_trends': 'Les tendances de changement du volume et du montant total des transactions peuvent refléter l\'activité globale et les changements de valeur du marché.',
        'q20_key_insights': 'Insights clés :',
        'q20_insight1': 'L\'analyse hebdomadaire peut révéler les tendances à court terme et les régularités cycliques du marché',
        'q20_insight2': 'La synchronisation du volume et du montant total des transactions reflète l\'activité globale du marché',
        'q20_insight3': 'Les modèles cycliques peuvent être influencés par des facteurs saisonniers, des événements du marché, etc.',
        'q20_statistics': '📈 Statistiques',
        'q20_weeks': 'Nombre de semaines',
        'q20_total_transactions': 'Total transactions',
        'q20_total_volume': 'Volume total',
        'q20_avg_transactions_per_week': 'Moyenne de transactions par semaine',
        'q20_avg_volume_per_week': 'Volume moyen par semaine',
        'q20_trend_chart': '📊 Graphique de tendance',
        'q20_title': 'Q20: Évolution du volume de ventes par semaine',
    },
    'en': {
        'app_title': '🏠 DVF Real Estate Transaction Data Analysis Platform',
        'db_config': '⚙️ Database Configuration',
        'db_settings': '🔧 Database Connection Settings',
        'db_tip': '💡 **Tip**: You can use the root user, no need to create userP6',
        'host': 'Host Address',
        'host_help': 'MySQL server address (localhost means local connection)',
        'user': 'Username',
        'user_help': 'MySQL username (you can use root or other existing user)',
        'password': 'Password',
        'password_help': 'MySQL password (root user password)',
        'database': 'Database Name',
        'database_help': 'Name of the database to connect to',
        'database_label': 'Database',
        'analysis_selection': '📊 Analysis Question Selection',
        'select_question': 'Select the analysis question to view:',
        'select_question_label': 'Select Question:',
        'db_status_check': '🔍 Database Status Check',
        'db_connected': '✅ Database connection successful',
        'tip_chart': '💡 Tip: Click on the chart to zoom, pan, and download',
        'data_source': 'Data Source',
        'view_data': '📊 View Data',
        'data_summary': 'Data Summary',
        'raw_data': '📋 View Raw Data',
        'database': 'Database',
        'rows': 'rows',
        # Error messages
        'db_auth_failed': '❌ **Database authentication failed!**',
        'db_not_found': '❌ **Database not found!**',
        'db_connect_failed': '❌ **Unable to connect to MySQL server!**',
        'query_error': '❌ Query execution error',
        'empty_result': '⚠️ Query returned empty result!',
        'table_empty': 'Table is empty',
        'table_not_found': 'Table does not exist or is inaccessible',
        'check_db_error': 'Error checking database status',
        # Diagnostic steps
        'diagnostic_steps': '🔍 Diagnostic Steps',
        'check_mysql_service': 'Check if MySQL service is running',
        'verify_connection': 'Verify database connection information',
        'check_permissions': 'Check user permissions',
        'confirm_db_created': 'Confirm database has been created',
        # Possible reasons
        'possible_reasons': 'Possible reasons:',
        'username_password_wrong': 'Username or password is incorrect',
        'user_not_exists': 'User does not exist',
        'no_access': 'User does not have access rights',
        'service_not_running': 'MySQL service is not started',
        'host_port_wrong': 'Host address or port is incorrect',
        # Solutions
        'solutions': 'Solutions:',
        'check_credentials': 'Check if username and password are correct',
        'confirm_mysql_running': 'Confirm MySQL service is running',
        'test_connection': 'Test connection with MySQL Workbench or command line',
        'create_user': 'If you need to create a user, run:',
        'check_service': 'Check if MySQL service is running',
        'check_firewall': 'Check firewall settings',
        # Data related
        'data_points': 'Data Points',
        'correlation': 'Correlation Coefficient',
        'avg_area': 'Average Area',
        'avg_price': 'Average Price',
        'table_exists': 'Table exists',
        'total_rows': 'Total rows in table',
        'no_data_rows': 'Number of rows with data',
        'view_query': '🔍 View Query',
        'possible_causes': 'Possible causes:',
        'no_data_in_db': 'No data in database (table is empty)',
        'data_not_imported': 'Data has not been imported into the database yet',
        'table_mismatch': 'Table structure mismatch or table does not exist',
        'solution_check_data': 'Check if there is data in the database',
        'solution_import_data': 'If there is no data, first run `create_tab.sql` to import data',
        # Q1 相关
        'q1_analysis_purpose': '📊 Analysis Purpose',
        'q1_analysis_description': 'This analysis aims to explore the **temporal trends** of **real estate transaction volumes** to understand market activity and cyclical changes.',
        'q1_research_questions': 'Research Questions:',
        'q1_research_q1': 'Does the number of transactions increase or decrease over time?',
        'q1_research_q2': 'Are there obvious seasonal patterns?',
        'q1_research_q3': 'Which months are most active in transactions?',
        'q1_expected_results': 'Expected Results:',
        'q1_expected_trend': 'By observing the trends in transaction volumes, we can understand the overall activity and cyclical patterns of the real estate market.',
        'q1_expected_seasonal': 'If seasonal patterns exist, they can help predict future changes in transaction volumes.',
        'q1_key_insights': 'Key Insights:',
        'q1_insight1': 'Changes in transaction volumes reflect market supply-demand relationships and investor confidence',
        'q1_insight2': 'Seasonal patterns may be influenced by holidays, policy adjustments, and other factors',
        'q1_insight3': 'Long-term trends can help judge the direction of market development',
        'q1_statistics': '📈 Statistics',
        'q1_total_transactions': 'Total Transactions',
        'q1_avg_per_month': 'Monthly Average',
        'q1_most_active_month': 'Most Active Month',
        'q1_trend_chart': '📊 Trend Chart',
        'q1_title': 'Q1: Monthly Transaction Volume Evolution',
        # Q2 相关
        'q2_analysis_purpose': '📊 Analysis Purpose',
        'q2_analysis_description': 'This analysis aims to understand the distribution of properties across different **price ranges** to identify the main price segments of the market.',
        'q2_research_questions': 'Research Questions:',
        'q2_research_q1': 'Which price range has the most transactions?',
        'q2_research_q2': 'Does the price distribution show a specific pattern?',
        'q2_research_q3': 'What is the proportion between high-end and low-end markets?',
        'q2_expected_results': 'Expected Results:',
        'q2_expected_distribution': 'Price distribution can help identify the main demand segments and understand market performance at different price levels.',
        'q2_expected_segments': 'By analyzing price range distribution, we can understand the market price structure and consumer purchasing power.',
        'q2_key_insights': 'Key Insights:',
        'q2_insight1': 'Price distribution reflects market supply-demand balance and consumer purchasing power',
        'q2_insight2': 'Main price ranges may reflect local economic levels and market characteristics',
        'q2_insight3': 'Price range concentration can reveal market price preferences',
        'q2_statistics': '📈 Statistics',
        'q2_total_mutations': 'Total Transactions',
        'q2_price_ranges': 'Number of Ranges',
        'q2_most_common_range': 'Most Common Range',
        'q2_avg_per_range': 'Average per Range',
        'q2_distribution_chart': '📊 Distribution Chart',
        'q2_title': 'Q2: Price Range Distribution',
        # Q3 相关
        'q3_analysis_purpose': '📊 Analysis Purpose',
        'q3_analysis_description': 'This analysis aims to compare average prices across different **transaction types** (such as sale, exchange, etc.) to understand the impact of transaction type on price.',
        'q3_research_questions': 'Research Questions:',
        'q3_research_q1': 'Which transaction type has the highest average price?',
        'q3_research_q2': 'How large are the price differences between different transaction types?',
        'q3_research_q3': 'Does transaction type affect property value?',
        'q3_expected_results': 'Expected Results:',
        'q3_expected_difference': 'Price differences between transaction types may reflect differences in market behavior, tax policies, or transaction motivations.',
        'q3_expected_impact': 'Understanding the impact of transaction type on price helps understand market mechanisms and transaction characteristics.',
        'q3_key_insights': 'Key Insights:',
        'q3_insight1': 'Transaction types may reflect different transaction motivations and market conditions',
        'q3_insight2': 'Price differences may be influenced by tax policies, transaction costs, and other factors',
        'q3_insight3': 'Certain transaction types may be more suitable for properties in specific price ranges',
        'q3_statistics': '📈 Statistics',
        'q3_transaction_types': 'Number of Types',
        'q3_highest_avg_price': 'Highest Average Price',
        'q3_lowest_avg_price': 'Lowest Average Price',
        'q3_price_difference': 'Price Difference',
        'q3_comparison_chart': '📊 Comparison Chart',
        'q3_title': 'Q3: Average Price by Transaction Type',
        # Q4 相关
        'q4_analysis_purpose': '📊 Analysis Purpose',
        'q4_analysis_description': 'This analysis aims to understand the proportional distribution of different **property types** (apartments, houses, etc.) in the market.',
        'q4_research_questions': 'Research Questions:',
        'q4_research_q1': 'Which property type is most common?',
        'q4_research_q2': 'What is the market share of different property types?',
        'q4_research_q3': 'Is the market biased towards a specific type?',
        'q4_expected_results': 'Expected Results:',
        'q4_expected_distribution': 'Property type distribution reflects market demand and supply structure, helping to understand market characteristics.',
        'q4_expected_market': 'Understanding property type distribution can help identify the main supply types and demand preferences in the market.',
        'q4_key_insights': 'Key Insights:',
        'q4_insight1': 'Property type distribution reflects market demand and supply structure',
        'q4_insight2': 'The proportion of different types may be influenced by geographical location, urban planning, and other factors',
        'q4_insight3': 'Market type distribution can help understand local real estate market characteristics',
        'q4_statistics': '📈 Statistics',
        'q4_total_properties': 'Total Properties',
        'q4_property_types': 'Number of Types',
        'q4_most_common_type': 'Most Common Type',
        'q4_distribution_chart': '📊 Distribution Chart',
        'q4_title': 'Q4: Property Type Distribution',
        # Q5 相关
        'q5_analysis_purpose': '📊 Analysis Purpose',
        'q5_analysis_description': 'This analysis aims to calculate the **average price per square meter** and compare unit price differences across different property types.',
        'q5_research_questions': 'Research Questions:',
        'q5_research_q1': 'Which property type has the highest unit price?',
        'q5_research_q2': 'What is the price-performance ratio of different property types?',
        'q5_research_q3': 'Are unit price differences reasonable?',
        'q5_expected_results': 'Expected Results:',
        'q5_expected_price': 'Unit price analysis can help evaluate the value of different property types and is an important reference indicator for investment decisions.',
        'q5_expected_comparison': 'By comparing unit prices, we can understand the value positioning and investment potential of different property types.',
        'q5_key_insights': 'Key Insights:',
        'q5_insight1': 'Unit price is an important indicator for evaluating property value, reflecting the value per unit area',
        'q5_insight2': 'Unit price differences between property types may be influenced by location, quality, demand, and other factors',
        'q5_insight3': 'Unit price analysis helps understand the investment value and market positioning of different property types',
        'q5_statistics': '📈 Statistics',
        'q5_property_types': 'Number of Types',
        'q5_highest_price_m2': 'Highest Unit Price',
        'q5_lowest_price_m2': 'Lowest Unit Price',
        'q5_avg_price_m2': 'Average Unit Price',
        'q5_price_comparison_chart': '📊 Price Comparison Chart',
        'q5_title': 'Q5: Price per Square Meter (by Type)',
        # Q6 相关
        'q6_analysis_purpose': '📊 Analysis Purpose',
        'q6_analysis_description': 'This analysis aims to analyze the **distribution of room numbers** in properties to understand the dominant housing types in the market.',
        'q6_research_questions': 'Research Questions:',
        'q6_research_q1': 'How many rooms are most common?',
        'q6_research_q2': 'Does the room number distribution show a specific pattern?',
        'q6_research_q3': 'What is the market preference?',
        'q6_expected_results': 'Expected Results:',
        'q6_expected_distribution': 'Room number distribution reflects market demand and family structure, helping to understand buyer preferences.',
        'q6_expected_market': 'Understanding dominant housing types helps understand the actual demand and supply structure of the market.',
        'q6_key_insights': 'Key Insights:',
        'q6_insight1': 'Room number distribution reflects market demand and family structure',
        'q6_insight2': 'Properties with different room numbers may target different groups (singles, families, etc.)',
        'q6_insight3': 'Dominant housing types may reflect local demographic structure and lifestyle',
        'q6_statistics': '📈 Statistics',
        'q6_total_properties': 'Total Properties',
        'q6_room_count_range': 'Room Count Range',
        'q6_most_common_rooms': 'Most Common Room Count',
        'q6_avg_rooms': 'Average Room Count',
        'q6_distribution_chart': '📊 Distribution Chart',
        'q6_title': 'Q6: Room Count Distribution',
        # Q7 相关
        'q7_analysis_purpose': '📊 Analysis Purpose',
        'q7_analysis_description': 'This analysis aims to identify **cities with the highest transaction volumes** to understand hot spots in the real estate market.',
        'q7_research_questions': 'Research Questions:',
        'q7_research_q1': 'Which cities are most active in transactions?',
        'q7_research_q2': 'Are transactions concentrated in certain cities?',
        'q7_research_q3': 'What is the volume difference between cities?',
        'q7_expected_results': 'Expected Results:',
        'q7_expected_ranking': 'Transaction volume ranking helps identify market hot spots and understand real estate activity in different cities.',
        'q7_expected_concentration': 'Transaction volume concentration may reflect cities\' economic vitality and real estate market development level.',
        'q7_key_insights': 'Key Insights:',
        'q7_insight1': 'Transaction volume ranking reflects real estate market activity in different cities',
        'q7_insight2': 'Cities with high transaction concentration may be economic centers or development hot spots',
        'q7_insight3': 'Volume differences between cities may reflect economic development level and population mobility',
        'q7_statistics': '📈 Statistics',
        'q7_total_transactions': 'Total Transactions',
        'q7_cities_shown': 'Number of Cities Shown',
        'q7_most_active_city': 'Most Active City',
        'q7_top_city_transactions': 'Top City Transactions',
        'q7_ranking_chart': '📊 Ranking Chart',
        'q7_title': 'Q7: Top 10 Cities by Transaction Volume',
        # Q8 相关
        'q8_analysis_purpose': '📊 Analysis Purpose',
        'q8_analysis_description': 'This analysis aims to compare average property prices across different **departments** to understand price differences between regions.',
        'q8_research_questions': 'Research Questions:',
        'q8_research_q1': 'Which department has the highest average price?',
        'q8_research_q2': 'How large are price differences between regions?',
        'q8_research_q3': 'Does price distribution show geographical patterns?',
        'q8_expected_results': 'Expected Results:',
        'q8_expected_difference': 'Price differences between departments reflect different economic development levels, geographical locations, and market demands.',
        'q8_expected_pattern': 'Price distribution may show obvious geographical patterns, such as higher prices in large cities.',
        'q8_key_insights': 'Key Insights:',
        'q8_insight1': 'Price differences between departments reflect the influence of economic development level and geographical location',
        'q8_insight2': 'Price differences may be influenced by city size, economic vitality, geographical location, etc.',
        'q8_insight3': 'Understanding regional price differences helps understand regional characteristics of the real estate market',
        'q8_statistics': '📈 Statistics',
        'q8_departments': 'Number of Departments',
        'q8_highest_avg_price': 'Highest Average Price',
        'q8_lowest_avg_price': 'Lowest Average Price',
        'q8_price_range': 'Price Range',
        'q8_comparison_chart': '📊 Comparison Chart',
        'q8_title': 'Q8: Average Price by Department',
        # Q9 相关
        'q9_analysis_purpose': '📊 Analysis Purpose',
        'q9_analysis_description': 'This analysis aims to analyze transaction volumes by **postal code area** to identify specific high-activity areas.',
        'q9_research_questions': 'Research Questions:',
        'q9_research_q1': 'Which postal code areas have the most frequent transactions?',
        'q9_research_q2': 'Are transactions concentrated in specific areas?',
        'q9_research_q3': 'What is the activity difference between areas?',
        'q9_expected_results': 'Expected Results:',
        'q9_expected_analysis': 'Postal code level analysis can more precisely identify market hot spots and understand micro-market activity.',
        'q9_expected_precision': 'Postal code analysis can provide more granular market insights than city level.',
        'q9_key_insights': 'Key Insights:',
        'q9_insight1': 'Postal code level analysis can identify specific market hot spot areas',
        'q9_insight2': 'Areas with high transaction concentration may be business centers, residential areas, or new development zones',
        'q9_insight3': 'Activity differences between areas may reflect geographical location, transportation convenience, and other factors',
        'q9_statistics': '📈 Statistics',
        'q9_postal_codes_shown': 'Number of Postal Codes Shown',
        'q9_total_transactions': 'Total Transactions',
        'q9_most_active_code': 'Most Active Postal Code',
        'q9_top_code_transactions': 'Top Area Transactions',
        'q9_ranking_chart': '📊 Ranking Chart',
        'q9_title': 'Q9: Top 15 Postal Codes by Transaction Volume',
        # Q10 相关
        'q10_analysis_purpose': '📊 Analysis Purpose',
        'q10_analysis_description': 'This analysis aims to analyze the **distribution of built surface areas** to understand the dominant area ranges in the market.',
        'q10_research_questions': 'Research Questions:',
        'q10_research_q1': 'Which area range has the most properties?',
        'q10_research_q2': 'Does the area distribution show a specific pattern?',
        'q10_research_q3': 'What area does the market prefer?',
        'q10_expected_results': 'Expected Results:',
        'q10_expected_distribution': 'Area distribution reflects market demand and buyers\' actual needs, helping to understand market characteristics.',
        'q10_expected_market': 'Understanding dominant area ranges helps understand the actual demand and supply structure of the market.',
        'q10_key_insights': 'Key Insights:',
        'q10_insight1': 'Area distribution reflects market demand and buyers\' actual needs',
        'q10_insight2': 'Properties in different area ranges may target different groups',
        'q10_insight3': 'Dominant area ranges may reflect local living standards and living habits',
        'q10_statistics': '📈 Statistics',
        'q10_total_properties': 'Total Properties',
        'q10_surface_ranges': 'Number of Ranges',
        'q10_most_common_range': 'Most Common Range',
        'q10_avg_surface': 'Average Surface',
        'q10_distribution_chart': '📊 Distribution Chart',
        'q10_title': 'Q10: Built Surface Area Distribution',
        # Q11 相关
        'analysis_purpose': '📊 Analysis Purpose',
        'analysis_description': 'This analysis aims to explore the correlation between **built surface area** and **property value**.',
        'research_questions': 'Research Questions:',
        'research_q1': 'Do properties with larger areas have higher prices?',
        'research_q2': 'Is there a linear relationship between area and price?',
        'research_q3': 'How strong is this relationship?',
        'expected_results': 'Expected Results:',
        'expected_strong': 'If correlation is strong (r > 0.7): area is a major determining factor of price',
        'expected_weak': 'If correlation is weak (r < 0.3): price is more influenced by other factors (location, property type, year, etc.)',
        'overall_correlation': '📈 Overall Correlation Analysis',
        'correlation_explanation': '🔍 Correlation Explanation',
        'weak_correlation': 'Weak Correlation',
        'medium_correlation': 'Moderate Correlation',
        'strong_correlation': 'Strong Correlation',
        'what_does_this_mean': 'What does this mean?',
        'weak_explanation': 'The **linear relationship** between area and price is not obvious',
        'weak_explanation2': 'Area alone cannot well predict price',
        'weak_explanation3': 'Price is more influenced by other factors',
        'why_horizontal': 'Why is the trendline horizontal?',
        'horizontal_explanation': 'When correlation is very weak, the trendline approaches the average of the data, making it almost horizontal. This indicates:',
        'horizontal_explanation2': 'Property prices vary greatly for different areas',
        'horizontal_explanation3': 'Area is not a major determining factor of price',
        'medium_explanation': 'There is a **certain linear relationship** between area and price',
        'medium_explanation2': 'Area can partially explain price variations',
        'medium_explanation3': 'But there are still other important factors affecting price',
        'strong_explanation': 'There is an **obvious linear relationship** between area and price',
        'strong_explanation2': 'Area is one of the major determining factors of price',
        'strong_explanation3': 'Area can be used to predict price (with some accuracy)',
        'by_property_type': '🏠 Analysis by Property Type',
        'property_type': 'Property Type',
        'type_correlation_note': 'Correlation may differ by property type. In the chart below, different colors represent different property types.',
        'scatter_plot': '📊 Scatter Plot',
        'overall_trendline': 'Overall Trendline',
        'type_trendline': 'Trendline',
        'trendline_note': 'Different colors represent different property types. The red dashed line is the trendline for all data. Only types with strong enough correlation (|r| ≥ 0.3) show their own trendline.',
        'trendline_note_weak': 'Different colors represent different property types. As overall correlation is weak (|r| < 0.3), no trendline is shown.',
        'trendline_note_simple': 'The **red dashed line** is the linear regression trendline, showing the linear relationship between area and price.',
        'trendline_note_no': 'As correlation is weak (|r| < 0.3), no trendline is shown because the linear relationship is not obvious.',
        'correlation_coefficient': 'Overall Correlation Coefficient r',
        'q11_title': 'Q11: Surface Area vs Property Value Correlation',
        # Q12 相关
        'q12_analysis_purpose': '📊 Analysis Purpose',
        'q12_analysis_description': 'This analysis aims to compare average land areas by **land nature** (residential, commercial, etc.).',
        'q12_research_questions': 'Research Questions:',
        'q12_research_q1': 'Which land nature has the largest average area?',
        'q12_research_q2': 'How do area differences vary between different natures?',
        'q12_research_q3': 'Does land nature affect area size?',
        'q12_expected_results': 'Expected Results:',
        'q12_expected_difference': 'Average area differences between land natures reflect different usage and planning requirements.',
        'q12_expected_usage': 'Understanding average areas by land nature helps understand land use patterns and planning characteristics.',
        'q12_key_insights': 'Key Insights:',
        'q12_insight1': 'Land nature reflects different usages and planning requirements',
        'q12_insight2': 'Area differences between land natures may be influenced by planning policies, usage needs, and other factors',
        'q12_insight3': 'Average area analysis helps understand land use efficiency and planning characteristics',
        'q12_statistics': '📈 Statistics',
        'q12_land_types': 'Number of Land Types',
        'q12_largest_avg_area': 'Largest Average Area',
        'q12_smallest_avg_area': 'Smallest Average Area',
        'q12_area_range': 'Area Range',
        'q12_comparison_chart': '📊 Comparison Chart',
        'q12_title': 'Q12: Average Land Area by Land Nature',
        # Q13 相关
        'q13_analysis_purpose': '📊 Analysis Purpose',
        'q13_analysis_description': 'This analysis aims to analyze **temporal trends of average prices** to understand market price fluctuations.',
        'q13_research_questions': 'Research Questions:',
        'q13_research_q1': 'Does average price change over time?',
        'q13_research_q2': 'Is there a trend of price increase or decrease?',
        'q13_research_q3': 'Do price fluctuations have patterns?',
        'q13_expected_results': 'Expected Results:',
        'q13_expected_trend': 'Price trend analysis helps understand market movements and is an important reference for investment and decisions.',
        'q13_expected_volatility': 'Price fluctuations may reflect the influence of supply-demand changes, economic cycles, and other factors.',
        'q13_key_insights': 'Key Insights:',
        'q13_insight1': 'Price trends reflect market supply-demand relationships and investor expectations',
        'q13_insight2': 'Price fluctuations may be influenced by economic cycles, policy adjustments, market sentiment, etc.',
        'q13_insight3': 'Long-term price trends help judge market development direction and investment timing',
        'q13_statistics': '📈 Statistics',
        'q13_months': 'Number of Months',
        'q13_highest_avg_price': 'Highest Average Price',
        'q13_lowest_avg_price': 'Lowest Average Price',
        'q13_current_avg_price': 'Current Average Price',
        'q13_trend_chart': '📊 Trend Chart',
        'q13_title': 'Q13: Monthly Average Price Evolution',
        # Q14 相关
        'q14_analysis_purpose': '📊 Analysis Purpose',
        'q14_analysis_description': 'This analysis aims to compare price statistics (average, minimum, maximum) by **property type** to comprehensively understand price distribution.',
        'q14_research_questions': 'Research Questions:',
        'q14_research_q1': 'Which property type has the highest average price?',
        'q14_research_q2': 'How large are price range differences (minimum to maximum)?',
        'q14_research_q3': 'What is price volatility by type?',
        'q14_expected_results': 'Expected Results:',
        'q14_expected_comparison': 'Price comparison helps evaluate value ranges of different property types and understand market price structure.',
        'q14_expected_range': 'Price range analysis can reveal price volatility and market diversity for different property types.',
        'q14_key_insights': 'Key Insights:',
        'q14_insight1': 'Price statistics reflect value positioning and market performance of different property types',
        'q14_insight2': 'Price range differences may reflect market diversity, supply-demand relationships, and other factors',
        'q14_insight3': 'Understanding price statistics helps understand investment value and risks of different property types',
        'q14_statistics': '📈 Statistics',
        'q14_property_types': 'Number of Types',
        'q14_highest_avg': 'Highest Average Price',
        'q14_largest_range': 'Largest Price Range',
        'q14_price_comparison_chart': '📊 Price Comparison Chart',
        'q14_title': 'Q14: Price Comparison by Property Type',
        # Q15 相关
        'q15_analysis_purpose': '📊 Analysis Purpose',
        'q15_analysis_description': 'This analysis aims to compare price distributions of **houses and apartments** to understand price differences between the two main property types.',
        'q15_research_questions': 'Research Questions:',
        'q15_research_q1': 'What is the difference in price distribution between houses and apartments?',
        'q15_research_q2': 'Which type has higher prices?',
        'q15_research_q3': 'Do price distributions show different patterns?',
        'q15_expected_results': 'Expected Results:',
        'q15_expected_comparison': 'Price comparison of houses and apartments helps understand market positioning and value differences between different property types.',
        'q15_expected_distribution': 'Price distribution patterns may reflect target groups and market characteristics of different property types.',
        'q15_key_insights': 'Key Insights:',
        'q15_insight1': 'Price distributions of houses and apartments reflect different market positioning and target groups',
        'q15_insight2': 'Price differences may be influenced by location, area, quality, demand, and other factors',
        'q15_insight3': 'Understanding price distributions helps understand investment value and market characteristics of different property types',
        'q15_statistics': '📈 Statistics',
        'q15_total_properties': 'Total Properties',
        'q15_houses': 'Number of Houses',
        'q15_apartments': 'Number of Apartments',
        'q15_house_median': 'House Median Price',
        'q15_apartment_median': 'Apartment Median Price',
        'q15_distribution_chart': '📊 Distribution Chart',
        'q15_title': 'Q15: Price Distribution - Houses vs Apartments',
        # Q16 相关
        'q16_analysis_purpose': '📊 Analysis Purpose',
        'q16_analysis_description': 'This analysis aims to calculate the **ratio of land area to built area** to understand land use in different cities.',
        'q16_research_questions': 'Research Questions:',
        'q16_research_q1': 'Which cities have the highest land/built area ratio?',
        'q16_research_q2': 'What do ratio differences reflect?',
        'q16_research_q3': 'How efficient is land use?',
        'q16_expected_results': 'Expected Results:',
        'q16_expected_ratio': 'Land/built area ratio reflects land use density, areas with high ratios may have more land space.',
        'q16_expected_efficiency': 'Understanding land use ratios helps understand planning characteristics and development patterns of different cities.',
        'q16_key_insights': 'Key Insights:',
        'q16_insight1': 'Land/built area ratio reflects land use density and development intensity',
        'q16_insight2': 'Areas with high ratios may have more land space, suitable for low-density development',
        'q16_insight3': 'Ratio differences may reflect urban planning policies, land supply, and other factors',
        'q16_statistics': '📈 Statistics',
        'q16_cities_shown': 'Number of Cities Shown',
        'q16_highest_ratio': 'Highest Ratio',
        'q16_lowest_ratio': 'Lowest Ratio',
        'q16_avg_ratio': 'Average Ratio',
        'q16_ranking_chart': '📊 Ranking Chart',
        'q16_title': 'Q16: Land/Built Area Ratio Top 10',
        # Q17 相关
        'q17_analysis_purpose': '📊 Analysis Purpose',
        'q17_analysis_description': 'This analysis aims to analyze the **number of properties per transaction** to understand transaction complexity.',
        'q17_research_questions': 'Research Questions:',
        'q17_research_q1': 'How many properties do most transactions contain?',
        'q17_research_q2': 'Are multi-property transactions common?',
        'q17_research_q3': 'What is the distribution of transaction complexity?',
        'q17_expected_results': 'Expected Results:',
        'q17_expected_complexity': 'The number of properties per transaction reflects transaction complexity, which may affect transaction process and price.',
        'q17_expected_pattern': 'Understanding transaction complexity distribution helps understand market transaction patterns and characteristics.',
        'q17_key_insights': 'Key Insights:',
        'q17_insight1': 'Transaction complexity reflects market transaction patterns and characteristics',
        'q17_insight2': 'Multi-property transactions may involve bulk transactions, investment portfolios, and other special situations',
        'q17_insight3': 'Transaction complexity may affect transaction process, price negotiation, and other factors',
        'q17_statistics': '📈 Statistics',
        'q17_total_transactions': 'Total Transactions',
        'q17_most_common_count': 'Most Common Property Count',
        'q17_max_properties': 'Maximum Properties per Transaction',
        'q17_avg_properties': 'Average Property Count',
        'q17_distribution_chart': '📊 Distribution Chart',
        'q17_title': 'Q17: Number of Properties per Transaction',
        # Q18 相关
        'q18_analysis_purpose': '📊 Analysis Purpose',
        'q18_analysis_description': 'This analysis aims to count **properties with and without land** to understand characteristics of different property types.',
        'q18_research_questions': 'Research Questions:',
        'q18_research_q1': 'Which property type is more likely to have land?',
        'q18_research_q2': 'What is the proportion of properties with and without land?',
        'q18_research_q3': 'Does land affect property type?',
        'q18_expected_results': 'Expected Results:',
        'q18_expected_characteristics': 'Land ownership reflects property completeness and value, an important indicator of property characteristics.',
        'q18_expected_distribution': 'Understanding land distribution helps understand characteristics and market positioning of different property types.',
        'q18_key_insights': 'Key Insights:',
        'q18_insight1': 'Land ownership reflects property completeness and value',
        'q18_insight2': 'Land ownership rates may vary significantly by property type',
        'q18_insight3': 'Land is an important component of property value, affecting market positioning',
        'q18_statistics': '📈 Statistics',
        'q18_property_types': 'Number of Property Types',
        'q18_total_with_land': 'Total with Land',
        'q18_total_without_land': 'Total without Land',
        'q18_land_ownership_rate': 'Land Ownership Rate',
        'q18_comparison_chart': '📊 Comparison Chart',
        'q18_title': 'Q18: Properties with/without Land Statistics',
        # Q19 相关
        'q19_analysis_purpose': '📊 Analysis Purpose',
        'q19_analysis_description': 'This analysis aims to analyze **transaction distribution by day of week** to understand transaction time patterns.',
        'q19_research_questions': 'Research Questions:',
        'q19_research_q1': 'Which day of the week has the most transactions?',
        'q19_research_q2': 'Are there differences between weekdays and weekends?',
        'q19_research_q3': 'Do transaction times have patterns?',
        'q19_expected_results': 'Expected Results:',
        'q19_expected_pattern': 'Transaction date distribution may reflect market behavior patterns, such as more active transactions on weekdays.',
        'q19_expected_behavior': 'Understanding transaction time patterns helps understand market operation patterns and transaction habits.',
        'q19_key_insights': 'Key Insights:',
        'q19_insight1': 'Transaction date distribution reflects market behavior patterns and work habits',
        'q19_insight2': 'Transaction volume differences between weekdays and weekends may reflect market operation patterns',
        'q19_insight3': 'Transaction time patterns may be influenced by legal procedures, office hours, and other factors',
        'q19_statistics': '📈 Statistics',
        'q19_total_transactions': 'Total Transactions',
        'q19_most_active_day': 'Most Active Day',
        'q19_least_active_day': 'Least Active Day',
        'q19_weekday_avg': 'Weekday Average',
        'q19_distribution_chart': '📊 Distribution Chart',
        'q19_title': 'Q19: Weekly Transaction Distribution',
        # Q20 相关
        'q20_analysis_purpose': '📊 Analysis Purpose',
        'q20_analysis_description': 'This analysis aims to analyze **weekly transaction volume and total transaction value** to understand weekly market trends.',
        'q20_research_questions': 'Research Questions:',
        'q20_research_q1': 'Do transaction volume and total value change synchronously?',
        'q20_research_q2': 'Are there cyclical patterns?',
        'q20_research_q3': 'How does market activity fluctuate?',
        'q20_expected_results': 'Expected Results:',
        'q20_expected_analysis': 'Weekly analysis can help identify short-term trends and cyclical patterns in the market.',
        'q20_expected_trends': 'Trends in transaction volume and total value can reflect overall market activity and value changes.',
        'q20_key_insights': 'Key Insights:',
        'q20_insight1': 'Weekly analysis can reveal short-term trends and cyclical patterns in the market',
        'q20_insight2': 'Synchronization of transaction volume and total value reflects overall market activity',
        'q20_insight3': 'Cyclical patterns may be influenced by seasonal factors, market events, etc.',
        'q20_statistics': '📈 Statistics',
        'q20_weeks': 'Number of Weeks',
        'q20_total_transactions': 'Total Transactions',
        'q20_total_volume': 'Total Transaction Value',
        'q20_avg_transactions_per_week': 'Average Transactions per Week',
        'q20_avg_volume_per_week': 'Average Value per Week',
        'q20_trend_chart': '📊 Weekly Trend Chart',
        'q20_title': 'Q20: Weekly Transaction Volume Analysis',
    },
    'ar': {
        'app_title': '🏠 منصة تحليل بيانات معاملات العقارات DVF',
        'db_config': '⚙️ إعدادات قاعدة البيانات',
        'db_settings': '🔧 إعدادات اتصال قاعدة البيانات',
        'db_tip': '💡 **نصيحة**: يمكنك استخدام المستخدم root، لا حاجة لإنشاء userP6',
        'host': 'عنوان الخادم',
        'host_help': 'عنوان خادم MySQL (localhost يعني الاتصال المحلي)',
        'user': 'اسم المستخدم',
        'user_help': 'اسم مستخدم MySQL (يمكنك استخدام root أو مستخدم موجود آخر)',
        'password': 'كلمة المرور',
        'password_help': 'كلمة مرور MySQL (كلمة مرور المستخدم root)',
        'database': 'اسم قاعدة البيانات',
        'database_help': 'اسم قاعدة البيانات للاتصال بها',
        'database_label': 'قاعدة البيانات',
        'analysis_selection': '📊 اختيار سؤال التحليل',
        'select_question': 'اختر سؤال التحليل لعرضه:',
        'select_question_label': 'اختر السؤال:',
        'db_status_check': '🔍 فحص حالة قاعدة البيانات',
        'db_connected': '✅ نجح الاتصال بقاعدة البيانات',
        'tip_chart': '💡 نصيحة: انقر على الرسم البياني للتكبير والتحريك والتنزيل',
        'data_source': 'مصدر البيانات',
        'view_data': '📊 عرض البيانات',
        'data_summary': 'ملخص البيانات',
        'raw_data': '📋 عرض البيانات الخام',
        'database': 'قاعدة البيانات',
        'rows': 'صفوف',
        # Error messages
        'db_auth_failed': '❌ **فشل المصادقة على قاعدة البيانات!**',
        'db_not_found': '❌ **قاعدة البيانات غير موجودة!**',
        'db_connect_failed': '❌ **تعذر الاتصال بخادم MySQL!**',
        'query_error': '❌ خطأ في تنفيذ الاستعلام',
        'empty_result': '⚠️ عاد الاستعلام بنتيجة فارغة!',
        'table_empty': 'الجدول فارغ',
        'table_not_found': 'الجدول غير موجود أو غير قابل للوصول',
        'check_db_error': 'خطأ في فحص حالة قاعدة البيانات',
        # Diagnostic steps
        'diagnostic_steps': '🔍 خطوات التشخيص',
        'check_mysql_service': 'تحقق من تشغيل خدمة MySQL',
        'verify_connection': 'التحقق من معلومات اتصال قاعدة البيانات',
        'check_permissions': 'التحقق من أذونات المستخدم',
        'confirm_db_created': 'تأكد من إنشاء قاعدة البيانات',
        # Possible reasons
        'possible_reasons': 'الأسباب المحتملة:',
        'username_password_wrong': 'اسم المستخدم أو كلمة المرور غير صحيحة',
        'user_not_exists': 'المستخدم غير موجود',
        'no_access': 'المستخدم ليس لديه حقوق الوصول',
        'service_not_running': 'خدمة MySQL غير قيد التشغيل',
        'host_port_wrong': 'عنوان الخادم أو المنفذ غير صحيح',
        # Solutions
        'solutions': 'الحلول:',
        'check_credentials': 'تحقق من صحة اسم المستخدم وكلمة المرور',
        'confirm_mysql_running': 'تأكد من تشغيل خدمة MySQL',
        'test_connection': 'اختبر الاتصال باستخدام MySQL Workbench أو سطر الأوامر',
        'create_user': 'إذا كنت بحاجة لإنشاء مستخدم، قم بتشغيل:',
        'check_service': 'تحقق من تشغيل خدمة MySQL',
        'check_firewall': 'تحقق من إعدادات الجدار الناري',
        # Data related
        'data_points': 'نقاط البيانات',
        'correlation': 'معامل الارتباط',
        'avg_area': 'المساحة المتوسطة',
        'avg_price': 'السعر المتوسط',
        'table_exists': 'الجدول موجود',
        'total_rows': 'إجمالي الصفوف في الجدول',
        'no_data_rows': 'عدد الصفوف التي تحتوي على بيانات',
        'view_query': '🔍 عرض الاستعلام',
        'possible_causes': 'الأسباب المحتملة:',
        'no_data_in_db': 'لا توجد بيانات في قاعدة البيانات (الجدول فارغ)',
        'data_not_imported': 'لم يتم استيراد البيانات إلى قاعدة البيانات بعد',
        'table_mismatch': 'عدم تطابق هيكل الجدول أو الجدول غير موجود',
        'solution_check_data': 'تحقق من وجود بيانات في قاعدة البيانات',
        'solution_import_data': 'إذا لم تكن هناك بيانات، قم أولاً بتشغيل `create_tab.sql` لاستيراد البيانات',
        # Q1 相关
        'q1_analysis_purpose': '📊 هدف التحليل',
        'q1_analysis_description': 'يهدف هذا التحليل إلى استكشاف **الاتجاهات الزمنية** لـ **عدد معاملات العقارات** لفهم نشاط السوق والتغيرات الدورية.',
        'q1_research_questions': 'أسئلة البحث:',
        'q1_research_q1': 'هل يزيد عدد المعاملات أم ينخفض بمرور الوقت؟',
        'q1_research_q2': 'هل توجد أنماط موسمية واضحة؟',
        'q1_research_q3': 'أي الأشهر أكثر نشاطاً في المعاملات؟',
        'q1_expected_results': 'النتائج المتوقعة:',
        'q1_expected_trend': 'من خلال مراقبة اتجاهات عدد المعاملات، يمكن فهم النشاط العام للسوق العقاري والأنماط الدورية.',
        'q1_expected_seasonal': 'إذا كانت هناك أنماط موسمية، يمكن أن تساعد في التنبؤ بالتغيرات المستقبلية في حجم المعاملات.',
        'q1_key_insights': 'الرؤى الرئيسية:',
        'q1_insight1': 'تعكس تغيرات عدد المعاملات علاقة العرض والطلب في السوق وثقة المستثمرين',
        'q1_insight2': 'قد تتأثر الأنماط الموسمية بالعطلات وتعديلات السياسات وعوامل أخرى',
        'q1_insight3': 'يمكن للاتجاهات طويلة الأجل أن تساعد في الحكم على اتجاه تطور السوق',
        'q1_statistics': '📈 الإحصائيات',
        'q1_total_transactions': 'إجمالي المعاملات',
        'q1_avg_per_month': 'المتوسط الشهري',
        'q1_most_active_month': 'أكثر شهر نشاطاً',
        'q1_trend_chart': '📊 مخطط الاتجاه',
        'q1_title': 'Q1: تطور عدد المعاملات الشهرية',
        # Q2 相关
        'q2_analysis_purpose': '📊 هدف التحليل',
        'q2_analysis_description': 'يهدف هذا التحليل إلى فهم توزيع العقارات عبر **نطاقات أسعار** مختلفة لتحديد شرائح الأسعار الرئيسية في السوق.',
        'q2_research_questions': 'أسئلة البحث:',
        'q2_research_q1': 'أي نطاق سعري يحتوي على أكبر عدد من المعاملات؟',
        'q2_research_q2': 'هل يظهر توزيع الأسعار نمطاً محدداً؟',
        'q2_research_q3': 'ما هي نسبة السوق عالي الجودة مقابل منخفض الجودة؟',
        'q2_expected_results': 'النتائج المتوقعة:',
        'q2_expected_distribution': 'يمكن أن يساعد توزيع الأسعار في تحديد شرائح الطلب الرئيسية وفهم أداء السوق عند مستويات أسعار مختلفة.',
        'q2_expected_segments': 'من خلال تحليل توزيع نطاقات الأسعار، يمكن فهم هيكل أسعار السوق والقوة الشرائية للمستهلكين.',
        'q2_key_insights': 'الرؤى الرئيسية:',
        'q2_insight1': 'يعكس توزيع الأسعار توازن العرض والطلب في السوق والقوة الشرائية للمستهلكين',
        'q2_insight2': 'قد تعكس نطاقات الأسعار الرئيسية المستويات الاقتصادية المحلية وخصائص السوق',
        'q2_insight3': 'يمكن أن تكشف تركيز نطاقات الأسعار عن تفضيلات أسعار السوق',
        'q2_statistics': '📈 الإحصائيات',
        'q2_total_mutations': 'إجمالي المعاملات',
        'q2_price_ranges': 'عدد النطاقات',
        'q2_most_common_range': 'النطاق الأكثر شيوعاً',
        'q2_avg_per_range': 'المتوسط لكل نطاق',
        'q2_distribution_chart': '📊 مخطط التوزيع',
        'q2_title': 'Q2: توزيع نطاقات الأسعار',
        # Q3 相关
        'q3_analysis_purpose': '📊 هدف التحليل',
        'q3_analysis_description': 'يهدف هذا التحليل إلى مقارنة متوسطات الأسعار عبر **أنواع المعاملات** المختلفة (مثل البيع والتبادل وما إلى ذلك) لفهم تأثير نوع المعاملة على السعر.',
        'q3_research_questions': 'أسئلة البحث:',
        'q3_research_q1': 'أي نوع معاملة له أعلى متوسط سعر؟',
        'q3_research_q2': 'ما مدى اختلافات الأسعار بين أنواع المعاملات المختلفة؟',
        'q3_research_q3': 'هل يؤثر نوع المعاملة على قيمة العقار؟',
        'q3_expected_results': 'النتائج المتوقعة:',
        'q3_expected_difference': 'قد تعكس اختلافات الأسعار بين أنواع المعاملات اختلافات في سلوك السوق أو السياسات الضريبية أو دوافع المعاملة.',
        'q3_expected_impact': 'يساعد فهم تأثير نوع المعاملة على السعر في فهم آليات السوق وخصائص المعاملات.',
        'q3_key_insights': 'الرؤى الرئيسية:',
        'q3_insight1': 'قد تعكس أنواع المعاملات دوافع معاملات مختلفة وظروف سوق مختلفة',
        'q3_insight2': 'قد تتأثر اختلافات الأسعار بالسياسات الضريبية وتكاليف المعاملات وعوامل أخرى',
        'q3_insight3': 'قد تكون بعض أنواع المعاملات أكثر ملاءمة للعقارات في نطاقات أسعار محددة',
        'q3_statistics': '📈 الإحصائيات',
        'q3_transaction_types': 'عدد الأنواع',
        'q3_highest_avg_price': 'أعلى متوسط سعر',
        'q3_lowest_avg_price': 'أدنى متوسط سعر',
        'q3_price_difference': 'الفرق في السعر',
        'q3_comparison_chart': '📊 مخطط المقارنة',
        'q3_title': 'Q3: متوسط السعر حسب نوع المعاملة',
        # Q4 相关
        'q4_analysis_purpose': '📊 هدف التحليل',
        'q4_analysis_description': 'يهدف هذا التحليل إلى فهم التوزيع النسبي لـ **أنواع العقارات** المختلفة (الشقق والمنازل وما إلى ذلك) في السوق.',
        'q4_research_questions': 'أسئلة البحث:',
        'q4_research_q1': 'أي نوع عقار هو الأكثر شيوعاً؟',
        'q4_research_q2': 'ما هي حصة السوق لأنواع العقارات المختلفة؟',
        'q4_research_q3': 'هل السوق منحاز لنوع محدد؟',
        'q4_expected_results': 'النتائج المتوقعة:',
        'q4_expected_distribution': 'يعكس توزيع أنواع العقارات هيكل الطلب والعرض في السوق، مما يساعد على فهم خصائص السوق.',
        'q4_expected_market': 'يمكن أن يساعد فهم توزيع أنواع العقارات في تحديد أنواع العرض الرئيسية وتفضيلات الطلب في السوق.',
        'q4_key_insights': 'الرؤى الرئيسية:',
        'q4_insight1': 'يعكس توزيع أنواع العقارات هيكل الطلب والعرض في السوق',
        'q4_insight2': 'قد تتأثر نسبة الأنواع المختلفة بالموقع الجغرافي والتخطيط الحضري وعوامل أخرى',
        'q4_insight3': 'يمكن أن يساعد توزيع أنواع السوق في فهم خصائص سوق العقارات المحلي',
        'q4_statistics': '📈 الإحصائيات',
        'q4_total_properties': 'إجمالي العقارات',
        'q4_property_types': 'عدد الأنواع',
        'q4_most_common_type': 'النوع الأكثر شيوعاً',
        'q4_distribution_chart': '📊 مخطط التوزيع',
        'q4_title': 'Q4: توزيع أنواع العقارات',
        # Q5 相关
        'q5_analysis_purpose': '📊 هدف التحليل',
        'q5_analysis_description': 'يهدف هذا التحليل إلى حساب **متوسط السعر لكل متر مربع** ومقارنة اختلافات السعر الوحدة عبر أنواع العقارات المختلفة.',
        'q5_research_questions': 'أسئلة البحث:',
        'q5_research_q1': 'أي نوع عقار له أعلى سعر وحدة؟',
        'q5_research_q2': 'ما هي نسبة السعر إلى الأداء لأنواع العقارات المختلفة؟',
        'q5_research_q3': 'هل اختلافات السعر الوحدة معقولة؟',
        'q5_expected_results': 'النتائج المتوقعة:',
        'q5_expected_price': 'يمكن أن يساعد تحليل السعر الوحدة في تقييم قيمة أنواع العقارات المختلفة وهو مؤشر مرجعي مهم لقرارات الاستثمار.',
        'q5_expected_comparison': 'من خلال مقارنة أسعار الوحدات، يمكننا فهم موضع القيمة وإمكانات الاستثمار لأنواع العقارات المختلفة.',
        'q5_key_insights': 'الرؤى الرئيسية:',
        'q5_insight1': 'السعر الوحدة هو مؤشر مهم لتقييم قيمة العقار، يعكس القيمة لكل وحدة مساحة',
        'q5_insight2': 'قد تتأثر اختلافات السعر الوحدة بين أنواع العقارات بالموقع والجودة والطلب وعوامل أخرى',
        'q5_insight3': 'يساعد تحليل السعر الوحدة في فهم قيمة الاستثمار وموضع السوق لأنواع العقارات المختلفة',
        'q5_statistics': '📈 الإحصائيات',
        'q5_property_types': 'عدد الأنواع',
        'q5_highest_price_m2': 'أعلى سعر وحدة',
        'q5_lowest_price_m2': 'أدنى سعر وحدة',
        'q5_avg_price_m2': 'متوسط السعر الوحدة',
        'q5_price_comparison_chart': '📊 مخطط مقارنة الأسعار',
        'q5_title': 'Q5: السعر لكل متر مربع (حسب النوع)',
        # Q6 相关
        'q6_analysis_purpose': '📊 هدف التحليل',
        'q6_analysis_description': 'يهدف هذا التحليل إلى تحليل **توزيع عدد الغرف** في العقارات لفهم أنواع المساكن السائدة في السوق.',
        'q6_research_questions': 'أسئلة البحث:',
        'q6_research_q1': 'كم عدد الغرف الأكثر شيوعاً؟',
        'q6_research_q2': 'هل يظهر توزيع عدد الغرف نمطاً محدداً؟',
        'q6_research_q3': 'ما هي تفضيلات السوق؟',
        'q6_expected_results': 'النتائج المتوقعة:',
        'q6_expected_distribution': 'يعكس توزيع عدد الغرف طلب السوق والهيكل العائلي، مما يساعد على فهم تفضيلات المشترين.',
        'q6_expected_market': 'يساعد فهم أنواع المساكن السائدة في فهم الطلب الفعلي وهيكل العرض في السوق.',
        'q6_key_insights': 'الرؤى الرئيسية:',
        'q6_insight1': 'يعكس توزيع عدد الغرف طلب السوق والهيكل العائلي',
        'q6_insight2': 'قد تستهدف العقارات بأعداد غرف مختلفة مجموعات مختلفة (عزاب، عائلات، إلخ)',
        'q6_insight3': 'قد تعكس أنواع المساكن السائدة الهيكل الديموغرافي المحلي وأسلوب الحياة',
        'q6_statistics': '📈 الإحصائيات',
        'q6_total_properties': 'إجمالي العقارات',
        'q6_room_count_range': 'نطاق عدد الغرف',
        'q6_most_common_rooms': 'عدد الغرف الأكثر شيوعاً',
        'q6_avg_rooms': 'متوسط عدد الغرف',
        'q6_distribution_chart': '📊 مخطط التوزيع',
        'q6_title': 'Q6: توزيع عدد الغرف',
        # Q7 相关
        'q7_analysis_purpose': '📊 هدف التحليل',
        'q7_analysis_description': 'يهدف هذا التحليل إلى تحديد **المدن ذات أعلى أحجام المعاملات** لفهم النقاط الساخنة في سوق العقارات.',
        'q7_research_questions': 'أسئلة البحث:',
        'q7_research_q1': 'أي المدن هي الأكثر نشاطاً في المعاملات؟',
        'q7_research_q2': 'هل تتركز المعاملات في مدن معينة؟',
        'q7_research_q3': 'ما هو الفرق في الحجم بين المدن؟',
        'q7_expected_results': 'النتائج المتوقعة:',
        'q7_expected_ranking': 'يساعد ترتيب حجم المعاملات في تحديد النقاط الساخنة في السوق وفهم نشاط العقارات في مدن مختلفة.',
        'q7_expected_concentration': 'قد يعكس تركيز حجم المعاملات الحيوية الاقتصادية للمدن ومستوى تطور سوق العقارات.',
        'q7_key_insights': 'الرؤى الرئيسية:',
        'q7_insight1': 'يعكس ترتيب حجم المعاملات نشاط سوق العقارات في مدن مختلفة',
        'q7_insight2': 'قد تكون المدن ذات التركيز العالي للمعاملات مراكز اقتصادية أو نقاط ساخنة للتنمية',
        'q7_insight3': 'قد تعكس الاختلافات في الحجم بين المدن مستوى التنمية الاقتصادية والتنقل السكاني',
        'q7_statistics': '📈 الإحصائيات',
        'q7_total_transactions': 'إجمالي المعاملات',
        'q7_cities_shown': 'عدد المدن المعروضة',
        'q7_most_active_city': 'أكثر مدينة نشاطاً',
        'q7_top_city_transactions': 'معاملات المدينة الأولى',
        'q7_ranking_chart': '📊 مخطط الترتيب',
        'q7_title': 'Q7: أعلى 10 مدن حسب حجم المعاملات',
        # Q8 相关
        'q8_analysis_purpose': '📊 هدف التحليل',
        'q8_analysis_description': 'يهدف هذا التحليل إلى مقارنة متوسطات أسعار العقارات عبر **المحافظات** المختلفة لفهم الاختلافات في الأسعار بين المناطق.',
        'q8_research_questions': 'أسئلة البحث:',
        'q8_research_q1': 'أي محافظة لديها أعلى متوسط سعر؟',
        'q8_research_q2': 'ما مدى اختلافات الأسعار بين المناطق؟',
        'q8_research_q3': 'هل يظهر توزيع الأسعار أنماطاً جغرافية؟',
        'q8_expected_results': 'النتائج المتوقعة:',
        'q8_expected_difference': 'تعكس اختلافات الأسعار بين المحافظات مستويات التنمية الاقتصادية والمواقع الجغرافية ومتطلبات السوق المختلفة.',
        'q8_expected_pattern': 'قد يظهر توزيع الأسعار أنماطاً جغرافية واضحة، مثل الأسعار الأعلى في المدن الكبيرة.',
        'q8_key_insights': 'الرؤى الرئيسية:',
        'q8_insight1': 'تعكس اختلافات الأسعار بين المحافظات تأثير مستوى التنمية الاقتصادية والموقع الجغرافي',
        'q8_insight2': 'قد تتأثر اختلافات الأسعار بحجم المدينة والحيوية الاقتصادية والموقع الجغرافي وعوامل أخرى',
        'q8_insight3': 'يساعد فهم الاختلافات في الأسعار الإقليمية في فهم الخصائص الإقليمية لسوق العقارات',
        'q8_statistics': '📈 الإحصائيات',
        'q8_departments': 'عدد المحافظات',
        'q8_highest_avg_price': 'أعلى متوسط سعر',
        'q8_lowest_avg_price': 'أدنى متوسط سعر',
        'q8_price_range': 'نطاق السعر',
        'q8_comparison_chart': '📊 مخطط المقارنة',
        'q8_title': 'Q8: متوسط السعر حسب المحافظة',
        # Q9 相关
        'q9_analysis_purpose': '📊 هدف التحليل',
        'q9_analysis_description': 'يهدف هذا التحليل إلى تحليل أحجام المعاملات حسب **منطقة الرمز البريدي** لتحديد المناطق عالية النشاط المحددة.',
        'q9_research_questions': 'أسئلة البحث:',
        'q9_research_q1': 'أي مناطق الرمز البريدي لديها المعاملات الأكثر تكراراً؟',
        'q9_research_q2': 'هل تتركز المعاملات في مناطق محددة؟',
        'q9_research_q3': 'ما هو الفرق في النشاط بين المناطق؟',
        'q9_expected_results': 'النتائج المتوقعة:',
        'q9_expected_analysis': 'يمكن لتحليل مستوى الرمز البريدي تحديد النقاط الساخنة في السوق بشكل أكثر دقة وفهم نشاط السوق الجزئي.',
        'q9_expected_precision': 'يمكن لتحليل الرمز البريدي تقديم رؤى سوقية أكثر تفصيلاً من مستوى المدينة.',
        'q9_key_insights': 'الرؤى الرئيسية:',
        'q9_insight1': 'يمكن لتحليل مستوى الرمز البريدي تحديد مناطق النقاط الساخنة في السوق المحددة',
        'q9_insight2': 'قد تكون المناطق ذات التركيز العالي للمعاملات مراكز تجارية أو مناطق سكنية أو مناطق تنمية جديدة',
        'q9_insight3': 'قد تعكس الاختلافات في النشاط بين المناطق الموقع الجغرافي وراحة المواصلات وعوامل أخرى',
        'q9_statistics': '📈 الإحصائيات',
        'q9_postal_codes_shown': 'عدد الرموز البريدية المعروضة',
        'q9_total_transactions': 'إجمالي المعاملات',
        'q9_most_active_code': 'أكثر رمز بريدي نشاطاً',
        'q9_top_code_transactions': 'معاملات المنطقة الأولى',
        'q9_ranking_chart': '📊 مخطط الترتيب',
        'q9_title': 'Q9: أعلى 15 رمز بريدي حسب حجم المعاملات',
        # Q10 相关
        'q10_analysis_purpose': '📊 هدف التحليل',
        'q10_analysis_description': 'يهدف هذا التحليل إلى تحليل **توزيع المساحات المبنية** لفهم نطاقات المساحة السائدة في السوق.',
        'q10_research_questions': 'أسئلة البحث:',
        'q10_research_q1': 'أي نطاق مساحة يحتوي على أكبر عدد من العقارات؟',
        'q10_research_q2': 'هل يظهر توزيع المساحة نمطاً محدداً؟',
        'q10_research_q3': 'ما المساحة التي يفضلها السوق؟',
        'q10_expected_results': 'النتائج المتوقعة:',
        'q10_expected_distribution': 'يعكس توزيع المساحة طلب السوق والاحتياجات الفعلية للمشترين، مما يساعد على فهم خصائص السوق.',
        'q10_expected_market': 'يساعد فهم نطاقات المساحة السائدة في فهم الطلب الفعلي وهيكل العرض في السوق.',
        'q10_key_insights': 'الرؤى الرئيسية:',
        'q10_insight1': 'يعكس توزيع المساحة طلب السوق والاحتياجات الفعلية للمشترين',
        'q10_insight2': 'قد تستهدف العقارات في نطاقات مساحة مختلفة مجموعات مختلفة',
        'q10_insight3': 'قد تعكس نطاقات المساحة السائدة مستويات المعيشة المحلية وعادات السكن',
        'q10_statistics': '📈 الإحصائيات',
        'q10_total_properties': 'إجمالي العقارات',
        'q10_surface_ranges': 'عدد النطاقات',
        'q10_most_common_range': 'النطاق الأكثر شيوعاً',
        'q10_avg_surface': 'المساحة المتوسطة',
        'q10_distribution_chart': '📊 مخطط التوزيع',
        'q10_title': 'Q10: توزيع المساحة المبنية',
        # Q11 相关
        'analysis_purpose': '📊 هدف التحليل',
        'analysis_description': 'يهدف هذا التحليل إلى استكشاف الارتباط بين **المساحة المبنية** و**قيمة العقار**.',
        'research_questions': 'أسئلة البحث:',
        'research_q1': 'هل العقارات ذات المساحات الأكبر لها أسعار أعلى؟',
        'research_q2': 'هل توجد علاقة خطية بين المساحة والسعر؟',
        'research_q3': 'ما مدى قوة هذه العلاقة؟',
        'expected_results': 'النتائج المتوقعة:',
        'expected_strong': 'إذا كانت العلاقة قوية (r > 0.7): المساحة هي عامل حاسم رئيسي للسعر',
        'expected_weak': 'إذا كانت العلاقة ضعيفة (r < 0.3): السعر يتأثر أكثر بعوامل أخرى (الموقع، نوع العقار، السنة، إلخ)',
        'overall_correlation': '📈 تحليل الارتباط الشامل',
        'correlation_explanation': '🔍 شرح الارتباط',
        'weak_correlation': 'ارتباط ضعيف',
        'medium_correlation': 'ارتباط متوسط',
        'strong_correlation': 'ارتباط قوي',
        'what_does_this_mean': 'ماذا يعني هذا؟',
        'weak_explanation': 'العلاقة الخطية** بين المساحة والسعر ليست واضحة',
        'weak_explanation2': 'المساحة وحدها لا يمكنها التنبؤ بالسعر بشكل جيد',
        'weak_explanation3': 'السعر يتأثر أكثر بعوامل أخرى',
        'why_horizontal': 'لماذا خط الاتجاه أفقي؟',
        'horizontal_explanation': 'عندما يكون الارتباط ضعيفاً جداً، يقترب خط الاتجاه من متوسط البيانات، مما يجعله أفقيًا تقريباً. يشير هذا إلى:',
        'horizontal_explanation2': 'أسعار العقارات تختلف بشكل كبير للمساحات المختلفة',
        'horizontal_explanation3': 'المساحة ليست عاملاً حاسماً رئيسياً للسعر',
        'medium_explanation': 'توجد **علاقة خطية معينة** بين المساحة والسعر',
        'medium_explanation2': 'المساحة يمكن أن تفسر جزئياً تغيرات السعر',
        'medium_explanation3': 'لكن لا تزال هناك عوامل مهمة أخرى تؤثر على السعر',
        'strong_explanation': 'توجد **علاقة خطية واضحة** بين المساحة والسعر',
        'strong_explanation2': 'المساحة هي أحد العوامل الحاسمة الرئيسية للسعر',
        'strong_explanation3': 'يمكن استخدام المساحة للتنبؤ بالسعر (بدقة معينة)',
        'by_property_type': '🏠 التحليل حسب نوع العقار',
        'property_type': 'نوع العقار',
        'type_correlation_note': 'قد يختلف الارتباط حسب نوع العقار. في الرسم البياني أدناه، تمثل الألوان المختلفة أنواع عقارات مختلفة.',
        'scatter_plot': '📊 مخطط مبعثر',
        'overall_trendline': 'خط الاتجاه الشامل',
        'type_trendline': 'خط الاتجاه',
        'trendline_note': 'تمثل الألوان المختلفة أنواع عقارات مختلفة. الخط الأحمر المتقطع هو خط الاتجاه لجميع البيانات. فقط الأنواع ذات الارتباط القوي بما فيه الكفاية (|r| ≥ 0.3) تعرض خط الاتجاه الخاص بها.',
        'trendline_note_weak': 'تمثل الألوان المختلفة أنواع عقارات مختلفة. نظراً لأن الارتباط الشامل ضعيف (|r| < 0.3)، لم يتم عرض خط الاتجاه.',
        'trendline_note_simple': 'الخط الأحمر المتقطع** هو خط الاتجاه للانحدار الخطي، يوضح العلاقة الخطية بين المساحة والسعر.',
        'trendline_note_no': 'نظراً لأن الارتباط ضعيف (|r| < 0.3)، لم يتم عرض خط الاتجاه لأن العلاقة الخطية ليست واضحة.',
        'correlation_coefficient': 'معامل الارتباط الشامل r',
        'q11_title': 'Q11: ارتباط المساحة المبنية مقابل قيمة العقار',
        # Q12 相关
        'q12_analysis_purpose': '📊 هدف التحليل',
        'q12_analysis_description': 'يهدف هذا التحليل إلى مقارنة متوسطات المساحات الأرضية حسب **طبيعة الأرض** (سكني، تجاري، إلخ).',
        'q12_research_questions': 'أسئلة البحث:',
        'q12_research_q1': 'أي طبيعة أرض لديها أكبر متوسط مساحة؟',
        'q12_research_q2': 'كيف تختلف المساحات بين الطبيعة المختلفة؟',
        'q12_research_q3': 'هل تؤثر طبيعة الأرض على حجم المساحة؟',
        'q12_expected_results': 'النتائج المتوقعة:',
        'q12_expected_difference': 'تعكس اختلافات متوسط المساحة بين طبيعة الأرض متطلبات الاستخدام والتخطيط المختلفة.',
        'q12_expected_usage': 'يساعد فهم متوسطات المساحة حسب طبيعة الأرض في فهم أنماط استخدام الأراضي وخصائص التخطيط.',
        'q12_key_insights': 'الرؤى الرئيسية:',
        'q12_insight1': 'تعكس طبيعة الأرض الاستخدامات ومتطلبات التخطيط المختلفة',
        'q12_insight2': 'قد تتأثر اختلافات المساحة بين الطبيعة بسياسات التخطيط واحتياجات الاستخدام وعوامل أخرى',
        'q12_insight3': 'يساعد تحليل متوسط المساحة في فهم كفاءة استخدام الأراضي وخصائص التخطيط',
        'q12_statistics': '📈 الإحصائيات',
        'q12_land_types': 'عدد أنواع الأراضي',
        'q12_largest_avg_area': 'أكبر متوسط مساحة',
        'q12_smallest_avg_area': 'أصغر متوسط مساحة',
        'q12_area_range': 'نطاق المساحة',
        'q12_comparison_chart': '📊 مخطط المقارنة',
        'q12_title': 'Q12: متوسط مساحة الأرض حسب طبيعة الأرض',
        # Q13 相关
        'q13_analysis_purpose': '📊 هدف التحليل',
        'q13_analysis_description': 'يهدف هذا التحليل إلى تحليل **الاتجاهات الزمنية لأسعار المتوسطة** لفهم تقلبات أسعار السوق.',
        'q13_research_questions': 'أسئلة البحث:',
        'q13_research_q1': 'هل يتغير متوسط السعر بمرور الوقت؟',
        'q13_research_q2': 'هل هناك اتجاه لزيادة أو انخفاض الأسعار؟',
        'q13_research_q3': 'هل لتقلبات الأسعار أنماط؟',
        'q13_expected_results': 'النتائج المتوقعة:',
        'q13_expected_trend': 'يساعد تحليل اتجاه السعر في فهم تحركات السوق وهو مرجع مهم للاستثمار والقرارات.',
        'q13_expected_volatility': 'قد تعكس تقلبات الأسعار تأثير تغيرات العرض والطلب والدورات الاقتصادية وعوامل أخرى.',
        'q13_key_insights': 'الرؤى الرئيسية:',
        'q13_insight1': 'تعكس اتجاهات الأسعار علاقات العرض والطلب في السوق وتوقعات المستثمرين',
        'q13_insight2': 'قد تتأثر تقلبات الأسعار بالدورات الاقتصادية وتعديلات السياسات ومشاعر السوق وغيرها',
        'q13_insight3': 'تساعد اتجاهات الأسعار طويلة الأجل في الحكم على اتجاه تطور السوق وتوقيت الاستثمار',
        'q13_statistics': '📈 الإحصائيات',
        'q13_months': 'عدد الأشهر',
        'q13_highest_avg_price': 'أعلى متوسط سعر',
        'q13_lowest_avg_price': 'أدنى متوسط سعر',
        'q13_current_avg_price': 'متوسط السعر الحالي',
        'q13_trend_chart': '📊 مخطط الاتجاه',
        'q13_title': 'Q13: تطور متوسط السعر الشهري',
        # Q14 相关
        'q14_analysis_purpose': '📊 هدف التحليل',
        'q14_analysis_description': 'يهدف هذا التحليل إلى مقارنة إحصائيات الأسعار (المتوسط، الأدنى، الأعلى) حسب **نوع العقار** لفهم توزيع الأسعار بشكل شامل.',
        'q14_research_questions': 'أسئلة البحث:',
        'q14_research_q1': 'أي نوع عقار له أعلى متوسط سعر؟',
        'q14_research_q2': 'ما مدى اختلافات نطاق السعر (من الأدنى إلى الأعلى)؟',
        'q14_research_q3': 'ما هي تقلبات الأسعار حسب النوع؟',
        'q14_expected_results': 'النتائج المتوقعة:',
        'q14_expected_comparison': 'تساعد مقارنة الأسعار في تقييم نطاقات القيمة لأنواع العقارات المختلفة وفهم هيكل أسعار السوق.',
        'q14_expected_range': 'يمكن لتحليل نطاق السعر أن يكشف عن تقلبات الأسعار وتنوع السوق لأنواع العقارات المختلفة.',
        'q14_key_insights': 'الرؤى الرئيسية:',
        'q14_insight1': 'تعكس إحصائيات الأسعار موضع القيمة وأداء السوق لأنواع العقارات المختلفة',
        'q14_insight2': 'قد تعكس اختلافات نطاق السعر تنوع السوق وعلاقات العرض والطلب وعوامل أخرى',
        'q14_insight3': 'يساعد فهم إحصائيات الأسعار في فهم قيمة الاستثمار والمخاطر لأنواع العقارات المختلفة',
        'q14_statistics': '📈 الإحصائيات',
        'q14_property_types': 'عدد الأنواع',
        'q14_highest_avg': 'أعلى متوسط سعر',
        'q14_largest_range': 'أكبر نطاق سعر',
        'q14_price_comparison_chart': '📊 مخطط مقارنة الأسعار',
        'q14_title': 'Q14: مقارنة الأسعار حسب نوع العقار',
        # Q15 相关
        'q15_analysis_purpose': '📊 هدف التحليل',
        'q15_analysis_description': 'يهدف هذا التحليل إلى مقارنة توزيعات أسعار **المنازل والشقق** لفهم الاختلافات في الأسعار بين نوعي العقارات الرئيسيين.',
        'q15_research_questions': 'أسئلة البحث:',
        'q15_research_q1': 'ما هو الفرق في توزيع الأسعار بين المنازل والشقق؟',
        'q15_research_q2': 'أي نوع له أسعار أعلى؟',
        'q15_research_q3': 'هل تظهر توزيعات الأسعار أنماطاً مختلفة؟',
        'q15_expected_results': 'النتائج المتوقعة:',
        'q15_expected_comparison': 'تساعد مقارنة أسعار المنازل والشقق في فهم موضع السوق والاختلافات في القيمة بين أنواع العقارات المختلفة.',
        'q15_expected_distribution': 'قد تعكس أنماط توزيع الأسعار المجموعات المستهدفة وخصائص السوق لأنواع العقارات المختلفة.',
        'q15_key_insights': 'الرؤى الرئيسية:',
        'q15_insight1': 'تعكس توزيعات أسعار المنازل والشقق مواضع السوق والمجموعات المستهدفة المختلفة',
        'q15_insight2': 'قد تتأثر اختلافات الأسعار بالموقع والمساحة والجودة والطلب وعوامل أخرى',
        'q15_insight3': 'يساعد فهم توزيعات الأسعار في فهم قيمة الاستثمار وخصائص السوق لأنواع العقارات المختلفة',
        'q15_statistics': '📈 الإحصائيات',
        'q15_total_properties': 'إجمالي العقارات',
        'q15_houses': 'عدد المنازل',
        'q15_apartments': 'عدد الشقق',
        'q15_house_median': 'السعر الوسيط للمنازل',
        'q15_apartment_median': 'السعر الوسيط للشقق',
        'q15_distribution_chart': '📊 مخطط التوزيع',
        'q15_title': 'Q15: توزيع الأسعار - المنازل مقابل الشقق',
        # Q16 相关
        'q16_analysis_purpose': '📊 هدف التحليل',
        'q16_analysis_description': 'يهدف هذا التحليل إلى حساب **نسبة مساحة الأرض إلى المساحة المبنية** لفهم استخدام الأراضي في مدن مختلفة.',
        'q16_research_questions': 'أسئلة البحث:',
        'q16_research_q1': 'أي المدن لديها أعلى نسبة أرض/مبني؟',
        'q16_research_q2': 'ماذا تعكس اختلافات النسبة؟',
        'q16_research_q3': 'ما مدى كفاءة استخدام الأراضي؟',
        'q16_expected_results': 'النتائج المتوقعة:',
        'q16_expected_ratio': 'تعكس نسبة الأرض/المبني كثافة استخدام الأراضي، المناطق ذات النسب العالية قد يكون لديها مساحة أرض أكبر.',
        'q16_expected_efficiency': 'يساعد فهم نسب استخدام الأراضي في فهم خصائص التخطيط وأنماط التنمية لمدن مختلفة.',
        'q16_key_insights': 'الرؤى الرئيسية:',
        'q16_insight1': 'تعكس نسبة الأرض/المبني كثافة استخدام الأراضي وكثافة التنمية',
        'q16_insight2': 'المناطق ذات النسب العالية قد يكون لديها مساحة أرض أكبر، مناسبة للتنمية منخفضة الكثافة',
        'q16_insight3': 'قد تعكس اختلافات النسبة سياسات التخطيط الحضري وإمدادات الأراضي وعوامل أخرى',
        'q16_statistics': '📈 الإحصائيات',
        'q16_cities_shown': 'عدد المدن المعروضة',
        'q16_highest_ratio': 'أعلى نسبة',
        'q16_lowest_ratio': 'أدنى نسبة',
        'q16_avg_ratio': 'متوسط النسبة',
        'q16_ranking_chart': '📊 مخطط الترتيب',
        'q16_title': 'Q16: نسبة الأرض/المساحة المبنية أعلى 10',
        # Q17 相关
        'q17_analysis_purpose': '📊 هدف التحليل',
        'q17_analysis_description': 'يهدف هذا التحليل إلى تحليل **عدد العقارات لكل معاملة** لفهم تعقيد المعاملات.',
        'q17_research_questions': 'أسئلة البحث:',
        'q17_research_q1': 'كم عدد العقارات التي تحتوي عليها معظم المعاملات؟',
        'q17_research_q2': 'هل المعاملات متعددة العقارات شائعة؟',
        'q17_research_q3': 'ما هو توزيع تعقيد المعاملات؟',
        'q17_expected_results': 'النتائج المتوقعة:',
        'q17_expected_complexity': 'يعكس عدد العقارات لكل معاملة تعقيد المعاملة، مما قد يؤثر على عملية المعاملة والسعر.',
        'q17_expected_pattern': 'يساعد فهم توزيع تعقيد المعاملات في فهم أنماط وخصائص معاملات السوق.',
        'q17_key_insights': 'الرؤى الرئيسية:',
        'q17_insight1': 'يعكس تعقيد المعاملات أنماط وخصائص معاملات السوق',
        'q17_insight2': 'قد تتضمن المعاملات متعددة العقارات معاملات مجمعة ومحافظ استثمارية وحالات خاصة أخرى',
        'q17_insight3': 'قد يؤثر تعقيد المعاملات على عملية المعاملة ومفاوضات الأسعار وعوامل أخرى',
        'q17_statistics': '📈 الإحصائيات',
        'q17_total_transactions': 'إجمالي المعاملات',
        'q17_most_common_count': 'عدد العقارات الأكثر شيوعاً',
        'q17_max_properties': 'الحد الأقصى للعقارات لكل معاملة',
        'q17_avg_properties': 'متوسط عدد العقارات',
        'q17_distribution_chart': '📊 مخطط التوزيع',
        'q17_title': 'Q17: عدد العقارات لكل معاملة',
        # Q18 相关
        'q18_analysis_purpose': '📊 هدف التحليل',
        'q18_analysis_description': 'يهدف هذا التحليل إلى إحصاء **العقارات ذات الأرض وبدون أرض** لفهم خصائص أنواع العقارات المختلفة.',
        'q18_research_questions': 'أسئلة البحث:',
        'q18_research_q1': 'أي نوع عقار من المرجح أن يكون لديه أرض؟',
        'q18_research_q2': 'ما هي نسبة العقارات ذات الأرض وبدون أرض؟',
        'q18_research_q3': 'هل تؤثر الأرض على نوع العقار؟',
        'q18_expected_results': 'النتائج المتوقعة:',
        'q18_expected_characteristics': 'تعكس ملكية الأرض اكتمال العقار وقيمته، مؤشر مهم لخصائص العقار.',
        'q18_expected_distribution': 'يساعد فهم توزيع الأراضي في فهم خصائص وموضع السوق لأنواع العقارات المختلفة.',
        'q18_key_insights': 'الرؤى الرئيسية:',
        'q18_insight1': 'تعكس ملكية الأرض اكتمال العقار وقيمته',
        'q18_insight2': 'قد تختلف معدلات ملكية الأرض بشكل كبير حسب نوع العقار',
        'q18_insight3': 'الأرض هي مكون مهم من قيمة العقار، تؤثر على موضع السوق',
        'q18_statistics': '📈 الإحصائيات',
        'q18_property_types': 'عدد أنواع العقارات',
        'q18_total_with_land': 'إجمالي مع أرض',
        'q18_total_without_land': 'إجمالي بدون أرض',
        'q18_land_ownership_rate': 'معدل ملكية الأرض',
        'q18_comparison_chart': '📊 مخطط المقارنة',
        'q18_title': 'Q18: إحصائيات العقارات مع/بدون أرض',
        # Q19 相关
        'q19_analysis_purpose': '📊 هدف التحليل',
        'q19_analysis_description': 'يهدف هذا التحليل إلى تحليل **توزيع المعاملات حسب يوم الأسبوع** لفهم أنماط وقت المعاملات.',
        'q19_research_questions': 'أسئلة البحث:',
        'q19_research_q1': 'أي يوم من الأسبوع لديه أكبر عدد من المعاملات؟',
        'q19_research_q2': 'هل توجد اختلافات بين أيام الأسبوع وعطلة نهاية الأسبوع؟',
        'q19_research_q3': 'هل لأوقات المعاملات أنماط؟',
        'q19_expected_results': 'النتائج المتوقعة:',
        'q19_expected_pattern': 'قد يعكس توزيع تاريخ المعاملة أنماط سلوك السوق، مثل المعاملات الأكثر نشاطاً في أيام الأسبوع.',
        'q19_expected_behavior': 'يساعد فهم أنماط وقت المعاملات في فهم أنماط تشغيل السوق وعادات المعاملات.',
        'q19_key_insights': 'الرؤى الرئيسية:',
        'q19_insight1': 'يعكس توزيع تاريخ المعاملة أنماط سلوك السوق وعادات العمل',
        'q19_insight2': 'قد تعكس اختلافات حجم المعاملات بين أيام الأسبوع وعطلة نهاية الأسبوع أنماط تشغيل السوق',
        'q19_insight3': 'قد تتأثر أنماط وقت المعاملات بالإجراءات القانونية وساعات العمل وعوامل أخرى',
        'q19_statistics': '📈 الإحصائيات',
        'q19_total_transactions': 'إجمالي المعاملات',
        'q19_most_active_day': 'أكثر يوم نشاطاً',
        'q19_least_active_day': 'أقل يوم نشاطاً',
        'q19_weekday_avg': 'متوسط أيام الأسبوع',
        'q19_distribution_chart': '📊 مخطط التوزيع',
        'q19_title': 'Q19: توزيع المعاملات الأسبوعي',
        # Q20 相关
        'q20_analysis_purpose': '📊 هدف التحليل',
        'q20_analysis_description': 'يهدف هذا التحليل إلى تحليل **حجم المعاملات الأسبوعي وإجمالي قيمة المعاملات** لفهم اتجاهات السوق الأسبوعية.',
        'q20_research_questions': 'أسئلة البحث:',
        'q20_research_q1': 'هل يتغير حجم المعاملات وإجمالي القيمة بشكل متزامن؟',
        'q20_research_q2': 'هل توجد أنماط دورية؟',
        'q20_research_q3': 'كيف تتقلب نشاطات السوق؟',
        'q20_expected_results': 'النتائج المتوقعة:',
        'q20_expected_analysis': 'يمكن أن يساعد التحليل الأسبوعي في تحديد الاتجاهات قصيرة الأجل والأنماط الدورية في السوق.',
        'q20_expected_trends': 'يمكن أن تعكس اتجاهات حجم المعاملات وإجمالي القيمة نشاط السوق العام وتغيرات القيمة.',
        'q20_key_insights': 'الرؤى الرئيسية:',
        'q20_insight1': 'يمكن أن يكشف التحليل الأسبوعي عن الاتجاهات قصيرة الأجل والأنماط الدورية في السوق',
        'q20_insight2': 'يعكس تزامن حجم المعاملات وإجمالي القيمة نشاط السوق العام',
        'q20_insight3': 'قد تتأثر الأنماط الدورية بالعوامل الموسمية وأحداث السوق وغيرها',
        'q20_statistics': '📈 الإحصائيات',
        'q20_weeks': 'عدد الأسابيع',
        'q20_total_transactions': 'إجمالي المعاملات',
        'q20_total_volume': 'إجمالي قيمة المعاملات',
        'q20_avg_transactions_per_week': 'متوسط المعاملات لكل أسبوع',
        'q20_avg_volume_per_week': 'متوسط القيمة لكل أسبوع',
        'q20_trend_chart': '📊 مخطط الاتجاه الأسبوعي',
        'q20_title': 'Q20: تحليل حجم المعاملات الأسبوعي',
    },
    'mg': {
        'app_title': '🏠 Platforma Fikarohana angon-drakitra DVF',
        'db_config': '⚙️ Fikirakirana Database',
        'db_settings': '🔧 Fikirakirana Fifandraisana Database',
        'db_tip': '💡 **Torolalana**: Azonao ampiasaina ny mpampiasa root, tsy mila mamorona userP6',
        'host': 'Adiresy Server',
        'host_help': 'Adiresy server MySQL (localhost dia midika fifandraisana eo an-toerana)',
        'user': 'Anaran\'mpampiasa',
        'user_help': 'Anaran\'mpampiasa MySQL (azonao ampiasaina ny root na mpampiasa hafa efa misy)',
        'password': 'Tenimiafina',
        'password_help': 'Tenimiafina MySQL (tenimiafina ny mpampiasa root)',
        'database': 'Anaran\'ny Database',
        'database_help': 'Anaran\'ny database hifandraisana aminy',
        'database_label': 'Database',
        'analysis_selection': '📊 Fidiana Fanontaniana Fikarohana',
        'select_question': 'Fidio ny fanontaniana fikarohana ho hitan\'ny:',
        'select_question_label': 'Fidio ny fanontaniana:',
        'db_status_check': '🔍 Fijerena ny toetry ny Database',
        'db_connected': '✅ Nahomby ny fifandraisana amin\'ny database',
        'tip_chart': '💡 Torolalana: Kitiho ny sary mba hanitatra, hanetsika ary handefa',
        'data_source': 'Loharanon\'ny angon-drakitra',
        'view_data': '📊 Hijery ny angon-drakitra',
        'data_summary': 'Famintinana ny angon-drakitra',
        'raw_data': '📋 Hijery ny angon-drakitra tsy voahodina',
        'database': 'Database',
        'rows': 'andalana',
        # Error messages
        'db_auth_failed': '❌ **Tsy nahomby ny fanamarinana ny database!**',
        'db_not_found': '❌ **Tsy hita ny database!**',
        'db_connect_failed': '❌ **Tsy afaka mifandray amin\'ny server MySQL!**',
        'query_error': '❌ Fahadisoana amin\'ny fandehanana ny query',
        'empty_result': '⚠️ Niverina tsy misy valiny ny query!',
        'table_empty': 'Tsy misy zavatra ao amin\'ny tabilao',
        'table_not_found': 'Tsy misy ny tabilao na tsy azo idirana',
        'check_db_error': 'Fahadisoana rehefa mijery ny toetry ny database',
        # Diagnostic steps
        'diagnostic_steps': '🔍 Dingana Fitsaboana',
        'check_mysql_service': 'Jereo raha mihazakazaka ny service MySQL',
        'verify_connection': 'Hamarinina ny fampahalalana fifandraisana database',
        'check_permissions': 'Jereo ny alalana ny mpampiasa',
        'confirm_db_created': 'Hamarinina fa voaforona ny database',
        # Possible reasons
        'possible_reasons': 'Antony mety:',
        'username_password_wrong': 'Diso ny anaran\'mpampiasa na ny tenimiafina',
        'user_not_exists': 'Tsy misy ny mpampiasa',
        'no_access': 'Tsy manana alalana ny mpampiasa',
        'service_not_running': 'Tsy mihazakazaka ny service MySQL',
        'host_port_wrong': 'Diso ny adiresy server na ny port',
        # Solutions
        'solutions': 'Vahaolana:',
        'check_credentials': 'Jereo raha marina ny anaran\'mpampiasa sy ny tenimiafina',
        'confirm_mysql_running': 'Hamarinina fa mihazakazaka ny service MySQL',
        'test_connection': 'Andramo ny fifandraisana amin\'ny MySQL Workbench na ny command line',
        'create_user': 'Raha mila mamorona mpampiasa, alefaso:',
        'check_service': 'Jereo raha mihazakazaka ny service MySQL',
        'check_firewall': 'Jereo ny fikirakirana firewall',
        # Data related
        'data_points': 'Tehaka angon-drakitra',
        'correlation': 'Coefficient de corrélation',
        'avg_area': 'Velarany antonony',
        'avg_price': 'Vidiny antonony',
        'table_exists': 'Misy ny tabilao',
        'total_rows': 'Isan\'ny andalana ao amin\'ny tabilao',
        'no_data_rows': 'Isan\'ny andalana misy angon-drakitra',
        'view_query': '🔍 Hijery ny query',
        'possible_causes': 'Antony mety:',
        'no_data_in_db': 'Tsy misy angon-drakitra ao amin\'ny database (tsy misy zavatra ao amin\'ny tabilao)',
        'data_not_imported': 'Mbola tsy voafindra ny angon-drakitra ao amin\'ny database',
        'table_mismatch': 'Tsy mifanaraka ny firafitry ny tabilao na tsy misy ny tabilao',
        'solution_check_data': 'Jereo raha misy angon-drakitra ao amin\'ny database',
        'solution_import_data': 'Raha tsy misy angon-drakitra, alefaso aloha ny `create_tab.sql` mba hampiditra angon-drakitra',
        # Q1 相关
        'q1_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q1_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **tendances ara-potoana** amin\'ny **isan\'ny fifanakalozana trano** mba hahatakatra ny fahavitrihan\'ny tsena sy ny fiovan\'ny tsingerina.',
        'q1_research_questions': 'Fanontaniana fikarohana:',
        'q1_research_q1': 'Mihabetsaka na mihena ve ny isan\'ny fifanakalozana rehefa mandeha ny fotoana?',
        'q1_research_q2': 'Misy lamina ara-taona ve?',
        'q1_research_q3': 'Inona ny volana izay mavitrika indrindra amin\'ny fifanakalozana?',
        'q1_expected_results': 'Vokatra azo antenaina:',
        'q1_expected_trend': 'Amin\'ny fijerena ny tendances amin\'ny isan\'ny fifanakalozana, azontsika atao ny mahatakatra ny fahavitrihana sy ny lamina tsingerina amin\'ny tsena trano.',
        'q1_expected_seasonal': 'Raha misy lamina ara-taona, azontsika atao ny maminavina ny fiovan\'ny habetsaky ny fifanakalozana amin\'ny ho avy.',
        'q1_key_insights': 'Fahitana lehibe:',
        'q1_insight1': 'Ny fiovan\'ny isan\'ny fifanakalozana dia maneho ny fifandraisan\'ny tsena amin\'ny fividianana sy ny fivarotana ary ny fahatokian\'ny mpampiasa vola',
        'q1_insight2': 'Ny lamina ara-taona dia mety ho voakasiky ny fety, ny fanitsiana ny politika, sns.',
        'q1_insight3': 'Ny tendances lavalava dia afaka manampy amin\'ny fitsarana ny làlan\'ny fivoaran\'ny tsena',
        'q1_statistics': '📈 Statistika',
        'q1_total_transactions': 'Total fifanakalozana',
        'q1_avg_per_month': 'Moyenne isam-bolana',
        'q1_most_active_month': 'Volana mavitrika indrindra',
        'q1_trend_chart': '📊 Sary tendance',
        'q1_title': 'Q1: Fivoaran\'ny isan\'ny fifanakalozana isam-bolana',
        # Q2 相关
        'q2_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q2_analysis_description': 'Ity fikarohana ity dia mikendry ny hahatakatra ny fizarana ny trano amin\'ny **sokajy vidiny** samihafa mba hamantarana ny sokajy vidiny lehibe amin\'ny tsena.',
        'q2_research_questions': 'Fanontaniana fikarohana:',
        'q2_research_q1': 'Inona ny sokajy vidiny izay manana fifanakalozana betsaka indrindra?',
        'q2_research_q2': 'Maneho lamina manokana ve ny fizarana ny vidiny?',
        'q2_research_q3': 'Inona ny ampahany eo amin\'ny tsena avo sy ny tsena ambany?',
        'q2_expected_results': 'Vokatra azo antenaina:',
        'q2_expected_distribution': 'Ny fizarana ny vidiny dia afaka manampy amin\'ny famantarana ny sokajy fangatahana lehibe sy ny hahatakatra ny fahombiazan\'ny tsena amin\'ny ambaratonga vidiny samihafa.',
        'q2_expected_segments': 'Amin\'ny fikarohana ny fizarana ny sokajy vidiny, azontsika atao ny mahatakatra ny firafitry ny vidiny sy ny hery fividianan\'ny mpanjifa.',
        'q2_key_insights': 'Fahitana lehibe:',
        'q2_insight1': 'Ny fizarana ny vidiny dia maneho ny fifandanjana amin\'ny tsena amin\'ny fividianana sy ny fivarotana ary ny hery fividianan\'ny mpanjifa',
        'q2_insight2': 'Ny sokajy vidiny lehibe dia mety maneho ny ambaratonga ara-toekarena eo an-toerana sy ny toetra amin\'ny tsena',
        'q2_insight3': 'Ny fifantohan\'ny sokajy vidiny dia afaka manambara ny safidiny amin\'ny vidiny amin\'ny tsena',
        'q2_statistics': '📈 Statistika',
        'q2_total_mutations': 'Total fifanakalozana',
        'q2_price_ranges': 'Isan\'ny sokajy',
        'q2_most_common_range': 'Sokajy mahazatra indrindra',
        'q2_avg_per_range': 'Moyenne isaky ny sokajy',
        'q2_distribution_chart': '📊 Sary fizarana',
        'q2_title': 'Q2: Fizarana ny sokajy vidiny',
        # Q3 相关
        'q3_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q3_analysis_description': 'Ity fikarohana ity dia mikendry ny hampitaha ny vidiny antonony amin\'ny **karazana fifanakalozana** samihafa (toy ny fivarotana, fifanakalozana, sns.) mba hahatakatra ny fiantraikan\'ny karazana fifanakalozana amin\'ny vidiny.',
        'q3_research_questions': 'Fanontaniana fikarohana:',
        'q3_research_q1': 'Inona ny karazana fifanakalozana izay manana vidiny antonony avo indrindra?',
        'q3_research_q2': 'Ahoana ny habetsaky ny fahasamihafan\'ny vidiny eo amin\'ny karazana fifanakalozana samihafa?',
        'q3_research_q3': 'Miantraika ve ny karazana fifanakalozana amin\'ny sandan\'ny trano?',
        'q3_expected_results': 'Vokatra azo antenaina:',
        'q3_expected_difference': 'Ny fahasamihafan\'ny vidiny eo amin\'ny karazana fifanakalozana dia mety maneho ny fahasamihafan\'ny fitondran-tenan\'ny tsena, ny politika hetra, na ny antony fifanakalozana.',
        'q3_expected_impact': 'Ny fahatakarana ny fiantraikan\'ny karazana fifanakalozana amin\'ny vidiny dia manampy amin\'ny fahatakarana ny mekanisma amin\'ny tsena sy ny toetra amin\'ny fifanakalozana.',
        'q3_key_insights': 'Fahitana lehibe:',
        'q3_insight1': 'Ny karazana fifanakalozana dia mety maneho antony fifanakalozana samihafa sy toe-javatra amin\'ny tsena samihafa',
        'q3_insight2': 'Ny fahasamihafan\'ny vidiny dia mety ho voakasiky ny politika hetra, ny vidin\'ny fifanakalozana, sns.',
        'q3_insight3': 'Ny karazana fifanakalozana sasany dia mety tsara kokoa amin\'ny trano ao amin\'ny sokajy vidiny manokana',
        'q3_statistics': '📈 Statistika',
        'q3_transaction_types': 'Isan\'ny karazana',
        'q3_highest_avg_price': 'Vidiny antonony avo indrindra',
        'q3_lowest_avg_price': 'Vidiny antonony ambany indrindra',
        'q3_price_difference': 'Fahasamihafan\'ny vidiny',
        'q3_comparison_chart': '📊 Sary fampitahana',
        'q3_title': 'Q3: Vidiny antonony amin\'ny karazana fifanakalozana',
        # Q4 相关
        'q4_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q4_analysis_description': 'Ity fikarohana ity dia mikendry ny hahatakatra ny fizarana ara-pahamaroan\'ny **karazana trano** samihafa (toy ny efitrano, trano, sns.) amin\'ny tsena.',
        'q4_research_questions': 'Fanontaniana fikarohana:',
        'q4_research_q1': 'Inona ny karazana trano izay mahazatra indrindra?',
        'q4_research_q2': 'Ahoana ny anjara amin\'ny tsena amin\'ny karazana trano samihafa?',
        'q4_research_q3': 'Mifantoka ve ny tsena amin\'ny karazana manokana?',
        'q4_expected_results': 'Vokatra azo antenaina:',
        'q4_expected_distribution': 'Ny fizarana ny karazana trano dia maneho ny firafitry ny fangatahana sy ny famatsiana amin\'ny tsena, manampy amin\'ny fahatakarana ny toetra amin\'ny tsena.',
        'q4_expected_market': 'Ny fahatakarana ny fizarana ny karazana trano dia afaka manampy amin\'ny famantarana ny karazana famatsiana lehibe sy ny safidiny amin\'ny fangatahana amin\'ny tsena.',
        'q4_key_insights': 'Fahitana lehibe:',
        'q4_insight1': 'Ny fizarana ny karazana trano dia maneho ny firafitry ny fangatahana sy ny famatsiana amin\'ny tsena',
        'q4_insight2': 'Ny ampahany amin\'ny karazana samihafa dia mety ho voakasiky ny toerana ara-jeografika, ny drafitry ny tanàna, sns.',
        'q4_insight3': 'Ny fizarana ny karazana tsena dia afaka manampy amin\'ny fahatakarana ny toetra amin\'ny tsena trano eo an-toerana',
        'q4_statistics': '📈 Statistika',
        'q4_total_properties': 'Total trano',
        'q4_property_types': 'Isan\'ny karazana',
        'q4_most_common_type': 'Karazana mahazatra indrindra',
        'q4_distribution_chart': '📊 Sary fizarana',
        'q4_title': 'Q4: Fizarana ny karazana trano',
        # Q5 相关
        'q5_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q5_analysis_description': 'Ity fikarohana ity dia mikendry ny hikajy ny **vidiny antonony isaky ny metatra toradroa** sy ny hampitaha ny fahasamihafan\'ny vidiny isaky ny metatra toradroa amin\'ny karazana trano samihafa.',
        'q5_research_questions': 'Fanontaniana fikarohana:',
        'q5_research_q1': 'Inona ny karazana trano izay manana vidiny isaky ny metatra toradroa avo indrindra?',
        'q5_research_q2': 'Ahoana ny vidiny isaky ny metatra toradroa amin\'ny karazana trano samihafa?',
        'q5_research_q3': 'Ara-drariny ve ny fahasamihafan\'ny vidiny isaky ny metatra toradroa?',
        'q5_expected_results': 'Vokatra azo antenaina:',
        'q5_expected_price': 'Ny fikarohana ny vidiny isaky ny metatra toradroa dia afaka manampy amin\'ny fanombanana ny sandan\'ny karazana trano samihafa, ary dia famantarana manan-danja amin\'ny fanapahan-kevitra fampiasam-bola.',
        'q5_expected_comparison': 'Amin\'ny fampitahana ny vidiny isaky ny metatra toradroa, azontsika atao ny mahatakatra ny toerana sandan\'ny karazana trano samihafa sy ny mety fampiasam-bola.',
        'q5_key_insights': 'Fahitana lehibe:',
        'q5_insight1': 'Ny vidiny isaky ny metatra toradroa dia famantarana manan-danja amin\'ny fanombanana ny sandan\'ny trano, maneho ny sandan\'ny velarany isaky ny metatra toradroa',
        'q5_insight2': 'Ny fahasamihafan\'ny vidiny isaky ny metatra toradroa amin\'ny karazana trano samihafa dia mety ho voakasiky ny toerana, ny kalitao, ny fangatahana, sns.',
        'q5_insight3': 'Ny fikarohana ny vidiny isaky ny metatra toradroa dia manampy amin\'ny fahatakarana ny sandan\'ny fampiasam-bola sy ny toerana amin\'ny tsena amin\'ny karazana trano samihafa',
        'q5_statistics': '📈 Statistika',
        'q5_property_types': 'Isan\'ny karazana',
        'q5_highest_price_m2': 'Vidiny isaky ny metatra toradroa avo indrindra',
        'q5_lowest_price_m2': 'Vidiny isaky ny metatra toradroa ambany indrindra',
        'q5_avg_price_m2': 'Vidiny isaky ny metatra toradroa antonony',
        'q5_price_comparison_chart': '📊 Sary fampitahana vidiny',
        'q5_title': 'Q5: Vidiny isaky ny metatra toradroa (amin\'ny karazana)',
        # Q6 相关
        'q6_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q6_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **fizarana ny isan\'ny efitrano** amin\'ny trano mba hahatakatra ny karazana trano mahazatra indrindra amin\'ny tsena.',
        'q6_research_questions': 'Fanontaniana fikarohana:',
        'q6_research_q1': 'Firy ny efitrano izay mahazatra indrindra?',
        'q6_research_q2': 'Maneho lamina manokana ve ny fizarana ny isan\'ny efitrano?',
        'q6_research_q3': 'Inona ny safidiny amin\'ny tsena?',
        'q6_expected_results': 'Vokatra azo antenaina:',
        'q6_expected_distribution': 'Ny fizarana ny isan\'ny efitrano dia maneho ny fangatahana amin\'ny tsena sy ny firafitry ny fianakaviana, manampy amin\'ny fahatakarana ny safidiny amin\'ny mpividy.',
        'q6_expected_market': 'Ny fahatakarana ny karazana trano mahazatra dia manampy amin\'ny fahatakarana ny fangatahana marina sy ny firafitry ny famatsiana amin\'ny tsena.',
        'q6_key_insights': 'Fahitana lehibe:',
        'q6_insight1': 'Ny fizarana ny isan\'ny efitrano dia maneho ny fangatahana amin\'ny tsena sy ny firafitry ny fianakaviana',
        'q6_insight2': 'Ny trano misy isan\'efitra samihafa dia mety manantena vondrona samihafa (mpitokana, fianakaviana, sns.)',
        'q6_insight3': 'Ny karazana trano mahazatra dia mety maneho ny firafitry ny mponina eo an-toerana sy ny fomba fiaina',
        'q6_statistics': '📈 Statistika',
        'q6_total_properties': 'Total trano',
        'q6_room_count_range': 'Sokajy isan\'efitra',
        'q6_most_common_rooms': 'Isan\'efitra mahazatra indrindra',
        'q6_avg_rooms': 'Isan\'efitra antonony',
        'q6_distribution_chart': '📊 Sary fizarana',
        'q6_title': 'Q6: Fizarana ny isan\'ny efitrano',
        # Q7 相关
        'q7_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q7_analysis_description': 'Ity fikarohana ity dia mikendry ny hamantarana ny **tanàna manana habetsaky ny fifanakalozana lehibe indrindra** mba hahatakatra ny faritra mafana amin\'ny tsena trano.',
        'q7_research_questions': 'Fanontaniana fikarohana:',
        'q7_research_q1': 'Inona ny tanàna izay mavitrika indrindra amin\'ny fifanakalozana?',
        'q7_research_q2': 'Mifantoka ve ny fifanakalozana amin\'ny tanàna sasany?',
        'q7_research_q3': 'Inona ny fahasamihafan\'ny habetsaky ny eo amin\'ny tanàna?',
        'q7_expected_results': 'Vokatra azo antenaina:',
        'q7_expected_ranking': 'Ny filaharana ny habetsaky ny fifanakalozana dia manampy amin\'ny famantarana ny faritra mafana amin\'ny tsena sy ny hahatakarana ny fahavitrihan\'ny trano amin\'ny tanàna samihafa.',
        'q7_expected_concentration': 'Ny fifantohan\'ny habetsaky ny fifanakalozana dia mety maneho ny fahavitrihan\'ny ara-toekarena sy ny ambaratongan\'ny fivoaran\'ny tsena trano amin\'ny tanàna.',
        'q7_key_insights': 'Fahitana lehibe:',
        'q7_insight1': 'Ny filaharana ny habetsaky ny fifanakalozana dia maneho ny fahavitrihan\'ny tsena trano amin\'ny tanàna samihafa',
        'q7_insight2': 'Ny tanàna misy fifantohan\'ny fifanakalozana avo dia mety ho ivon-toekarena na faritra mafana amin\'ny fivoarana',
        'q7_insight3': 'Ny fahasamihafan\'ny habetsaky ny eo amin\'ny tanàna dia mety maneho ny ambaratongan\'ny fivoaran\'ny toekarena sy ny fivezivezen\'ny mponina',
        'q7_statistics': '📈 Statistika',
        'q7_total_transactions': 'Total fifanakalozana',
        'q7_cities_shown': 'Isan\'ny tanàna aseho',
        'q7_most_active_city': 'Tanàna mavitrika indrindra',
        'q7_top_city_transactions': 'Fifanakalozana amin\'ny tanàna voalohany',
        'q7_ranking_chart': '📊 Sary filaharana',
        'q7_title': 'Q7: Tanàna 10 voalohany amin\'ny habetsaky ny fifanakalozana',
        # Q8 相关
        'q8_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q8_analysis_description': 'Ity fikarohana ity dia mikendry ny hampitaha ny vidiny antonony amin\'ny trano amin\'ny **departementa** samihafa mba hahatakatra ny fahasamihafan\'ny vidiny eo amin\'ny faritra.',
        'q8_research_questions': 'Fanontaniana fikarohana:',
        'q8_research_q1': 'Inona ny departementa izay manana vidiny antonony avo indrindra?',
        'q8_research_q2': 'Ahoana ny habetsaky ny fahasamihafan\'ny vidiny eo amin\'ny faritra?',
        'q8_research_q3': 'Maneho lamina ara-jeografika ve ny fizarana ny vidiny?',
        'q8_expected_results': 'Vokatra azo antenaina:',
        'q8_expected_difference': 'Ny fahasamihafan\'ny vidiny eo amin\'ny departementa dia maneho ny ambaratongan\'ny fivoaran\'ny toekarena, ny toerana ara-jeografika, sy ny fangatahana amin\'ny tsena samihafa.',
        'q8_expected_pattern': 'Ny fizarana ny vidiny dia mety maneho lamina ara-jeografika mazava, toy ny vidiny avo kokoa amin\'ny tanàna lehibe.',
        'q8_key_insights': 'Fahitana lehibe:',
        'q8_insight1': 'Ny fahasamihafan\'ny vidiny eo amin\'ny departementa dia maneho ny fiantraikan\'ny ambaratongan\'ny fivoaran\'ny toekarena sy ny toerana ara-jeografika',
        'q8_insight2': 'Ny fahasamihafan\'ny vidiny dia mety ho voakasiky ny haben\'ny tanàna, ny fahavitrihan\'ny ara-toekarena, ny toerana ara-jeografika, sns.',
        'q8_insight3': 'Ny fahatakarana ny fahasamihafan\'ny vidiny ara-paritany dia manampy amin\'ny fahatakarana ny toetra ara-paritany amin\'ny tsena trano',
        'q8_statistics': '📈 Statistika',
        'q8_departments': 'Isan\'ny departementa',
        'q8_highest_avg_price': 'Vidiny antonony avo indrindra',
        'q8_lowest_avg_price': 'Vidiny antonony ambany indrindra',
        'q8_price_range': 'Sokajy vidiny',
        'q8_comparison_chart': '📊 Sary fampitahana',
        'q8_title': 'Q8: Vidiny antonony amin\'ny departementa',
        # Q9 相关
        'q9_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q9_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny habetsaky ny fifanakalozana amin\'ny **faritra kaody paositra** mba hamantarana ny faritra mavitrika manokana.',
        'q9_research_questions': 'Fanontaniana fikarohana:',
        'q9_research_q1': 'Inona ny faritra kaody paositra izay manana fifanakalozana matetika indrindra?',
        'q9_research_q2': 'Mifantoka ve ny habetsaky ny fifanakalozana amin\'ny faritra manokana?',
        'q9_research_q3': 'Inona ny fahasamihafan\'ny fahavitrihana eo amin\'ny faritra?',
        'q9_expected_results': 'Vokatra azo antenaina:',
        'q9_expected_analysis': 'Ny fikarohana amin\'ny ambaratonga kaody paositra dia afaka mamantarana tsara kokoa ny faritra mafana amin\'ny tsena sy ny hahatakarana ny fahavitrihan\'ny tsena kely.',
        'q9_expected_precision': 'Ny fikarohana kaody paositra dia afaka manome fahitana tsena tsara kokoa noho ny ambaratonga tanàna.',
        'q9_key_insights': 'Fahitana lehibe:',
        'q9_insight1': 'Ny fikarohana amin\'ny ambaratonga kaody paositra dia afaka mamantarana ny faritra mafana amin\'ny tsena manokana',
        'q9_insight2': 'Ny faritra misy fifantohan\'ny habetsaky ny fifanakalozana avo dia mety ho ivon-toekarena, faritra fonenana, na faritra fivoarana vaovao',
        'q9_insight3': 'Ny fahasamihafan\'ny fahavitrihana eo amin\'ny faritra dia mety maneho ny toerana ara-jeografika, ny fahafaham-po amin\'ny fitaterana, sns.',
        'q9_statistics': '📈 Statistika',
        'q9_postal_codes_shown': 'Isan\'ny kaody paositra aseho',
        'q9_total_transactions': 'Total fifanakalozana',
        'q9_most_active_code': 'Kaody paositra mavitrika indrindra',
        'q9_top_code_transactions': 'Fifanakalozana amin\'ny faritra voalohany',
        'q9_ranking_chart': '📊 Sary filaharana',
        'q9_title': 'Q9: Kaody paositra 15 voalohany amin\'ny habetsaky ny fifanakalozana',
        # Q10 相关
        'q10_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q10_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **fizarana ny velarany namboarina** mba hahatakatra ny sokajy velarany mahazatra indrindra amin\'ny tsena.',
        'q10_research_questions': 'Fanontaniana fikarohana:',
        'q10_research_q1': 'Inona ny sokajy velarany izay manana trano betsaka indrindra?',
        'q10_research_q2': 'Maneho lamina manokana ve ny fizarana ny velarany?',
        'q10_research_q3': 'Inona ny velarany izay tian\'ny tsena?',
        'q10_expected_results': 'Vokatra azo antenaina:',
        'q10_expected_distribution': 'Ny fizarana ny velarany dia maneho ny fangatahana amin\'ny tsena sy ny filan\'ny mpividy marina, manampy amin\'ny fahatakarana ny toetra amin\'ny tsena.',
        'q10_expected_market': 'Ny fahatakarana ny sokajy velarany mahazatra dia manampy amin\'ny fahatakarana ny fangatahana marina sy ny firafitry ny famatsiana amin\'ny tsena.',
        'q10_key_insights': 'Fahitana lehibe:',
        'q10_insight1': 'Ny fizarana ny velarany dia maneho ny fangatahana amin\'ny tsena sy ny filan\'ny mpividy marina',
        'q10_insight2': 'Ny trano ao amin\'ny sokajy velarany samihafa dia mety manantena vondrona samihafa',
        'q10_insight3': 'Ny sokajy velarany mahazatra dia mety maneho ny ambaratonga fiainana eo an-toerana sy ny fomba fiainana',
        'q10_statistics': '📈 Statistika',
        'q10_total_properties': 'Total trano',
        'q10_surface_ranges': 'Isan\'ny sokajy',
        'q10_most_common_range': 'Sokajy mahazatra indrindra',
        'q10_avg_surface': 'Velarany antonony',
        'q10_distribution_chart': '📊 Sary fizarana',
        'q10_title': 'Q10: Fizarana ny velarany namboarina',
        # Q11 相关
        'analysis_purpose': '📊 Tanjona ny fikarohana',
        'analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny fifandraisana eo amin\'ny **velarany namboarina** sy ny **sandan\'ny trano**.',
        'research_questions': 'Fanontaniana fikarohana:',
        'research_q1': 'Ny trano misy velarany lehibe kokoa dia manana vidiny avo kokoa ve?',
        'research_q2': 'Misy fifandraisana linear ve eo amin\'ny velarany sy ny vidiny?',
        'research_q3': 'Ahoana ny herin\'ity fifandraisana ity?',
        'expected_results': 'Vokatra azo antenaina:',
        'expected_strong': 'Raha mafy ny fifandraisana (r > 0.7): ny velarany dia antony lehibe amin\'ny vidiny',
        'expected_weak': 'Raha malemy ny fifandraisana (r < 0.3): ny vidiny dia voakasiky ny antony hafa (toerana, karazana trano, taona, sns.)',
        'overall_correlation': '📈 Fikarohana ny fifandraisana manontolo',
        'correlation_explanation': '🔍 Fanazavana ny fifandraisana',
        'weak_correlation': 'Fifandraisana malemy',
        'medium_correlation': 'Fifandraisana antonony',
        'strong_correlation': 'Fifandraisana mafy',
        'what_does_this_mean': 'Inona no dika izany?',
        'weak_explanation': 'Ny **fifandraisana linear** eo amin\'ny velarany sy ny vidiny dia tsy mazava',
        'weak_explanation2': 'Ny velarany irery dia tsy afaka maminavina tsara ny vidiny',
        'weak_explanation3': 'Ny vidiny dia voakasiky ny antony hafa',
        'why_horizontal': 'Nahoana no mitsivalana ny tsipika tendance?',
        'horizontal_explanation': 'Rehefa malemy ny fifandraisana, ny tsipika tendance dia manakaiky ny antonony amin\'ny angon-drakitra, ka mampiseho fa mitsivalana. Izany dia maneho:',
        'horizontal_explanation2': 'Ny vidin\'ny trano dia miova be amin\'ny velarany samihafa',
        'horizontal_explanation3': 'Ny velarany dia tsy antony lehibe amin\'ny vidiny',
        'medium_explanation': 'Misy **fifandraisana linear sasany** eo amin\'ny velarany sy ny vidiny',
        'medium_explanation2': 'Ny velarany dia afaka manazava amin\'ny ampahany ny fiovan\'ny vidiny',
        'medium_explanation3': 'Nefa misy antony hafa manan-danja mbola miantraika amin\'ny vidiny',
        'strong_explanation': 'Misy **fifandraisana linear mazava** eo amin\'ny velarany sy ny vidiny',
        'strong_explanation2': 'Ny velarany dia iray amin\'ny antony lehibe amin\'ny vidiny',
        'strong_explanation3': 'Azonao ampiasaina ny velarany mba haminavina ny vidiny (miaraka amin\'ny fahamarinana sasany)',
        'by_property_type': '🏠 Fikarohana amin\'ny karazana trano',
        'property_type': 'Karazana trano',
        'type_correlation_note': 'Ny fifandraisana dia mety hiova amin\'ny karazana trano. Amin\'ny sary etsy ambany, loko samihafa dia maneho karazana trano samihafa.',
        'scatter_plot': '📊 Sary miparitaka',
        'overall_trendline': 'Tsipika tendance manontolo',
        'type_trendline': 'Tsipika tendance',
        'trendline_note': 'Loko samihafa dia maneho karazana trano samihafa. Ny tsipika mena miparitaka dia ny tsipika tendance ho an\'ny angon-drakitra rehetra. Ny karazana misy fifandraisana mafy ampy (|r| ≥ 0.3) ihany no mampiseho ny tsipika tendance manokana.',
        'trendline_note_weak': 'Loko samihafa dia maneho karazana trano samihafa. Satria malemy ny fifandraisana manontolo (|r| < 0.3), tsy mampiseho tsipika tendance.',
        'trendline_note_simple': 'Ny **tsipika mena miparitaka** dia ny tsipika tendance regression linear, mampiseho ny fifandraisana linear eo amin\'ny velarany sy ny vidiny.',
        'trendline_note_no': 'Satria malemy ny fifandraisana (|r| < 0.3), tsy mampiseho tsipika tendance satria tsy mazava ny fifandraisana linear.',
        'correlation_coefficient': 'Coefficient de corrélation manontolo r',
        'q11_title': 'Q11: Fifandraisana ny velarany namboarina sy ny sandan\'ny trano',
        # Q12 相关
        'q12_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q12_analysis_description': 'Ity fikarohana ity dia mikendry ny hampitaha ny velarany tany antonony amin\'ny **karazana tany** (trano, varotra, sns.).',
        'q12_research_questions': 'Fanontaniana fikarohana:',
        'q12_research_q1': 'Inona ny karazana tany izay manana velarany antonony lehibe indrindra?',
        'q12_research_q2': 'Ahoana ny fahasamihafan\'ny velarany eo amin\'ny karazana samihafa?',
        'q12_research_q3': 'Miantraika ve ny karazana tany amin\'ny haben\'ny velarany?',
        'q12_expected_results': 'Vokatra azo antenaina:',
        'q12_expected_difference': 'Ny fahasamihafan\'ny velarany antonony eo amin\'ny karazana tany dia maneho ny filan\'ny fampiasana sy ny drafitra samihafa.',
        'q12_expected_usage': 'Ny fahatakarana ny velarany antonony amin\'ny karazana tany dia manampy amin\'ny fahatakarana ny lamina fampiasana tany sy ny toetra amin\'ny drafitra.',
        'q12_key_insights': 'Fahitana lehibe:',
        'q12_insight1': 'Ny karazana tany dia maneho ny fampiasana sy ny filan\'ny drafitra samihafa',
        'q12_insight2': 'Ny fahasamihafan\'ny velarany eo amin\'ny karazana dia mety ho voakasiky ny politika drafitra, ny filan\'ny fampiasana, sns.',
        'q12_insight3': 'Ny fikarohana ny velarany antonony dia manampy amin\'ny fahatakarana ny fahombiazan\'ny fampiasana tany sy ny toetra amin\'ny drafitra',
        'q12_statistics': '📈 Statistika',
        'q12_land_types': 'Isan\'ny karazana tany',
        'q12_largest_avg_area': 'Velarany antonony lehibe indrindra',
        'q12_smallest_avg_area': 'Velarany antonony kely indrindra',
        'q12_area_range': 'Sokajy velarany',
        'q12_comparison_chart': '📊 Sary fampitahana',
        'q12_title': 'Q12: Velarany tany antonony amin\'ny karazana tany',
        # Q13 相关
        'q13_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q13_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **tendances ara-potoana amin\'ny vidiny antonony** mba hahatakatra ny fiovan\'ny vidiny amin\'ny tsena.',
        'q13_research_questions': 'Fanontaniana fikarohana:',
        'q13_research_q1': 'Miova ve ny vidiny antonony rehefa mandeha ny fotoana?',
        'q13_research_q2': 'Misy tendance amin\'ny fiakaran\'ny vidiny na ny fidin\'ny vidiny ve?',
        'q13_research_q3': 'Misy lamina ve amin\'ny fiovan\'ny vidiny?',
        'q13_expected_results': 'Vokatra azo antenaina:',
        'q13_expected_trend': 'Ny fikarohana ny tendance vidiny dia manampy amin\'ny fahatakarana ny fihetsiky ny tsena ary dia famantarana manan-danja amin\'ny fampiasam-bola sy ny fanapahan-kevitra.',
        'q13_expected_volatility': 'Ny fiovan\'ny vidiny dia mety maneho ny fiantraikan\'ny fiovan\'ny fividianana sy ny fivarotana, ny tsingerina ara-toekarena, sns.',
        'q13_key_insights': 'Fahitana lehibe:',
        'q13_insight1': 'Ny tendances vidiny dia maneho ny fifandraisana amin\'ny tsena amin\'ny fividianana sy ny fivarotana ary ny antenain\'ny mpampiasa vola',
        'q13_insight2': 'Ny fiovan\'ny vidiny dia mety ho voakasiky ny tsingerina ara-toekarena, ny fanitsiana ny politika, ny fihetseham-po amin\'ny tsena, sns.',
        'q13_insight3': 'Ny tendances vidiny lavalava dia manampy amin\'ny fitsarana ny làlan\'ny fivoaran\'ny tsena sy ny fotoana fampiasam-bola',
        'q13_statistics': '📈 Statistika',
        'q13_months': 'Isan\'ny volana',
        'q13_highest_avg_price': 'Vidiny antonony avo indrindra',
        'q13_lowest_avg_price': 'Vidiny antonony ambany indrindra',
        'q13_current_avg_price': 'Vidiny antonony ankehitriny',
        'q13_trend_chart': '📊 Sary tendance',
        'q13_title': 'Q13: Fivoaran\'ny vidiny antonony isam-bolana',
        # Q14 相关
        'q14_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q14_analysis_description': 'Ity fikarohana ity dia mikendry ny hampitaha ny statistika vidiny (antonony, ambany indrindra, avo indrindra) amin\'ny **karazana trano** mba hahatakatra ny fizarana ny vidiny amin\'ny ankapobeny.',
        'q14_research_questions': 'Fanontaniana fikarohana:',
        'q14_research_q1': 'Inona ny karazana trano izay manana vidiny antonony avo indrindra?',
        'q14_research_q2': 'Ahoana ny habetsaky ny fahasamihafan\'ny sokajy vidiny (ambany indrindra ka hatramin\'ny avo indrindra)?',
        'q14_research_q3': 'Ahoana ny fiovan\'ny vidiny amin\'ny karazana?',
        'q14_expected_results': 'Vokatra azo antenaina:',
        'q14_expected_comparison': 'Ny fampitahana ny vidiny dia manampy amin\'ny fanombanana ny sokajy sandan\'ny karazana trano samihafa sy ny hahatakarana ny firafitry ny vidiny amin\'ny tsena.',
        'q14_expected_range': 'Ny fikarohana ny sokajy vidiny dia afaka manambara ny fiovan\'ny vidiny sy ny fahasamihafan\'ny tsena amin\'ny karazana trano samihafa.',
        'q14_key_insights': 'Fahitana lehibe:',
        'q14_insight1': 'Ny statistika vidiny dia maneho ny toerana sandan\'ny karazana trano samihafa sy ny fahombiazan\'ny tsena',
        'q14_insight2': 'Ny fahasamihafan\'ny sokajy vidiny dia mety maneho ny fahasamihafan\'ny tsena, ny fifandraisana amin\'ny fividianana sy ny fivarotana, sns.',
        'q14_insight3': 'Ny fahatakarana ny statistika vidiny dia manampy amin\'ny fahatakarana ny sandan\'ny fampiasam-bola sy ny loza amin\'ny karazana trano samihafa',
        'q14_statistics': '📈 Statistika',
        'q14_property_types': 'Isan\'ny karazana',
        'q14_highest_avg': 'Vidiny antonony avo indrindra',
        'q14_largest_range': 'Sokajy vidiny lehibe indrindra',
        'q14_price_comparison_chart': '📊 Sary fampitahana vidiny',
        'q14_title': 'Q14: Fampitahana ny vidiny amin\'ny karazana trano',
        # Q15 相关
        'q15_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q15_analysis_description': 'Ity fikarohana ity dia mikendry ny hampitaha ny fizarana ny vidiny amin\'ny **trano sy ny efitrano** mba hahatakatra ny fahasamihafan\'ny vidiny eo amin\'ny karazana trano lehibe roa.',
        'q15_research_questions': 'Fanontaniana fikarohana:',
        'q15_research_q1': 'Inona ny fahasamihafan\'ny fizarana ny vidiny eo amin\'ny trano sy ny efitrano?',
        'q15_research_q2': 'Inona ny karazana izay manana vidiny avo kokoa?',
        'q15_research_q3': 'Maneho lamina samihafa ve ny fizarana ny vidiny?',
        'q15_expected_results': 'Vokatra azo antenaina:',
        'q15_expected_comparison': 'Ny fampitahana ny vidiny amin\'ny trano sy ny efitrano dia manampy amin\'ny fahatakarana ny toerana amin\'ny tsena sy ny fahasamihafan\'ny sandan\'ny karazana trano samihafa.',
        'q15_expected_distribution': 'Ny lamina fizarana ny vidiny dia mety maneho ny vondrona manantena sy ny toetra amin\'ny tsena amin\'ny karazana trano samihafa.',
        'q15_key_insights': 'Fahitana lehibe:',
        'q15_insight1': 'Ny fizarana ny vidiny amin\'ny trano sy ny efitrano dia maneho ny toerana amin\'ny tsena samihafa sy ny vondrona manantena samihafa',
        'q15_insight2': 'Ny fahasamihafan\'ny vidiny dia mety ho voakasiky ny toerana, ny velarany, ny kalitao, ny fangatahana, sns.',
        'q15_insight3': 'Ny fahatakarana ny fizarana ny vidiny dia manampy amin\'ny fahatakarana ny sandan\'ny fampiasam-bola sy ny toetra amin\'ny tsena amin\'ny karazana trano samihafa',
        'q15_statistics': '📈 Statistika',
        'q15_total_properties': 'Total trano',
        'q15_houses': 'Isan\'ny trano',
        'q15_apartments': 'Isan\'ny efitrano',
        'q15_house_median': 'Vidiny median amin\'ny trano',
        'q15_apartment_median': 'Vidiny median amin\'ny efitrano',
        'q15_distribution_chart': '📊 Sary fizarana',
        'q15_title': 'Q15: Fizarana ny vidiny - Trano vs Efitrano',
        # Q16 相关
        'q16_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q16_analysis_description': 'Ity fikarohana ity dia mikendry ny hikajy ny **tahan\'ny velarany tany amin\'ny velarany namboarina** mba hahatakatra ny fampiasana tany amin\'ny tanàna samihafa.',
        'q16_research_questions': 'Fanontaniana fikarohana:',
        'q16_research_q1': 'Inona ny tanàna izay manana tahan\'ny tany/namboarina avo indrindra?',
        'q16_research_q2': 'Inona no maneho ny fahasamihafan\'ny tahan?',
        'q16_research_q3': 'Ahoana ny fahombiazan\'ny fampiasana tany?',
        'q16_expected_results': 'Vokatra azo antenaina:',
        'q16_expected_ratio': 'Ny tahan\'ny tany/namboarina dia maneho ny hakitroky ny fampiasana tany, ny faritra misy tahan avo dia mety manana velarany tany bebe kokoa.',
        'q16_expected_efficiency': 'Ny fahatakarana ny tahan fampiasana tany dia manampy amin\'ny fahatakarana ny toetra amin\'ny drafitra sy ny lamina fivoarana amin\'ny tanàna samihafa.',
        'q16_key_insights': 'Fahitana lehibe:',
        'q16_insight1': 'Ny tahan\'ny tany/namboarina dia maneho ny hakitroky ny fampiasana tany sy ny herin\'ny fivoarana',
        'q16_insight2': 'Ny faritra misy tahan avo dia mety manana velarany tany bebe kokoa, mety amin\'ny fivoarana ambany hakitroka',
        'q16_insight3': 'Ny fahasamihafan\'ny tahan dia mety maneho ny politika drafitra an-tanàna, ny famatsiana tany, sns.',
        'q16_statistics': '📈 Statistika',
        'q16_cities_shown': 'Isan\'ny tanàna aseho',
        'q16_highest_ratio': 'Tahan avo indrindra',
        'q16_lowest_ratio': 'Tahan ambany indrindra',
        'q16_avg_ratio': 'Tahan antonony',
        'q16_ranking_chart': '📊 Sary filaharana',
        'q16_title': 'Q16: Tahan\'ny tany/velarany namboarina 10 voalohany',
        # Q17 相关
        'q17_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q17_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **isan\'ny trano isaky ny fifanakalozana** mba hahatakatra ny fahasarotan\'ny fifanakalozana.',
        'q17_research_questions': 'Fanontaniana fikarohana:',
        'q17_research_q1': 'Firy ny trano izay misy amin\'ny ankamaroan\'ny fifanakalozana?',
        'q17_research_q2': 'Mahazatra ve ny fifanakalozana maro trano?',
        'q17_research_q3': 'Ahoana ny fizarana ny fahasarotan\'ny fifanakalozana?',
        'q17_expected_results': 'Vokatra azo antenaina:',
        'q17_expected_complexity': 'Ny isan\'ny trano isaky ny fifanakalozana dia maneho ny ambaratongan\'ny fahasarotan\'ny fifanakalozana, izay mety hiantraika amin\'ny dingana sy ny vidiny amin\'ny fifanakalozana.',
        'q17_expected_pattern': 'Ny fahatakarana ny fizarana ny fahasarotan\'ny fifanakalozana dia manampy amin\'ny fahatakarana ny lamina sy ny toetra amin\'ny fifanakalozana amin\'ny tsena.',
        'q17_key_insights': 'Fahitana lehibe:',
        'q17_insight1': 'Ny fahasarotan\'ny fifanakalozana dia maneho ny lamina sy ny toetra amin\'ny fifanakalozana amin\'ny tsena',
        'q17_insight2': 'Ny fifanakalozana maro trano dia mety ahitana fifanakalozana miaraka, portfolio fampiasam-bola, ary toe-javatra manokana hafa',
        'q17_insight3': 'Ny fahasarotan\'ny fifanakalozana dia mety hiantraika amin\'ny dingana fifanakalozana, ny fifampiraharahana vidiny, sns.',
        'q17_statistics': '📈 Statistika',
        'q17_total_transactions': 'Total fifanakalozana',
        'q17_most_common_count': 'Isan\'ny trano mahazatra indrindra',
        'q17_max_properties': 'Isan\'ny trano ambony indrindra isaky ny fifanakalozana',
        'q17_avg_properties': 'Isan\'ny trano antonony',
        'q17_distribution_chart': '📊 Sary fizarana',
        'q17_title': 'Q17: Isan\'ny trano isaky ny fifanakalozana',
        # Q18 相关
        'q18_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q18_analysis_description': 'Ity fikarohana ity dia mikendry ny hisoratra ny **isan\'ny trano misy tany sy tsy misy tany** mba hahatakatra ny toetra amin\'ny karazana trano samihafa.',
        'q18_research_questions': 'Fanontaniana fikarohana:',
        'q18_research_q1': 'Inona ny karazana trano izay mety manana tany kokoa?',
        'q18_research_q2': 'Ahoana ny tahan\'ny trano misy tany sy tsy misy tany?',
        'q18_research_q3': 'Miantraika ve ny tany amin\'ny karazana trano?',
        'q18_expected_results': 'Vokatra azo antenaina:',
        'q18_expected_characteristics': 'Ny fananana tany dia maneho ny fahatanterahan\'ny trano sy ny sandany, famantarana manan-danja amin\'ny toetra amin\'ny trano.',
        'q18_expected_distribution': 'Ny fahatakarana ny fizarana ny tany dia manampy amin\'ny fahatakarana ny toetra sy ny toerana amin\'ny tsena amin\'ny karazana trano samihafa.',
        'q18_key_insights': 'Fahitana lehibe:',
        'q18_insight1': 'Ny fananana tany dia maneho ny fahatanterahan\'ny trano sy ny sandany',
        'q18_insight2': 'Ny tahan fananana tany dia mety hiova be amin\'ny karazana trano',
        'q18_insight3': 'Ny tany dia singa manan-danja amin\'ny sandan\'ny trano, miantraika amin\'ny toerana amin\'ny tsena',
        'q18_statistics': '📈 Statistika',
        'q18_property_types': 'Isan\'ny karazana trano',
        'q18_total_with_land': 'Total misy tany',
        'q18_total_without_land': 'Total tsy misy tany',
        'q18_land_ownership_rate': 'Tahan fananana tany',
        'q18_comparison_chart': '📊 Sary fampitahana',
        'q18_title': 'Q18: Statistika trano misy/tsy misy tany',
        # Q19 相关
        'q19_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q19_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **fizarana ny fifanakalozana amin\'ny andro amin\'ny herinandro** mba hahatakatra ny lamina fotoana amin\'ny fifanakalozana.',
        'q19_research_questions': 'Fanontaniana fikarohana:',
        'q19_research_q1': 'Inona ny andro amin\'ny herinandro izay manana fifanakalozana betsaka indrindra?',
        'q19_research_q2': 'Misy fahasamihafana ve eo amin\'ny andro fiasana sy ny fialantsasatra?',
        'q19_research_q3': 'Misy lamina ve amin\'ny fotoana fifanakalozana?',
        'q19_expected_results': 'Vokatra azo antenaina:',
        'q19_expected_pattern': 'Ny fizarana ny daty fifanakalozana dia mety maneho ny lamina fihetsiky ny tsena, toy ny fifanakalozana mavitrika kokoa amin\'ny andro fiasana.',
        'q19_expected_behavior': 'Ny fahatakarana ny lamina fotoana amin\'ny fifanakalozana dia manampy amin\'ny fahatakarana ny lamina fiasan\'ny tsena sy ny fahazarana amin\'ny fifanakalozana.',
        'q19_key_insights': 'Fahitana lehibe:',
        'q19_insight1': 'Ny fizarana ny daty fifanakalozana dia maneho ny lamina fihetsiky ny tsena sy ny fahazarana amin\'ny asa',
        'q19_insight2': 'Ny fahasamihafan\'ny habetsaky ny fifanakalozana eo amin\'ny andro fiasana sy ny fialantsasatra dia mety maneho ny lamina fiasan\'ny tsena',
        'q19_insight3': 'Ny lamina fotoana amin\'ny fifanakalozana dia mety ho voakasiky ny dingana ara-dalàna, ny ora fiasana, sns.',
        'q19_statistics': '📈 Statistika',
        'q19_total_transactions': 'Total fifanakalozana',
        'q19_most_active_day': 'Andro mavitrika indrindra',
        'q19_least_active_day': 'Andro tsy mavitrika indrindra',
        'q19_weekday_avg': 'Antonony amin\'ny andro fiasana',
        'q19_distribution_chart': '📊 Sary fizarana',
        'q19_title': 'Q19: Fizarana ny fifanakalozana isam-pivoriana',
        # Q20 相关
        'q20_analysis_purpose': '📊 Tanjona ny fikarohana',
        'q20_analysis_description': 'Ity fikarohana ity dia mikendry ny hikaroka ny **habetsaky ny fifanakalozana isam-pivoriana sy ny totalin\'ny sandan\'ny fifanakalozana** mba hahatakatra ny fironana amin\'ny tsena isam-pivoriana.',
        'q20_research_questions': 'Fanontaniana fikarohana:',
        'q20_research_q1': 'Miova miaraka ve ny habetsaky ny fifanakalozana sy ny totalin\'ny sandany?',
        'q20_research_q2': 'Misy lamina tsingerina ve?',
        'q20_research_q3': 'Ahoana ny fiovan\'ny fahavitrihan\'ny tsena?',
        'q20_expected_results': 'Vokatra azo antenaina:',
        'q20_expected_analysis': 'Ny fikarohana isam-pivoriana dia afaka manampy amin\'ny famantarana ny fironana fohy sy ny lamina tsingerina amin\'ny tsena.',
        'q20_expected_trends': 'Ny fironana amin\'ny habetsaky ny fifanakalozana sy ny totalin\'ny sandany dia afaka maneho ny fahavitrihana ankapobeny amin\'ny tsena sy ny fiovan\'ny sandany.',
        'q20_key_insights': 'Fahitana lehibe:',
        'q20_insight1': 'Ny fikarohana isam-pivoriana dia afaka manambara ny fironana fohy sy ny lamina tsingerina amin\'ny tsena',
        'q20_insight2': 'Ny fiarahana amin\'ny habetsaky ny fifanakalozana sy ny totalin\'ny sandany dia maneho ny fahavitrihana ankapobeny amin\'ny tsena',
        'q20_insight3': 'Ny lamina tsingerina dia mety ho voakasiky ny antony ara-potoana, ny zava-nitranga amin\'ny tsena, sns.',
        'q20_statistics': '📈 Statistika',
        'q20_weeks': 'Isan\'ny herinandro',
        'q20_total_transactions': 'Total fifanakalozana',
        'q20_total_volume': 'Totalin\'ny sandan\'ny fifanakalozana',
        'q20_avg_transactions_per_week': 'Fifanakalozana antonony isaky ny herinandro',
        'q20_avg_volume_per_week': 'Sandany antonony isaky ny herinandro',
        'q20_trend_chart': '📊 Sary fironana isam-pivoriana',
        'q20_title': 'Q20: Fikarohana ny habetsaky ny fifanakalozana isam-pivoriana',
    }
}

def get_text(key):
    """获取当前语言的文本"""
    lang = st.session_state.get('language', 'zh')
    # 如果当前语言没有该键，尝试从中文获取（作为后备）
    if lang in LANGUAGES and key in LANGUAGES[lang]:
        return LANGUAGES[lang][key]
    elif 'zh' in LANGUAGES and key in LANGUAGES['zh']:
        return LANGUAGES['zh'][key]
    else:
        return key

def init_session_state():
    """初始化会话状态"""
    if 'language' not in st.session_state:
        st.session_state.language = 'zh'

# ============================================
# 数据库连接（使用缓存）
# ============================================
@st.cache_resource
def init_connection(host, user, password, database):
    """初始化数据库连接，只返回连接对象或错误代码"""
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return mydb
    except mysql.connector.Error as e:
        # 返回错误代码和原始错误信息，不在这里生成多语言文本
        error_msg = str(e)
        if "Access denied" in error_msg or "28000" in error_msg:
            return (None, "AUTH_FAILED", error_msg, host, user, database)
        elif "Unknown database" in error_msg:
            return (None, "DB_NOT_FOUND", error_msg, host, user, database)
        elif "Can't connect" in error_msg or "2003" in error_msg:
            return (None, "CONNECT_FAILED", error_msg, host, user, database)
        else:
            return (None, "OTHER_ERROR", error_msg, host, user, database)
    except Exception as e:
        return (None, "UNKNOWN_ERROR", str(e), host, user, database)

def format_error_message(error_code, error_msg, host, user, database):
    """根据当前语言格式化错误信息"""
    lang = st.session_state.get('language', 'zh')
    
    if error_code == "AUTH_FAILED":
        if lang == 'zh':
            return f"""{get_text('db_auth_failed')}

**{get_text('possible_reasons')}**
1. {get_text('username_password_wrong')}
2. {get_text('user_not_exists')}
3. {get_text('no_access')}

**{get_text('solutions')}**
- {get_text('check_credentials')}
- {get_text('confirm_mysql_running')}
- {get_text('test_connection')}：
  ```
  mysql -u {user} -p
  ```
- {get_text('create_user')}
  ```sql
  CREATE USER '{user}'@'localhost' IDENTIFIED BY '你的密码';
  GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'localhost';
  FLUSH PRIVILEGES;
  ```"""
        elif lang == 'ar':
            return f"""{get_text('db_auth_failed')}

**{get_text('possible_reasons')}**
1. {get_text('username_password_wrong')}
2. {get_text('user_not_exists')}
3. {get_text('no_access')}

**{get_text('solutions')}**
- {get_text('check_credentials')}
- {get_text('confirm_mysql_running')}
- {get_text('test_connection')}:
  ```
  mysql -u {user} -p
  ```
- {get_text('create_user')}
  ```sql
  CREATE USER '{user}'@'localhost' IDENTIFIED BY 'كلمة المرور الخاصة بك';
  GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'localhost';
  FLUSH PRIVILEGES;
  ```"""
        elif lang == 'en':
            return f"""{get_text('db_auth_failed')}

**{get_text('possible_reasons')}**
1. {get_text('username_password_wrong')}
2. {get_text('user_not_exists')}
3. {get_text('no_access')}

**{get_text('solutions')}**
- {get_text('check_credentials')}
- {get_text('confirm_mysql_running')}
- {get_text('test_connection')}:
  ```
  mysql -u {user} -p
  ```
- {get_text('create_user')}
  ```sql
  CREATE USER '{user}'@'localhost' IDENTIFIED BY 'your password';
  GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'localhost';
  FLUSH PRIVILEGES;
  ```"""
        elif lang == 'mg':
            return f"""{get_text('db_auth_failed')}

**{get_text('possible_reasons')}**
1. {get_text('username_password_wrong')}
2. {get_text('user_not_exists')}
3. {get_text('no_access')}

**{get_text('solutions')}**
- {get_text('check_credentials')}
- {get_text('confirm_mysql_running')}
- {get_text('test_connection')}:
  ```
  mysql -u {user} -p
  ```
- {get_text('create_user')}
  ```sql
  CREATE USER '{user}'@'localhost' IDENTIFIED BY 'tenimiafinao';
  GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'localhost';
  FLUSH PRIVILEGES;
  ```"""
        else:  # fr
            return f"""{get_text('db_auth_failed')}

**{get_text('possible_reasons')}**
1. {get_text('username_password_wrong')}
2. {get_text('user_not_exists')}
3. {get_text('no_access')}

**{get_text('solutions')}**
- {get_text('check_credentials')}
- {get_text('confirm_mysql_running')}
- {get_text('test_connection')}：
  ```
  mysql -u {user} -p
  ```
- {get_text('create_user')}
  ```sql
  CREATE USER '{user}'@'localhost' IDENTIFIED BY 'votre mot de passe';
  GRANT ALL PRIVILEGES ON {database}.* TO '{user}'@'localhost';
  FLUSH PRIVILEGES;
  ```"""
    
    elif error_code == "DB_NOT_FOUND":
        if lang == 'zh':
            return f"""{get_text('db_not_found')}

**{get_text('solutions')}**
- 确认数据库 '{database}' 已创建
- 运行 `create_tab.sql` 创建数据库和表
- 或手动创建数据库：
  ```sql
  CREATE DATABASE {database};
  ```"""
        else:
            return f"""{get_text('db_not_found')}

**{get_text('solutions')}**
- Confirmer que la base de données '{database}' a été créée
- Exécuter `create_tab.sql` pour créer la base de données et les tables
- Ou créer manuellement la base de données :
  ```sql
  CREATE DATABASE {database};
  ```"""
    
    elif error_code == "CONNECT_FAILED":
        if lang == 'zh':
            return f"""{get_text('db_connect_failed')}

**{get_text('possible_reasons')}**
1. {get_text('service_not_running')}
2. {get_text('host_port_wrong')}

**{get_text('solutions')}**
- {get_text('check_service')}
  - Windows: 打开"服务"应用，查找 MySQL 服务
  - 或运行: `net start MySQL80` (根据版本调整)
- 确认主机地址 '{host}' 正确
- {get_text('check_firewall')}"""
        else:
            return f"""{get_text('db_connect_failed')}

**{get_text('possible_reasons')}**
1. {get_text('service_not_running')}
2. {get_text('host_port_wrong')}

**{get_text('solutions')}**
- {get_text('check_service')}
  - Windows: Ouvrir "Services", trouver le service MySQL
  - Ou exécuter: `net start MySQL80` (ajuster selon votre version)
- Confirmer que l'adresse du serveur '{host}' est correcte
- {get_text('check_firewall')}"""
    
    else:
        if lang == 'zh':
            return f"❌ 数据库连接失败: {error_msg}"
        else:
            return f"❌ Échec de la connexion à la base de données: {error_msg}"

# ============================================
# 查询函数
# ============================================
def execute_query(query, connection):
    """执行SQL查询并返回DataFrame"""
    try:
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        st.error(f"{get_text('query_error')}: {e}")
        with st.expander(get_text('view_query')):
            st.code(query, language="sql")
        return pd.DataFrame()

def show_empty_result_message(query, mydb, table_name=None):
    """显示空结果时的提示信息和调试信息"""
    st.warning(get_text('empty_result'))
    st.info(f"""
    **{get_text('possible_causes')}**
    1. {get_text('no_data_in_db')}
    2. {get_text('data_not_imported')}
    3. {get_text('table_mismatch')}
    
    **{get_text('solutions')}**
    - {get_text('solution_check_data')}
    - {get_text('solution_import_data')}
    """)
    with st.expander(get_text('view_query')):
        st.code(query, language="sql")
    
    if table_name:
        lang = st.session_state.get('language', 'zh')
        debug_title = "🔍 调试信息" if lang == 'zh' else "🔍 Informations de débogage"
        with st.expander(debug_title):
            try:
                # 检查表是否存在
                check_query = f"SHOW TABLES LIKE '{table_name}';"
                tables_df = pd.read_sql(check_query, mydb)
                if not tables_df.empty:
                    if lang == 'zh':
                        st.success(f"✅ {table_name} {get_text('table_exists')}")
                    else:
                        st.success(f"✅ {table_name} {get_text('table_exists')}")
                    # 检查表中有多少行
                    count_query = f"SELECT COUNT(*) as total FROM {table_name};"
                    count_df = pd.read_sql(count_query, mydb)
                    if lang == 'zh':
                        st.info(f"📊 {table_name} {get_text('total_rows')}: {count_df['total'].iloc[0]}")
                    else:
                        st.info(f"📊 {table_name} {get_text('total_rows')}: {count_df['total'].iloc[0]}")
                else:
                    if lang == 'zh':
                        st.error(f"❌ {table_name} {get_text('table_not_found')}！需要先运行 create_tab.sql 创建表结构")
                    else:
                        st.error(f"❌ {table_name} {get_text('table_not_found')} ! Exécutez d'abord create_tab.sql pour créer la structure de la table")
            except Exception as e:
                if lang == 'zh':
                    st.error(f"检查表时出错: {e}")
                else:
                    st.error(f"Erreur lors de la vérification de la table: {e}")

# ============================================
# 可视化函数 - 问题1-10
# ============================================
def question1(mydb):
    """Q1: Évolution du nombre de mutations par mois"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q1_analysis_purpose')}
    
    {get_text('q1_analysis_description')}
    
    **{get_text('q1_research_questions')}**
    - {get_text('q1_research_q1')}
    - {get_text('q1_research_q2')}
    - {get_text('q1_research_q3')}
    
    **{get_text('q1_expected_results')}**
    - {get_text('q1_expected_trend')}
    - {get_text('q1_expected_seasonal')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
           COUNT(*) as nombre_mutations
    FROM MUTATION
    GROUP BY mois
    ORDER BY mois;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q1_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('data_points'), f"{len(df):,}")
        with col2:
            total_transactions = df['nombre_mutations'].sum()
            st.metric(get_text('q1_total_transactions'), f"{total_transactions:,}")
        with col3:
            avg_per_month = df['nombre_mutations'].mean()
            st.metric(get_text('q1_avg_per_month'), f"{avg_per_month:.0f}")
        with col4:
            max_month = df.loc[df['nombre_mutations'].idxmax(), 'mois']
            max_value = df['nombre_mutations'].max()
            st.metric(get_text('q1_most_active_month'), f"{max_month}\n({max_value:,})")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q1_key_insights')}")
        st.info(f"""
        - {get_text('q1_insight1')}
        - {get_text('q1_insight2')}
        - {get_text('q1_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q1_trend_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q1: 每月交易数量变化趋势'
            labels_dict = {'mois': '月份', 'nombre_mutations': '交易数量'}
        else:
            title = 'Q1: Évolution du nombre de mutations par mois'
            labels_dict = {'mois': 'Mois', 'nombre_mutations': 'Nombre de mutations'}
        
        fig = px.line(df, x='mois', y='nombre_mutations', 
                     title=title,
                     labels=labels_dict)
        fig.update_traces(mode='lines+markers', line=dict(width=2), marker=dict(size=8))
        fig.update_layout(
            hovermode='x unified',
            xaxis_title=labels_dict['mois'],
            yaxis_title=labels_dict['nombre_mutations']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question2(mydb):
    """Q2: Distribution des valeurs foncières par tranche"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q2_analysis_purpose')}
    
    {get_text('q2_analysis_description')}
    
    **{get_text('q2_research_questions')}**
    - {get_text('q2_research_q1')}
    - {get_text('q2_research_q2')}
    - {get_text('q2_research_q3')}
    
    **{get_text('q2_expected_results')}**
    - {get_text('q2_expected_distribution')}
    - {get_text('q2_expected_segments')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT 
        CASE 
            WHEN valeur_fonciere < 100000 THEN '0-100k'
            WHEN valeur_fonciere < 200000 THEN '100k-200k'
            WHEN valeur_fonciere < 300000 THEN '200k-300k'
            WHEN valeur_fonciere < 500000 THEN '300k-500k'
            ELSE '500k+'
        END as tranche,
        COUNT(*) as nombre
    FROM MUTATION
    WHERE valeur_fonciere IS NOT NULL
    GROUP BY tranche
    ORDER BY MIN(valeur_fonciere);
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q2_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_mutations = df['nombre'].sum()
            st.metric(get_text('q2_total_mutations'), f"{total_mutations:,}")
        with col2:
            st.metric(get_text('q2_price_ranges'), len(df))
        with col3:
            most_common = df.loc[df['nombre'].idxmax(), 'tranche']
            most_common_value = df['nombre'].max()
            st.metric(get_text('q2_most_common_range'), f"{most_common}\n({most_common_value:,})")
        with col4:
            avg_per_range = df['nombre'].mean()
            st.metric(get_text('q2_avg_per_range'), f"{avg_per_range:.0f}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q2_key_insights')}")
        st.info(f"""
        - {get_text('q2_insight1')}
        - {get_text('q2_insight2')}
        - {get_text('q2_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q2_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q2: 价格区间分布'
            labels_dict = {'tranche': '价格区间', 'nombre': '交易数量'}
        else:
            title = 'Q2: Distribution des valeurs foncières par tranche'
            labels_dict = {'tranche': 'Tranche de prix', 'nombre': 'Nombre de mutations'}
        
        fig = px.bar(df, x='tranche', y='nombre', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['tranche'],
            yaxis_title=labels_dict['nombre']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question3(mydb):
    """Q3: Valeur foncière moyenne par nature de mutation"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q3_analysis_purpose')}
    
    {get_text('q3_analysis_description')}
    
    **{get_text('q3_research_questions')}**
    - {get_text('q3_research_q1')}
    - {get_text('q3_research_q2')}
    - {get_text('q3_research_q3')}
    
    **{get_text('q3_expected_results')}**
    - {get_text('q3_expected_difference')}
    - {get_text('q3_expected_impact')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT nm.nature_mutation, 
           AVG(m.valeur_fonciere) as valeur_moyenne
    FROM MUTATION m
    JOIN NATURE_MUTATION nm ON m.id_nature_mutation = nm.id_nature_mutation
    WHERE m.valeur_fonciere IS NOT NULL
    GROUP BY nm.nature_mutation
    ORDER BY valeur_moyenne DESC;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q3_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q3_transaction_types'), len(df))
        with col2:
            highest_price = df['valeur_moyenne'].max()
            st.metric(get_text('q3_highest_avg_price'), f"{highest_price:,.0f} €")
        with col3:
            lowest_price = df['valeur_moyenne'].min()
            st.metric(get_text('q3_lowest_avg_price'), f"{lowest_price:,.0f} €")
        with col4:
            price_diff = highest_price - lowest_price
            st.metric(get_text('q3_price_difference'), f"{price_diff:,.0f} €")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q3_key_insights')}")
        st.info(f"""
        - {get_text('q3_insight1')}
        - {get_text('q3_insight2')}
        - {get_text('q3_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q3_comparison_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q3: 不同交易类型的平均价格对比'
            labels_dict = {'valeur_moyenne': '平均价格 (€)', 'nature_mutation': '交易类型'}
        else:
            title = 'Q3: Valeur foncière moyenne par nature de mutation'
            labels_dict = {'valeur_moyenne': 'Valeur moyenne (€)', 'nature_mutation': 'Nature de mutation'}
        
        fig = px.bar(df, x='valeur_moyenne', y='nature_mutation', orientation='h',
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['valeur_moyenne'],
            yaxis_title=labels_dict['nature_mutation']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question4(mydb):
    """Q4: Répartition des biens par type de local"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q4_analysis_purpose')}
    
    {get_text('q4_analysis_description')}
    
    **{get_text('q4_research_questions')}**
    - {get_text('q4_research_q1')}
    - {get_text('q4_research_q2')}
    - {get_text('q4_research_q3')}
    
    **{get_text('q4_expected_results')}**
    - {get_text('q4_expected_distribution')}
    - {get_text('q4_expected_market')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT tl.type_local, 
           COUNT(*) as nombre
    FROM BIEN b
    JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
    WHERE tl.type_local IS NOT NULL
    GROUP BY tl.type_local
    ORDER BY nombre DESC;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q4_statistics'))
        col1, col2, col3 = st.columns(3)
        with col1:
            total_properties = df['nombre'].sum()
            st.metric(get_text('q4_total_properties'), f"{total_properties:,}")
        with col2:
            st.metric(get_text('q4_property_types'), len(df))
        with col3:
            most_common = df.loc[df['nombre'].idxmax(), 'type_local']
            most_common_value = df['nombre'].max()
            percentage = (most_common_value / total_properties) * 100
            st.metric(get_text('q4_most_common_type'), f"{most_common}\n({percentage:.1f}%)")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q4_key_insights')}")
        st.info(f"""
        - {get_text('q4_insight1')}
        - {get_text('q4_insight2')}
        - {get_text('q4_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q4_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q4: 房产类型分布'
        else:
            title = 'Q4: Répartition des biens par type de local'
        
        fig = px.pie(df, values='nombre', names='type_local', 
                    title=title)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question5(mydb):
    """Q5: Prix moyen au m² par type de local"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q5_analysis_purpose')}
    
    {get_text('q5_analysis_description')}
    
    **{get_text('q5_research_questions')}**
    - {get_text('q5_research_q1')}
    - {get_text('q5_research_q2')}
    - {get_text('q5_research_q3')}
    
    **{get_text('q5_expected_results')}**
    - {get_text('q5_expected_price')}
    - {get_text('q5_expected_comparison')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT tl.type_local, 
           AVG(m.valeur_fonciere / b.surface_reelle_bati) as prix_m2
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
    WHERE b.surface_reelle_bati > 0 
      AND m.valeur_fonciere IS NOT NULL
    GROUP BY tl.type_local
    ORDER BY prix_m2 DESC;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q5_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q5_property_types'), len(df))
        with col2:
            highest_price = df['prix_m2'].max()
            st.metric(get_text('q5_highest_price_m2'), f"{highest_price:,.0f} €/m²")
        with col3:
            lowest_price = df['prix_m2'].min()
            st.metric(get_text('q5_lowest_price_m2'), f"{lowest_price:,.0f} €/m²")
        with col4:
            avg_price = df['prix_m2'].mean()
            st.metric(get_text('q5_avg_price_m2'), f"{avg_price:,.0f} €/m²")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q5_key_insights')}")
        st.info(f"""
        - {get_text('q5_insight1')}
        - {get_text('q5_insight2')}
        - {get_text('q5_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q5_price_comparison_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q5: 不同房产类型的单价对比'
            labels_dict = {'type_local': '房产类型', 'prix_m2': '单价 (€/m²)'}
        else:
            title = 'Q5: Prix moyen au m² par type de local'
            labels_dict = {'type_local': 'Type de local', 'prix_m2': 'Prix au m² (€)'}
        
        fig = px.bar(df, x='type_local', y='prix_m2', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['type_local'],
            yaxis_title=labels_dict['prix_m2']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question6(mydb):
    """Q6: Distribution du nombre de pièces principales"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q6_analysis_purpose')}
    
    {get_text('q6_analysis_description')}
    
    **{get_text('q6_research_questions')}**
    - {get_text('q6_research_q1')}
    - {get_text('q6_research_q2')}
    - {get_text('q6_research_q3')}
    
    **{get_text('q6_expected_results')}**
    - {get_text('q6_expected_distribution')}
    - {get_text('q6_expected_market')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT nombre_pieces_principales, 
           COUNT(*) as nombre_biens
    FROM BIEN
    WHERE nombre_pieces_principales IS NOT NULL
    GROUP BY nombre_pieces_principales
    ORDER BY nombre_pieces_principales;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q6_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_properties = df['nombre_biens'].sum()
            st.metric(get_text('q6_total_properties'), f"{total_properties:,}")
        with col2:
            room_range = f"{df['nombre_pieces_principales'].min()}-{df['nombre_pieces_principales'].max()}"
            st.metric(get_text('q6_room_count_range'), room_range)
        with col3:
            most_common = df.loc[df['nombre_biens'].idxmax(), 'nombre_pieces_principales']
            most_common_value = df['nombre_biens'].max()
            st.metric(get_text('q6_most_common_rooms'), f"{most_common} {get_text('rows') if lang == 'zh' else 'pièces'}\n({most_common_value:,})")
        with col4:
            # 计算加权平均房间数
            avg_rooms = (df['nombre_pieces_principales'] * df['nombre_biens']).sum() / df['nombre_biens'].sum()
            st.metric(get_text('q6_avg_rooms'), f"{avg_rooms:.1f}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q6_key_insights')}")
        st.info(f"""
        - {get_text('q6_insight1')}
        - {get_text('q6_insight2')}
        - {get_text('q6_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q6_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q6: 房间数分布'
            labels_dict = {'nombre_pieces_principales': '房间数', 'nombre_biens': '房产数量'}
        else:
            title = 'Q6: Distribution du nombre de pièces principales'
            labels_dict = {'nombre_pieces_principales': 'Nombre de pièces', 'nombre_biens': 'Nombre de biens'}
        
        fig = px.bar(df, x='nombre_pieces_principales', y='nombre_biens', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['nombre_pieces_principales'],
            yaxis_title=labels_dict['nombre_biens']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question7(mydb):
    """Q7: Top 10 des communes par nombre de transactions"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q7_analysis_purpose')}
    
    {get_text('q7_analysis_description')}
    
    **{get_text('q7_research_questions')}**
    - {get_text('q7_research_q1')}
    - {get_text('q7_research_q2')}
    - {get_text('q7_research_q3')}
    
    **{get_text('q7_expected_results')}**
    - {get_text('q7_expected_ranking')}
    - {get_text('q7_expected_concentration')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT c.commune, 
           COUNT(DISTINCT m.id_mutation) as nb_transactions
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    JOIN COMMUNE c ON b.id_commune = c.id_commune
    GROUP BY c.commune
    ORDER BY nb_transactions DESC
    LIMIT 10;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q7_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_transactions = df['nb_transactions'].sum()
            st.metric(get_text('q7_total_transactions'), f"{total_transactions:,}")
        with col2:
            st.metric(get_text('q7_cities_shown'), len(df))
        with col3:
            most_active = df.loc[df['nb_transactions'].idxmax(), 'commune']
            st.metric(get_text('q7_most_active_city'), most_active)
        with col4:
            top_transactions = df['nb_transactions'].max()
            st.metric(get_text('q7_top_city_transactions'), f"{top_transactions:,}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q7_key_insights')}")
        st.info(f"""
        - {get_text('q7_insight1')}
        - {get_text('q7_insight2')}
        - {get_text('q7_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q7_ranking_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q7: 交易量前10名城市'
            labels_dict = {'nb_transactions': '交易数量', 'commune': '城市'}
        else:
            title = 'Q7: Top 10 des communes par nombre de transactions'
            labels_dict = {'nb_transactions': 'Nombre de transactions', 'commune': 'Commune'}
        
        fig = px.bar(df, x='nb_transactions', y='commune', orientation='h',
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['nb_transactions'],
            yaxis_title=labels_dict['commune']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question8(mydb):
    """Q8: Valeur foncière moyenne par département"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q8_analysis_purpose')}
    
    {get_text('q8_analysis_description')}
    
    **{get_text('q8_research_questions')}**
    - {get_text('q8_research_q1')}
    - {get_text('q8_research_q2')}
    - {get_text('q8_research_q3')}
    
    **{get_text('q8_expected_results')}**
    - {get_text('q8_expected_difference')}
    - {get_text('q8_expected_pattern')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT d.code_departement, 
           AVG(m.valeur_fonciere) as valeur_moyenne
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    JOIN COMMUNE c ON b.id_commune = c.id_commune
    JOIN DEPARTEMENT d ON c.code_departement = d.code_departement
    WHERE m.valeur_fonciere IS NOT NULL
    GROUP BY d.code_departement
    ORDER BY valeur_moyenne DESC;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q8_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q8_departments'), len(df))
        with col2:
            highest_price = df['valeur_moyenne'].max()
            st.metric(get_text('q8_highest_avg_price'), f"{highest_price:,.0f} €")
        with col3:
            lowest_price = df['valeur_moyenne'].min()
            st.metric(get_text('q8_lowest_avg_price'), f"{lowest_price:,.0f} €")
        with col4:
            price_range = highest_price - lowest_price
            st.metric(get_text('q8_price_range'), f"{price_range:,.0f} €")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q8_key_insights')}")
        st.info(f"""
        - {get_text('q8_insight1')}
        - {get_text('q8_insight2')}
        - {get_text('q8_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q8_comparison_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q8: 不同省份的平均价格对比'
            labels_dict = {'code_departement': '省份', 'valeur_moyenne': '平均价格 (€)'}
        else:
            title = 'Q8: Valeur foncière moyenne par département'
            labels_dict = {'code_departement': 'Département', 'valeur_moyenne': 'Valeur moyenne (€)'}
        
        fig = px.bar(df, x='code_departement', y='valeur_moyenne', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['code_departement'],
            yaxis_title=labels_dict['valeur_moyenne']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question9(mydb):
    """Q9: Volume de transactions par code postal"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q9_analysis_purpose')}
    
    {get_text('q9_analysis_description')}
    
    **{get_text('q9_research_questions')}**
    - {get_text('q9_research_q1')}
    - {get_text('q9_research_q2')}
    - {get_text('q9_research_q3')}
    
    **{get_text('q9_expected_results')}**
    - {get_text('q9_expected_analysis')}
    - {get_text('q9_expected_precision')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT c.code_postal, 
           COUNT(*) as nombre_transactions
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    JOIN COMMUNE c ON b.id_commune = c.id_commune
    WHERE c.code_postal IS NOT NULL
    GROUP BY c.code_postal
    ORDER BY nombre_transactions DESC
    LIMIT 15;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q9_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q9_postal_codes_shown'), len(df))
        with col2:
            total_transactions = df['nombre_transactions'].sum()
            st.metric(get_text('q9_total_transactions'), f"{total_transactions:,}")
        with col3:
            most_active = df.loc[df['nombre_transactions'].idxmax(), 'code_postal']
            st.metric(get_text('q9_most_active_code'), most_active)
        with col4:
            top_transactions = df['nombre_transactions'].max()
            st.metric(get_text('q9_top_code_transactions'), f"{top_transactions:,}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q9_key_insights')}")
        st.info(f"""
        - {get_text('q9_insight1')}
        - {get_text('q9_insight2')}
        - {get_text('q9_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q9_ranking_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q9: 交易量前15名邮政编码'
            labels_dict = {'code_postal': '邮政编码', 'nombre_transactions': '交易数量'}
        else:
            title = 'Q9: Top 15 des codes postaux par nombre de transactions'
            labels_dict = {'code_postal': 'Code postal', 'nombre_transactions': 'Nombre de transactions'}
        
        fig = px.bar(df, x='code_postal', y='nombre_transactions', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['code_postal'],
            yaxis_title=labels_dict['nombre_transactions']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question10(mydb):
    """Q10: Distribution des surfaces bâties"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q10_analysis_purpose')}
    
    {get_text('q10_analysis_description')}
    
    **{get_text('q10_research_questions')}**
    - {get_text('q10_research_q1')}
    - {get_text('q10_research_q2')}
    - {get_text('q10_research_q3')}
    
    **{get_text('q10_expected_results')}**
    - {get_text('q10_expected_distribution')}
    - {get_text('q10_expected_market')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT 
        CASE 
            WHEN surface_reelle_bati < 50 THEN '0-50m²'
            WHEN surface_reelle_bati < 100 THEN '50-100m²'
            WHEN surface_reelle_bati < 150 THEN '100-150m²'
            WHEN surface_reelle_bati < 200 THEN '150-200m²'
            ELSE '200m²+'
        END as tranche_surface,
        COUNT(*) as nombre
    FROM BIEN
    WHERE surface_reelle_bati IS NOT NULL
    GROUP BY tranche_surface
    ORDER BY MIN(surface_reelle_bati);
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q10_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_properties = df['nombre'].sum()
            st.metric(get_text('q10_total_properties'), f"{total_properties:,}")
        with col2:
            st.metric(get_text('q10_surface_ranges'), len(df))
        with col3:
            most_common = df.loc[df['nombre'].idxmax(), 'tranche_surface']
            most_common_value = df['nombre'].max()
            st.metric(get_text('q10_most_common_range'), f"{most_common}\n({most_common_value:,})")
        with col4:
            # 计算平均面积（需要从原始数据计算，这里用近似值）
            # 由于我们只有区间，使用区间中值来估算
            avg_surface = 0
            total_count = df['nombre'].sum()
            for _, row in df.iterrows():
                range_str = row['tranche_surface']
                if range_str == '0-50m²':
                    mid = 25
                elif range_str == '50-100m²':
                    mid = 75
                elif range_str == '100-150m²':
                    mid = 125
                elif range_str == '150-200m²':
                    mid = 175
                else:  # '200m²+'
                    mid = 250  # 假设平均值
                avg_surface += mid * row['nombre']
            avg_surface = avg_surface / total_count
            st.metric(get_text('q10_avg_surface'), f"{avg_surface:.0f} m²")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q10_key_insights')}")
        st.info(f"""
        - {get_text('q10_insight1')}
        - {get_text('q10_insight2')}
        - {get_text('q10_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q10_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q10: 建筑面积分布'
            labels_dict = {'tranche_surface': '面积区间', 'nombre': '房产数量'}
        else:
            title = 'Q10: Distribution des surfaces bâties'
            labels_dict = {'tranche_surface': 'Tranche de surface', 'nombre': 'Nombre de biens'}
        
        fig = px.bar(df, x='tranche_surface', y='nombre', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['tranche_surface'],
            yaxis_title=labels_dict['nombre']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

# ============================================
# 可视化函数 - 问题11-20
# ============================================
def question11(mydb):
    """Q11: Corrélation surface bâtie vs valeur foncière"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('analysis_purpose')}
    
    {get_text('analysis_description')}
    
    **{get_text('research_questions')}**
    - {get_text('research_q1')}
    - {get_text('research_q2')}
    - {get_text('research_q3')}
    
    **{get_text('expected_results')}**
    - {get_text('expected_strong')}
    - {get_text('expected_weak')}
    """)
    
    st.markdown("---")
    
    # 查询数据（包含房产类型以便分组分析）
    query = """
    SELECT b.surface_reelle_bati, 
           m.valeur_fonciere,
           tl.type_local
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    LEFT JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
    WHERE b.surface_reelle_bati IS NOT NULL 
      AND b.surface_reelle_bati > 0
      AND m.valeur_fonciere IS NOT NULL
      AND m.valeur_fonciere < 1000000
    LIMIT 500;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        correlation = df['surface_reelle_bati'].corr(df['valeur_fonciere'])
        
        # 显示统计信息
        st.subheader(get_text('overall_correlation'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('data_points'), f"{len(df):,}")
        with col2:
            st.metric(f"{get_text('correlation')} (r)", f"{correlation:.3f}")
        with col3:
            st.metric(get_text('avg_area'), f"{df['surface_reelle_bati'].mean():.1f} m²")
        with col4:
            st.metric(get_text('avg_price'), f"{df['valeur_fonciere'].mean():,.0f} €")
        
        # 解释相关系数
        st.markdown(f"#### {get_text('correlation_explanation')}")
        if abs(correlation) < 0.3:
            if lang == 'zh':
                st.warning(f"""
                **{get_text('weak_correlation')}** (|r| = {abs(correlation):.3f} < 0.3)
                
                **{get_text('what_does_this_mean')}**
                - {get_text('weak_explanation')}
                - {get_text('weak_explanation2')}
                - {get_text('weak_explanation3')}：
                  - 📍 **地理位置**（市中心 vs 郊区）
                  - 🏠 **房产类型**（公寓 vs 别墅）
                  - 📅 **交易年份**
                  - 🏘️ **社区环境**
                  - 📐 **其他特征**（房间数、装修等）
                
                **{get_text('why_horizontal')}**
                {get_text('horizontal_explanation')}
                - {get_text('horizontal_explanation2')}
                - {get_text('horizontal_explanation3')}
                """)
            else:
                st.warning(f"""
                **{get_text('weak_correlation')}** (|r| = {abs(correlation):.3f} < 0.3)
                
                **{get_text('what_does_this_mean')}**
                - {get_text('weak_explanation')}
                - {get_text('weak_explanation2')}
                - {get_text('weak_explanation3')}：
                  - 📍 **Emplacement géographique** (centre-ville vs banlieue)
                  - 🏠 **Type de bien** (appartement vs maison)
                  - 📅 **Année de transaction**
                  - 🏘️ **Environnement du quartier**
                  - 📐 **Autres caractéristiques** (nombre de pièces, rénovation, etc.)
                
                **{get_text('why_horizontal')}**
                {get_text('horizontal_explanation')}
                - {get_text('horizontal_explanation2')}
                - {get_text('horizontal_explanation3')}
                """)
        elif abs(correlation) < 0.7:
            st.info(f"""
            **{get_text('medium_correlation')}** (0.3 ≤ |r| = {abs(correlation):.3f} < 0.7)
            
            **{get_text('what_does_this_mean')}**
            - {get_text('medium_explanation')}
            - {get_text('medium_explanation2')}
            - {get_text('medium_explanation3')}
            """)
        else:
            st.success(f"""
            **{get_text('strong_correlation')}** (|r| = {abs(correlation):.3f} ≥ 0.7)
            
            **{get_text('what_does_this_mean')}**
            - {get_text('strong_explanation')}
            - {get_text('strong_explanation2')}
            - {get_text('strong_explanation3')}
            """)
        
        # 按房产类型分组分析（如果有房产类型数据）
        has_type_data = 'type_local' in df.columns and df['type_local'].notna().any()
        
        if has_type_data:
            st.markdown("---")
            st.subheader(get_text('by_property_type'))
            
            type_correlations = []
            for prop_type in df['type_local'].dropna().unique():
                type_df = df[df['type_local'] == prop_type]
                if len(type_df) > 10:  # 至少需要10个数据点
                    type_corr = type_df['surface_reelle_bati'].corr(type_df['valeur_fonciere'])
                    if lang == 'zh':
                        type_correlations.append({
                            '房产类型': prop_type,
                            '数据点数': len(type_df),
                            '相关系数': type_corr,
                            '平均面积': type_df['surface_reelle_bati'].mean(),
                            '平均价格': type_df['valeur_fonciere'].mean()
                        })
                    else:
                        type_correlations.append({
                            'Type de bien': prop_type,
                            'Points de données': len(type_df),
                            'Coefficient de corrélation': type_corr,
                            'Surface moyenne': type_df['surface_reelle_bati'].mean(),
                            'Prix moyen': type_df['valeur_fonciere'].mean()
                        })
            
            if type_correlations:
                corr_df = pd.DataFrame(type_correlations)
                st.dataframe(corr_df, use_container_width=True)
                st.caption(f"💡 {get_text('type_correlation_note')}")
        
        st.markdown("---")
        st.subheader(get_text('scatter_plot'))
        
        # 创建散点图：如果有房产类型数据，用分组图；否则用整体图
        show_trendline = abs(correlation) >= 0.3
        
        if has_type_data:
            # 有房产类型数据，创建分组散点图
            try:
                if lang == 'zh':
                    title_grouped = 'Q11: 建筑面积 vs 房产价值相关性（按房产类型分组）'
                    labels_grouped = {'surface_reelle_bati': '建筑面积 (m²)', 
                                     'valeur_fonciere': '房产价值 (€)',
                                     'type_local': '房产类型'}
                else:
                    title_grouped = 'Q11: Corrélation surface bâtie vs valeur foncière (par type de bien)'
                    labels_grouped = {'surface_reelle_bati': 'Surface bâtie (m²)', 
                                     'valeur_fonciere': 'Valeur foncière (€)',
                                     'type_local': 'Type de bien'}
                fig = px.scatter(df, x='surface_reelle_bati', y='valeur_fonciere',
                               color='type_local',
                               title=title_grouped,
                               labels=labels_grouped,
                               opacity=0.6)
                
                # 为整体数据添加趋势线（如果相关性足够强）
                if show_trendline:
                    df_plot = df[['surface_reelle_bati', 'valeur_fonciere']].copy()
                    z = np.polyfit(df_plot['surface_reelle_bati'], df_plot['valeur_fonciere'], 1)
                    p = np.poly1d(z)
                    x_trend = np.linspace(df_plot['surface_reelle_bati'].min(), 
                                         df_plot['surface_reelle_bati'].max(), 100)
                    y_trend = p(x_trend)
                    fig.add_scatter(x=x_trend, y=y_trend, mode='lines', 
                                   name=get_text('overall_trendline'),
                                   line=dict(color='red', width=3, dash='dash'),
                                   showlegend=True)
                
                # 为相关性强的类型添加趋势线
                for prop_type in df['type_local'].dropna().unique():
                    type_df = df[df['type_local'] == prop_type]
                    if len(type_df) > 10:
                        type_corr = type_df['surface_reelle_bati'].corr(type_df['valeur_fonciere'])
                        if abs(type_corr) >= 0.3:
                            z = np.polyfit(type_df['surface_reelle_bati'], type_df['valeur_fonciere'], 1)
                            p = np.poly1d(z)
                            x_trend = np.linspace(type_df['surface_reelle_bati'].min(), 
                                                 type_df['surface_reelle_bati'].max(), 100)
                            y_trend = p(x_trend)
                            fig.add_scatter(x=x_trend, y=y_trend, mode='lines', 
                                           name=f'{prop_type} {get_text("type_trendline")}',
                                           line=dict(width=2, dash='dash'),
                                           showlegend=True)
            except Exception:
                # 如果出错，使用简单版本
                if lang == 'zh':
                    title_grouped = 'Q11: 建筑面积 vs 房产价值相关性（按房产类型分组）'
                    labels_grouped = {'surface_reelle_bati': '建筑面积 (m²)', 
                                     'valeur_fonciere': '房产价值 (€)',
                                     'type_local': '房产类型'}
                else:
                    title_grouped = 'Q11: Corrélation surface bâtie vs valeur foncière (par type de bien)'
                    labels_grouped = {'surface_reelle_bati': 'Surface bâtie (m²)', 
                                     'valeur_fonciere': 'Valeur foncière (€)',
                                     'type_local': 'Type de bien'}
                fig = px.scatter(df, x='surface_reelle_bati', y='valeur_fonciere',
                               color='type_local',
                               title=title_grouped,
                               labels=labels_grouped,
                               opacity=0.6)
        else:
            # 没有房产类型数据，创建整体散点图
            df_plot = df[['surface_reelle_bati', 'valeur_fonciere']].copy()
            
            if lang == 'zh':
                title = 'Q11: 建筑面积 vs 房产价值相关性'
                labels_dict = {'surface_reelle_bati': '建筑面积 (m²)', 'valeur_fonciere': '房产价值 (€)'}
                trendline_name = '趋势线'
            else:
                title = 'Q11: Corrélation surface bâtie vs valeur foncière'
                labels_dict = {'surface_reelle_bati': 'Surface bâtie (m²)', 'valeur_fonciere': 'Valeur foncière (€)'}
                trendline_name = 'Ligne de tendance'
            
            if show_trendline:
                try:
                    fig = px.scatter(df_plot, x='surface_reelle_bati', y='valeur_fonciere', 
                                    title=title,
                                    labels=labels_dict,
                                    trendline="ols",
                                    trendline_color_override="red",
                                    opacity=0.6)
                    fig.update_traces(selector=dict(type='scatter', mode='lines', name='OLS trendline'),
                                     line=dict(width=3, dash='dash'))
                except Exception:
                    fig = px.scatter(df_plot, x='surface_reelle_bati', y='valeur_fonciere', 
                                    title=title,
                                    labels=labels_dict,
                                    opacity=0.6)
                    z = np.polyfit(df_plot['surface_reelle_bati'], df_plot['valeur_fonciere'], 1)
                    p = np.poly1d(z)
                    x_trend = np.linspace(df_plot['surface_reelle_bati'].min(), df_plot['surface_reelle_bati'].max(), 100)
                    y_trend = p(x_trend)
                    fig.add_scatter(x=x_trend, y=y_trend, mode='lines', name=trendline_name,
                                   line=dict(color='red', width=3, dash='dash'))
            else:
                fig = px.scatter(df_plot, x='surface_reelle_bati', y='valeur_fonciere', 
                                title=title,
                                labels=labels_dict,
                                opacity=0.6)
        
        # 更新布局
        fig.update_layout(
            hovermode='closest',
            showlegend=True,
            annotations=[
                dict(
                    x=0.02,
                    y=0.98,
                    xref="paper",
                    yref="paper",
                    text=f"{get_text('correlation_coefficient')} = {correlation:.3f}",
                    showarrow=False,
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="black",
                    borderwidth=1
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 根据是否显示趋势线，显示不同的说明
        if has_type_data:
            if show_trendline:
                st.caption(f"💡 {get_text('trendline_note')}")
            else:
                st.caption(f"💡 {get_text('trendline_note_weak')}")
        else:
            if show_trendline:
                st.caption(f"💡 {get_text('trendline_note_simple')}")
            else:
                st.caption(f"ℹ️ {get_text('trendline_note_no')}")
        
        # 显示数据摘要
        with st.expander(get_text('data_summary')):
            st.dataframe(df.describe())
        
        with st.expander(get_text('raw_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question12(mydb):
    """Q12: Surface terrain moyenne par nature de culture"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q12_analysis_purpose')}
    
    {get_text('q12_analysis_description')}
    
    **{get_text('q12_research_questions')}**
    - {get_text('q12_research_q1')}
    - {get_text('q12_research_q2')}
    - {get_text('q12_research_q3')}
    
    **{get_text('q12_expected_results')}**
    - {get_text('q12_expected_difference')}
    - {get_text('q12_expected_usage')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT nc.code_nature_culture, 
           AVG(b.surface_terrain) as surface_moyenne
    FROM BIEN b
    JOIN NATURE_CULTURE nc ON b.nature_culture = nc.code_nature_culture
    WHERE b.surface_terrain IS NOT NULL 
      AND b.surface_terrain > 0
    GROUP BY nc.code_nature_culture
    ORDER BY surface_moyenne DESC;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q12_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q12_land_types'), len(df))
        with col2:
            largest_area = df['surface_moyenne'].max()
            st.metric(get_text('q12_largest_avg_area'), f"{largest_area:,.0f} m²")
        with col3:
            smallest_area = df['surface_moyenne'].min()
            st.metric(get_text('q12_smallest_avg_area'), f"{smallest_area:,.0f} m²")
        with col4:
            area_range = largest_area - smallest_area
            st.metric(get_text('q12_area_range'), f"{area_range:,.0f} m²")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q12_key_insights')}")
        st.info(f"""
        - {get_text('q12_insight1')}
        - {get_text('q12_insight2')}
        - {get_text('q12_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q12_comparison_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q12: 不同土地性质的平均面积对比'
            labels_dict = {'code_nature_culture': '土地性质', 'surface_moyenne': '平均面积 (m²)'}
        else:
            title = 'Q12: Surface terrain moyenne par nature de culture'
            labels_dict = {'code_nature_culture': 'Nature de culture', 'surface_moyenne': 'Surface moyenne (m²)'}
        
        fig = px.bar(df, x='code_nature_culture', y='surface_moyenne', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['code_nature_culture'],
            yaxis_title=labels_dict['surface_moyenne']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question13(mydb):
    """Q13: Évolution du prix moyen mensuel"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q13_analysis_purpose')}
    
    {get_text('q13_analysis_description')}
    
    **{get_text('q13_research_questions')}**
    - {get_text('q13_research_q1')}
    - {get_text('q13_research_q2')}
    - {get_text('q13_research_q3')}
    
    **{get_text('q13_expected_results')}**
    - {get_text('q13_expected_trend')}
    - {get_text('q13_expected_volatility')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
           AVG(valeur_fonciere) as prix_moyen
    FROM MUTATION
    WHERE valeur_fonciere IS NOT NULL
    GROUP BY mois
    ORDER BY mois;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q13_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q13_months'), len(df))
        with col2:
            highest_price = df['prix_moyen'].max()
            st.metric(get_text('q13_highest_avg_price'), f"{highest_price:,.0f} €")
        with col3:
            lowest_price = df['prix_moyen'].min()
            st.metric(get_text('q13_lowest_avg_price'), f"{lowest_price:,.0f} €")
        with col4:
            current_price = df['prix_moyen'].iloc[-1]
            st.metric(get_text('q13_current_avg_price'), f"{current_price:,.0f} €")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q13_key_insights')}")
        st.info(f"""
        - {get_text('q13_insight1')}
        - {get_text('q13_insight2')}
        - {get_text('q13_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q13_trend_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q13: 平均价格时间趋势'
            labels_dict = {'mois': '月份', 'prix_moyen': '平均价格 (€)'}
        else:
            title = 'Q13: Évolution du prix moyen mensuel'
            labels_dict = {'mois': 'Mois', 'prix_moyen': 'Prix moyen (€)'}
        
        fig = px.line(df, x='mois', y='prix_moyen', 
                     title=title,
                     labels=labels_dict)
        fig.update_traces(mode='lines+markers', line=dict(width=2), marker=dict(size=8))
        fig.update_layout(
            hovermode='x unified',
            xaxis_title=labels_dict['mois'],
            yaxis_title=labels_dict['prix_moyen']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question14(mydb):
    """Q14: Comparaison prix moyen par type de bien"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q14_analysis_purpose')}
    
    {get_text('q14_analysis_description')}
    
    **{get_text('q14_research_questions')}**
    - {get_text('q14_research_q1')}
    - {get_text('q14_research_q2')}
    - {get_text('q14_research_q3')}
    
    **{get_text('q14_expected_results')}**
    - {get_text('q14_expected_comparison')}
    - {get_text('q14_expected_range')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT tl.type_local,
           AVG(m.valeur_fonciere) as prix_moyen,
           MIN(m.valeur_fonciere) as prix_min,
           MAX(m.valeur_fonciere) as prix_max
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
    WHERE m.valeur_fonciere IS NOT NULL
    GROUP BY tl.type_local, tl.id_type_local
    ORDER BY prix_moyen DESC;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q14_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q14_property_types'), len(df))
        with col2:
            highest_avg = df['prix_moyen'].max()
            st.metric(get_text('q14_highest_avg'), f"{highest_avg:,.0f} €")
        with col3:
            df['price_range'] = df['prix_max'] - df['prix_min']
            largest_range = df['price_range'].max()
            st.metric(get_text('q14_largest_range'), f"{largest_range:,.0f} €")
        with col4:
            # 显示价格范围最大的类型
            max_range_type = df.loc[df['price_range'].idxmax(), 'type_local']
            st.metric("价格范围最大类型" if lang == 'zh' else "Type avec la plus large fourchette", max_range_type)
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q14_key_insights')}")
        st.info(f"""
        - {get_text('q14_insight1')}
        - {get_text('q14_insight2')}
        - {get_text('q14_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q14_price_comparison_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q14: 不同房产类型的价格统计对比'
            xaxis_title = '房产类型'
            yaxis_title = '价格 (€)'
            bar_names = {'prix_moyen': '平均价格', 'prix_min': '最低价格', 'prix_max': '最高价格'}
        else:
            title = 'Q14: Comparaison des prix par type de bien'
            xaxis_title = 'Type de local'
            yaxis_title = 'Prix (€)'
            bar_names = {'prix_moyen': 'Prix moyen', 'prix_min': 'Prix min', 'prix_max': 'Prix max'}
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name=bar_names['prix_moyen'], x=df['type_local'], y=df['prix_moyen']))
        fig.add_trace(go.Bar(name=bar_names['prix_min'], x=df['type_local'], y=df['prix_min']))
        fig.add_trace(go.Bar(name=bar_names['prix_max'], x=df['type_local'], y=df['prix_max']))
        fig.update_layout(title=title,
                         xaxis_title=xaxis_title,
                         yaxis_title=yaxis_title,
                         barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question15(mydb):
    """Q15: Distribution des prix pour maisons vs appartements"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q15_analysis_purpose')}
    
    {get_text('q15_analysis_description')}
    
    **{get_text('q15_research_questions')}**
    - {get_text('q15_research_q1')}
    - {get_text('q15_research_q2')}
    - {get_text('q15_research_q3')}
    
    **{get_text('q15_expected_results')}**
    - {get_text('q15_expected_comparison')}
    - {get_text('q15_expected_distribution')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT tl.type_local, 
           m.valeur_fonciere
    FROM MUTATION m
    JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
    JOIN BIEN b ON mb.id_bien = b.id_bien
    JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
    WHERE tl.type_local IN ('Maison', 'Appartement')
      AND m.valeur_fonciere IS NOT NULL
      AND m.valeur_fonciere < 800000;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q15_statistics'))
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            total_properties = len(df)
            st.metric(get_text('q15_total_properties'), f"{total_properties:,}")
        with col2:
            houses_count = len(df[df['type_local'] == 'Maison'])
            st.metric(get_text('q15_houses'), f"{houses_count:,}")
        with col3:
            apartments_count = len(df[df['type_local'] == 'Appartement'])
            st.metric(get_text('q15_apartments'), f"{apartments_count:,}")
        with col4:
            house_median = df[df['type_local'] == 'Maison']['valeur_fonciere'].median()
            st.metric(get_text('q15_house_median'), f"{house_median:,.0f} €")
        with col5:
            apartment_median = df[df['type_local'] == 'Appartement']['valeur_fonciere'].median()
            st.metric(get_text('q15_apartment_median'), f"{apartment_median:,.0f} €")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q15_key_insights')}")
        st.info(f"""
        - {get_text('q15_insight1')}
        - {get_text('q15_insight2')}
        - {get_text('q15_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q15_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q15: 房屋与公寓的价格分布对比'
            labels_dict = {'type_local': '房产类型', 'valeur_fonciere': '房产价值 (€)'}
        else:
            title = 'Q15: Distribution des prix - Maisons vs Appartements'
            labels_dict = {'type_local': 'Type de bien', 'valeur_fonciere': 'Valeur foncière (€)'}
        
        fig = px.box(df, x='type_local', y='valeur_fonciere', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['type_local'],
            yaxis_title=labels_dict['valeur_fonciere']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question16(mydb):
    """Q16: Ratio surface terrain / surface bâtie par commune"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q16_analysis_purpose')}
    
    {get_text('q16_analysis_description')}
    
    **{get_text('q16_research_questions')}**
    - {get_text('q16_research_q1')}
    - {get_text('q16_research_q2')}
    - {get_text('q16_research_q3')}
    
    **{get_text('q16_expected_results')}**
    - {get_text('q16_expected_ratio')}
    - {get_text('q16_expected_efficiency')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT c.commune,
           AVG(b.surface_terrain / NULLIF(b.surface_reelle_bati, 0)) as ratio_moyen
    FROM BIEN b
    JOIN COMMUNE c ON b.id_commune = c.id_commune
    WHERE b.surface_terrain > 0 
      AND b.surface_reelle_bati > 0
    GROUP BY c.commune
    HAVING COUNT(*) > 5
    ORDER BY ratio_moyen DESC
    LIMIT 10;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q16_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q16_cities_shown'), len(df))
        with col2:
            highest_ratio = df['ratio_moyen'].max()
            st.metric(get_text('q16_highest_ratio'), f"{highest_ratio:.2f}")
        with col3:
            lowest_ratio = df['ratio_moyen'].min()
            st.metric(get_text('q16_lowest_ratio'), f"{lowest_ratio:.2f}")
        with col4:
            avg_ratio = df['ratio_moyen'].mean()
            st.metric(get_text('q16_avg_ratio'), f"{avg_ratio:.2f}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q16_key_insights')}")
        st.info(f"""
        - {get_text('q16_insight1')}
        - {get_text('q16_insight2')}
        - {get_text('q16_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q16_ranking_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q16: 土地/建筑面积比前10名城市'
            labels_dict = {'ratio_moyen': '平均比值', 'commune': '城市'}
        else:
            title = 'Q16: Top 10 ratio surface terrain/surface bâtie par commune'
            labels_dict = {'ratio_moyen': 'Ratio moyen', 'commune': 'Commune'}
        
        fig = px.bar(df, x='ratio_moyen', y='commune', orientation='h',
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['ratio_moyen'],
            yaxis_title=labels_dict['commune']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question17(mydb):
    """Q17: Nombre de biens par transaction"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q17_analysis_purpose')}
    
    {get_text('q17_analysis_description')}
    
    **{get_text('q17_research_questions')}**
    - {get_text('q17_research_q1')}
    - {get_text('q17_research_q2')}
    - {get_text('q17_research_q3')}
    
    **{get_text('q17_expected_results')}**
    - {get_text('q17_expected_complexity')}
    - {get_text('q17_expected_pattern')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT nb_biens, 
           COUNT(*) as nb_mutations
    FROM (
        SELECT m.id_mutation, 
               COUNT(mb.id_bien) as nb_biens
        FROM MUTATION m
        JOIN MUTATION_BIEN mb ON m.id_mutation = mb.id_mutation
        GROUP BY m.id_mutation
    ) as subq
    GROUP BY nb_biens
    ORDER BY nb_biens;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q17_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_transactions = df['nb_mutations'].sum()
            st.metric(get_text('q17_total_transactions'), f"{total_transactions:,}")
        with col2:
            most_common = df.loc[df['nb_mutations'].idxmax(), 'nb_biens']
            most_common_value = df['nb_mutations'].max()
            st.metric(get_text('q17_most_common_count'), f"{most_common} {get_text('rows') if lang == 'zh' else 'biens'}\n({most_common_value:,})")
        with col3:
            max_properties = df['nb_biens'].max()
            st.metric(get_text('q17_max_properties'), max_properties)
        with col4:
            # 计算加权平均
            avg_properties = (df['nb_biens'] * df['nb_mutations']).sum() / df['nb_mutations'].sum()
            st.metric(get_text('q17_avg_properties'), f"{avg_properties:.2f}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q17_key_insights')}")
        st.info(f"""
        - {get_text('q17_insight1')}
        - {get_text('q17_insight2')}
        - {get_text('q17_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q17_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q17: 每笔交易的房产数量分布'
            labels_dict = {'nb_biens': '房产数量', 'nb_mutations': '交易数量'}
        else:
            title = 'Q17: Nombre de biens par transaction'
            labels_dict = {'nb_biens': 'Nombre de biens', 'nb_mutations': 'Nombre de mutations'}
        
        fig = px.bar(df, x='nb_biens', y='nb_mutations', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['nb_biens'],
            yaxis_title=labels_dict['nb_mutations']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question18(mydb):
    """Q18: Pourcentage de biens avec/sans terrain par type"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q18_analysis_purpose')}
    
    {get_text('q18_analysis_description')}
    
    **{get_text('q18_research_questions')}**
    - {get_text('q18_research_q1')}
    - {get_text('q18_research_q2')}
    - {get_text('q18_research_q3')}
    
    **{get_text('q18_expected_results')}**
    - {get_text('q18_expected_characteristics')}
    - {get_text('q18_expected_distribution')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT tl.type_local,
           SUM(CASE WHEN b.surface_terrain > 0 THEN 1 ELSE 0 END) as avec_terrain,
           SUM(CASE WHEN b.surface_terrain IS NULL OR b.surface_terrain = 0 THEN 1 ELSE 0 END) as sans_terrain
    FROM BIEN b
    JOIN TYPE_LOCAL tl ON b.id_type_local = tl.id_type_local
    WHERE tl.type_local IS NOT NULL
    GROUP BY tl.type_local;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q18_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(get_text('q18_property_types'), len(df))
        with col2:
            total_with_land = df['avec_terrain'].sum()
            st.metric(get_text('q18_total_with_land'), f"{total_with_land:,}")
        with col3:
            total_without_land = df['sans_terrain'].sum()
            st.metric(get_text('q18_total_without_land'), f"{total_without_land:,}")
        with col4:
            total_all = total_with_land + total_without_land
            land_rate = (total_with_land / total_all * 100) if total_all > 0 else 0
            st.metric(get_text('q18_land_ownership_rate'), f"{land_rate:.1f}%")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q18_key_insights')}")
        st.info(f"""
        - {get_text('q18_insight1')}
        - {get_text('q18_insight2')}
        - {get_text('q18_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q18_comparison_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q18: 不同房产类型的土地拥有情况'
            xaxis_title = '房产类型'
            yaxis_title = '房产数量'
            bar_names = {'avec_terrain': '有土地', 'sans_terrain': '无土地'}
        else:
            title = 'Q18: Biens avec/sans terrain par type'
            xaxis_title = 'Type de local'
            yaxis_title = 'Nombre de biens'
            bar_names = {'avec_terrain': 'Avec terrain', 'sans_terrain': 'Sans terrain'}
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name=bar_names['avec_terrain'], x=df['type_local'], y=df['avec_terrain']))
        fig.add_trace(go.Bar(name=bar_names['sans_terrain'], x=df['type_local'], y=df['sans_terrain']))
        fig.update_layout(title=title,
                         xaxis_title=xaxis_title,
                         yaxis_title=yaxis_title,
                         barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "BIEN")

def question19(mydb):
    """Q19: Transactions par jour de la semaine"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q19_analysis_purpose')}
    
    {get_text('q19_analysis_description')}
    
    **{get_text('q19_research_questions')}**
    - {get_text('q19_research_q1')}
    - {get_text('q19_research_q2')}
    - {get_text('q19_research_q3')}
    
    **{get_text('q19_expected_results')}**
    - {get_text('q19_expected_pattern')}
    - {get_text('q19_expected_behavior')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT DAYNAME(date_mutation) as jour_semaine,
           DAYOFWEEK(date_mutation) as jour_num,
           COUNT(*) as nombre_transactions
    FROM MUTATION
    GROUP BY jour_semaine, jour_num
    ORDER BY jour_num;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q19_statistics'))
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_transactions = df['nombre_transactions'].sum()
            st.metric(get_text('q19_total_transactions'), f"{total_transactions:,}")
        with col2:
            most_active = df.loc[df['nombre_transactions'].idxmax(), 'jour_semaine']
            most_active_value = df['nombre_transactions'].max()
            st.metric(get_text('q19_most_active_day'), f"{most_active}\n({most_active_value:,})")
        with col3:
            least_active = df.loc[df['nombre_transactions'].idxmin(), 'jour_semaine']
            least_active_value = df['nombre_transactions'].min()
            st.metric(get_text('q19_least_active_day'), f"{least_active}\n({least_active_value:,})")
        with col4:
            # 计算工作日平均（周一到周五）
            weekday_df = df[df['jour_num'].between(2, 6)]
            weekday_avg = weekday_df['nombre_transactions'].mean() if len(weekday_df) > 0 else 0
            st.metric(get_text('q19_weekday_avg'), f"{weekday_avg:.0f}")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q19_key_insights')}")
        st.info(f"""
        - {get_text('q19_insight1')}
        - {get_text('q19_insight2')}
        - {get_text('q19_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q19_distribution_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q19: 一周中不同日期的交易分布'
            labels_dict = {'jour_semaine': '星期', 'nombre_transactions': '交易数量'}
        else:
            title = 'Q19: Transactions par jour de la semaine'
            labels_dict = {'jour_semaine': 'Jour de la semaine', 'nombre_transactions': 'Nombre de transactions'}
        
        fig = px.bar(df, x='jour_semaine', y='nombre_transactions', 
                    title=title,
                    labels=labels_dict)
        fig.update_layout(
            xaxis_title=labels_dict['jour_semaine'],
            yaxis_title=labels_dict['nombre_transactions']
        )
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question20(mydb):
    """Q20: Comparaison volumes de ventes par semaine"""
    
    # 分析目的说明
    lang = st.session_state.get('language', 'zh')
    st.markdown(f"""
    ### {get_text('q20_analysis_purpose')}
    
    {get_text('q20_analysis_description')}
    
    **{get_text('q20_research_questions')}**
    - {get_text('q20_research_q1')}
    - {get_text('q20_research_q2')}
    - {get_text('q20_research_q3')}
    
    **{get_text('q20_expected_results')}**
    - {get_text('q20_expected_analysis')}
    - {get_text('q20_expected_trends')}
    """)
    
    st.markdown("---")
    
    query = """
    SELECT YEARWEEK(date_mutation) as semaine,
           COUNT(*) as nb_transactions,
           SUM(valeur_fonciere) as volume_total,
           AVG(valeur_fonciere) as moyenne_transaction
    FROM MUTATION
    WHERE valeur_fonciere IS NOT NULL
    GROUP BY semaine
    ORDER BY semaine;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        # 计算统计信息
        st.subheader(get_text('q20_statistics'))
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric(get_text('q20_weeks'), len(df))
        with col2:
            total_transactions = df['nb_transactions'].sum()
            st.metric(get_text('q20_total_transactions'), f"{total_transactions:,}")
        with col3:
            total_volume = df['volume_total'].sum()
            st.metric(get_text('q20_total_volume'), f"{total_volume:,.0f} €")
        with col4:
            avg_transactions = df['nb_transactions'].mean()
            st.metric(get_text('q20_avg_transactions_per_week'), f"{avg_transactions:.0f}")
        with col5:
            avg_volume = df['volume_total'].mean()
            st.metric(get_text('q20_avg_volume_per_week'), f"{avg_volume:,.0f} €")
        
        # 显示关键洞察
        st.markdown(f"#### {get_text('q20_key_insights')}")
        st.info(f"""
        - {get_text('q20_insight1')}
        - {get_text('q20_insight2')}
        - {get_text('q20_insight3')}
        """)
        
        st.markdown("---")
        st.subheader(get_text('q20_trend_chart'))
        
        # 创建图表
        if lang == 'zh':
            title = 'Q20: 每周交易量和交易总额趋势'
            xaxis_title = '周'
            yaxis_title_1 = '交易数量'
            yaxis_title_2 = '交易总额 (€)'
            trace_names = {'transactions': '交易数量', 'volume': '交易总额'}
        else:
            title = 'Q20: Évolution du volume de ventes par semaine'
            xaxis_title = 'Semaine'
            yaxis_title_1 = 'Nombre de transactions'
            yaxis_title_2 = 'Volume total (€)'
            trace_names = {'transactions': 'Nb transactions', 'volume': 'Volume total'}
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df['semaine'], y=df['nb_transactions'], name=trace_names['transactions'], mode='lines+markers'),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=df['semaine'], y=df['volume_total'], name=trace_names['volume'], mode='lines+markers'),
            secondary_y=True,
        )
        fig.update_layout(title=title)
        fig.update_xaxes(title_text=xaxis_title)
        fig.update_yaxes(title_text=yaxis_title_1, secondary_y=False)
        fig.update_yaxes(title_text=yaxis_title_2, secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

# ============================================
# 主应用
# ============================================
def main():
    # 初始化会话状态
    init_session_state()
    
    # 获取当前语言（在语言选择器之前获取，以便正确应用RTL）
    current_lang = st.session_state.get('language', 'zh')
    
    # 为阿拉伯语添加RTL支持，其他语言使用LTR
    if current_lang == 'ar':
        st.markdown("""
        <style>
        /* RTL支持 - 阿拉伯语 */
        .stApp {
            direction: rtl !important;
        }
        .stApp > header {
            direction: rtl !important;
        }
        .main .block-container {
            direction: rtl !important;
            text-align: right !important;
        }
        .stSidebar {
            direction: rtl !important;
            text-align: right !important;
        }
        .stSidebar .stMarkdown {
            direction: rtl !important;
            text-align: right !important;
        }
        /* 确保文本元素RTL */
        .main p, .main div, .main span, .main h1, .main h2, .main h3, .main h4, .main h5, .main h6, 
        .main li, .main label, .stSidebar p, .stSidebar div, .stSidebar span, 
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
            direction: rtl !important;
            text-align: right !important;
        }
        /* 输入框RTL - 标签和输入框对齐 */
        .stTextInput label {
            direction: rtl !important;
            text-align: right !important;
        }
        .stTextInput > div > div > input {
            direction: rtl !important;
            text-align: right !important;
        }
        /* 选择框RTL */
        .stSelectbox label {
            direction: rtl !important;
            text-align: right !important;
        }
        .stSelectbox > div > div {
            direction: rtl !important;
            text-align: right !important;
        }
        /* Radio按钮RTL */
        .stRadio label {
            direction: rtl !important;
            text-align: right !important;
        }
        .stRadio > label {
            direction: rtl !important;
            text-align: right !important;
        }
        /* Expander RTL */
        .streamlit-expanderHeader {
            direction: rtl !important;
            text-align: right !important;
        }
        /* Info/Error/Warning框RTL */
        .stAlert {
            direction: rtl !important;
            text-align: right !important;
        }
        .stAlert > div {
            direction: rtl !important;
            text-align: right !important;
        }
        /* 列表RTL */
        ul, ol {
            direction: rtl !important;
            text-align: right !important;
            padding-right: 1.5em !important;
            padding-left: 0 !important;
        }
        li {
            direction: rtl !important;
            text-align: right !important;
        }
        /* 确保图表容器不改变方向 */
        .js-plotly-plot {
            direction: ltr !important;
        }
        /* 表格RTL */
        .stDataFrame {
            direction: rtl !important;
        }
        table {
            direction: rtl !important;
        }
        /* 代码块保持LTR */
        pre, code {
            direction: ltr !important;
            text-align: left !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # 非阿拉伯语时确保LTR（强制覆盖之前的RTL样式）
        st.markdown("""
        <style>
        .stApp {
            direction: ltr !important;
        }
        .stApp > header {
            direction: ltr !important;
        }
        .main .block-container {
            direction: ltr !important;
            text-align: left !important;
        }
        .stSidebar {
            direction: ltr !important;
            text-align: left !important;
        }
        .stSidebar .stMarkdown {
            direction: ltr !important;
            text-align: left !important;
        }
        /* 确保文本元素LTR */
        .main p, .main div, .main span, .main h1, .main h2, .main h3, .main h4, .main h5, .main h6, 
        .main li, .main label, .stSidebar p, .stSidebar div, .stSidebar span, 
        .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
            direction: ltr !important;
            text-align: left !important;
        }
        /* 输入框LTR */
        .stTextInput > div > div > input {
            direction: ltr !important;
            text-align: left !important;
        }
        /* 选择框LTR */
        .stSelectbox > div > div {
            direction: ltr !important;
            text-align: left !important;
        }
        /* 图表容器LTR */
        .js-plotly-plot {
            direction: ltr !important;
        }
        /* 表格LTR */
        .stDataFrame {
            direction: ltr !important;
        }
        table {
            direction: ltr !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # 侧边栏 - 语言选择（放在最顶部）
    st.sidebar.markdown("### 🌐 语言 / Langue")
    
    # 使用 key 参数确保组件状态稳定，避免不必要的重新运行
    language_options = ['zh', 'fr', 'en', 'ar', 'mg']
    language_labels = {
        'zh': '🇨🇳 中文',
        'fr': '🇫🇷 Français',
        'en': '🇬🇧 English',
        'ar': '🇸🇦 العربية',
        'mg': '🇲🇬 Malagasy'
    }
    
    # 获取当前语言的索引
    current_lang = st.session_state.get('language', 'zh')
    current_index = language_options.index(current_lang) if current_lang in language_options else 0
    
    language = st.sidebar.radio(
        "",
        options=language_options,
        format_func=lambda x: language_labels.get(x, x),
        index=current_index,
        horizontal=True,
        key='language_selector'
    )
    
    # 更新语言设置（不清除连接缓存，保持已登录状态）
    # 只有当语言真正改变时才更新，并触发重新渲染以应用RTL/LTR样式
    if st.session_state.get('language') != language:
        st.session_state.language = language
        # 语言改变时重新渲染以应用正确的RTL/LTR样式
        st.rerun()
    st.sidebar.markdown("---")
    
    # 标题
    st.title(get_text('app_title'))
    st.markdown("---")
    
    # 侧边栏 - 数据库配置
    st.sidebar.title(get_text('db_config'))
    with st.sidebar.expander(get_text('db_settings'), expanded=True):
        st.info(get_text('db_tip'))
        # 使用 session_state 保存数据库配置，避免语言切换时丢失
        if 'db_config' not in st.session_state:
            st.session_state.db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '',
                'database': 'foncieres'
            }
        
        db_host = st.text_input(get_text('host'), value=st.session_state.db_config['host'], help=get_text('host_help'), key='db_host')
        db_user = st.text_input(get_text('user'), value=st.session_state.db_config['user'], help=get_text('user_help'), key='db_user')
        db_password = st.text_input(get_text('password'), value=st.session_state.db_config['password'], type="password", help=get_text('password_help'), key='db_password')
        db_database = st.text_input(get_text('database'), value=st.session_state.db_config['database'], help=get_text('database_help'), key='db_database')
        
        # 更新 session_state 中的配置
        st.session_state.db_config = {
            'host': db_host,
            'user': db_user,
            'password': db_password,
            'database': db_database
        }
    
    st.sidebar.markdown("---")
    
    # 侧边栏 - 分析问题选择
    st.sidebar.title(get_text('analysis_selection'))
    st.sidebar.markdown(get_text('select_question'))
    
    # 问题列表（多语言，使用get_text动态获取标题）
    question_functions = [question1, question2, question3, question4, question5, 
                         question6, question7, question8, question9, question10,
                         question11, question12, question13, question14, question15,
                         question16, question17, question18, question19, question20]
    
    question_keys = ['q1_title', 'q2_title', 'q3_title', 'q4_title', 'q5_title',
                    'q6_title', 'q7_title', 'q8_title', 'q9_title', 'q10_title',
                    'q11_title', 'q12_title', 'q13_title', 'q14_title', 'q15_title',
                    'q16_title', 'q17_title', 'q18_title', 'q19_title', 'q20_title']
    
    # 创建问题字典，使用当前语言的标题
    questions = {get_text(key): func for key, func in zip(question_keys, question_functions)}
    
    selected_question = st.sidebar.selectbox(
        get_text('select_question_label'),
        list(questions.keys())
    )
    
    # 数据库连接
    result = init_connection(db_host, db_user, db_password, db_database)
    
    if isinstance(result, tuple) and result[0] is None:
        # 连接失败，根据当前语言格式化错误信息
        error_code = result[1]
        error_msg = result[2]
        host = result[3] if len(result) > 3 else db_host
        user = result[4] if len(result) > 4 else db_user
        database = result[5] if len(result) > 5 else db_database
        error_detail = format_error_message(error_code, error_msg, host, user, database)
        st.error(error_detail)
        st.markdown("---")
        st.markdown(f"### {get_text('diagnostic_steps')}")
        if language == 'zh':
            st.markdown(f"""
            1. **{get_text('check_mysql_service')}**
               - Windows: 打开"服务"，查找 "MySQL" 服务，确保状态为"正在运行"
               - 或在命令行运行: `net start MySQL80` (根据你的 MySQL 版本调整)
            
            2. **{get_text('verify_connection')}**
               - 使用 MySQL Workbench 或命令行测试连接
               - 命令: `mysql -u {db_user} -p` (然后输入密码)
            
            3. **{get_text('check_permissions')}**
               - 确认用户 `{db_user}` 存在且有访问 `{db_database}` 数据库的权限
               - 如果用户不存在，需要创建用户并授权
            
            4. **{get_text('confirm_db_created')}**
               - 运行 `create_tab.sql` 创建数据库和表结构
            """)
        elif language == 'ar':
            st.markdown(f"""
            1. **{get_text('check_mysql_service')}**
               - Windows: افتح "Services"، ابحث عن خدمة "MySQL"، تأكد من أن الحالة هي "قيد التشغيل"
               - أو قم بالتشغيل من سطر الأوامر: `net start MySQL80` (اضبط حسب إصدار MySQL الخاص بك)
            
            2. **{get_text('verify_connection')}**
               - اختبر الاتصال باستخدام MySQL Workbench أو سطر الأوامر
               - الأمر: `mysql -u {db_user} -p` (ثم أدخل كلمة المرور)
            
            3. **{get_text('check_permissions')}**
               - تأكد من وجود المستخدم `{db_user}` وأن لديه صلاحيات الوصول إلى قاعدة البيانات `{db_database}`
               - إذا لم يكن المستخدم موجوداً، قم بإنشاء المستخدم ومنح الصلاحيات
            
            4. **{get_text('confirm_db_created')}**
               - قم بتشغيل `create_tab.sql` لإنشاء قاعدة البيانات وهيكل الجداول
            """)
        elif language == 'en':
            st.markdown(f"""
            1. **{get_text('check_mysql_service')}**
               - Windows: Open "Services", find the "MySQL" service, ensure the status is "Running"
               - Or run in command line: `net start MySQL80` (adjust according to your MySQL version)
            
            2. **{get_text('verify_connection')}**
               - Test the connection using MySQL Workbench or command line
               - Command: `mysql -u {db_user} -p` (then enter the password)
            
            3. **{get_text('check_permissions')}**
               - Confirm that user `{db_user}` exists and has access permissions to database `{db_database}`
               - If the user does not exist, create the user and grant permissions
            
            4. **{get_text('confirm_db_created')}**
               - Run `create_tab.sql` to create the database and table structure
            """)
        elif language == 'mg':
            st.markdown(f"""
            1. **{get_text('check_mysql_service')}**
               - Windows: Sokafy "Services", hitady ny service "MySQL", aoka ho "Mihazakazaka" ny satany
               - Na alefaso amin'ny command line: `net start MySQL80` (ampifanaraho araka ny dikan'ny MySQL anao)
            
            2. **{get_text('verify_connection')}**
               - Andramo ny fifandraisana amin'ny MySQL Workbench na ny command line
               - Baiko: `mysql -u {db_user} -p` (ary ampidiro ny tenimiafina)
            
            3. **{get_text('check_permissions')}**
               - Hamarinina fa misy ny mpampiasa `{db_user}` ary manana alalana hiditra amin'ny database `{db_database}`
               - Raha tsy misy ny mpampiasa, mamorona mpampiasa ary manome alalana
            
            4. **{get_text('confirm_db_created')}**
               - Alefaso ny `create_tab.sql` mba hamorona ny database sy ny firafitry ny tabilao
            """)
        else:  # fr
            st.markdown(f"""
            1. **{get_text('check_mysql_service')}**
               - Windows: Ouvrir "Services", trouver le service "MySQL", s'assurer que le statut est "En cours d'exécution"
               - Ou exécuter en ligne de commande: `net start MySQL80` (ajuster selon votre version MySQL)
            
            2. **{get_text('verify_connection')}**
               - Tester la connexion avec MySQL Workbench ou la ligne de commande
               - Commande: `mysql -u {db_user} -p` (puis entrer le mot de passe)
            
            3. **{get_text('check_permissions')}**
               - Confirmer que l'utilisateur `{db_user}` existe et a les permissions d'accès à la base de données `{db_database}`
               - Si l'utilisateur n'existe pas, créer l'utilisateur et accorder les permissions
            
            4. **{get_text('confirm_db_created')}**
               - Exécuter `create_tab.sql` pour créer la base de données et la structure des tables
            """)
        st.stop()
    
    mydb = result
    
    # 显示连接成功提示
    st.sidebar.success("✅ 数据库连接成功")
    
    # 数据库状态检查（在侧边栏）
    with st.sidebar.expander(get_text('db_status_check'), expanded=False):
        try:
            # 检查主要表的数据量
            tables_to_check = ['MUTATION', 'BIEN', 'COMMUNE', 'DEPARTEMENT']
            row_text = get_text('rows')
            for table in tables_to_check:
                try:
                    count_query = f"SELECT COUNT(*) as count FROM {table};"
                    count_df = pd.read_sql(count_query, mydb)
                    count = count_df['count'].iloc[0]
                    if count > 0:
                        st.success(f"✅ {table}: {count:,} {row_text}")
                    else:
                        if language == 'zh':
                            st.warning(f"⚠️ {table}: 0 {row_text}（表为空）")
                        else:
                            st.warning(f"⚠️ {table}: 0 {row_text} (table vide)")
                except Exception as e:
                    if language == 'zh':
                        st.error(f"❌ {table}: 表不存在或无法访问")
                    else:
                        st.error(f"❌ {table}: Table inexistante ou inaccessible")
        except Exception as e:
            if language == 'zh':
                st.error(f"检查数据库状态时出错: {e}")
            else:
                st.error(f"Erreur lors de la vérification de l'état de la base de données: {e}")
    
    # 显示选中的问题
    st.header(selected_question)
    
    # 执行对应的查询和可视化
    questions[selected_question](mydb)
    
    # 页脚信息
    st.sidebar.markdown("---")
    st.sidebar.info(get_text('tip_chart'))
    st.sidebar.markdown(f"**{get_text('database_label')}**: {db_database}")
    st.sidebar.markdown(f"**{get_text('data_source')}**: DVF (Demandes de valeurs foncières)")

if __name__ == "__main__":
    main()

