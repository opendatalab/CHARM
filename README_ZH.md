# CHARM✨ Benchmarking Chinese Commonsense Reasoning of LLMs: From Chinese-Specifics to Reasoning-Memorization Correlations
[![arXiv](https://img.shields.io/badge/arXiv-2403.14112-b31b1b.svg)](https://arxiv.org/abs/2403.14112)
[![license](https://img.shields.io/github/license/InternLM/opencompass.svg)](./LICENSE)
<div align="center">

📃[Paper](https://arxiv.org/abs/2403.14112)
🏰[Project Page](https://opendatalab.github.io/CHARM/)
🏆[Leaderboard](https://opendatalab.github.io/CHARM/leaderboard.html)
✨[Findings](https://opendatalab.github.io/CHARM/findings.html)
</div>

<div align="center">
    📖 <a href="./README_ZH.md">   中文</a> | <a href="./README.md">English</a>
</div>

## CHARM 的构建流程


<div style="display: flex; justify-content: center;" align="center">
<center>
<img src="./docs/figure/Fig2_CHARM_construction.png">
</div>

## 与其他常识推理评测基准的比较
<html lang="en">
        <table align="center">
            <thead class="fixed-header">
                <tr>
                    <th>基准</th>
                    <th>汉语</th>
                    <th>常识推理</th>
                    <th>中国特有知识</th>
                    <th>中国和世界知识域</th>
                    <th>推理和记忆的关系</th>
                </tr>
            </thead>
            <tr>
                <td><a href="https://arxiv.org/abs/2302.04752"> davis2023benchmarks</a> 中提到的基准</td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
            </tr>
            <tr>
                <td><a href="https://arxiv.org/abs/1809.05053"> XNLI</a>, <a
                        href="https://arxiv.org/abs/2005.00333">XCOPA</a>,<a
                        href="https://arxiv.org/abs/2112.10668">XStoryCloze</a></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
            </tr>
            <tr>
                <td><a href="https://arxiv.org/abs/2007.08124">LogiQA</a>,<a
                        href="https://arxiv.org/abs/2004.05986">CLUE</a>, <a
                        href="https://arxiv.org/abs/2306.09212">CMMLU</a></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
            </tr>
            <tr>
                <td><a href="https://arxiv.org/abs/2312.12853">CORECODE</a> </td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
                <td><strong><span style="color: red;">&#x2718;</span></strong></td>
            </tr>
            <tr>
                <td><strong><a href="https://arxiv.org/abs/2403.14112">CHARM (ours)</a> </strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
                <td><strong><span style="color: green;">&#x2714;</span></strong></td>
            </tr>
        </table>


## 🚀 新增功能
- **[2024.5.24]** 开源CHARM数据 !!! 🔥🔥🔥
- **[2024.5.15]** CHARM已被计算语言学协会第62届年会（ACL 2024）主会议接受！！！ 🔥🔥🔥
- **[2024.3.21]** 论文发布在 [ArXiv](https://arxiv.org/abs/2403.14112).

## 🧾 待办
- [ ] 支持在Opencompass上进行推理和评测。

## 🛠️ 在 Opencompass 上进行推理和评测
以下是快速下载 CHARM 并在 OpenCompass 上进行评估的步骤。

### 1. OpenCompass 环境设置
请参考 [OpenCompass](https://github.com/open-compass/OpenCompass/?tab=readme-ov-file#%EF%B8%8F-installation) 的安装步骤。

### 2. 下载 CHARM
```bash
git clone https://github.com/opendatalab/CHARM CHARM
```
### 3. 推理和评测
```bash
cd opencompass
mkdir data
ln -snf path_to_CHARM_repo/data/CHARM ./data/CHARM

# 在CHARM上对模型hf_llama3_8b_instruct做推理和评测
python run.py --models hf_llama3_8b_instruct --datasets charm_gen
```

## 🖊️ 引用
```bibtex
@misc{sun2024benchmarking,
      title={Benchmarking Chinese Commonsense Reasoning of LLMs: From Chinese-Specifics to Reasoning-Memorization Correlations}, 
      author={Jiaxing Sun and Weiquan Huang and Jiang Wu and Chenya Gu and Wei Li and Songyang Zhang and Hang Yan and Conghui He},
      year={2024},
      eprint={2403.14112},
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## 💳 许可

此项目是在Apache 2.0许可下发布的 [license](./LICENSE).