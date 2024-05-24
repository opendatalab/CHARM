import os, sys
import os.path as osp
from copy import deepcopy
import pandas as pd
import argparse

from models_and_prompts import (
    is_CN_LLM,
    is_EN_LLM,
    sort_by_model_and_prompting,
    sort_by_prompting,
    RENAME_MODEL_DICT,
)

# ===================== 简称命名规则 =====================
# ------- 任务的domain
# Chinese domain: cn
# Global domain: gl
#
# ------- 模型
# Chinese-oriented LLM: CN_LLM
# English LLM: EN_LLM
#
# ====================================================

avg_cn_tasks = 'Avg. cn tasks'
avg_gl_tasks = 'Avg. gl tasks'


class CharmReaSummarizer:

    def __init__(
        self,
        *,
        sum_files,
        task_pairs,
        dst_root_dir,
        zh_prompting_name,
        en_prompting_name,
        dataset_prefix='rea-',
    ):
        if isinstance(sum_files, str):
            sum_files = [sum_files]
        assert isinstance(sum_files, list)
        self.sum_files = sum_files

        self.task_pairs = task_pairs
        self.dst_root_dir = dst_root_dir
        self.zh_prompting_name = zh_prompting_name
        self.en_prompting_name = en_prompting_name
        self.dataset_prefix = dataset_prefix

        os.makedirs(self.dst_root_dir, exist_ok=True)

        self._load_sum_files()
        self._auto_parse_prompting()
        self._auto_parse_models()
        self._select_tasks()

    def _load_sum_files(self):

        for sum_file in self.sum_files:
            assert osp.isfile(sum_file), f"{sum_file} does not exist"
            assert sum_file.endswith('.csv'), f"{sum_file} is not a csv file"

        dfs = []
        for sum_file in self.sum_files:
            df = pd.read_csv(sum_file)
            dfs.append(df)
            print(f"{sum_file}: {df.shape}")

        col_names = dfs[0].columns
        for df in dfs:
            assert df.columns.tolist() == col_names.tolist(
            ), "columns of sum files are not the same"
            assert df.columns[0] == 'dataset'

        self.sum_df = pd.concat(dfs, ignore_index=True)

        # check duplicated dataset
        assert self.sum_df['dataset'].duplicated().sum(
        ) == 0, "duplicated dataset in sum files"

        drop_cols = ["version", "metric", "mode"]
        self.sum_df = self.sum_df.drop(columns=drop_cols)

        n_row_total = self.sum_df.shape[0]
        n_row_suffix = self.sum_df['dataset'].str.startswith(
            self.dataset_prefix).sum()
        print(f"{n_row_total=}")
        print(
            f"drop {n_row_total-n_row_suffix} rows not startswith {self.dataset_prefix}"
        )
        self.sum_df = self.sum_df[self.sum_df['dataset'].str.startswith(
            self.dataset_prefix)]

        # remove the dataset_prefix
        self.sum_df['dataset'] = self.sum_df['dataset'].apply(
            lambda x: x[len(self.dataset_prefix):])

        self.sum_df.sort_values(by=['dataset'], inplace=True)

    def _auto_parse_prompting(self):

        datasets = self.sum_df['dataset']

        self.sum_df['prompting'] = datasets.apply(lambda x: x.split("_")[-1])
        self.sum_df['task'] = datasets.apply(
            lambda x: "_".join(x.split("_")[:-1]))

        self.sum_df.set_index(['task', 'prompting'], inplace=True)
        self.sum_df.drop(columns=['dataset'], inplace=True)

        self.sum_df.to_csv(osp.join(self.dst_root_dir, "summary_raw.csv"))

    def _auto_parse_models(self):

        CN_LLMs = []
        EN_LLMs = []
        for model_name in self.sum_df.columns.tolist():
            if is_CN_LLM(model_name):
                CN_LLMs.append(model_name)
            elif is_EN_LLM(model_name):
                EN_LLMs.append(model_name)
            else:
                raise ValueError(f"Unknown model name: {model_name}")

        self.CN_LLMs = CN_LLMs
        self.EN_LLMs = EN_LLMs

    def _select_tasks(self):

        # ---------------------------- select tasks
        tasks = [_ for pair in self.task_pairs.values() for _ in pair]

        index_tasks = self.sum_df.index.get_level_values('task').tolist()
        for task in tasks:
            assert task in index_tasks, f"{task} not in sum_files: {self.sum_files}"

        print(f"{self.sum_df.shape=}")
        self.task_df = deepcopy(self.sum_df.loc[tasks])
        del self.sum_df
        print(f"{self.task_df.shape=}")

        # ---------------------------- rename index
        rename_dict = dict()
        renamed_task_pairs = dict()
        for task_name, task_pair in self.task_pairs.items():
            assert task_pair[0].lower().startswith('global_')
            assert task_pair[1].lower().startswith('chinese_')
            rename_dict[task_pair[0]] = "gl_" + task_name
            rename_dict[task_pair[1]] = "cn_" + task_name
            renamed_task_pairs[task_name] = ("gl_" + task_name,
                                             "cn_" + task_name)
        self.task_pairs = renamed_task_pairs
        self.task_df.rename(index=rename_dict, inplace=True)

        # ---------------------------- get gl_tasks and cn_tasks
        self.gl_tasks = [pair[0]
                         for pair in self.task_pairs.values()]  # global
        self.cn_tasks = [pair[1]
                         for pair in self.task_pairs.values()]  # Chinese

        assert all([
            _.lower().startswith(('world_', 'global_', 'gl_'))
            for _ in self.gl_tasks
        ])
        assert all(
            [_.lower().startswith(('cn_', 'chinese_')) for _ in self.cn_tasks])

    def output_tables(self):

        df = deepcopy(self.task_df)
        assert set(df.columns.tolist()).issubset(
            set(list(RENAME_MODEL_DICT.keys())))
        df.rename(columns=RENAME_MODEL_DICT, inplace=True)

        df = df.stack().unstack(level='task')
        df.index.rename(['prompting', 'model'], inplace=True)
        df = df.swaplevel(0, 1).sort_index()

        # ---------------------------- sort

        sorted_index = sort_by_model_and_prompting(df.index)
        df = df.reindex(sorted_index)

        ft_df_copy = deepcopy(df)
        df[avg_cn_tasks] = ft_df_copy[self.cn_tasks].mean(axis=1)
        df[avg_gl_tasks] = ft_df_copy[self.gl_tasks].mean(axis=1)
        df = df.round(decimals=2)
        df = df[self.cn_tasks + [avg_cn_tasks] + self.gl_tasks +
                [avg_gl_tasks]]

        # only keep cn and gl tasks
        df_cn = df[self.cn_tasks + [avg_cn_tasks]]
        df_cn.to_csv(
            osp.join(self.dst_root_dir, "Table9_all_promptings_cn_tasks.csv"))
        df_cn.to_excel(
            osp.join(self.dst_root_dir, "Table9_all_promptings_cn_tasks.xlsx"))

        df_gl = df[self.gl_tasks + [avg_gl_tasks]]
        df_gl.to_csv(
            osp.join(self.dst_root_dir,
                     "Table10_table_all_promptings_gl_tasks.csv"))
        df_gl.to_excel(
            osp.join(self.dst_root_dir,
                     "Table10_table_all_promptings_gl_tasks.xlsx"))

        # ---------------------------- select prompting
        # for CN_LLMs: only keep self.zh_prompting_name
        # for EN_LLMs: only keep self.en_prompting_name
        keep_list = []
        for index in df.index:
            model_name = index[0]
            prompting = index[1]
            if is_CN_LLM(model_name) and prompting == self.zh_prompting_name:
                keep_list.append(True)
                continue
            elif is_EN_LLM(model_name) and prompting == self.en_prompting_name:
                keep_list.append(True)
                continue
            keep_list.append(False)

        df2 = df[keep_list]

        out_basename = f"Table5_{self.en_prompting_name}_{self.zh_prompting_name}"
        df2.to_csv(osp.join(self.dst_root_dir, f"{out_basename}.csv"))
        df2.to_excel(osp.join(self.dst_root_dir, f"{out_basename}.xlsx"))

    def process(self):
        self.output_tables()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("compass_csv_file", type=str, help="compass summary csv file")

    args = parser.parse_args()
    sum_file = osp.realpath(args.compass_csv_file)
    assert osp.isfile(sum_file), f"{sum_file} does not exist"

    dst_root_dir = osp.splitext(sum_file)[0]
    os.system(f"rm -rf {dst_root_dir}/*")

    task_pairs = {
        "AJ": ('Global_Anachronisms_Judgment', 'Chinese_Anachronisms_Judgment'),
        "TU": ('Global_Time_Understanding', 'Chinese_Time_Understanding'),
        "SqU": ('Global_Sequence_Understanding', 'Chinese_Sequence_Understanding'),
        "MMR": ('Global_Movie_and_Music_Recommendation',
                'Chinese_Movie_and_Music_Recommendation'),
        "SpU": ('Global_Sport_Understanding', 'Chinese_Sport_Understanding'),
        "NLI": ('Global_Natural_Language_Inference',
                'Chinese_Natural_Language_Inference'),
        "RC": ('Global_Reading_Comprehension', 'Chinese_Reading_Comprehension'),
    } # yapf: disable


    summarizer = CharmReaSummarizer(
        sum_files=sum_file,
        task_pairs=task_pairs,
        dst_root_dir=dst_root_dir,
        zh_prompting_name='ZH-CoT',
        en_prompting_name='XLT',
    )
    summarizer.process()


if __name__ == '__main__':
    main()
