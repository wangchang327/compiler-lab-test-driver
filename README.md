# 编译原理实践 测试用代码

## 使用前准备

* ```bash
  git clone --recursive https://github.com/wangchang327/compiler-lab-test-driver.git
  ```

* 确保可执行文件在compiler-lab-test-driver的根目录下

* 如要测试 RISCV 生成, 需要提前打开一个名为 ```riscv``` 的 docker 虚拟机:

  ```bash
  docker run -it --name riscv --rm riscv-dev-env
  ```

## 使用

````bash
python3 test.py e/t/r
````

输出图示:

<img src="fig.png" width="600px" />
