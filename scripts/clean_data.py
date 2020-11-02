import json
import pandas as pd
import numpy as np
import datetime as dt
import os

ldr_date = dt.date(2018, 9, 16)
home_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
text_file = home_path + '/ChatExport/result.json'
with open(text_file, encoding="utf8") as f:
    d = json.load(f)
cols = ['type','date','from','from_id','text','sticker_emoji','file','media_type','photo','action']
text_df = pd.json_normalize(d['messages'])[cols]

text_df = text_df[text_df['action']!='phone_call']
text_df['from_id'] = text_df['from_id'].astype('str')
text_df['datetime'] = pd.to_datetime(text_df['date'])
# text_df['datetime_vn_lc'] = text_df['datetime'].dt.tz_localize(tz='Asia/Ho_Chi_Minh')
text_df['date'] = text_df['datetime'].dt.date

text_df['hour'] = text_df['datetime'].dt.hour

text_df['from'] = np.where(text_df['from']=='Trường Hoàng',
                           u'\U0001F425'+u'\U0001F49B'+u'\U0001F33B', text_df['from'])

text_df['text2'] = text_df['text'].replace('[\'!#$%&()*+,-./:;<=>?@^_`{|}~]', '', regex=True)
text_df['text2'] = text_df['text2'].replace('\\s+', ' ', regex=True)

text_df['word_count'] = text_df['text2'].str.split().str.len()

# dayOfWeek={0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
# text_df['weekday_id'] = text_df['datetime'].dt.dayofweek
# text_df['weekday'] = text_df['weekday_id'].map(dayOfWeek)

text_df['isLDR'] = np.where(text_df['date'] <= ldr_date,
                            0, 1)

day_intervals = [text_df['hour'].between(6, 9),
                 text_df['hour'].between(10, 13),
                 text_df['hour'].between(14, 17),
                 text_df['hour'].between(18, 21),
                 text_df['hour'].between(22, 23),
                 text_df['hour'].between(0, 5)]
day_parts = ['6-9','10-13','14-17','18-21','22-24','24-5']

text_df['daypart'] = np.select(day_intervals, day_parts, 0)

# text_df['datetime_eu'] = text_df['datetime_vn_lc'].dt.tz_convert('Europe/Berlin').dt.tz_localize(None)
# text_df['datetime_eu_lc'] = text_df['datetime_vn_lc'].dt.tz_convert('Europe/Berlin')

# text_df['hour_eu'] = text_df['datetime_eu'].dt.hour
# day_intervals_eu = [text_df['hour_eu'].between(6, 9),
#                  text_df['hour_eu'].between(10, 13),
#                  text_df['hour_eu'].between(14, 17),
#                  text_df['hour_eu'].between(18, 21),
#                  text_df['hour_eu'].between(22, 23),
#                  text_df['hour_eu'].between(0, 5)]
# text_df['daypart_eu'] = np.select(day_intervals_eu, day_parts,0)

# text_df['isNight'] = np.where((text_df['daypart']=='night') & (text_df['daypart_eu']=='night'),
#                               1, 0)

text_df['datetime_next'] = np.where(text_df['datetime']==max(text_df['datetime']),
                                    text_df['datetime'],
                                    text_df['datetime'].shift(-1))

text_df['buffer'] = (text_df['datetime_next'] - text_df['datetime']).dt.seconds/(60*60*24)

# text_df['sticker_local_path'] = np.where(text_df['media_type']=='sticker', 
#                                    'ChatExport/' + text_df['file'],
#                                    np.nan)

sticker_path = 'https://raw.githubusercontent.com/truonghm/telegram-text-analysis/master/'
text_df['sticker_url'] = np.where(text_df['media_type']=='sticker', 
                                   sticker_path + 'ChatExport/' + text_df['file'],
                                   np.nan)
# text_df['sticker_html'] = np.where(text_df['media_type']=='sticker', 
#                                    '<img src="'+ text_df['sticker_url'] + '" width="30" height="30"/>',
#                                    np.nan)

# text_df['date_int'] = pd.to_numeric(text_df['datetime'].dt.strftime('%Y%m%d'), errors='coerce')
text_df['month'] = text_df['datetime'].dt.strftime('%Y%m')
text_df['year'] = text_df['datetime'].dt.year.astype('str')

cols = ['date','from','media_type',
        'datetime','text2','word_count','isLDR','daypart','datetime_next','buffer',
        'sticker_url','month','year']
text_df[cols].to_csv(home_path + '/data/text_df.csv', index=False)

stickers_df = text_df[text_df['media_type']=='sticker'].groupby(['sticker_url','from']).agg({'from_id':'count'}).reset_index()
stickers_df.to_csv(home_path + '/data/stickers_df.csv',index=False)
# stickers_df['sticker_html'] = '<img src="'+ stickers_df['sticker_url'] + '" width="30" height="30"/>'