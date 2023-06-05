from multiprocessing import Pool
class mytest():

    def __init__(self):

        self.a = []

    def test(self, arg1):

        self.a.append(arg1)
        return self.a
import networkx as nx
class test():
    def __init__(self):
        self.G = nx.path_graph(3)
        self.G.nodes[0]["foo"] = 0

    # def fun_(self, G, a):
    #         # def fun(G, a):
    #         self.G.nodes[0]["foo"] = self.G.nodes[0]["foo"] + a
    #         # print(G.nodes(data=True))
    #         return 1, self.G
        # temp = fun(*arg)
        # G = temp[-1]
        # return G
    def fun_f(*arg):
        def fun(G, a):
            G.nodes[0]["foo"] = G.nodes[0]["foo"] + a
            print('1;',G.nodes(data=True))
            return 1, G

        temp = fun(*arg)
        G = temp[-1]
        print('2:',G.nodes(data=True))
        return temp

if __name__ == '__main__':
    p = Pool(2)
    b = test()
    args = [(b.G,1), (b.G,4), (b.G,3), (b.G,2)]
    result = []
    for each in args:
        c = p.apply_async(b.fun_f, each)
        # b.G = c.get()[-1]
        result.append(c.get()[-1])
    for ee in result:
        print('3;',ee.nodes(data=True))
    # G = v[-1][-1]
    print('4;',b.G.nodes(data=True))




    # b = mytest()
    # arg = [8,9,10]
    # rslt1 = p.map_async(b.test, arg)  # 异步执行进程1，传入两个参数
    #     # b.a = rslt1.get()[0]
    # # for a in rslt1:
    # #     print(b.a)
    # #     pass
    # print(rslt1.get())


# print(next(rest))
# print(G.nodes(data=True))