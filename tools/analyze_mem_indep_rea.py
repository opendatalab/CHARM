import os, sys
import os.path as osp
from copy import deepcopy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

from mmengine import load

from utils import df_to_xlsx, dump_to_json_file, load_mem_sum_file
from models_and_prompts import (
    is_CN_LLM,
    is_EN_LLM,
    sort_by_model_and_prompting,
    sort_by_prompting,
    get_model_brand,
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


class CharmMemSelector:

    def __init__(
        self,
        *,
        mem_data_dir,
        rea_data_dir,
        task_names,
        mem_sum_file,
        mem_results_dir,
        rea_results_dir,
        model_names,
        dst_root_dir,
        rea_prefix='charm-reason-',
        mem_prefix='charm-memory-',
        prompting="brand_adpative",
    ):
        self.mem_data_dir = mem_data_dir
        self.rea_data_dir = rea_data_dir
        self.task_names = task_names
        self.mem_sum_file = mem_sum_file
        self.mem_results_dir = mem_results_dir
        self.rea_results_dir = rea_results_dir
        self.dst_root_dir = dst_root_dir
        self.rea_prefix = rea_prefix
        self.mem_prefix = mem_prefix
        self.model_names = model_names
        self.prompting = prompting

        os.makedirs(self.dst_root_dir, exist_ok=True)

        self.mem_sum_df = load_mem_sum_file(
            self.mem_sum_file,
            self.task_names,
            self.mem_prefix,
        )
        self._check_models()
        self._load_charm_data()
        self._load_mem_results()
        self._load_rea_results()

    def _load_single_bench(self, bench_dir, expected_cols):
        bench_dfs = dict()
        for task in self.task_names:
            bench_file = osp.join(bench_dir, f"{task}.json")
            assert osp.isfile(bench_file), f"{bench_file} does not exist"
            bench = load(bench_file)
            assert isinstance(bench, dict)
            assert 'examples' in bench
            examples = bench['examples']

            df = pd.DataFrame(examples)
            assert set(expected_cols).issubset(df.columns)

            bench_dfs[task] = df

        return bench_dfs

    def _load_charm_data(self):

        self.mem_bench_dfs = self._load_single_bench(
            self.mem_data_dir, expected_cols=['id', 'input', 'target', 'rids'])

        self.rea_bench_dfs = self._load_single_bench(
            self.rea_data_dir,
            expected_cols=['id', 'input', 'target', 'category', 'mids'])

    def _check_models(self):

        for model_name in self.model_names:
            assert model_name in self.mem_sum_df.columns.tolist()

    def _load_mem_results(self):

        res_file_prefix = osp.splitext(self.mem_sum_file)[0]
        mem_result_dfs = dict()

        for model_name in self.model_names:
            for task in self.task_names:
                task_dir = f"{res_file_prefix}-{self.mem_prefix}{task}"
                res_file = osp.join(task_dir, model_name + ".json")
                assert osp.isfile(res_file), f"{res_file} does not exist"
                res_dict = load(res_file)

                assert "details" in res_dict
                details = res_dict["details"].values()
                details_df = pd.DataFrame(details)

                mem_result_dfs[(model_name, task)] = details_df

        self.mem_result_dfs = mem_result_dfs

    def _load_rea_results(self):
        rea_result_dfs = dict()

        for model_name in self.model_names:
            for task in self.task_names:
                if self.prompting == "brand_adpative":
                    if is_CN_LLM(model_name):
                        prompting = "ZH-CoT"
                    elif is_EN_LLM(model_name):
                        prompting = "XLT"
                    else:
                        raise ValueError(f"Unknown model name: {model_name}")
                else:
                    prompting = self.prompting

                res_file_name = f"{self.rea_prefix}{task}_{prompting}.json"
                res_file = osp.join(self.rea_results_dir, model_name,
                                    res_file_name)
                assert osp.isfile(res_file), f"{res_file} does not exist"
                res_dict = load(res_file)

                assert "details" in res_dict
                details = res_dict["details"].values()
                details_df = pd.DataFrame(details)

                assert details_df.shape[0] == self.rea_bench_dfs[task].shape[0]

                rea_result_dfs[(model_name, task)] = pd.concat(
                    [self.rea_bench_dfs[task], details_df], axis=1)

        self.rea_result_dfs = rea_result_dfs

    def _filter_single_mem_result(self, task, src_mem_result_dfs):
        bench_df = self.mem_bench_dfs[task]

        num_examples = src_mem_result_dfs[self.model_names[0]].shape[0]
        assert bench_df.shape[0] == num_examples
        for model in self.model_names:
            assert src_mem_result_dfs[model].shape[0] == num_examples

        mem_correct_df = [df['correct'] for df in src_mem_result_dfs.values()]
        mem_correct_df = pd.DataFrame(mem_correct_df).T
        mem_correct_df.columns = src_mem_result_dfs.keys()

        mem_correct_mask = mem_correct_df.all(axis=1)
        incorrect_bench_df = bench_df[~mem_correct_mask]
        mem_incorrect_mids = incorrect_bench_df['id'].tolist()
        mem_incorrect_rids = incorrect_bench_df['rids'].tolist()
        mem_incorrect_rids = list(
            set([_ for ids in mem_incorrect_rids for _ in ids]))

        mem_incorrect_rids2mids = dict()
        for rid in mem_incorrect_rids:
            mem_incorrect_rids2mids[rid] = []
        for _, row in incorrect_bench_df.iterrows():
            for rid in row['rids']:
                mem_incorrect_rids2mids[rid].append(row['id'])

        dst_dir = osp.join(self.dst_root_dir, "invalid_ids")
        os.makedirs(dst_dir, exist_ok=True)
        dump_to_json_file(mem_incorrect_mids,
                          osp.join(dst_dir, f"mem_incorrect_mids-{task}.json"))
        dump_to_json_file(mem_incorrect_rids,
                          osp.join(dst_dir, f"mem_incorrect_rids-{task}.json"))
        dump_to_json_file(
            mem_incorrect_rids2mids,
            osp.join(dst_dir, f"mem_incorrect_rids2mids-{task}.json"))

        # --------------------------- vis
        mem_predict_df = [
            df['judging_prompt'] for df in src_mem_result_dfs.values()
        ]
        mem_predict_df = pd.DataFrame(mem_predict_df).T
        mem_predict_df.columns = [
            _ + "_pred" for _ in src_mem_result_dfs.keys()
        ]

        vis_df = pd.concat([mem_correct_df, mem_predict_df], axis=1)
        vis_df['all_models_correct'] = mem_correct_mask
        reorder_cols = ['all_models_correct']
        for col in src_mem_result_dfs.keys():
            reorder_cols.append(col)
            reorder_cols.append(col + "_pred")
        vis_df = vis_df[reorder_cols]

        vis_df = pd.concat([deepcopy(bench_df), vis_df], axis=1)

        dst_dir = osp.join(self.dst_root_dir, "vis_mem")
        os.makedirs(dst_dir, exist_ok=True)
        df_to_xlsx(vis_df, osp.join(dst_dir, f"vis_mem-{task}.xlsx"))
        dump_to_json_file(vis_df.to_dict(orient='records'),
                          osp.join(dst_dir, f"vis_mem-{task}.json"))

        return mem_correct_mask, mem_incorrect_mids, mem_incorrect_rids

    def filter_mem(self):

        filtered_mem_masks = dict()
        incorrect_mids = dict()
        incorrect_rids = dict()

        for task in self.task_names:
            cur_mem_results_dfs = dict()
            for model in self.model_names:
                cur_mem_results_dfs[model] = self.mem_result_dfs[(model, task)]

            (filtered_mem_masks[task], incorrect_mids[task],
             incorrect_rids[task]) = self._filter_single_mem_result(
                 task, cur_mem_results_dfs)

            print(
                f'filtering mem-[{task}] {filtered_mem_masks[task].sum()} / {filtered_mem_masks[task].shape[0]}'
            )

        self.filtered_mem_masks = filtered_mem_masks
        self.incorrect_mids = incorrect_mids
        self.incorrect_rids = incorrect_rids

    def select_rea(self):
        dst_dir = osp.join(self.dst_root_dir, "selected_rea")
        dst_bench_dir = osp.join(dst_dir, "bench")
        dst_result_dir = osp.join(dst_dir, "result")
        dst_merged_dir = osp.join(dst_dir, "merged")
        os.makedirs(dst_bench_dir, exist_ok=True)
        os.makedirs(dst_result_dir, exist_ok=True)
        os.makedirs(dst_merged_dir, exist_ok=True)

        slct_rea_bench_dfs = dict()
        for task in self.task_names:
            cur_rea_bench_df = self.rea_bench_dfs[task]
            slct_rea_bench_df = cur_rea_bench_df[
                ~cur_rea_bench_df['id'].isin(self.incorrect_rids[task])]
            slct_rea_bench_dfs[task] = slct_rea_bench_df
            slct_rea_bench_df.to_csv(osp.join(dst_bench_dir, f"{task}.csv"),
                                     index=False)
            print(
                f"filter rea-[{task}] {slct_rea_bench_df.shape[0]} / {cur_rea_bench_df.shape[0]}"
            )

        slct_rea_result_dfs = dict()
        for task in self.task_names:
            for model in self.model_names:
                cur_rea_result_df = self.rea_result_dfs[(model, task)]
                slct_rea_result_df = cur_rea_result_df[
                    ~cur_rea_result_df['id'].isin(self.incorrect_rids[task])]
                slct_rea_result_dfs[(model, task)] = slct_rea_result_df
                assert slct_rea_result_df.shape[0] == \
                    slct_rea_bench_dfs[task].shape[0]
                model_dir = osp.join(dst_result_dir, model)
                os.makedirs(model_dir, exist_ok=True)
                slct_rea_result_df.to_csv(osp.join(model_dir, f"{task}.csv"),
                                          index=False)
                slct_rea_result_df.to_excel(
                    osp.join(model_dir, f"{task}.xlsx"),
                    index=False,
                )

                # filter the correct
                incorrect_slct_rea_result_df = slct_rea_result_df[
                    ~slct_rea_result_df['correct']]
                incorrect_slct_rea_result_df.to_csv(
                    osp.join(model_dir, f"incorrect_{task}.csv"),
                    index=False,
                )
                incorrect_slct_rea_result_df.to_excel(
                    osp.join(model_dir, f"incorrect_{task}.xlsx"),
                    index=False,
                )

        self.slct_rea_bench_dfs = slct_rea_bench_dfs
        self.slct_rea_result_dfs = slct_rea_result_dfs

        # merge results dfs
        for task in self.task_names:
            bench_df = slct_rea_bench_dfs[task]
            merged_dfs = [bench_df]
            for model in self.model_names:
                model_result_df = slct_rea_result_dfs[(model, task)]
                model_result_df = model_result_df.drop(
                    columns=bench_df.columns)
                merged_dfs.append(model_result_df)
            merged_df = pd.concat(merged_dfs,
                                  axis=1,
                                  keys=['bench'] + self.model_names)
            merged_df.to_csv(osp.join(dst_merged_dir, f"{task}.csv"),
                             index=False)
            merged_df.to_excel(osp.join(dst_merged_dir, f"{task}.xlsx"))

            # filter the row where all models are correct
            correct_df = merged_df.xs('correct', level=1, axis=1)
            correct_mask = correct_df.all(axis=1)
            incorrect_df = merged_df[~correct_mask]
            # drop useless columns
            incorrect_df.drop(
                columns=[
                    ('bench', 'id'),
                    ('bench', 'target'),
                    ('bench', 'category'),
                    ('bench', 'mids'),
                ],
                inplace=True,
            )
            for model in self.model_names:
                incorrect_df.drop(columns=[(model, 'prompt')], inplace=True)
            incorrect_basename = f"mono_{'_vs_'.join(self.model_names)}_{task}_incorrect"
            try:
                incorrect_df.to_csv(
                    osp.join(dst_merged_dir, incorrect_basename + ".csv"),
                    index=False,
                )
                incorrect_df.to_excel(
                    osp.join(dst_merged_dir, incorrect_basename + ".xlsx"))
            except Exception as e:
                print(f"Error when saving {incorrect_basename}: {e}")

    def _account_task(self, src_rea_result_df):
        num_examples = src_rea_result_df.shape[0]
        num_correct = src_rea_result_df['correct'].sum()
        num_acc = num_correct / num_examples * 100

        return {
            'num_examples': num_examples,
            'num_correct': num_correct,
            'acc': num_acc,
        }

    def account(self):

        # -------------------------------------- account raw
        model_dfs = []

        for model_name in self.model_names:
            model_dict = dict()
            for task in self.task_names:
                model_dict[task + '-original'] = self._account_task(
                    self.rea_result_dfs[(model_name, task)])
                model_dict[task + '-selected'] = self._account_task(
                    self.slct_rea_result_dfs[(model_name, task)])
            model_df = pd.DataFrame(model_dict).T
            num_examples = model_df['num_examples']
            model_df.drop(columns=['num_examples'], inplace=True)
            model_df.columns = pd.MultiIndex.from_product([[model_name],
                                                           model_df.columns])
            model_dfs.append(model_df)

        out_df = pd.concat(model_dfs, axis=1).round(decimals=2)
        out_df['dataset'] = [x.split('-')[0] for x in out_df.index]
        out_df['version'] = [x.split('-')[1] for x in out_df.index]
        out_df['num_examples'] = num_examples
        out_df.set_index(['dataset', 'version', 'num_examples'], inplace=True)

        out_df.to_csv(osp.join(self.dst_root_dir, "raw_account.csv"))
        out_df.to_excel(osp.join(self.dst_root_dir, "raw_account.xlsx"))

        # -------------------------------------- total
        out_df.reset_index(inplace=True)
        out_df.set_index(['dataset', 'version'], inplace=True)
        original_total = out_df.xs('original', level='version').sum(axis=0)
        selected_total = out_df.xs('selected', level='version').sum(axis=0)
        for model_name in self.model_names:
            original_total[(model_name, 'acc')] = original_total[
                (model_name,
                 'num_correct')] / original_total['num_examples'] * 100
            selected_total[(model_name, 'acc')] = selected_total[
                (model_name,
                 'num_correct')] / selected_total['num_examples'] * 100

        original_total_df = original_total.to_frame().T
        selected_total_df = selected_total.to_frame().T

        original_total_df['dataset'] = ['total']
        original_total_df['version'] = ['original']
        original_total_df.set_index(['dataset', 'version'], inplace=True)

        selected_total_df['dataset'] = ['total']
        selected_total_df['version'] = ['selected']
        selected_total_df.set_index(['dataset', 'version'], inplace=True)

        out_df = pd.concat([out_df, original_total_df, selected_total_df],
                           axis=0).round(decimals=2)
        out_df.reset_index(inplace=True)
        out_df.set_index(['dataset', 'version', 'num_examples'], inplace=True)

        out_df.to_csv(osp.join(self.dst_root_dir, "account.csv"))
        out_df.to_excel(osp.join(self.dst_root_dir, "account.xlsx"))

        out_dict = dict()
        for model_name in self.model_names:
            out_dict[model_name] = dict()
            out_dict[model_name]['original_acc'] = float(out_df.loc[
                ('total', 'original'),
                (model_name, 'acc'),
            ])
            out_dict[model_name]['selected_acc'] = float(out_df.loc[
                ('total', 'selected'),
                (model_name, 'acc'),
            ])
            out_dict[model_name]['original_num'] = int(
                original_total_df.loc[('total', 'original'), 'num_examples'])
            out_dict[model_name]['selected_num'] = int(
                selected_total_df.loc[('total', 'selected'), 'num_examples'])

        dump_to_json_file(out_dict, osp.join(self.dst_root_dir,
                                             "account.json"))

    def process(self):
        self.filter_mem()
        self.select_rea()
        self.account()


class FRMMAnalyzer:
    """
    generate Table12 and part of Table7 in https://arxiv.org/abs/2403.14112
    """

    def __init__(self, src_models, dst_FRMM_dir):
        self.src_models = src_models
        self.dst_FRMM_dir = dst_FRMM_dir

        self.model_num = len(self.src_models)
        self._load_monos()

    def _load_monos(self):
        mono_results = dict()

        for model_name in self.src_models:
            mono_file = osp.join(self.dst_FRMM_dir, model_name, 'account.json')
            assert osp.isfile(mono_file), f"{mono_file} does not exist"
            mono_res = load(mono_file)
            assert isinstance(mono_res, dict)
            assert len(mono_res) == 1
            assert model_name in mono_res
            assert "original_acc" in mono_res[model_name]
            assert "selected_acc" in mono_res[model_name]
            mono_results[model_name] = mono_res[model_name]
        self.mono_results = mono_results
        self.mono_res_df = pd.DataFrame(mono_results).T
        self.mono_res_df.rename(index=RENAME_MODEL_DICT, inplace=True)
        # set index name
        self.mono_res_df.index.name = "model"
        # set float to int
        self.mono_res_df['original_num'] = self.mono_res_df[
            'original_num'].astype(int)
        self.mono_res_df['selected_num'] = self.mono_res_df[
            'selected_num'].astype(int)

    def process(self):

        dst_dir = osp.join(self.dst_FRMM_dir, "_ranking")
        os.makedirs(dst_dir, exist_ok=True)

        # ----------------------------------- filtering info
        filtering_info_df = deepcopy(self.mono_res_df)
        filtering_info_df.sort_values('original_acc',
                                      ascending=False,
                                      inplace=True)
        filtering_info_df = filtering_info_df[[
            'original_num', 'original_acc', 'selected_num', 'selected_acc'
        ]]
        filtering_info_df.rename(
            columns={
                'original_num': '# Original',
                'original_acc': 'Original Acc.',
                'selected_num': '# Retained',
                'selected_acc': 'Retained Acc.'
            },
            inplace=True,
        )
        filtering_info_df.to_csv(osp.join(dst_dir, "Table12.csv"))
        filtering_info_df.to_excel(osp.join(dst_dir, "Table12.xlsx"))

        # ----------------------------------- rank
        original_model_list = filtering_info_df.index.tolist()
        selected_model_list = self.mono_res_df.sort_values(
            'selected_acc', ascending=False).index.tolist()
        # calculate the rank diff between original and selected
        rank_diff = []
        for selected_idx, model_name in enumerate(selected_model_list):
            original_idx = original_model_list.index(model_name)
            rank_diff.append(original_idx - selected_idx)

        # use up and down array to display rank change
        rank_diff_str = []
        for diff in rank_diff:
            if diff < 0:
                rank_diff_str.append(f"↓{abs(diff)}")

            elif diff > 0:
                rank_diff_str.append(f"↑{abs(diff)}")
            else:
                rank_diff_str.append("-")

        rank_df = pd.DataFrame({
            "Integrated Reasoning":
            original_model_list,
            "Memorization-independent Reasoning (FRMM)":
            [f"{a} ({b})" for a, b in zip(selected_model_list, rank_diff_str)]
        })
        rank_df[""] = [_ + 1 for _ in rank_df.index]
        rank_df.set_index("", inplace=True)
        rank_df.to_csv(osp.join(dst_dir, "Table7_FRMM.csv"))
        rank_df.to_excel(osp.join(dst_dir, "Table7_FRMM.xlsx"))


class MIBAnalyzer:
    """
    generate Figure11, Table13 and part of Table7 in https://arxiv.org/abs/2403.14112
    """

    def __init__(self, src_models, dst_MIB_dir):
        self.src_models = src_models
        self.renamed_models = [RENAME_MODEL_DICT[_] for _ in self.src_models]
        self.dst_MIB_dir = dst_MIB_dir

        self.model_num = len(self.src_models)
        self._load_combats()

    def _load_combats(self):
        combats = dict()

        for i in range(self.model_num):
            for j in range(i + 1, self.model_num):
                model_pair = (self.src_models[i], self.src_models[j])
                combat_file = osp.join(self.dst_MIB_dir,
                                       '_vs_'.join(model_pair), 'account.json')
                assert osp.isfile(combat_file), f"{combat_file} does not exist"

                combats[model_pair] = load(combat_file)
        self.combats = combats

    def average_combats(self):
        model_num = self.model_num

        all_combats_original_acc = dict()
        all_combats_selected_acc = dict()

        for model_pair in self.combats:
            for model_name in model_pair:
                original_acc = self.combats[model_pair][model_name][
                    'original_acc']
                selected_acc = self.combats[model_pair][model_name][
                    'selected_acc']

                if model_name not in all_combats_original_acc:
                    all_combats_original_acc[model_name] = []
                if model_name not in all_combats_selected_acc:
                    all_combats_selected_acc[model_name] = []
                all_combats_original_acc[model_name].append(original_acc)
                all_combats_selected_acc[model_name].append(selected_acc)

        assert len(all_combats_original_acc) == model_num
        assert len(all_combats_selected_acc) == model_num

        # ------------------------
        original_scores = dict()
        selected_scores = dict()
        for model_name in all_combats_original_acc:
            original_scores[model_name] = sum(
                all_combats_original_acc[model_name]) / model_num
        for model_name in all_combats_selected_acc:
            selected_scores[model_name] = sum(
                all_combats_selected_acc[model_name]) / model_num

        avg_dict = {
            'original_scores': original_scores,
            'selected_scores': selected_scores,
        }
        dst_dir = osp.join(self.dst_MIB_dir, "_average_combats")
        os.makedirs(dst_dir, exist_ok=True)
        dump_to_json_file(avg_dict, osp.join(dst_dir, "avg_scores.json"))
        self.avg_dict = avg_dict

    def draw_combat_matrix(self):
        """
        generate Table13 and Figure11
        """
        dst_dir = osp.join(self.dst_MIB_dir, "_combat_mat")
        os.makedirs(dst_dir, exist_ok=True)

        combat_res_mat = np.zeros((self.model_num, self.model_num))

        for model_pair in self.combats:
            model_name1 = model_pair[0]
            model_name2 = model_pair[1]
            idx1 = self.src_models.index(model_name1)
            idx2 = self.src_models.index(model_name2)

            model1_acc = self.combats[model_pair][model_name1]['selected_acc']
            model2_acc = self.combats[model_pair][model_name2]['selected_acc']

            combat_res_mat[idx1, idx2] = model1_acc - model2_acc
            combat_res_mat[idx2, idx1] = model2_acc - model1_acc

        # --------------------- to df and sort
        combat_res_df = pd.DataFrame(combat_res_mat,
                                     index=self.renamed_models,
                                     columns=self.renamed_models)
        combat_res_df['mean'] = combat_res_df.mean(axis=1)
        combat_res_df.sort_values(by='mean', inplace=True, ascending=False)
        combat_res_df = combat_res_df[list(combat_res_df.index) + ['mean']]
        combat_res_df = combat_res_df.round(decimals=2)
        combat_res_df.to_csv(osp.join(dst_dir, f'Figure11.csv'))
        combat_res_df.to_excel(osp.join(dst_dir, f'Figure11.xlsx'))

        combat_mean_res_df = combat_res_df['mean']
        combat_mean_res_df.to_csv(osp.join(dst_dir, f'Table13.csv'))
        combat_mean_res_df.to_excel(osp.join(dst_dir, f'Table13.xlsx'))

        sorted_combat_res_mat = np.array(combat_res_df.values)[:, :-1]
        sorted_combat_models = list(combat_res_df.index)
        # plot
        plt.figure(figsize=(12, 9))
        sns.heatmap(sorted_combat_res_mat,
                    annot=True,
                    xticklabels=sorted_combat_models,
                    yticklabels=sorted_combat_models,
                    cmap='RdBu_r',
                    center=0)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=45, va='top')
        plt.tight_layout()
        plt.savefig(osp.join(dst_dir, f'Figure11.png'))

        self.combat_res_df = combat_res_df
        self.sorted_combat_res_mat = sorted_combat_res_mat
        self.sorted_combat_models = sorted_combat_models

    def rank_models(self):
        """
        generate part of Table7
        """
        dst_dir = osp.join(self.dst_MIB_dir, "_ranking")
        os.makedirs(dst_dir, exist_ok=True)

        avg_original_scores = self.avg_dict['original_scores']
        avg_original_scores = sorted(avg_original_scores.items(),
                                     key=lambda x: x[1],
                                     reverse=True)

        avg_original_models = [_[0] for _ in avg_original_scores]
        sorted_combat_models = self.sorted_combat_models

        # rename
        avg_original_models = [
            RENAME_MODEL_DICT[_] for _ in avg_original_models
        ]

        # calculate the rank diff between original and combat
        rank_diff = []
        for combat_idx, model_name in enumerate(sorted_combat_models):
            original_idx = avg_original_models.index(model_name)
            rank_diff.append(original_idx - combat_idx)

        # use up and down array to display rank change
        rank_diff_str = []
        for diff in rank_diff:
            if diff < 0:
                rank_diff_str.append(f"↓{abs(diff)}")
            elif diff > 0:
                rank_diff_str.append(f"↑{abs(diff)}")
            else:
                rank_diff_str.append("-")

        rank_df = pd.DataFrame({
            "Integrated Reasoning":
            avg_original_models,
            "Memorization-independent Reasoning (MIB)": [
                f"{a} ({b})"
                for a, b in zip(sorted_combat_models, rank_diff_str)
            ]
        })
        rank_df[""] = [_ + 1 for _ in rank_df.index]
        rank_df.set_index("", inplace=True)

        rank_df.to_csv(osp.join(dst_dir, "Table7_MIB.csv"))
        rank_df.to_excel(osp.join(dst_dir, "Table7_MIB.xlsx"))

    def process(self):
        self.average_combats()
        self.draw_combat_matrix()  # Figure11
        self.rank_models()  # Table7


def merge_two_rank(dst_FRMM_dir, dst_MIB_dir, dst_root_dir):
    """
    generate Table7 in https://arxiv.org/abs/2403.14112
    """
    rank1_csv = osp.join(dst_FRMM_dir, "_ranking", "Table7_FRMM.csv")
    rank2_csv = osp.join(dst_MIB_dir, "_ranking", "Table7_MIB.csv")

    rank1_df = pd.read_csv(rank1_csv, index_col=0)
    rank2_df = pd.read_csv(rank2_csv, index_col=0)

    col1_name = "Integrated Reasoning"
    assert col1_name in rank1_df.columns
    assert col1_name in rank2_df.columns
    assert rank1_df[col1_name].equals(rank2_df[col1_name])

    merged_df = pd.concat(
        [rank1_df, rank2_df.drop(columns=[col1_name])], axis=1)
    merged_df.to_csv(osp.join(dst_root_dir, "Table7.csv"))
    merged_df.to_excel(osp.join(dst_root_dir, "Table7.xlsx"))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("charm_data_dir",
                        type=str,
                        help="root directory of the CHARM dataset")
    parser.add_argument(
        "rea_results_dir",
        type=str,
        help="directory of the reasoning task results from opencompass")
    parser.add_argument(
        "mem_results_dir",
        type=str,
        help="directory of the memorization task results from opencompass")
    parser.add_argument(
        "mem_csv_file",
        type=str,
        help="summary csv file for memorization tasks from opencompass")
    parser.add_argument("--dst_root_dir",
                        type=str,
                        default="output/CHARM_mem_indep_mem",
                        help="root directory to save the output files")
    args = parser.parse_args()

    # --------------------------------------- directories

    mem_data_dir = osp.join(args.charm_data_dir, "memorization")
    rea_data_dir = osp.join(args.charm_data_dir, "reasoning")
    assert osp.isdir(mem_data_dir), f"{mem_data_dir} does not exist"

    task_names = [
        'Chinese_Anachronisms_Judgment',
        'Chinese_Time_Understanding',
        'Chinese_Movie_and_Music_Recommendation',
        'Chinese_Sport_Understanding',
    ]

    dst_root_dir = args.dst_root_dir
    # --------------------------------------- models
    mem_sum_df = pd.read_csv(args.mem_csv_file)
    drop_cols = ["dataset"]
    mem_sum_df = mem_sum_df.drop(columns=drop_cols)
    model_names = mem_sum_df.columns

    selected_brands = [
        'internlm2',
        'yi',
        'deepseek',
        'qwen',
        'gpt-3',
        'gpt-4',
        'gemini',
        'llama-3',
    ]
    src_models = [
        _ for _ in model_names if get_model_brand(_) in selected_brands
    ]
    src_model_num = len(src_models)

    # ------------- Filtering Reasoning Questions based on Mono-LLM-Memorization (FRMM)
    # https://arxiv.org/abs/2403.14112, Appendix I.1

    dst_FRMM_dir = osp.join(dst_root_dir, 'FRMM')
    for model_name in src_models:
        print(f"============================ processing {model_name}")
        dst_dir = osp.join(dst_FRMM_dir, model_name)
        selector = CharmMemSelector(
            mem_data_dir=mem_data_dir,
            rea_data_dir=rea_data_dir,
            task_names=task_names,
            mem_sum_file=args.mem_csv_file,
            mem_results_dir=args.mem_results_dir,
            rea_results_dir=args.rea_results_dir,
            model_names=[model_name],
            dst_root_dir=dst_dir,
        )
        selector.process()

    # generate Table12 and part of Table7 in https://arxiv.org/abs/2403.14112
    frmm = FRMMAnalyzer(src_models=src_models, dst_FRMM_dir=dst_FRMM_dir)
    frmm.process()

    # ------------- Memorization-Independent Battles among LLMs (MIB)
    # https://arxiv.org/abs/2403.14112, Appendix I.2

    dst_MIB_dir = osp.join(dst_root_dir, 'MIB')
    for i in range(src_model_num):
        for j in range(i + 1, src_model_num):
            model_pair = [src_models[i], src_models[j]]
            print(f"============================ processing {model_pair}")
            dst_dir = osp.join(dst_MIB_dir, '_vs_'.join(model_pair))
            selector = CharmMemSelector(
                mem_data_dir=mem_data_dir,
                rea_data_dir=rea_data_dir,
                task_names=task_names,
                mem_sum_file=args.mem_csv_file,
                mem_results_dir=args.mem_results_dir,
                rea_results_dir=args.rea_results_dir,
                model_names=model_pair,
                dst_root_dir=dst_dir,
            )
            selector.process()

    # generate Figure11, Table13 and part of Table7 in https://arxiv.org/abs/2403.14112
    mib = MIBAnalyzer(src_models=src_models, dst_MIB_dir=dst_MIB_dir)
    mib.process()

    # --------------------------------------- generate Table7 in https://arxiv.org/abs/2403.14112
    merge_two_rank(dst_FRMM_dir, dst_MIB_dir, dst_root_dir)


if __name__ == '__main__':
    main()
