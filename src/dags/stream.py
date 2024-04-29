from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
  'owner': 'eng_team',
  'depends_on_past': False,
  'start_date': datetime(2024, 4, 4, 10, 00),
  'email_on_failure': False,
  'email_on_retry': False,
  'retries': 1,
  'retry_delay': timedelta(minutes=5),
}

def format_date(data):
  print('received data:', data)
  story = {}
  story['author'] = data['by']
  story['title'] = data['title']
  story['url'] = data.get('url', '')
  story['created_at'] = data['time']
  story['score'] = data['score']
  story['comment_count'] = data['descendants']
  story['top_comments'] = data.get('kids', [])
  return story

def get_top_stories():
  import json
  import requests

  stories = []

  new_story_ids = requests.get('https://hacker-news.firebaseio.com/v0/newstories.json')
  new_story_ids = new_story_ids.json()
  for story_id in new_story_ids[:5]:
    story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json')
    print(story.json())
    story = format_date(story.json())
    stories.append(story)
  
  stories = json.dumps(stories)
  return stories

def stream_from_HN():
  import json
  from kafka import KafkaProducer
  res = get_top_stories()
  
  producer = KafkaProducer(bootstrap_servers='localhost:9092', max_block_ms=5000)
  producer.send('hn_new_stories', json.dumps(res).encode('utf-8'))

stream_from_HN()

# dag = DAG(
#   'hn_stream_pipeline',
#   default_args=default_args,
#   description='A simple DAG to stream new stories from Hacker News',
#   schedule_interval=timedelta(minutes=5),
# )    

# run_task = PythonOperator(
#   task_id='run_data_streaming',
#   python_callable=stream_from_HN,
#   dag=dag,
# )

# run_task