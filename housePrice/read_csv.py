import csv
import sys

class csvReader(object):
    def read_csv(self,fpath):
        """
        读取csv文件,(可以通过Excel打开编辑)
        :return: 包含文件内容的矩阵
        """
        with open(fpath, 'r') as file:
            try:
                contents = csv.reader(file)
                matrix = []
                for row in contents:
                    # print(row)
                    matrix.append(row)
                file.close()
            except:
                print('读取错误：该文件不是csv类型！')
                sys.exit(233)
        return matrix

    def extract_matrix(self,matrix):
        """
        提取矩阵中的信息
        :return:字典类型的列表（一个字典存储一个行的信息）
        """
        keys=[]
        for key in matrix[0]:
            keys.append(key)

        rows=[]
        count=1
        firstRow = True
        while count<len(matrix):
            tmp_dict={}
            key_id=0
            for value in matrix[count]:
                if len(matrix[count])!= len(keys):
                    print("Error: len(matrix[count])!= len(keys)")
                    sys.exit(233)

                cur_key=keys[key_id]
                tmp_dict[cur_key]=value
                key_id+=1
            if firstRow is False:
                rows.append(tmp_dict)
            else:
                firstRow=False
            count+=1
        return rows

if __name__=='__main__':
    csvs=csvReader()
    matrix=csvs.read_csv('lianjia.csv')
    rows=csvs.extract_matrix(matrix)
    print(rows)


