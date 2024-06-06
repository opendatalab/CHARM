import os.path as osp
import pandas as pd
import argparse


def insert_table_to_html(excel_file_path, html_file_path):
    df = pd.read_excel(excel_file_path)

    # 除去名为 "prompt" 的列
    df = df.loc[:, ~df.columns.str.contains('prompt', case=False)]
    for col in df.columns[1:]:  # 从第二列开始
        if df[col].dtype != 'object':
            max_val = df[col].max()  # 找到每一列最大值
            df[col] = df[col].apply(lambda x: f'max_{x}_max'
                                    if x == max_val else x)

    # 将数据转换为HTML格式
    html_table = df.to_html(index=False,
                            header=False,
                            justify='center',
                            classes='fixed-header')
    #将最大值加粗
    html_table = html_table.replace('max_',
                                    '<strong>').replace('_max', '</strong>')

    # 删除html_table的第一行
    html_table = html_table.split('\n', 1)[1]

    # 构建要插入的完整HTML内容
    insert_html_EN = '''
    <h4>Accuracy on CHARM reasoning tasks</h4>
    <table align="center">
      <thead class="fixed-header">
        <tr>
          <th rowspan="2" style="vertical-align: middle;">LLM</th>
          <th colspan="8" style="text-align: center;border-right: 1px solid black;" scope="colgroup">
            Chinese Commonsense Domain</th>
          <th colspan="8" scope="colgroup" style="text-align: center;"> Global Commonsense Domain</th>
        </tr>
        <tr style="text-align: center;">
          <th>AJ</th>
          <th>TU</th>
          <th>SqU</th>
          <th>MMR</th>
          <th>SpU</th>
          <th>NLI</th>
          <th>RC</th>
          <th style="border-right: 1px solid black;">Avg.</th>
          <th>AJ</th>
          <th>TU</th>
          <th>SqU</th>
          <th>MMR</th>
          <th>SpU</th>
          <th>NLI</th>
          <th>RC</th>
          <th>Avg.</th>
        </tr>
      </thead>
      {html_table}'''

    insert_html_ZH = '''
    <h4>CHARM 推理任务的评测结果</h4>
      <table align="center">
        <thead class="fixed-header">
          <tr>
            <th rowspan="2" style="vertical-align: middle;">LLM</th>
            <th colspan="8" style="text-align: center;border-right: 1px solid black;" scope="colgroup">
              中国常识领域</th>
            <th colspan="8" scope="colgroup" style="text-align: center;"> 全球常识领域</th>
          </tr>
          <tr style="text-align: center;">
            <th>AJ</th>
            <th>TU</th>
            <th>SqU</th>
            <th>MMR</th>
            <th>SpU</th>
            <th>NLI</th>
            <th>RC</th>
            <th style="border-right: 1px solid black;">Avg.</th>
            <th>AJ</th>
            <th>TU</th>
            <th>SqU</th>
            <th>MMR</th>
            <th>SpU</th>
            <th>NLI</th>
            <th>RC</th>
            <th>Avg.</th>
          </tr>
        </thead>
    {html_table}'''

    # 读取HTML文件
    with open(html_file_path, 'r') as file:
        filedata = file.read()

    # 在HTML文件中查找要替换的部分并替换为生成的HTML表格
    start_tag = '<section id="Reasoning task">'
    end_tag = '</section>'
    start_index = filedata.find(start_tag)
    end_index = filedata.find(end_tag, start_index) + len(end_tag)
    if html_file_path.endswith("ZH.html"):
        insert_html = insert_html_ZH
        print(html_file_path)
    else:
        insert_html = insert_html_EN

    new_filedata = filedata[:start_index] + start_tag + insert_html.format(
        html_table=html_table) + filedata[end_index:]

    return new_filedata


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src_xlsx_file", type=str)
    parser.add_argument("--work_dir", type=str, default="./docs")
    args = parser.parse_args()

    src_xlsx_file = args.src_xlsx_file
    work_dir = args.work_dir

    for html_file in [
            "leaderboard.html",
            "leaderboard_ZH.html",
    ]:
        old_html_file = osp.join(work_dir, html_file)
        new_html_file = osp.join(work_dir, f"new__{html_file}")

        new_html = insert_table_to_html(src_xlsx_file, old_html_file)
        with open(new_html_file, 'w') as file:
            file.write(new_html)
        print(f"New HTML file is saved at {new_html_file}")
