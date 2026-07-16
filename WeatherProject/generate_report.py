# generate_report.py
import pandas as pd
import os
import webbrowser
from datetime import datetime

# 读取 CSV 数据
def load_data():
    """加载两个 CSV 文件，返回数据帧字典"""
    try:
        df_today = pd.read_csv(' weather1.csv', encoding='gb2312')
        df_14 = pd.read_csv(' weather14.csv', encoding='gb2312')
        return df_today, df_14
    except Exception as e:
        print(f"读取 CSV 文件失败，请确认文件名正确: {e}")
        return None, None

# 计算统计摘要 
def calc_stats(df, columns):
    """计算指定列的均值、最大、最小，返回字典"""
    stats = {}
    for col in columns:
        if col not in df.columns:
            continue
        # 转为数值，忽略非数值
        series = pd.to_numeric(df[col], errors='coerce')
        if series.notna().any():
            stats[col] = {
                '均值': f"{series.mean():.1f}",
                '最大': f"{series.max()}",
                '最小': f"{series.min()}"
            }
        else:
            stats[col] = {'均值': '无数据', '最大': '无数据', '最小': '无数据'}
    return stats

# 扫描图片文件 
def find_images():
    """查找当前目录下所有的 .png 图片（递归）"""
    png_files = [f for f in os.listdir('.') if f.lower().endswith('.png')]
    return sorted(png_files)

# 生成 HTML 报告 
def generate_html(df_today, df_14):
    # 统计当天
    today_cols = ['温度', '相对湿度', '空气质量']
    stats_today = calc_stats(df_today, today_cols)

    # 统计14天
    cols_14 = ['最高气温', '最低气温', '风级']
    stats_14 = calc_stats(df_14, cols_14)

    # 天气现象统计
    if '天气' in df_14.columns:
        weather_count = df_14['天气'].value_counts().to_dict()
    else:
        weather_count = {}

    # 获取图片
    images = find_images()

    # 构建 HTML 表格函数
    def build_stats_table(stats, title):
        html = f"<h3>{title}</h3><table border='1' cellpadding='5'><tr><th>指标</th><th>均值</th><th>最大</th><th>最小</th></tr>"
        for col, vals in stats.items():
            html += f"<tr><td>{col}</td><td>{vals['均值']}</td><td>{vals['最大']}</td><td>{vals['最小']}</td></tr>"
        html += "</table>"
        return html

    # 天气现象频次表格
    def build_weather_table(weather_dict):
        html = "<h3>未来14天天气现象分布</h3><table border='1' cellpadding='5'><tr><th>天气</th><th>天数</th></tr>"
        for wea, cnt in weather_dict.items():
            html += f"<tr><td>{wea}</td><td>{cnt}</td></tr>"
        html += "</table>"
        return html

    # 生成图片展示
    def build_images_section(images):
        if not images:
            return "<p> 未找到图片，请先保存图片。</p>"
        html = "<h3> 图表展示</h3><div style='display:flex;flex-wrap:wrap;gap:20px;'>"
        for img in images:
            html += f"<div style='max-width:45%;'><img src='{img}' style='width:100%;border:1px solid #ccc;border-radius:8px;'><br><span style='font-size:12px;'>{img}</span></div>"
        html += "</div>"
        return html

    # 生成完整 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>成都天气综合分析报告</title>
        <style>
            body {{ font-family: 'Microsoft YaHei', Arial, sans-serif; margin: 40px; background: #f9f9f9; }}
            .container {{ max-width: 1200px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            h2 {{ color: #34495e; margin-top: 30px; }}
            h3 {{ color: #2c3e50; margin-top: 20px; }}
            table {{ border-collapse: collapse; width: auto; margin: 10px 0 20px; }}
            th {{ background: #3498db; color: white; font-weight: bold; }}
            td, th {{ padding: 8px 15px; text-align: center; }}
            tr:nth-child(even) {{ background: #f2f2f2; }}
            .footer {{ margin-top: 40px; color: #7f8c8d; font-size: 14px; border-top: 1px solid #ddd; padding-top: 15px; text-align: center; }}
            .img-section {{ display: flex; flex-wrap: wrap; gap: 20px; }}
            .img-item {{ flex: 1 1 45%; min-width: 300px; }}
        </style>
    </head>
    <body>
    <div class="container">
        <h1> 成都天气数据分析综合报告</h1>
        <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <h2> 当天（24小时）统计</h2>
        {build_stats_table(stats_today, '')}

        <h2> 未来14天统计</h2>
        {build_stats_table(stats_14, '')}

        {build_weather_table(weather_count)}

        {build_images_section(images)}

        <div class="footer">
            <p>报告由 Python 自动生成 | 数据来源：中国天气网 (weather.com.cn)</p>
        </div>
    </div>
    </body>
    </html>
    """

    # 写入文件
    with open('综合报告.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("报告已生成：综合报告.html")
    # 自动打开
    webbrowser.open('综合报告.html')

# 主函数
def main():
    df_today, df_14 = load_data()
    if df_today is None or df_14 is None:
        return
    generate_html(df_today, df_14)

if __name__ == '__main__':
    main()
