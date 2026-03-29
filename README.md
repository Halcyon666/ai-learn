# Start Up

```shell
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r/
conda config --set show_channel_urls yes
```

```shell
conda install <package_name>
conda list

# 移除环境
conda remove -n <environment_name> --all -y

cd /d D:\project\backend\ai-learn

# Collecting package metadata (repodata.json): \ Retrying (Retry(total=2, connect=None, read=None, redirect=None, status=None)) after connection broken by 'ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None)': /pkgs/main/noarch/repodata.json.zst
# try with global proxy!

# 安装依赖
conda env create -f environment.yml
# 激活依赖
conda activate ai-env

conda env remove -n ai-env

# 退出当前环境
conda deactivate

```

```shell
# run mcp-client.py

d:\software\anaconda3\Scripts\activate.bat

conda activate ai-env

python mcp-client.py

```

## Repository Contents

```text
README.md
environment.yml
requirements-pip.txt
basic/
  01-learn-pandas.ipynb
  02-numpy.ipynb
  03-pytorch.ipynb
  04-transformers.ipynb
  05-langchain.ipynb
  06-state-graph.ipynb
  07-neo4j.ipynb
  data-strruct.ipynb
  daily-python.ipynb
  loop-and-function.ipynb
data/
  20251130_833918931_MiFitness_hlth_center_aggregated_fitness_data.csv
  20251130_833918931_MiFitness_hlth_center_fitness_data.csv
  atlantis.csv
  atlantis_modified.csv
  atlantis_modified.json
  atlantis_modified.xlsx
  pandas_test.csv
imgs/
  image1.png
  image2.png
  image3.png
langchain/
  Data.csv
  L1-Model-Parser.ipynb
  L2-Memory.ipynb
  L3-Chains.ipynb
  L4-QnA.ipynb
  L5-Evaluation.ipynb
  L6-Agent.ipynb
  OutdoorClothingCatalog_1000.csv
  image.png
  ollama command.md
  faiss_index/
    index.faiss
    index.pkl
  images/
    image.png
notebooks/
  matplotlib.ipynb
  population.ipynb
  stability.ipynb
simple-mcp/
  mcp-client.py
  mcp-server.py
```
