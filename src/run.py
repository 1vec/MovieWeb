from movienest import create_app

if __name__ == '__main__':
    app = create_app() #作为模块调用movienest
    app.run() #运行app
