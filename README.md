# 编译原理实践 测试用代码

## 使用前准备

* 对 MiniVM 的代码进行改动, 使得它能输出程序的返回值: 在 ```main.cpp``` 返回之前添加

  ```C++
  if (ret) cout << endl << (*ret) % 256 << endl;
  ```

* 确保可执行文件和测试代码在同一路径下, 并填写正确的测试样例和 MiniVM 的位置.

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