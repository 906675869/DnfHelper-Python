from configparser import ConfigParser


def config():
    try:
        conf = ConfigParser()
        conf.read('static/helper.ini', encoding="utf-8-sig")
        return conf
    except Exception as e:
        print(e)
        exit()
