
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


## Folder Structure
The folder is structured as follows :

- `./reasoning`: Contains questions from each of the reasoning tasks in both the global and Chinese commonsense domains.
- `./reasoning_Translate-EN`: Contains the English translations of the `./reasoning`.
- `./memorization`: Contains corresponding memorization questions for the AJ, TU, MMR, SpU tasks in the Chinese commonsense domain.
- `./memorization_Translate-EN`: Contains the English translations of the `./memorization`.
- `./few-shot-examples`: Contains three-shot examples of each reasoning tasks.
- `./few-shot-examples_Translate-EN`: Contains the English translations of the `./few-shot-examples`.

## Translation

All files, including `reasoning`, `memorization` and `few-shot-examples`, have been translated into English using the [DeepL API](https://www.deepl.com/api.html). Please note that translations of topics involving traditional Chinese poetry, idioms, movie names, etc., done via the API may have inaccuracies. The translated English files are only for the convenience of displaying to people who are not native Chinese speaker. The original Chinese questions should be referred to for accurate understanding.
