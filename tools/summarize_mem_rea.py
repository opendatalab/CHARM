import os
import os.path as osp
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import argparse

from models_and_prompts import (
    is_CN_LLM,
    is_EN_LLM,
    sort_by_model,
    get_model_brand,
    get_model_size_b,
)

from utils import load_rea_sum_files, load_mem_sum_file

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


class CharmMemReaSummarizer:

    def __init__(
        self,
        *,
        rea_sum_file,
        mem_sum_file,
        task_names,
        dst_root_dir,
        reasoning_random_scores=None,
        rea_prefix='charm-reason-',
        mem_prefix='charm-memory-',
    ):
        assert osp.isfile(rea_sum_file), f"{rea_sum_file} does not exist"
        assert osp.isfile(mem_sum_file), f"{mem_sum_file} does not exist"
        assert isinstance(task_names, list)

        self.rea_sum_file = rea_sum_file
        self.mem_sum_file = mem_sum_file
        self.task_names = task_names

        self.dst_root_dir = dst_root_dir
        os.makedirs(self.dst_root_dir, exist_ok=True)

        self.reasoning_random_scores = reasoning_random_scores
        self.rea_prefix = rea_prefix
        self.mem_prefix = mem_prefix

        self._load_sum_files()
        self._preprocess_sum_df()

    def _load_sum_files(self):

        self.rea_df = load_rea_sum_files([self.rea_sum_file], self.rea_prefix)
        self.mem_df = load_mem_sum_file(self.mem_sum_file, self.task_names,
                                       self.mem_prefix)

    def _preprocess_sum_df(self):

        # ------------------ process rea
        datasets = self.rea_df['dataset']
        self.rea_df['prompting'] = datasets.apply(lambda x: x.split("_")[-1])
        self.rea_df['task'] = datasets.apply(
            lambda x: "_".join(x.split("_")[:-1]))

        self.rea_df.drop(columns=['dataset'], inplace=True)
        self.rea_df = self.rea_df[self.rea_df['task'].isin(self.task_names)]
        self.rea_df.set_index(['task', 'prompting'], inplace=True)

        self.rea_df = self.rea_df.apply(pd.to_numeric, errors='ignore')

        # ------------------ intersection of mem and rea
        rea_cols = self.rea_df.columns
        mem_cols = self.mem_df.columns
        intersection_cols = set(rea_cols) & set(mem_cols)

        if len(intersection_cols) < len(mem_cols):
            print(
                f"Warning: following models are not in reasoning results: {set(mem_cols) - set(rea_cols)}"
            )
        if len(intersection_cols) < len(rea_cols):
            print(
                f"Warning: following models are not in memorization results: {set(rea_cols) - set(mem_cols)}"
            )

        intersection_cols = list(intersection_cols)
        intersection_cols = sort_by_model(intersection_cols)

        self.mem_df = self.mem_df[intersection_cols]
        self.rea_df = self.rea_df[intersection_cols]

    def _draw_brand(self, mem_arr, rea_arr, model_names, task_name, prompting):

        model_num = len(model_names)
        assert len(mem_arr) == model_num
        assert len(rea_arr) == model_num
        assert isinstance(task_name, str)
        assert isinstance(prompting, str)

        # ------------------------------------ group model by brand
        model_df = pd.DataFrame({
            'model': model_names,
            'mem': mem_arr,
            'rea': rea_arr
        })
        model_df['brand'] = model_df['model'].apply(get_model_brand)
        model_df['model_size'] = model_df['model'].apply(get_model_size_b)

        brand_group = model_df.groupby('brand')
        brand_names = brand_group.groups.keys()
        brand_names = sort_by_model(brand_names)

        # ------------------------------------ get marker and color
        markers = [
            'o', 'v', 'x', '+', '^', 's', 'p', '*', 'h', '<', '>', 'H', 'D',
            'd', 'P', 'X'
        ]
        brand2marker = dict(zip(brand_names, markers))
        model_df['marker'] = model_df['brand'].apply(lambda x: brand2marker[x])

        colors = plt.cm.get_cmap('tab20').colors
        if len(brand_names) > len(colors):
            colors = colors * (len(brand_names) // len(colors) + 1)
        assert len(colors) >= len(brand_names)
        colors = colors[:len(brand_names)]
        brand2color = dict(zip(brand_names, colors))
        model_df['facecolor'] = model_df['brand'].apply(
            lambda x: brand2color[x])

        # ------------------------------------ get random res
        if task_name == "avg_4task":
            rea_random_score = np.mean(
                list(self.reasoning_random_scores.values()))
        else:
            rea_random_score = self.reasoning_random_scores[task_name]
        mem_random_arr = np.array([0, 100])
        rea_random_arr = np.array([rea_random_score, rea_random_score])

        # ------------------------------------ draw scatter
        fig, ax = plt.subplots(figsize=(8, 4.8))
        msf = 5  # marker size factor
        for _, row in model_df.iterrows():
            ax.scatter(row['mem'],
                       row['rea'],
                       label=row['model'],
                       facecolor=row['facecolor'],
                       marker=row['marker'],
                       s=row['model_size'] * msf)

        ax.plot(mem_random_arr,
                rea_random_arr,
                label="random",
                color='gray',
                linestyle='--')

        ax.set_xlim(min(mem_arr) - 5, 100)
        ax.set_xlabel("Memorization Performance")
        ax.set_ylabel("Integrated Reasoning Performance")
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', ncol=1)
        if task_name != "avg_4task":
            ax.set_title(f'{task_name} ({prompting})')
        fig.tight_layout()

        # --------- save
        dst_dir = osp.join(self.dst_root_dir, "brand_scatter")
        os.makedirs(dst_dir, exist_ok=True)

        if task_name == "avg_4task":
            fig_name = f"Figure3_{prompting}.png"
        else:
            fig_name = f"Figure9_{task_name}_{prompting}.png"
        fig.savefig(osp.join(dst_dir, fig_name))

    def draw_task(self, task_name="avg_4task", prompting="brand_adaptive"):

        cur_mem_df = deepcopy(self.mem_df)
        cur_rea_df = deepcopy(self.rea_df)

        if prompting == "brand_adaptive":
            adaptive_res_list = []
            model_names = cur_rea_df.columns
            for model_name in model_names:
                if is_CN_LLM(model_name):
                    adapt_prompting = 'ZH-CoT'
                elif is_EN_LLM(model_name):
                    adapt_prompting = 'XLT'
                else:
                    raise ValueError(f"Unknown model name: {model_name}")
                model_res = cur_rea_df[model_name].xs(adapt_prompting,
                                                      level="prompting")
                adaptive_res_list.append(model_res)

            cur_rea_df = pd.DataFrame(adaptive_res_list).T

        else:
            cur_rea_df = cur_rea_df.xs(prompting, level="prompting")

        if task_name == "avg_4task":
            cur_mem_res = cur_mem_df.mean(axis=0)
            cur_rea_res = cur_rea_df.mean(axis=0)
        else:
            cur_mem_res = cur_mem_df.loc[task_name]
            cur_rea_res = cur_rea_df.loc[task_name]

        cur_mem_res = cur_mem_res.to_dict()
        cur_rea_res = cur_rea_res.to_dict()
        assert len(cur_mem_res) == len(cur_rea_res)

        model_names = list(cur_mem_res.keys())
        mem_arr = list(cur_mem_res.values())
        rea_arr = [cur_rea_res[k] for k in model_names]

        self._draw_brand(mem_arr, rea_arr, model_names, task_name, prompting)

    def process(self):
        for task_name in self.task_names:
            self.draw_task(task_name)

        self.draw_task()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "rea_compass_csv_file",
        type=str,
        help="opencompass summary csv file for reasoning tasks")
    parser.add_argument(
        "mem_compass_csv_file",
        type=str,
        help="opencompass summary csv file for memorization tasks")
    parser.add_argument("--dst_root_dir",
                        type=str,
                        default="output/CHARM_rea_mem_relation",
                        help="root directory to save the output files")
    args = parser.parse_args()

    # -----------------------------------------
    task_names = [
        'Chinese_Anachronisms_Judgment',
        'Chinese_Time_Understanding',
        'Chinese_Movie_and_Music_Recommendation',
        'Chinese_Sport_Understanding',
        "avg_4task",
    ]
    reasoning_random_scores = {
        'Chinese_Anachronisms_Judgment': 50,
        'Chinese_Time_Understanding': 25,
        'Chinese_Movie_and_Music_Recommendation': 25,
        'Chinese_Sport_Understanding': 50,
    }

    dst_root_dir = args.dst_root_dir
    os.system(f"rm -rf {dst_root_dir}")
    summarizer = CharmMemReaSummarizer(
        rea_sum_file=args.rea_compass_csv_file,
        mem_sum_file=args.mem_compass_csv_file,
        task_names=task_names,
        reasoning_random_scores=reasoning_random_scores,
        dst_root_dir=dst_root_dir,
    )
    summarizer.process()
