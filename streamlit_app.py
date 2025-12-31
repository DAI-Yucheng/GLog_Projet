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
    }
}

def get_text(key):
    """获取当前语言的文本"""
    lang = st.session_state.get('language', 'zh')
    return LANGUAGES[lang].get(key, key)

def init_session_state():
    """初始化会话状态"""
    if 'language' not in st.session_state:
        st.session_state.language = 'zh'

# ============================================
# 数据库连接（使用缓存）
# ============================================
@st.cache_resource
def init_connection(host, user, password, database):
    """初始化数据库连接"""
    lang = st.session_state.get('language', 'zh')
    try:
        mydb = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return mydb
    except mysql.connector.Error as e:
        error_msg = str(e)
        if "Access denied" in error_msg or "28000" in error_msg:
            if lang == 'zh':
                error_detail = f"""{get_text('db_auth_failed')}

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
            else:
                error_detail = f"""{get_text('db_auth_failed')}

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
            return (None, error_detail)
        elif "Unknown database" in error_msg:
            if lang == 'zh':
                error_detail = f"""{get_text('db_not_found')}

**{get_text('solutions')}**
- 确认数据库 '{database}' 已创建
- 运行 `create_tab.sql` 创建数据库和表
- 或手动创建数据库：
  ```sql
  CREATE DATABASE {database};
  ```"""
            else:
                error_detail = f"""{get_text('db_not_found')}

**{get_text('solutions')}**
- Confirmer que la base de données '{database}' a été créée
- Exécuter `create_tab.sql` pour créer la base de données et les tables
- Ou créer manuellement la base de données :
  ```sql
  CREATE DATABASE {database};
  ```"""
            return (None, error_detail)
        elif "Can't connect" in error_msg or "2003" in error_msg:
            if lang == 'zh':
                error_detail = f"""{get_text('db_connect_failed')}

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
                error_detail = f"""{get_text('db_connect_failed')}

**{get_text('possible_reasons')}**
1. {get_text('service_not_running')}
2. {get_text('host_port_wrong')}

**{get_text('solutions')}**
- {get_text('check_service')}
  - Windows: Ouvrir "Services", trouver le service MySQL
  - Ou exécuter: `net start MySQL80` (ajuster selon votre version)
- Confirmer que l'adresse du serveur '{host}' est correcte
- {get_text('check_firewall')}"""
            return (None, error_detail)
        else:
            if lang == 'zh':
                return (None, f"❌ 数据库连接失败: {error_msg}")
            else:
                return (None, f"❌ Échec de la connexion à la base de données: {error_msg}")
    except Exception as e:
        if lang == 'zh':
            return (None, f"❌ 未知错误: {e}")
        else:
            return (None, f"❌ Erreur inconnue: {e}")

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
    query = """
    SELECT DATE_FORMAT(date_mutation, '%Y-%m') as mois, 
           COUNT(*) as nombre_mutations
    FROM MUTATION
    GROUP BY mois
    ORDER BY mois;
    """
    df = execute_query(query, mydb)
    if not df.empty:
        fig = px.line(df, x='mois', y='nombre_mutations', 
                     title='Q1: Évolution du nombre de mutations par mois',
                     labels={'mois': 'Mois', 'nombre_mutations': 'Nombre de mutations'})
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)
    else:
        show_empty_result_message(query, mydb, "MUTATION")

def question2(mydb):
    """Q2: Distribution des valeurs foncières par tranche"""
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
        fig = px.bar(df, x='tranche', y='nombre', 
                    title='Q2: Distribution des valeurs foncières par tranche',
                    labels={'tranche': 'Tranche de prix', 'nombre': 'Nombre de mutations'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question3(mydb):
    """Q3: Valeur foncière moyenne par nature de mutation"""
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
        fig = px.bar(df, x='valeur_moyenne', y='nature_mutation', orientation='h',
                    title='Q3: Valeur foncière moyenne par nature de mutation',
                    labels={'valeur_moyenne': 'Valeur moyenne (€)', 'nature_mutation': 'Nature de mutation'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question4(mydb):
    """Q4: Répartition des biens par type de local"""
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
        fig = px.pie(df, values='nombre', names='type_local', 
                    title='Q4: Répartition des biens par type de local')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question5(mydb):
    """Q5: Prix moyen au m² par type de local"""
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
        fig = px.bar(df, x='type_local', y='prix_m2', 
                    title='Q5: Prix moyen au m² par type de local',
                    labels={'type_local': 'Type de local', 'prix_m2': 'Prix au m² (€)'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question6(mydb):
    """Q6: Distribution du nombre de pièces principales"""
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
        fig = px.bar(df, x='nombre_pieces_principales', y='nombre_biens', 
                    title='Q6: Distribution du nombre de pièces principales',
                    labels={'nombre_pieces_principales': 'Nombre de pièces', 'nombre_biens': 'Nombre de biens'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question7(mydb):
    """Q7: Top 10 des communes par nombre de transactions"""
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
        fig = px.bar(df, x='nb_transactions', y='commune', orientation='h',
                    title='Q7: Top 10 des communes par nombre de transactions',
                    labels={'nb_transactions': 'Nombre de transactions', 'commune': 'Commune'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question8(mydb):
    """Q8: Valeur foncière moyenne par département"""
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
        fig = px.bar(df, x='code_departement', y='valeur_moyenne', 
                    title='Q8: Valeur foncière moyenne par département',
                    labels={'code_departement': 'Département', 'valeur_moyenne': 'Valeur moyenne (€)'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question9(mydb):
    """Q9: Volume de transactions par code postal"""
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
        fig = px.bar(df, x='code_postal', y='nombre_transactions', 
                    title='Q9: Top 15 des codes postaux par nombre de transactions',
                    labels={'code_postal': 'Code postal', 'nombre_transactions': 'Nombre de transactions'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question10(mydb):
    """Q10: Distribution des surfaces bâties"""
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
        fig = px.bar(df, x='tranche_surface', y='nombre', 
                    title='Q10: Distribution des surfaces bâties',
                    labels={'tranche_surface': 'Tranche de surface', 'nombre': 'Nombre de biens'})
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
        fig = px.bar(df, x='code_nature_culture', y='surface_moyenne', 
                    title='Q12: Surface terrain moyenne par nature de culture',
                    labels={'code_nature_culture': 'Nature de culture', 'surface_moyenne': 'Surface moyenne (m²)'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question13(mydb):
    """Q13: Évolution du prix moyen mensuel"""
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
        fig = px.line(df, x='mois', y='prix_moyen', 
                     title='Q13: Évolution du prix moyen mensuel',
                     labels={'mois': 'Mois', 'prix_moyen': 'Prix moyen (€)'})
        fig.update_traces(mode='lines+markers')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question14(mydb):
    """Q14: Comparaison prix moyen par type de bien"""
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
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Prix moyen', x=df['type_local'], y=df['prix_moyen']))
        fig.add_trace(go.Bar(name='Prix min', x=df['type_local'], y=df['prix_min']))
        fig.add_trace(go.Bar(name='Prix max', x=df['type_local'], y=df['prix_max']))
        fig.update_layout(title='Q14: Comparaison des prix par type de bien',
                         xaxis_title='Type de local',
                         yaxis_title='Prix (€)',
                         barmode='group')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question15(mydb):
    """Q15: Distribution des prix pour maisons vs appartements"""
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
        fig = px.box(df, x='type_local', y='valeur_fonciere', 
                    title='Q15: Distribution des prix - Maisons vs Appartements',
                    labels={'type_local': 'Type de bien', 'valeur_fonciere': 'Valeur foncière (€)'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question16(mydb):
    """Q16: Ratio surface terrain / surface bâtie par commune"""
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
        fig = px.bar(df, x='ratio_moyen', y='commune', orientation='h',
                    title='Q16: Top 10 ratio surface terrain/surface bâtie par commune',
                    labels={'ratio_moyen': 'Ratio moyen', 'commune': 'Commune'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question17(mydb):
    """Q17: Nombre de biens par transaction"""
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
        fig = px.bar(df, x='nb_biens', y='nb_mutations', 
                    title='Q17: Nombre de biens par transaction',
                    labels={'nb_biens': 'Nombre de biens', 'nb_mutations': 'Nombre de mutations'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question18(mydb):
    """Q18: Pourcentage de biens avec/sans terrain par type"""
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
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Avec terrain', x=df['type_local'], y=df['avec_terrain']))
        fig.add_trace(go.Bar(name='Sans terrain', x=df['type_local'], y=df['sans_terrain']))
        fig.update_layout(title='Q18: Biens avec/sans terrain par type',
                         xaxis_title='Type de local',
                         yaxis_title='Nombre de biens',
                         barmode='stack')
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question19(mydb):
    """Q19: Transactions par jour de la semaine"""
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
        fig = px.bar(df, x='jour_semaine', y='nombre_transactions', 
                    title='Q19: Transactions par jour de la semaine',
                    labels={'jour_semaine': 'Jour de la semaine', 'nombre_transactions': 'Nombre de transactions'})
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

def question20(mydb):
    """Q20: Comparaison volumes de ventes par semaine"""
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
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Scatter(x=df['semaine'], y=df['nb_transactions'], name="Nb transactions", mode='lines+markers'),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=df['semaine'], y=df['volume_total'], name="Volume total", mode='lines+markers'),
            secondary_y=True,
        )
        fig.update_layout(title='Q20: Évolution du volume de ventes par semaine')
        fig.update_xaxis_title("Semaine")
        fig.update_yaxis_title("Nombre de transactions", secondary_y=False)
        fig.update_yaxis_title("Volume total (€)", secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        with st.expander(get_text('view_data')):
            st.dataframe(df)

# ============================================
# 主应用
# ============================================
def main():
    # 初始化会话状态
    init_session_state()
    
    # 侧边栏 - 语言选择（放在最顶部）
    st.sidebar.markdown("### 🌐 语言 / Langue")
    language = st.sidebar.radio(
        "",
        options=['zh', 'fr'],
        format_func=lambda x: '🇨🇳 中文' if x == 'zh' else '🇫🇷 Français',
        index=0 if st.session_state.language == 'zh' else 1,
        horizontal=True
    )
    st.session_state.language = language
    st.sidebar.markdown("---")
    
    # 标题
    st.title(get_text('app_title'))
    st.markdown("---")
    
    # 侧边栏 - 数据库配置
    st.sidebar.title(get_text('db_config'))
    with st.sidebar.expander(get_text('db_settings'), expanded=True):
        st.info(get_text('db_tip'))
        db_host = st.text_input(get_text('host'), value="localhost", help=get_text('host_help'))
        db_user = st.text_input(get_text('user'), value="root", help=get_text('user_help'))
        db_password = st.text_input(get_text('password'), value="", type="password", help=get_text('password_help'))
        db_database = st.text_input(get_text('database'), value="foncieres", help=get_text('database_help'))
    
    st.sidebar.markdown("---")
    
    # 侧边栏 - 分析问题选择
    st.sidebar.title(get_text('analysis_selection'))
    st.sidebar.markdown(get_text('select_question'))
    
    # 问题列表（双语）
    questions_zh = {
        "Q1: 每月交易数量变化": question1,
        "Q2: 价格区间分布": question2,
        "Q3: 按交易类型的平均价格": question3,
        "Q4: 房产类型分布": question4,
        "Q5: 每平方米价格（按类型）": question5,
        "Q6: 房间数分布": question6,
        "Q7: 交易量Top10城市": question7,
        "Q8: 各省平均价格": question8,
        "Q9: 邮政编码交易量Top15": question9,
        "Q10: 建筑面积分布": question10,
        "Q11: 面积与价格相关性": question11,
        "Q12: 土地性质平均面积": question12,
        "Q13: 月度平均价格变化": question13,
        "Q14: 房产类型价格对比": question14,
        "Q15: 房屋vs公寓价格分布": question15,
        "Q16: 土地/建筑面积比Top10": question16,
        "Q17: 每笔交易的房产数量": question17,
        "Q18: 有/无土地房产统计": question18,
        "Q19: 一周交易分布": question19,
        "Q20: 周交易量分析": question20,
    }
    
    questions_fr = {
        "Q1: Évolution du nombre de mutations par mois": question1,
        "Q2: Distribution des valeurs foncières par tranche": question2,
        "Q3: Valeur foncière moyenne par nature de mutation": question3,
        "Q4: Répartition des biens par type de local": question4,
        "Q5: Prix moyen au m² par type de local": question5,
        "Q6: Distribution du nombre de pièces principales": question6,
        "Q7: Top 10 des communes par nombre de transactions": question7,
        "Q8: Valeur foncière moyenne par département": question8,
        "Q9: Top 15 des codes postaux par nombre de transactions": question9,
        "Q10: Distribution des surfaces bâties": question10,
        "Q11: Corrélation surface bâtie vs valeur foncière": question11,
        "Q12: Surface terrain moyenne par nature de culture": question12,
        "Q13: Évolution du prix moyen mensuel": question13,
        "Q14: Comparaison des prix par type de bien": question14,
        "Q15: Distribution des prix - Maisons vs Appartements": question15,
        "Q16: Ratio surface terrain/surface bâtie par commune": question16,
        "Q17: Nombre de biens par transaction": question17,
        "Q18: Biens avec/sans terrain par type": question18,
        "Q19: Transactions par jour de la semaine": question19,
        "Q20: Évolution du volume de ventes par semaine": question20,
    }
    
    questions = questions_zh if language == 'zh' else questions_fr
    
    selected_question = st.sidebar.selectbox(
        get_text('select_question_label'),
        list(questions.keys())
    )
    
    # 数据库连接
    result = init_connection(db_host, db_user, db_password, db_database)
    
    if isinstance(result, tuple) and result[0] is None:
        # 连接失败，显示错误信息
        st.error(result[1])
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
        else:
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

