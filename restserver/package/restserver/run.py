# coding=utf8
import os
from package.restserver.app import create_app
from package.restserver.config import CConfig
from package.log.log import CLogger

app=create_app()

if __name__=="__main__":

    CLogger().set_level(
        CLogger.LOG_LEVELINFO
    )

    if os.name == 'nt':
        # import os
        print(os.path.dirname(os.path.abspath(__file__)))
        # os.system("tzutil /s \"UTC\"");
        CLogger().set_target_file(os.path.dirname(os.path.abspath(__file__)) + '/restserver.log')
    else:
        # os.environ['TZ'] = 'UTC'
        # time.tzset()
        CLogger().set_target_file('/var/log/restserver.log')

    app.run(
        host=CConfig.HOST,
        port=CConfig.PORT,
        debug=CConfig.DEBUG,
        threaded=True
    )
