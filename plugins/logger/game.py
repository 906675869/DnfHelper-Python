from plugins.logger.interface import LogInterface


class GameLog(LogInterface):
    def info(self, arg):
        self.__ordinary(arg, 1)

    def debug(self, arg):
        self.__ordinary(arg, 0)

    def warning(self, arg):
        self.__colorful(arg, 0)

    def error(self, arg):
        self.__colorful(arg, 1)

    def critical(self, arg):
        pass

    def __colorful(self, msg, msg_type):
        # �߲ʹ���
        pass

    def __ordinary(self, msg, msg_type):
        # ��ͨ����
        pass
