from numpy import *
import copy
class Tensor:
    dis=1   #张量的维度
    dimension=[]        #张量每个维度上的轴长
    tensor=[0]  #张量本身
    elementNum=1    #张量中元素的个数
    def createTensor(self): #根据用户输入定义一个张量
        print("请输入张量的维度：",end="")
        a=0
        while 1:
            a=input()
            if self.isnumber(a)&int(a)>=0:
                self.dis=int(a)
                break
            else:
                print("输入格式错误，请重新输入一个正整数：",end="")
        print("请输入每个维度的长度并用空格隔开：",end="")
        while 1:
            b=input()
            c=b.split()
            d=''.join(c)
            if d.__len__()!=self.dis:
                print("您输入的维度长度的个数不等于当前张量的维度，请重新输入：",end="")
            else:
                j = 0
                for i in d:
                    self.dimension.append(int(i))
                    j += 1
                    if j == self.dis:
                        break
                break
        for i in self.dimension:
            self.elementNum*=i
        self.tensor=ones(self.elementNum).reshape(self.dimension)
        print(self.tensor)
    @classmethod
    def isnumber(cls, s):   #判断一个变量是否是一个整数
        try:
            int(s)
            return True
        except ValueError as e:
            return False
    def getNorm(self):      #获取张量的norm
        t = self.tensor ** 2
        norm = t.sum()
        return norm
    @staticmethod
    def getInnerProduct(tensor1, tensor2):  #获取两个张量的InnerProduct
        s1 = tensor1.shape
        s2 = tensor2.shape
        if s1 != s2:
            print("the dimensions of tensor1 and tensor2 are not equal!")
            return
        else:
            t = tensor1 * tensor2
            return t
    def rankOneToTensor(self,vectorList):   #根据list中的n个一维向量生成一个n维的张量
        len=[]
        total=1
        for i in vectorList:
            # print(i)
            len.append(i.size)
            total*=i.size
        tensor=ones(total).reshape(len)
        # print(tensor)
        d=[]
        self.computeTensor(tensor,vectorList,d)
        # print(tensor)
        return tensor
    def computeTensor(self,tensor,vector,disArray): #根据vector这个向量数组，计算tensor中每个元素的值，在rankOneToTensor中用到
        if tensor.ndim>1:
            for i in arange(tensor.shape[0]):
                d=copy.deepcopy(disArray)
                d.append(i)
                self.computeTensor(tensor[i],vector,d)
        else:
            for j in arange(tensor.size):
                for k in range(len(vector)-1):
                    tensor[j]*=vector[k][disArray[k]]
                tensor[j]*=vector[len(vector)-1][j]
    def tensorMultipliedMatrix(self,n,matrix):  #张量乘以矩阵。！！！！！！还没做完
        print(self.dimension)
        if n>self.dis:
            print("您所要乘的维度超出了tensor的总维度!")
            return
        if self.dimension[n-1]!=matrix.shape[1]:
            print("tensor的第"+str(n)+"个维度的轴长不等于矩阵的列数")
            return
        t=self.tensor.copy()
        t.reshape(3,8)
        print(t)
        # print(self.tensor)
    @staticmethod
    def tensorToMatrix(tensor,n):#张量转换成矩阵！！！！还没做完
        if tensor.ndim<n:
            print("该张量的维度小于n")
            return
    @staticmethod
    def tensorToVector(tensor):#张量转换成向量
        vector=tensor.reshape(-1)
        return vector

def kronecker(matrix1,matrix2):#暴力方式实现kronecker-product
    a=matrix1.shape[0]*matrix2.shape[0]
    b=matrix1.shape[1]*matrix2.shape[1]
    m=arange(a*b).reshape(a,b)
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            ma=matrixMultiplyNumber(matrix2,matrix1[i][j])
            for k in range(ma.shape[0]):
                for l in range(ma.shape[1]):
                    m[i*ma.shape[0]+k][j*ma.shape[1]+l]=ma[k][l]
    return m
def matrixMultiplyNumber(matrix,m):#矩阵乘以一个数
    a=matrix.shape[0]
    b=matrix.shape[1]
    ma=arange(a*b).reshape(a,b)
    for i in range(a):
        for j in range(b):
            ma[i][j]=matrix[i][j]*m
    return ma
def kroneckerByVector(matrix1,matrix2):#运用列向量的kronecker-product得到矩阵的kronecker-product
    a = matrix1.shape[0] * matrix2.shape[0]
    b = matrix1.shape[1] * matrix2.shape[1]
    m = arange(a * b).reshape(a, b)
    for i in range(matrix1.shape[1]):
        v1=getMatrixColumn(matrix1,i)
        print(v1)
        for j in range(matrix2.shape[1]):
            v2=getMatrixColumn(matrix2,j)
            print(v2)
            v3=kronecker_vec(v1,v2)
            print(v3)
            for k in range(v3.size):
                m[k][i*matrix2.shape[1]+j]=v3[k]
    return m
def khatri_rao(matrix1,matrix2):#Khtri=Rao product
    a=matrix1.shape[1]
    b=matrix2.shape[1]
    if a!=b:
        print("两个矩阵的列数不等")
        return
    c=matrix1.shape[0]*matrix2.shape[0]
    m=arange(a*c).reshape(c,a)
    for i in range(a):
        v1=getMatrixColumn(matrix1,i)
        v2=getMatrixColumn(matrix2,i)
        v3=kronecker_vec(v1,v2)
        for j in range(v3.size):
            m[j][i]=v3[j]
    return m
def getMatrixColumn(matrix,x):  #获取矩阵的某一列，得到一个列向量
    v=arange(matrix.shape[0])
    for i in range(v.size):
        v[i]=matrix[i][x]
    return v
def vectorMultiplyNumber(m,v):#列向量乘以一个数
    vec=arange(v.size)
    for i in range(v.size):
        vec[i]=v[i]*m
    return vec
def kronecker_vec(v1,v2):#列向量的Kronecker-product
    v=arange(v1.size*v2.size)
    for i in range(v1.size):
        vec=vectorMultiplyNumber(v1[i],v2)
        for j in range(vec.size):
            v[i*v2.size+j]=vec[j]
    return v
def hadamard(matrix1,matrix2):#hadamard-product
    if matrix1.shape[0]!=matrix2.shape[0] or matrix1.shape[1]!=matrix1.shape[1]:
        print("两个矩阵的行列不等")
        return
    m=matrix1*matrix2
    return m
t=Tensor()
print("测试用例")
print("创建一个tensor")
t.createTensor()
print("获得tensor的norm")
print(t.getNorm())
list=[]
a1=array([1,2,3])
list.append(a1)
a2=array([1,2,3])
list.append(a2)
a3=array([1,2,3])
list.append(a3)
a4=array([1,2])
list.append(a4)
print("多个一维向量得到一个tensor")
t.rankOneToTensor(list)
a5=array([[2,2,2],[2,2,2]])
# t.tensorMultipliedMatrix(2,a5)
a6=array([[[1,4,7,10],[2,5,8,11],[3,6,9,12]],[[13,16,19,22],[14,17,20,23],[15,18,21,24]]])
print("tensor to vector")
print(t.tensorToVector(a6))
a7=array([[2,2,3],[5,4,4]])
a8=array([[3,3],[3,3]])
a9=array([[2,4],[3,1],[4,4]])
a10=array([[2,2],[3,3]])
print("暴力获得kronecker")
print(kronecker(a7,a8))
print("列向量的kronecker-product")
print(kronecker_vec(a2,a3))
print("使用列向量的kronecker-product获得矩阵的kronecker-product")
print(kroneckerByVector(a7,a8))
print("khatri-rao product")
print(khatri_rao(a8,a9))
print("hadamard product")
print(hadamard(a8,a10))


