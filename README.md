# CHARM✨ Benchmarking Chinese Commonsense Reasoning of LLMs: From Chinese-Specifics to Reasoning-Memorization Correlations
[![arXiv](https://img.shields.io/badge/arXiv-2312.14033-b31b1b.svg)](https://arxiv.org/abs/2312.14033)

<div align="center">

📃[Paper](https://arxiv.org/abs/2312.14033)
🏰[Project Page](https://gitlab.pjlab.org.cn/wujiang/charm/-/tree/dev/docs/index.html)
<!-- 📚[LeaderBoard](https://open-compass.github.io/T-Eval/leaderboard.html) -->
<!-- 🤗[HuggingFace](https://huggingface.co/datasets/lovesnowbest/T-Eval) -->

</div>

<div align="center">
    📖 <a href="./README_ZH.md">   中文</a> | <a href="./README.md">English</a>
</div>

## ☀️Introduction


We introduce CHARM, the first benchmark for comprehensively and in-depth evaluating the commonsense reasoning ability of large language models (LLMs) in Chinese, which covers both globally known and Chinese-specific commonsense. We evaluated 7 English and 12 Chinese-oriented LLMs on CHARM, employing 5 representative prompt strategies for improving LLMs' reasoning ability, such as Chain-of-Thought. Our findings indicate that the LLM's language orientation and the task's domain influence the effectiveness of the prompt strategy, which enriches previous research findings.
We built closely-interconnected reasoning and memorization tasks, and found that some LLMs struggle with memorizing Chinese commonsense, affecting their reasoning ability, while others show differences in reasoning despite similar memorization performance. We also evaluated the LLMs' memorization-independent reasoning abilities and analyzed the typical errors. Our study precisely identified the LLMs' strengths and weaknesses, providing the clear direction for optimization. It can also serve as a reference for studies in other fields. 

<div style="display: flex; justify-content: center;" align="center">
<center>
<img src="./docs/figure/Fig2_CHARM_construction.png">
</div>


## 🚀 What's New
- **[2024.3.21]** Paper available on [ArXiv](https://arxiv.orgxxxxx). 🔥🔥🔥

## 🧾 TODO
- [ ] Release the data for CHARM.


## ✨CHARM
**CHARM** is the first benchmark for comprehensively and in-depth evaluating the commonsense reasoning ability of large language models (LLMs) in Chinese, which covers both globally known and Chinese-specific commonsense. In addition, the CHARM can evaluate the LLMs' memorization-independent reasoning abilities and analyze the typical errors.


### 📖 Commonsense Domain
#### 🌐 Global commonsense domain
Global commonsense domain consists of universally understood commonsense.
It covers objects and aspects of modern life that an individual should be aware of.
It includes foundational knowledge that someone with a basic modern education is expected to know.  When it involves individuals, they are globally recognized figures.

#### 🚩 Chinese commonsense domain
Chinese commonsense domain encompasses Chinese-specific elements. We categoried them into 7 aspects:
- **History (H)** includes important events and figures in Chinese history, China's dynasties, and other basic  facts and shared knowledge about the history of China.

- **Traditional Culture and Arts (CA)** encompasses Chinese traditional cultural arts, literary works, and traditional lifestyles.

- **Daily Life and Customs (LC)** includes modern Chinese daily routines, clothing, food, housing, transportation festivals and so on.

- **Entertainment (E)** includes the movies, television programs, music, and other entertainments in modern Chinese daily life.
- **Public Figures (F)** encompasses the public figures well-known in Chinese society.
- **Geography (G)** includes China's geographical distribution, natural landscapes, and characteristic regional cultures.

- **Chinese Language (L)** includes the fundamentals of the Chinese language, such as Chinese characters, idioms and so on.

### 📋 Task List

- **Reasoning Tasks :** The charm consists of 7 reasoning tasks, which are: **Anachronisms Judgment (AJ), Time Understanding (TU), Sequence Understanding (SqU), Movie and Music Recommendation (MMR), Sport Understanding (SpU), Natural Language Inference (NLI), Reading Comprehension (RC).**

- **Memorization Tasks:** We chose that can be readily associated in this manner, **AJ, TU, MMR, SpU,** refered as the Memorization-Reasoning-Interconnected (MRI) tasks, and built
the reltated memorization questions.

<table align="center">
    <thead>
        <tr>
            <th>Task Type</th>
            <th>Task</th>
            <th>Domain</th>
            <th>Chinese aspects</th>
            <!-- <th>Construction</th> -->
            <th>Question Type</th>
            <th># Question</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="14" style="vertical-align: middle;">Reasoning</td>
            <td rowspan="2" >Anachronisms Judgment (AJ)</td>
            <td>Chinese</td>
            <td><i>H, AC, LC, F</i></td>
            <!-- <td>[H]</td> -->
            <td>2-option MCQ</td>
            <td>150</td>
        </tr>
        <tr>
            <td>global</td>
            <td>-</td>
            <!-- <td>[T][H]</td> -->
            <td>2-option MCQ</td>
            <td>150</td>
        </tr>
        <tr>
    <td rowspan="2">Time Understanding (TU)</td>
    <td>Chinese</td>
    <td><i>H, AC, LC</i></td>
    <!-- <td>[H]</td> -->
    <td>4-option MCQ</td>
    <td>100</td> 
    <tr>
    <tr>
    <td rowspan="2">Sequence Understanding (SqU)</td>
    <td>Chinese</td>
    <td><i>H, CA, LC, G, L</i></td>
    <!-- <td>[H]</td> -->
    <td>4-option MCQ</td>
    <td>100</td>
</tr>
<tr>
    <td>global</td>
    <td>-</td>
    <!-- <td>[T][H]</td> -->
    <td>4-option MCQ</td>
    <td>100</td>
</tr>

<tr>
    <td rowspan="2">Movie and Music Recommendation (MMR)</td>
    <td>Chinese</td>
    <td><i>E</i></td>
    <!-- <td>[H]</td> -->
    <td>4-option MCQ</td>
    <td>50</td>
</tr>
<tr>
    <td>global</td>
    <td>-</td>
    <!-- <td>[T]</td> -->
    <td>4-option MCQ</td>
    <td>50</td>
</tr>
<tr>
    <td rowspan="2">Sport Understanding (SpU)</td>
    <td>Chinese</td>
    <td><i>F</i></td>
    <!-- <td>[H]</td> -->
    <td>2-option MCQ</td>
    <td>200</td>
</tr>
<tr>
    <td>global</td>
    <td>-</td>
    <!-- <td>[H]</td> -->
    <td>2-option MCQ</td>
    <td>200</td>
</tr>

<tr>
    <td rowspan="2">Natural Language Inference (NLI)</td>
    <td>Chinese</td>
    <td><i>G, E, L</i></td>
    <!-- <td>[S][H]</td> -->
    <td>3-option MCQ</td>
    <td>100</td>
</tr>
<tr>
    <td>global</td>
    <td>-</td>
    <!-- <td>[S]</td> -->
    <td>3-option MCQ</td>
    <td>100</td>
</tr>

<tr>
    <td rowspan="2">Reading Comprehension (RC)</td>
    <td>Chinese</td>
    <td>all 7 aspects</td>
    <!-- <td>[S]</td> -->
    <td>4-option MCQ</td>
    <td>200</td>
</tr>
<tr>
    <td>global</td>
    <td>-</td>
    <!-- <td>[S]</td> -->
    <td>4-option MCQ</td>
    <td>200</td>
</tr>
<tr>
    <td rowspan="4" style="vertical-align: middle;">Memorization</td>
    <td>Anachronisms Judgment (AJ)</td>
    <td>Chinese</td>
    <td><i>H, AC, LC, F</i></td>
    <!-- <td>[H]</td> -->
    <td>Free-form QA</td>
    <td>150</td>
</tr>

<tr>
    <td>Time Understanding (TU)</td>
    <td>Chinese</td>
    <td><i>H, AC, LC</i></td>
    <!-- <td>[H]</td> -->
    <td>Free-form QA</td>
    <td>83</td>
</tr>

<tr>
    <td>Movie and Music Recommendation (MMR)</td>
    <td>Chinese</td>
    <td><i>E</i></td>
    <!-- <td>[H]</td> -->
    <td>Free-form QA</td>
    <td>399</td>
</tr>

<tr>
    <td>Sport Understanding (SpU)</td>
    <td>Chinese</td>
    <td><i>F</i></td>
    <!-- <td>[H]</td> -->
    <td>Free-form QA</td>
    <td>127</td>
</tr>


</tr>

</tr>
    </tbody>
</table>


## 📒Model Performance

### Reasoning Tasks
<table align="center">
    <thead>
        <tr >
            <th rowspan="2" style="vertical-align: middle;">LLM</th>
            <th colspan="8" style="text-align: center;border-right: 1px solid black;"scope="colgroup" >Chinese Commonsense Domain</th>
            <th colspan="8" scope="colgroup"style="text-align: center;"> Global Commonsense Domain</th>
        </tr>
        <tr style="text-align: center;">
            <th>AJ</th><th>TU</th><th>SqU</th><th>MMR</th><th>SpU</th><th>NLI</th><th>RC</th><th style="border-right: 1px solid black;">Avg.</th>
            <th>AJ</th><th>TU</th><th>SqU</th><th>MMR</th><th>SpU</th><th>NLI</th><th>RC</th><th>Avg.</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>GPT-3.5-1106</td>
            <td>85.33</td><td>39.0</td><td>65.0</td><td>42.0</td><td>80.5</td><td>61.0</td><td>50.5</td><td style="border-right: 1px solid black;">60.48</td>
            <td>90.00</td><td>94.0</td><td>87.0</td><td>46.0</td><td>88.5</td><td>66.0</td><td>49.5</td><td>74.43</td>
        </tr>
        <tr>
    <td>GPT-4-1106</td>
    <td>96.67</td><td><strong>60.0</strong></td><td>85.0</td><td>74.0</td><td>86.0</td><td>77.0</td><td>62.5</td><td style="text-decoration: underline;">77.31</u></td>
    <td><strong>95.33</strong></td><td><strong>98.0</strong></td><td><strong>97.0</strong></td><td><strong>66.0</strong></td><td>90.0</td><td>72.0</td><td><strong>72.0</strong></td><td><strong>84.33</strong></td>
</tr>
<tr>
    <td>LLaMA-2-7B</td>
    <td>51.33</td><td>36.0</td><td>11.0</td><td>14.0</td><td>49.5</td><td>52.0</td><td>8.0</td><td>31.69</td>
    <td>62.67</td><td>17.0</td><td>14.0</td><td>16.0</td><td>49.5</td><td>22.0</td><td>13.0</td><td>27.74</td>
</tr>
<tr>
    <td>LLaMA-2-13B</td>
    <td>56.00</td><td>33.0</td><td>38.0</td><td>30.0</td><td>58.0</td><td>47.0</td><td>38.0</td><td>42.86</td>
    <td>66.67</td><td>24.0</td><td>39.0</td><td>50.0</td><td>53.5</td><td>57.0</td><td>33.5</td><td>46.24</td>
</tr>
<tr>
    <td>LLaMA-2-70B</td>
    <td>57.33</td><td>37.0</td><td>52.0</td><td>32.0</td><td>55.0</td><td>56.0</td><td>41.5</td><td>47.26</td>
    <td>72.67</td><td>84.0</td><td>73.0</td><td>42.0</td><td>64.0</td><td>61.0</td><td>41.5</td><td>62.60</td>
</tr>
<tr>
    <td>Vicuna-7B-v1.5-16k</td>
    <td>52.00</td><td>29.0</td><td>34.0</td><td>32.0</td><td>51.0</td><td>49.0</td><td>35.5</td><td>40.36</td>
    <td>45.33</td><td>64.0</td><td>37.0</td><td>26.0</td><td>58.5</td><td>52.0</td><td>32.5</td><td>45.05</td>
</tr>
<tr>
    <td>Vicuna-13B-v1.5-16k</td>
    <td>64.67</td><td>25.0</td><td>32.0</td><td>26.0</td><td>51.5</td><td>60.0</td><td>40.0</td><td>42.74</td>
    <td>72.67</td><td>74.0</td><td>41.0</td><td>50.0</td><td>68.0</td><td>61.0</td><td>36.0</td><td>57.52</td>
</tr>
<tr style="border-top: 1px solid black;">
    <td>ChatGLM3-6B-32k</td>
    <td>66.00</td><td>40.0</td><td>59.0</td><td>38.0</td><td>77.0</td><td>72.0</td><td>37.5</td><td>55.64</td>
    <td>34.00</td><td>69.0</td><td>71.0</td><td>28.0</td><td>75.5</td><td>63.0</td><td>34.0</td><td>53.50</td>
</tr>
<tr>
    <td>Baichuan2-7B</td>
    <td>76.00</td><td>41.0</td><td>48.0</td><td>38.0</td><td>72.0</td><td>53.0</td><td>49.5</td><td>53.93</td>
    <td>55.33</td><td>65.0</td><td>54.0</td><td>26.0</td><td>60.5</td><td>59.0</td><td>29.0</td><td>49.83</td>
</tr>
<tr>
    <td>Baichuan2-13B</td>
    <td>85.33</td><td>40.0</td><td>48.0</td><td>46.0</td><td>72.5</td><td>66.0</td><td>51.5</td><td>58.48</td>
    <td>77.33</td><td>74.0</td><td>58.0</td><td>40.0</td><td>71.0</td><td>61.0</td><td>39.0</td><td>60.05</td>
</tr>
<tr>
    <td>InternLM2-7B</td>
    <td>88.00</td><td>38.0</td><td>58.0</td><td>38.0</td><td>76.0</td><td>81.0</td><td>25.0</td><td>57.71</td>
    <td>74.67</td><td>80.0</td><td>62.0</td><td>20.0</td><td>78.0</td><td><strong>76.0</strong></td><td>23.5</td><td>59.17</td>
</tr>
<tr>
    <td>InternLM2-20B</td>
    <td>88.00</td><td>55.0</td><td>54.0</td><td>44.0</td><td>74.5</td><td>80.0</td><td>23.0</td><td>59.79</td>
    <td>82.67</td><td>83.0</td><td>61.0</td><td>14.0</td><td>74.5</td><td>72.0</td><td>27.0</td><td>59.17</td>
</tr>
<tr>
    <td>Yi-6B</td>
    <td>70.67</td><td>32.0</td><td>47.0</td><td>32.0</td><td>75.0</td><td>50.0</td><td>42.0</td><td>49.81</td>
    <td>79.33</td><td>63.0</td><td>43.0</td><td>14.0</td><td>70.5</td><td>57.0</td><td>33.5</td><td>51.48</td>
</tr>
<tr>
    <td>Yi-34B</td>
    <td>96.00</td><td>55.0</td><td>89.0</td><td>76.0</td><td><strong>88.5</strong></td><td>72.0</td><td>51.5</td><td>75.43</td>
    <td>88.67</td><td>92.0</td><td>87.0</td><td>56.0</td><td>89.0</td><td>70.0</td><td>47.5</td><td>75.74</td>
</tr>
<tr>
    <td>DeepSeek-7B</td>
    <td>81.33</td><td>34.0</td><td>50.0</td><td>50.0</td><td>79.5</td><td>57.0</td><td>31.5</td><td>54.76</td>
    <td>68.00</td><td>76.0</td><td>47.0</td><td>50.0</td><td>72.5</td><td>59.0</td><td>32.5</td><td>57.86</td>
</tr>
<tr>
    <td>DeepSeek-67B</td>
    <td>96.67</td><td>57.0</td><td>83.0</td><td><strong>92.0</strong></td><td>87.5</td><td>77.0</td><td>34.5</td><td>75.38</td>
    <td>90.00</td><td>95.0</td><td>86.0</td><td>22.0</td><td>88.0</td><td>73.0</td><td>39.0</td><td>70.43</td>
</tr>
<tr>
    <td>Qwen-7B</td>
    <td>70.67</td><td>38.0</td><td>55.0</td><td>48.0</td><td>71.0</td><td>57.0</td><td>49.5</td><td>55.60</td>
    <td>74.67</td><td>78.0</td><td>69.0</td><td>50.0</td><td>72.5</td><td>55.0</td><td>36.0</td><td>62.17</td>
</tr>
<tr>
    <td>Qwen-14B</td>
    <td>87.33</td><td>54.0</td><td>77.0</td><td>60.0</td><td>82.5</td><td>66.0</td><td>55.0</td><td>68.83</td>
    <td>84.00</td><td>83.0</td><td>83.0</td><td>44.0</td><td>84.5</td><td>71.0</td><td>40.0</td><td>69.93</td>
</tr>
<tr>
    <td>Qwen-72B</td>
    <td><strong>98.00</strong></td><td>59.0</td><td><strong>91.0</strong></td><td>84.0</td><td>86.5</td><td><strong>84.0</strong></td><td><strong>67.5</strong></td><td><strong>81.43</strong></td>
    <td>94.00</td><td>92.0</td><td>93.0</td><td>64.0</td><td><strong>93.0</strong></td><td>71.0</td><td>63.5</td><td style="text-decoration: underline;">81.50</u></td>
</tr>
    </tbody>
</table>
We selected the empirically optimal prompt strategy: XLT for English LLMs and ZH-CoT for Chinese-oriented LLMs. The table above shows the accuracy of LLMs on CHARM reasoning tasks. For detailed experimental results, please refer to the paper.

### Prompt Strategy
We average the 19 × 5 LLM-prompt combinations along the above two dimensions and here is the obtained result.
<table align="center">
    <thead>
        <tr>
            <th></th>
            <th><strong>Prompt</strong></th>
            <th><strong>Avg. all LLMs</strong></th>
            <th><strong>Avg. CN-LLMs</strong></th>
            <th><strong>Avg. EN-LLMs</strong></th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="5">Avg. all domains</td>
            <td>Direct</td>
            <td>46.28</td>
            <td>48.41</td>
            <td>42.64</td>
        </tr>
        <tr>
            <td>ZH-CoT</td>
            <td>56.66</td>
            <td><strong>62.40</strong></td>
            <td>46.81</td>
        </tr>
        <tr>
            <td>EN-CoT</td>
            <td>54.46</td>
            <td>58.19</td>
            <td>48.06</td>
        </tr>
        <tr>
            <td>Translate-EN</td>
            <td>53.88</td>
            <td>55.51</td>
            <td>51.07</td>
        </tr>
        <tr>
            <td>XLT</td>
            <td>56.81</td>
            <td>59.09</td>
            <td><strong>52.90</strong></td>
        </tr>
        <tr>
            <td rowspan="5">Avg. Chinese domain</td>
            <td>Direct</td>
            <td>45.43</td>
            <td>47.76</td>
            <td>41.44</td>
        </tr>
        <tr>
            <td>ZH-CoT</td>
            <td><strong>56.35</strong></td>
            <td><strong>62.23</strong></td>
            <td>46.26</td>
        </tr>
        <tr>
            <td>EN-CoT</td>
            <td>52.06</td>
            <td>56.36</td>
            <td>44.68</td>
        </tr>
        <tr>
            <td>Translate-EN</td>
            <td>47.25</td>
            <td>47.82</td>
            <td>46.27</td>
        </tr>
        <tr>
            <td>XLT</td>
            <td>53.80</td>
            <td>56.63</td>
            <td><strong>48.96</strong></td>
        </tr>
        <tr>
            <td rowspan="5">Avg. global domain</td>
            <td>Direct</td>
            <td>47.13</td>
            <td>49.05</td>
            <td>43.85</td>
        </tr>
        <tr>
            <td>ZH-CoT</td>
            <td>56.96</td>
            <td>62.57</td>
            <td>47.35</td>
        </tr>
        <tr>
            <td>EN-CoT</td>
            <td>56.85</td>
            <td>60.01</td>
            <td>51.44</td>
        </tr>
        <tr>
            <td>Translate-EN</td>
            <td><strong>60.50</strong></td>
            <td><strong>63.20</strong></td>
            <td>55.87</td>
        </tr>
        <tr>
            <td> XLT</td>
            <td>59.82</td>
            <td>61.56</td>
            <td><strong>56.84</strong></td>
        </tr>

</table>


💡 Results showed that LLMs' orientation and the task's domain affect prompt strategy performance, which enriches previous research findings.

- **From the LLM dimension**, it's clear that various LLMs prefer different prompt strategies: XLT consistently excels for English LLMs among the 5 strategies, while for Chinese-oriented LLMs, despite some complexity, ZH-CoT generally performs best. 

- **From the commonsense domain dimension**, strategies that use English for reasoning (like XLT, Translate-EN, etc.) are suitable for the global domain; however, ZH-CoT generally performs better in the Chinese domain.


The conclusion here differs from previous studies ([Huang et al., 2023a](https://arxiv.org/pdf/2305.07004.pdf), [Zhang et al., 2023a](https://aclanthology.org/2023.emnlp-main.491.pdf) , [Shi et al., 2022](https://arxiv.org/pdf/2210.03057.pdf)), which suggested that employing English for non-English reasoning tasks was more effective than using the native language.



### Integrated Reasoning vs Memorization
We evaluated the correlation between the integrated
reasoning and the memorization on the MRI tasks. Here is the average performance of the LLMs on the 4 MRI tasks.

<div style="display: flex; justify-content: center;" align="center">
<center>
<img src="./docs/figure/Fig_mem-integrated_rea-avg_v4.png" width="50%">
</div>

💡 As shown in Figure, the 19 LLMs can be roughly divided into the three types:

- **Type I: Low memorization and low integrated reasoning ability.** We found that apart from OpenAI's GPT series, all other English LLMs belong to this type.

- **Type II: High memorization and medium integrated reasoning ability.** GPT3.5 and all Chinese-oriented LLMs below 30B belong to this type. It's worth noting that some LLMs have high memorization performance, but relatively poor integrated reasoning ability.

- **Type III: Ultra-high memorization and high integrated reasoning ability.** This category includes GPT4 and the three Chinese-oriented LLMs that exceed a size of 30B.


### Memorization-Independent Reasoning
We propose two methods to compare the LLMs' memorization-independent reasoning on the MRI tasks : **Mono-LLM-Memorization (FRMM) and Memorization-Independent Battles among LLMs (MIB)**  (For specific details about the FRMM and MIB methods, please refer to the paper.) Here is the result of FRMM and MIB methods.

<table align="center">
    <thead>
        <tr>
            <th rowspan="2">Rank</th>
            <th rowspan="2">Integrated Reasoning</th>
            <th colspan="2">Memorization-independent Reasoning</th>
        </tr>
        <tr>
            <th>FRMM</th>
            <th>MIB</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>1</td>
            <td>DeepSeek-67B</td>
            <td>Yi-34B (<span style="color:red;">↑3</span>)</td>
            <td>GPT-4 (<span style="color:red;">↑2</span>)</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Qwen-72B</td>
            <td>DeepSeek-67B (<span style="color:green;">↓1</span>)</td>
            <td>Yi-34B (<span style="color:red;">↑2</span>)</td>
        </tr>
        <tr>
            <td>3</td>
            <td>GPT-4</td>
            <td>GPT-4 (-)</td>
            <td>Qwen-72B (<span style="color:green;">↓1</span>)</td>
        </tr>
        <tr>
            <td>4</td>
            <td>Yi-34B</td>
            <td>Qwen-72B (<span style="color:green;">↓2</span>)</td>
            <td>DeepSeek-67B (<span style="color:green;">↓3</span>)</td>
        </tr>
        <tr>
            <td>5</td>
            <td>Qwen-14B</td>
            <td>GPT-3.5 (<span style="color:red;">↑2</span>)</td>
            <td>GPT-3.5 (<span style="color:red;">↑2</span>)</td>
        </tr>
        <tr>
            <td>6</td>
            <td>InternLM2-20B</td>
            <td>Qwen-14B (<span style="color:green;">↓1</span>)</td>
            <td>Qwen-14B (<span style="color:green;">↓1</span>)</td>
        </tr>
        <tr>
            <td>7</td>
            <td>GPT-3.5</td>
            <td>InternLM2-20B (<span style="color:green;">↓1</span>)</td>
            <td>InternLM2-20B (<span style="color:green;">↓1</span>)</td>
        </tr>
        <tr>
            <td>8</td>
            <td>InternLM2-7B</td>
            <td>InternLM2-7B (-)</td>
            <td>InternLM2-7B (-)</td>
        </tr>
        <tr>
            <td>9</td>
            <td>DeepSeek-7B</td>
            <td>Baichuan2-13B (<span style="color:red;">↑1</span>)</td>
            <td>Baichuan2-13B (<span style="color:red;">↑1</span>)</td>
        </tr>
        <tr>
            <td>10</td>
            <td>Baichuan2-13B</td>
            <td>DeepSeek-7B (<span style="color:green;">↓1</span>)</td>
            <td>DeepSeek-7B (<span style="color:green;">↓1</span>)</td>
        </tr>
        <tr>
            <td>11</td>
            <td>Baichuan2-7B</td>
            <td>Yi-6B (<span style="color:red;">↑3</span>)</td>
            <td>Baichuan2-7B (-)</td>
        </tr>
        <tr>
            <td>12</td>
            <td>ChatGLM3-6B</td>
            <td>ChatGLM3-6B (-)</td>
            <td>ChatGLM3-6B (-)</td>
        </tr>
        <tr>
            <td>13</td>
            <td>Qwen-7B</td>
            <td>Baichuan2-7B (<span style="color:green;">↓2</span>)</td>
            <td>Qwen-7B (-)</td>
        </tr>
        <tr>
            <td>14</td>
            <td>Yi-6B</td>
            <td>Qwen-7B (<span style="color:green;">↓1</span>)</td>
            <td>Yi-6B (-)</td>
        </tr>
        <tr>
            <td>15</td>
            <td>LLaMA-2-70B</td>
            <td>LLaMA-2-13B (<span style="color:red;">↑1</span>)</td>
            <td>LLaMA-2-13B (<span style="color:red;">↑1</span>)</td>
        </tr>
        <tr>
            <td>16</td>
            <td>LLaMA-2-13B</td>
            <td>LLaMA-2-70B (<span style="color:green;">↓1</span>)</td>
            <td>LLaMA-2-70B (<span style="color:green;">↓1</span>)</td>
        </tr>
        <tr>
            <td>17</td>
            <td>Vicuna-13B-v1.5</td>
            <td>Vicuna-13B-v1.5 (-)</td>
            <td>Vicuna-13B-v1.5 (-)</td>
        </tr>
        <tr>
            <td>18</td>
            <td>Vicuna-7B-v1.5</td>
            <td>LLaMA-2-7B (<span style="color:red;">↑1</span>)</td>
            <td>Vicuna-7B-v1.5 (-)</td>
        </tr>
        <tr>
            <td>19</td>
            <td>LLaMA-2-7B</td>
            <td>Vicuna-7B-v1.5 (<span style="color:green;">↓1</span>)</td>
            <td>LLaMA-2-7B (-)</td>
        </tr>
    </tbody>
</table>


💡 If Language Models (LLMs) provide incorrect responses to retained reasoning questions, these can be termed as memorization-independent reasoning errors. We analyzed these errors by manually reviewing the reasoning process and categorized them into four main types.

- **Understanding Error:** In this case, the LLM was unable to accurately comprehend the question, including misunderstanding the content, ignoring or even modifying important information in the premise, and failing to grasp the core query of the question.

- **Knowledge Error:** The LLM incorporated inaccurate knowledge during the reasoning process. It's important to highlight that the knowledge pieces related to the reasoning question were previously examined in the related memorization questions, which the LLM answered correctly. However, the LLM output incorrect information during the reasoning phase.

- **Logical Error:** The LLM made logical reasoning errors, such as mathematical reasoning errors, inability to reach the correct conclusion based on sufficient information, or reaching the correct conclusion but outputing the wrong option.
- **Other Errors:** These are other scattered, relatively rare types of errors.

💡 Distribution of the memorization-independent reasoning errors
<div style="display: flex; justify-content: center;" align="center">
<center>
<img src="./docs/figure/Fig_pie_chart-mem_independent_err-3LLms.png" width="40%">
</div>


💡 Examples of the 3 types of memorization-independent reasoning errors of LLMs
<div style="display: flex; justify-content: center;" align="center">
<center>
<img src="./docs/figure/Fig_mem-independent-rea-err-example.png" width="80%">>
</div>


## 🛠️Inference CHARM with OpenCompass


## 🖊️ Citation