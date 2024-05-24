
## ✨CHARM
**CHARM** 是首个全面深入评估大型语言模型（LLMs）在中文常识推理能力的基准测试，它覆盖了国际普遍认知的常识以及独特的中国文化常识。此外，CHARM 还可以评估 LLMs 独立于记忆的推理能力，并分析其典型错误。


### 📖 常识领域
#### 🌐 全球常识领域
全球常识领域包含了具有普遍理解性的常识，覆盖了现代生活中的各种对象和方面，是个体应当了解的知识。这些内容包括基础教育期望个体所掌握的基本知识。涉及到人物时，这些都是在全球范围内广为认可的人物。
#### 🚩 中国常识领域
中国常识领域包含了特定于中国的元素，我们将其分为以下七个方面：
- **历史 *(H)* ：** 包括中国历史上的重要事件和人物、中国的朝代以及关于中国历史的其他基础事实和共享知识。

- **传统文化与艺术 *(CA)*** 囊括中国的传统文化艺术、文学作品和传统生活方式。

- **日常生活和习俗 *(LC)*** 包括现代中国的日常生活、服装、食品、住房、交通、节日等。

- **娱乐 *(E)* :** 包括现代中国日常生活中的电影、电视节目、音乐和其他娱乐活动。
- **公众人物 *(F)*** 涵盖在中国社会广为人知的公众人物。
- **地理 *(G)*** 包括中国的地理分布、自然景观和特色地区文化。

- **汉语语言 *(L)*** 包括中国语言的基本知识，如汉字、成语等。

### 📋 任务列表

- **推理任务 :** CHARM 由7个推理任务组成，包括：**时代错误判断（AJ）、时间理解（TU）、序列理解（SqU）、电影和音乐推荐（MMR）、体育理解（SpU）、自然语言推断（NLI）以及阅读理解（RC）。**

- **记忆任务：** 我们选择了**AJ（时代错误判断）、TU（时间理解）、MMR（电影和音乐推荐）以及 SpU（体育理解）** ，这些被称为记忆-推理-互联（MRI）的任务，我们构建了与这些推理任务相关的记忆任务。

<table align="center">
    <thead>
        <tr>
            <th>任务类型</th>
            <th>任务</th>
            <th>常识领域</th>
            <th>中国常识方面</th>
            <!-- <th>Construction</th> -->
            <th>题目类型</th>
            <th># 题目数量</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="14" style="vertical-align: middle;">推理</td>
            <td rowspan="2" >时代错误 (AJ)</td>
            <td>中国的</td>
            <td><i>H, AC, LC, F</i></td>
            <!-- <td>[H]</td> -->
            <td>二选项多选题</td>
            <td>150</td>
        </tr>
        <tr>
            <td>全球的</td>
            <td>-</td>
            <!-- <td>[T][H]</td> -->
            <td>二选项多选题</td>
            <td>150</td>
        </tr>
        <tr>
    <td rowspan="2">时间理解 (TU)</td>
    <td>中国的</td>
    <td><i>H, AC, LC</i></td>
    <!-- <td>[H]</td> -->
    <td>四选项多选题</td>
    <td>100</td> 
    <tr>
    <tr>
    <td rowspan="2">顺序理解 (SqU)</td>
    <td>中国的</td>
    <td><i>H, CA, LC, G, L</i></td>
    <!-- <td>[H]</td> -->
    <td>四选项多选题</td>
    <td>100</td>
</tr>
<tr>
    <td>全球的</td>
    <td>-</td>
    <!-- <td>[T][H]</td> -->
    <td>四选项多选题</td>
    <td>100</td>
</tr>

<tr>
    <td rowspan="2">电影和音乐推荐 (MMR)</td>
    <td>中国的</td>
    <td><i>E</i></td>
    <!-- <td>[H]</td> -->
    <td>四选项多选题</td>
    <td>50</td>
</tr>
<tr>
    <td>全球的</td>
    <td>-</td>
    <!-- <td>[T]</td> -->
    <td>四选项多选题</td>
    <td>50</td>
</tr>
<tr>
    <td rowspan="2">体育理解 (SpU)</td>
    <td>中国的</td>
    <td><i>F</i></td>
    <!-- <td>[H]</td> -->
    <td>二选项多选题</td>
    <td>200</td>
</tr>
<tr>
    <td>全球的</td>
    <td>-</td>
    <!-- <td>[H]</td> -->
    <td>二选项多选题</td>
    <td>200</td>
</tr>

<tr>
    <td rowspan="2">自然语言推理 (NLI)</td>
    <td>中国的</td>
    <td><i>G, E, L</i></td>
    <!-- <td>[S][H]</td> -->
    <td>三选项多选题</td>
    <td>100</td>
</tr>
<tr>
    <td>全球的</td>
    <td>-</td>
    <!-- <td>[S]</td> -->
    <td>三选项多选题</td>
    <td>100</td>
</tr>

<tr>
    <td rowspan="2">阅读理解 (RC)</td>
    <td>中国的</td>
    <td>全部7个方面</td>
    <!-- <td>[S]</td> -->
    <td>四选项多选题</td>
    <td>200</td>
</tr>
<tr>
    <td>全球的</td>
    <td>-</td>
    <!-- <td>[S]</td> -->
    <td>四选项多选题</td>
    <td>200</td>
</tr>
<tr>
    <td rowspan="4" style="vertical-align: middle;">Memorization</td>
    <td>时代错误 (AJ)</td>
    <td>中国的</td>
    <td><i>H, AC, LC, F</i></td>
    <!-- <td>[H]</td> -->
    <td>问答题</td>
    <td>150</td>
</tr>

<tr>
    <td>时间理解 (TU)</td>
    <td>中国的</td>
    <td><i>H, AC, LC</i></td>
    <!-- <td>[H]</td> -->
    <td>问答题</td>
    <td>83</td>
</tr>

<tr>
    <td>电影和音乐推荐 (MMR)</td>
    <td>中国的</td>
    <td><i>E</i></td>
    <!-- <td>[H]</td> -->
    <td>问答题</td>
    <td>399</td>
</tr>

<tr>
    <td>体育理解 (SpU)</td>
    <td>中国的</td>
    <td><i>F</i></td>
    <!-- <td>[H]</td> -->
    <td>问答题</td>
    <td>127</td>
</tr>


</tr>

</tr>
    </tbody>
</table>



## 文件结构
CHARM文件结构如下所示:

- `./reasoning`: 包含全球和中国常识领域中每个推理任务的问题。
- `./reasoning_Translate-EN`: 包含`./reasoning`的英文翻译。.
- `./memorization`: 包含中文常识领域中AJ、TU、MMR、SpU任务的相应记忆问题。
- `./memorization_Translate-EN`: 包含 `./memorization`的英文翻译。
- `./few-shot-examples`:包含每个推理任务的三个示例。
- `./few-shot-examples_Translate-EN`: 包含 `./few-shot-examples`的英文翻译。

## Translation

所有文件，包括 `reasoning`, `memorization` and `few-shot-examples`, 均通过 [DeepL API](https://www.deepl.com/api.html) 翻译成英文。请注意，通过 API 完成的涉及传统中国诗歌、成语、电影名称等主题的翻译可能存在不准确之处。翻译后的英文文件仅为方便非母语为中文的人士查看。如需准确理解，应参考原始的中文问题。
