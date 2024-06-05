import os
import os.path as osp
import pandas as pd
import json


def load_rea_sum_files(sum_files, dataset_prefix):

    for sum_file in sum_files:
        assert osp.isfile(sum_file), f"{sum_file} does not exist"
        assert sum_file.endswith('.csv'), f"{sum_file} is not a csv file"

    dfs = []
    for sum_file in sum_files:
        df = pd.read_csv(sum_file)
        dfs.append(df)
        print(f"{sum_file}: {df.shape}")

    col_names = dfs[0].columns
    for df in dfs:
        assert df.columns.tolist() == col_names.tolist(
        ), "columns of sum files are not the same"
        assert df.columns[0] == 'dataset'

    sum_df = pd.concat(dfs, ignore_index=True)
    sum_df.fillna("", inplace=True)

    n_row_total = sum_df.shape[0]
    n_row_suffix = sum_df['dataset'].str.startswith(dataset_prefix).sum()
    print(f"{n_row_total=}")
    print(
        f"drop {n_row_total-n_row_suffix} rows not startswith {dataset_prefix}"
    )
    sum_df = sum_df[sum_df['dataset'].str.startswith(dataset_prefix)]

    n_row_total = sum_df.shape[0]
    n_row_metric_score = (sum_df['metric'] == 'score').sum()
    print(f"drop {n_row_total-n_row_metric_score} rows not metric is score")
    sum_df = sum_df[sum_df['metric'] == 'score']

    # check duplicated dataset
    assert sum_df['dataset'].duplicated().sum(
    ) == 0, "duplicated dataset in sum files"

    drop_cols = ["version", "metric", "mode"]
    sum_df = sum_df.drop(columns=drop_cols)

    # remove the dataset_prefix
    sum_df['dataset'] = sum_df['dataset'].apply(
        lambda x: x[len(dataset_prefix):])

    sum_df.sort_values(by=['dataset'], inplace=True)

    return sum_df


def load_mem_sum_file(mem_sum_file, expected_task_names, mem_prefix):

    assert osp.isfile(mem_sum_file)
    assert mem_sum_file.endswith('.csv')
    mem_df = pd.read_csv(mem_sum_file)

    assert 'dataset' in mem_df.columns
    mem_df = mem_df[mem_df['dataset'].str.startswith(mem_prefix)]
    mem_df['dataset'] = mem_df['dataset'].apply(lambda x: x[len(mem_prefix):])

    task_names = mem_df['dataset'].to_list()

    if 'avg_4task' in expected_task_names:
        expected_task_names = expected_task_names.copy()
        expected_task_names.remove('avg_4task')
    assert set(task_names) == set(
        expected_task_names), f"{task_names} != {expected_task_names}"

    mem_df = mem_df.apply(pd.to_numeric, errors='ignore')
    mem_df.set_index('dataset', inplace=True)

    return mem_df


def dump_to_json_file(obj, dst_file):
    assert dst_file.endswith('.json')
    with open(dst_file, 'w', encoding='utf-8') as f:
        json.dump(obj, f, indent=4, ensure_ascii=False)


def df_to_xlsx(df, dst_file, index=False):

    assert isinstance(df, pd.DataFrame)
    assert dst_file.endswith('.xlsx')

    # output to xlsx
    writer = pd.ExcelWriter(dst_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=index)
    workbook = writer.book
    # freeze the first row
    worksheet = writer.sheets['Sheet1']
    worksheet.freeze_panes(1, 0)
    # set all cell boundary line to black
    cell_format = workbook.add_format({'bottom': True, 'right': True})
    worksheet.conditional_format(0, 0, df.shape[0], df.shape[1], {
        'type': 'no_blanks',
        'format': cell_format
    })
    writer.close()
