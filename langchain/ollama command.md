## Command of Ollama

```shell
# show all running models
ollama ps
# show detail about xx model
ollama show xx
# stop xx model
ollama stop xx
# list all models
ollama list

ollama run phi3:3.8b

ollama run phi3:mini

ollama run metallama

```

## 如何将该 GGUF 文件导入 Ollama

目录准备
假设你下载后放在本地目录，比如：

D:\models\nomic-embed-text-v1.5.Q2_K.gguf

新建 Modelfile
在该目录下创建一个 Modelfile 文件，内容如下：

FROM ./nomic-embed-text-v1.5.Q2_K.gguf

执行导入命令
打开命令行，切换到该目录，运行：

ollama create nomic-embed-small -f Modelfile

运行测试
导入完成后，可以测试运行：

ollama run nomic-embed-small

虽然这是一个 embedding 模型，但它能帮助你验证整个导入流程是否顺畅，对流程的掌握非常有帮助。
