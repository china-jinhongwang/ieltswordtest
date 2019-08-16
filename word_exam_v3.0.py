# _*_coding : UTF-8_*_
# 开发团队：NONE
# 开发人员：41570
# 开发时间：2019/7/31 17:29
# 文件名称：word_exam.PY
# 开发工具：PyCharm
import random
import numpy as np
import os
import time


def get_ielts_dict(filename):
    ielts_dict = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            ls = line.split(">")
            ielts_dict[ls[0]] = ls[1].strip("\n")
    return ielts_dict


def words_test(n, ielts_dict):
    err_dict = {}
    count = 0
    c = 0
    start_time = time.perf_counter()
    sample_list = random.sample(list(ielts_dict), n)
    print()

    for k in sample_list:
        c += 1
        dict_item = {}
        try:
            pro = ielts_dict[k].split("$")[0]
            print("第{}/{}个单词>> {} {}".format(c, n, k, pro))
            a_list = np.arange(1, 5)
            np.random.shuffle(a_list)
            ch_key_list = random.sample(ielts_dict.keys(), 4)
            if not (k in ch_key_list):
                ch_key_list[0] = k
            for i in range(4):
                value = ielts_dict[ch_key_list[i]]
                dict_item[a_list[i]] = value
            for item in sorted(dict_item):
                print("  {}、{}".format(item, dict_item[item].split('$')[1]))
            while True:
                try:
                    p = input("请输入正确的选项：")
                    if eval(p) in [1, 2, 3, 4]:
                        break
                except:
                    pass

            if dict_item[eval(p)].split("$")[1] != ielts_dict[k].split("$")[1]:
                err_dict[k] = ielts_dict[k]
                print("Sorry，正确答案为：{}、{}".format(k, ielts_dict[k].split("$")[1]))
            else:
                print("恭喜你，答对了！！！")
                count += 1
        except:
            pass
        print()
    end_time = time.perf_counter()
    print("本次测验一共用时{}分{}秒,正确率为：{}/{}={:.2f}%".format(int((end_time-start_time)//60), \
        int((end_time-start_time)%60), count, n, 100 * count / n))

    return err_dict

def print_errwords(err_dict):
    print("你本次测验错误的单词如下：")
    cnt = 0
    for item in err_dict:
        cnt += 1
        print("第{}/{}个单词>> {}: {}".format(cnt, len(err_dict), item, err_dict[item]))


def save_errwords(name, err_dict):
    dict_tmp = {}
    if not os.path.exists("{}.txt".format(name)):
        with open("{}.txt".format(name), 'w', encoding='utf-8') as f:
            f.write("")

    with open("{}.txt".format(name), 'r', encoding="utf-8") as f:
        for line in f:
            ls = line.split(":")
            if len(ls) == 2:
                dict_tmp[ls[0]] = ls[1].strip("\n")
        dict_tmp = dict(dict_tmp, **err_dict)

    with open("{}.txt".format(name), 'w') as f:
            f.write("")

    with open("{}.txt".format(name), "a", encoding="utf-8") as f:
        for item in dict_tmp:
            f.writelines(item + ">" + dict_tmp[item] + "\n")


if __name__ == '__main__':
    filename = "ielts_dict_rv.txt"
    ielts_dict = get_ielts_dict(filename)
    name = input("请输入你的姓名：")
    n = eval(input("请输入抽样样本数量："))
    err_dict = words_test(n, ielts_dict)
    save_errwords(name, err_dict)
    print_errwords(err_dict)

