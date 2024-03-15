import logging
from logfmter import Logfmter

# Enable logging
logging.basicConfig(
    format='timestamp=%(asctime)s logger=%(name)s level=%(levelname)s msg="%(message)s"',
    datefmt="%Y-%m-%dT%H:%M:%S",
    level=logging.INFO,  #уровень логов
    handlers=[logging.FileHandler("./logs/logfmter_bot.log"), logging.StreamHandler()],  # указываем что логи нужно записать в файл, и в консоль
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



import logging
from logfmter import Logfmter

formatter = Logfmter(
    keys=["timestamp","logger","at", "process","msq"],
    mapping={"timestamp": "asctime","logger": "name","at": "levelname", "process": "processName","msq": "message"}
    datefmt="%Y-%m-%dT%H:%M:%S"
)

handler_stdout = logging.StreamHandler()
handler_file = logging.FileHandler("./logs/logfmter_bot.log")
handler_stdout.setFormatter(formatter)
handler_file.setFormatter(formatter)
logging.basicConfig(
    handlers=[handler_stdout,handler_file])

logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# logging.error("hello") # at=ERROR process=MainProceess msg=hello




# import logging
# from logfmter import Logfmter

# formatter = Logfmter(keys=["at", "processName"])

# handler = logging.StreamHandler()
# handler.setFormatter(formatter)

# logging.basicConfig(handlers=[handler])

# logging.error("hello") # at=ERROR processName=MainProceess msg=hello