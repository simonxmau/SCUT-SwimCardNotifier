class LastRemain:

    @staticmethod
    def get():
        num = 0
        try:
            with open('last_remain', 'r') as f:
                num = int(f.read())
        except:
            pass
        return num

    @staticmethod
    def save(num):
        with open('last_remain', 'w') as f:
            f.write(str(num))
            return True
        return False


if __name__ == '__main__':
    print(LastRemain.get())
    print(LastRemain.save(2))
    print(LastRemain.get())
