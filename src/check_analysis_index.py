# -*-coding:utf-8-*-
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import telegram

today = datetime.today()
this_day = today.strftime("%Y.%m.%d")
one_days_before = (today - timedelta(1)).strftime("%Y.%m.%d")
tow_days_before = (today - timedelta(2)).strftime("%Y.%m.%d")
bot = telegram.Bot(token="1136684466:AAGbpu5NjIhrVKr3tK6VKelS1AOSF2PgW5A")


def check_index():

    try:
        # ES Connect
        es_client = Elasticsearch(['121.125.71.147',
                                   '121.125.71.148',
                                   '121.125.71.149'],
                                  port=9200, timeout=20,
                                  http_auth=('elastic', 'wtlcnNyrDPVko01lZfIl'))
        es_client.info()

        index_name = "index-nudge-result-analysis"

        query = """
        {
          "size": 0,
          "query": {
            "bool": {
              "filter": [
                {
                  "term": {
                    "log_day": "%s"
                  }
                }
              ]
            }
          },"aggs": {
            "NAME": {
              "terms": {
                "field": "action_body.category",
                "size": 1000
              }
            }
          }
        }
        """

        response = es_client.search(index=index_name, body=query % one_days_before)
        list_day = response['aggregations']['NAME']['buckets']

        message = "<넛지 성과 분석>(" + today.strftime("%Y-%m-%d") + ")\n"

        if not list_day:
            message += "ALIAS ERROR"

        for day in list_day:
            message += str(day['key']) + " : " + str(day['doc_count']) + "건\n"

        print(message)
        bot.sendMessage(chat_id='1228894509', text=str(message))
        bot.sendMessage(chat_id='976803858', text=str(message))
        bot.sendMessage(chat_id='1070666335', text=str(message))

    except Exception as es_err:
        print(es_err)
        err_message = "넛지 성과 분석 ERROR"
        err_message += str(es_err)
        bot.sendMessage(chat_id='1228894509', text=err_message)


if __name__ == '__main__':
    check_index()

