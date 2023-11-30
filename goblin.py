import logging


logger = logging.getLogger(__name__)
handler = logging.FileHandler('test.log', encoding='utf-8')
formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Давай протестируем файл на данные?')
try:
    10 / 0
except Exception as e:
    logger.exception(e)