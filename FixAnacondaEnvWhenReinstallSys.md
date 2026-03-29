# 重新安装Windowns系统之后恢复Conda环境

## 检查conda目录下的conda是不是正常的

```bat

D:\software\anaconda3\Scripts\conda.exe --version

D:\software\anaconda3\condabin\conda.bat --version

```

## 正式修复

```bat
D:\software\anaconda3\condabin\conda.bat init cmd.exe
```

```powershell
D:\software\anaconda3\condabin\conda.bat init powershell
```

## 检查修复后的环境

在powershell和cmd中分别执行如下命令

```powershell
conda --version
```
