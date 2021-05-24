# wangchang
import os
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('text', type=str, help='The phase to test')
args = parser.parse_args()


class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def delblankline(infile, outfile):
    infopen = open(
        infile,
        'r',
    )
    outfopen = open(outfile, 'w+')

    lines = infopen.readlines()
    for line in lines:
        if line.split():
            outfopen.writelines(line)
        else:
            outfopen.writelines('')

    infopen.close()
    outfopen.close()


test_dir = 'open-test-cases/sysy/section1/functional_test'
minivm_dir = 'MiniVM'

mode = ''
if args.text[0] == 'e':
    mode = '-e'
elif args.text[0] == 't':
    mode = '-t'

if mode != '':
    print('Building minivm')
    os.system(
        'cd ' + minivm_dir +
        ' && rm -rf build && mkdir build && cd build && cmake .. && make -j8')
    print('')

print('Building compiler')
os.system('make -j8 all')
print('')

test_files = os.listdir(test_dir)
pass_count, fail_count = 0, 0
compile_t, run_t = [], []
ignored = False
for fl in test_files:
    name, ext = fl.split('.')[0], fl.split('.')[1]
    if ext != 'sy':
        continue
    if (mode == '-t' or mode == '') and (name[0]
                                         == '9') and (name[1] >= '2'
                                                      and name[1] <= '7'):
        ignored = True
        continue
    start = time.time()
    os.system('./compiler -S {} {} -o output.S'.format(
        mode, test_dir + '/' + name + '.sy'))
    end = time.time()
    compile_t.append((end - start) * 1000.0)
    print('Compilation done')

    print('Testing {}'.format(name))

    if mode != '':
        start = time.time()
        if os.path.exists(test_dir + '/' + name + '.in'):
            os.system(minivm_dir +
                      '/build/minivm {} output.S < {} > test.tmp.out'.format(
                          '-t' if mode == '-t' else '', test_dir + '/' + name +
                          '.in'))
        else:
            os.system(minivm_dir +
                      '/build/minivm {} output.S > test.tmp.out'.format(
                          '-t' if mode == '-t' else ''))
        end = time.time()
    else:
        os.system('docker cp riscv.sh riscv:/root/')
        os.system('docker cp output.S riscv:/root/')
        if os.path.exists(test_dir + '/' + name + '.in'):
            os.system(
                'docker cp {} riscv:/root/test.in'.format(test_dir + '/' +
                                                          name + '.in'))
        start = time.time()
        os.system('docker exec -it riscv bash /root/riscv.sh')
        end = time.time()
        os.system('docker cp riscv:/root/test.tmp.out .')
    delblankline('test.tmp.out', 'test.out')
    print('\tDone executing the compiler and minivm\n\t|')
    run_t.append(end - start)

    try:
        myoutput = open('test.out', 'r')
        delblankline(test_dir + '/{}.out'.format(name), 'std.out')
        stdoutput = open('std.out', 'r')
    except BaseException:
        print('\tOpening file error. Aborted')
        exit(1)

    print('\tComparing output')
    passed = True
    mydata = myoutput.readlines()
    stddata = stdoutput.readlines()

    try:
        for i in range(len(stddata)):
            mydata[i] = mydata[i].strip()
            stddata[i] = stddata[i].strip()
            if (stddata[i] != ''):
                print(
                    '\t|\tLine {}: My output is {}; Standard output is {}; Passed: {}'
                    .format(i + 1, mydata[i], stddata[i],
                            mydata[i] == stddata[i]))
            passed = passed and (mydata[i] == stddata[i])
    except BaseException:
        passed = False

    myoutput.close()
    stdoutput.close()
    if not passed:
        print(bcolors.FAIL + '\tFAILED!\n' + bcolors.ENDC)
        fail_count += 1
        input("Press enter to continue")
    else:
        pass_count += 1
        print(bcolors.OKGREEN + '\tPASSED!\n' + bcolors.ENDC)

ign_info = "(6 Ignored)" if ignored else ""
print(bcolors.OKBLUE + "\nFinished. {} Passed / {} Failed: [{}%] {}".format(
    pass_count, fail_count, int(pass_count /
                                (pass_count + fail_count) * 100), ign_info) +
      bcolors.ENDC)
print(bcolors.OKBLUE +
      "Total compilation time: {:.2f}ms. Maximum compilation time: {:.2f}ms".
      format(sum(compile_t), max(compile_t)) + bcolors.ENDC)
print(bcolors.WARNING +
      "Total run time: {:.4f}s. Maximum run time: {:.4f}s\n".format(
          sum(run_t), max(run_t)) + bcolors.ENDC)

print('Cleaning up')
os.system('cd ' + minivm_dir + ' && rm -rf build')
os.system('rm -f output.S && rm -f *.out && make clean')
