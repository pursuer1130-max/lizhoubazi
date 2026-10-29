#!/usr/bin/env python3
"""Offline, reproducible chart data. No predictions, network, or telemetry."""
import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
VERSION = '1.0.0'
TRIGRAMS = [
    ('乾', (1, 1, 1), '金'), ('兑', (1, 1, 0), '金'),
    ('离', (1, 0, 1), '火'), ('震', (1, 0, 0), '木'),
    ('巽', (0, 1, 1), '木'), ('坎', (0, 1, 0), '水'),
    ('艮', (0, 0, 1), '土'), ('坤', (0, 0, 0), '土'),
]
# Rows: upper trigram; columns: lower trigram; order follows TRIGRAMS.
KING_WEN = [
    [(1,'乾'),(10,'履'),(13,'同人'),(25,'无妄'),(44,'姤'),(6,'讼'),(33,'遁'),(12,'否')],
    [(43,'夬'),(58,'兑'),(49,'革'),(17,'随'),(28,'大过'),(47,'困'),(31,'咸'),(45,'萃')],
    [(14,'大有'),(38,'睽'),(30,'离'),(21,'噬嗑'),(50,'鼎'),(64,'未济'),(56,'旅'),(35,'晋')],
    [(34,'大壮'),(54,'归妹'),(55,'丰'),(51,'震'),(32,'恒'),(40,'解'),(62,'小过'),(16,'豫')],
    [(9,'小畜'),(61,'中孚'),(37,'家人'),(42,'益'),(57,'巽'),(59,'涣'),(53,'渐'),(20,'观')],
    [(5,'需'),(60,'节'),(63,'既济'),(3,'屯'),(48,'井'),(29,'坎'),(39,'蹇'),(8,'比')],
    [(26,'大畜'),(41,'损'),(22,'贲'),(27,'颐'),(18,'蛊'),(4,'蒙'),(52,'艮'),(23,'剥')],
    [(11,'泰'),(19,'临'),(36,'明夷'),(24,'复'),(46,'升'),(7,'师'),(15,'谦'),(2,'坤')],
]


def _int(value):
    return type(value) is int


def hexagram(bits):
    if len(bits) != 6 or any(not _int(x) or x not in (0, 1) for x in bits):
        raise ValueError('六爻必须为六个0/1，按初爻到上爻排列')
    lower = next(i for i,t in enumerate(TRIGRAMS) if tuple(bits[:3]) == t[1])
    upper = next(i for i,t in enumerate(TRIGRAMS) if tuple(bits[3:]) == t[1])
    number, name = KING_WEN[upper][lower]
    return {'number':number, 'name':name, 'upper':TRIGRAMS[upper][0],
            'lower':TRIGRAMS[lower][0], 'lines_bottom_to_top':list(bits),
            'display_top_to_bottom':['━━━━━━' if b else '━━  ━━' for b in reversed(bits)]}


def liuyao(data):
    lines = data.get('lines')
    if not isinstance(lines, list) or len(lines) != 6 or any(not _int(x) or x not in (6,7,8,9) for x in lines):
        raise ValueError('lines须为六个6/7/8/9整数，初爻在前；布尔值无效')
    bits = [x % 2 for x in lines]
    changed = [1-b if x in (6,9) else b for x,b in zip(lines,bits)]
    return {'input_lines_bottom_to_top':lines, 'base':hexagram(bits),
            'moving_lines':[i+1 for i,x in enumerate(lines) if x in (6,9)],
            'changed':hexagram(changed),
            'scope':'仅卦象层，不含纳甲、世应、六亲、旬空或应期计算'}


def meihua(data):
    nums = data.get('numbers')
    if not isinstance(nums, list) or len(nums) != 3 or any(not _int(x) or not 1 <= x <= 10**12 for x in nums):
        raise ValueError('numbers须为三个1至10^12的正整数')
    upper, lower, moving = (nums[0]-1)%8, (nums[1]-1)%8, (nums[2]-1)%6+1
    bits = list(TRIGRAMS[lower][1] + TRIGRAMS[upper][1])
    changed = bits.copy()
    changed[moving-1] ^= 1
    body, use = (upper, lower) if moving <= 3 else (lower, upper)
    return {'numbers':nums, 'convention':'三数分别取上卦、下卦、动爻；余0取8/6',
            'base':hexagram(bits), 'moving_lines':[moving], 'changed':hexagram(changed),
            'mutual':hexagram(bits[1:4]+bits[2:5]),
            'body':{'trigram':TRIGRAMS[body][0],'element':TRIGRAMS[body][2]},
            'use':{'trigram':TRIGRAMS[use][0],'element':TRIGRAMS[use][2]}}


def bazi(data):
    if data.get('calendar') != 'solar':
        raise ValueError('自动八字仅接受核实的公历solar；农历须先可靠转换并注明闰月')
    if data.get('utc_offset') != '+08:00':
        raise ValueError('本版引擎限UTC+08:00，其他时区须使用外部可靠排盘，不可只改标签')
    if data.get('time_basis') != 'civil_standard':
        raise ValueError('time_basis须为civil_standard；本版不做真太阳时或地方时校正')
    if data.get('time_precision') not in ('minute','second'):
        raise ValueError('出生时间须明确到分钟或秒；未知时辰不得用中午代填')
    if not isinstance(data.get('birth_city'),str) or not data['birth_city'].strip():
        raise ValueError('请提供出生城市，用于核对历史时区/夏令时')
    dst = data.get('dst_minutes')
    if not _int(dst) or dst not in (0,60):
        raise ValueError('dst_minutes须明确为0或60，先核实当年当地是否夏令时')
    sect = data.get('sect',2)
    if not _int(sect) or sect not in (1,2):
        raise ValueError('sect须为1或2')
    value = data.get('birth')
    if not isinstance(value,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',value):
        raise ValueError('birth格式须为YYYY-MM-DDTHH:MM:SS')
    birth = datetime.fromisoformat(value)
    standard = birth - timedelta(minutes=dst)
    if not 1901 <= birth.year <= 2099 or not 1901 <= standard.year <= 2099:
        raise ValueError('本版自动八字范围1901–2099')
    gender = data.get('gender_convention')
    if gender not in (None,'male','female'):
        raise ValueError('gender_convention须为null、male或female；仅用于大运传统顺逆口径')
    sys.path.insert(0,str(Path(__file__).resolve().parent/'vendor'))
    from lunar_python import Solar
    calendar_version = json.loads((Path(__file__).resolve().parent/'vendor/PROVENANCE.json').read_text(encoding='utf-8'))['version']
    solar = Solar.fromYmdHms(standard.year,standard.month,standard.day,standard.hour,standard.minute,standard.second)
    lunar = solar.getLunar()
    chart = lunar.getEightChar()
    chart.setSect(sect)
    pillars = {}
    for key,label in [('Year','year'),('Month','month'),('Day','day'),('Time','hour')]:
        pillars[label] = {
            'ganzhi':getattr(chart,'get'+key)(),
            'elements':getattr(chart,'get'+key+'WuXing')(),
            'hidden_stems':getattr(chart,'get'+key+'HideGan')(),
            'stem_ten_god':getattr(chart,'get'+key+'ShiShenGan')(),
            'branch_ten_gods':getattr(chart,'get'+key+'ShiShenZhi')(),
            'nayin':getattr(chart,'get'+key+'NaYin')(),
        }
    warnings = ['计算结果是历法与传统符号数据，不是科学预测。','夏令时/时区由输入声明，脚本未替你核验。']
    if standard.hour in (22,23,0):
        warnings.append('临近子时/换日：建议比较sect=1/2；时柱仍遵循库独立晚子时规则。')
    near = []
    for name,term in lunar.getJieQiTable().items():
        dt = datetime(term.getYear(),term.getMonth(),term.getDay(),term.getHour(),term.getMinute(),term.getSecond())
        if abs((standard-dt).total_seconds()) <= 7200:
            near.append({'name':name,'standard_time':dt.isoformat()})
    if near:
        warnings.append('距节气不超过2小时；须按可靠历表复核，尤其精确到交节分钟的输入。')
    prev_jie, next_jie = lunar.getPrevJie(),lunar.getNextJie()
    result = {'calendar_engine':'lunar-python '+calendar_version,
              'input_clock':value,'normalized_standard_time':standard.isoformat(),
              'utc_offset':'+08:00','dst_minutes_subtracted':dst,'birth_city':data['birth_city'],
              'conventions':{'year':'库精确立春规则','month':'库节令规则','day':'lunar-python sect='+str(sect),
                             'hour':'库getTime()独立晚子时规则','time_basis':'civil_standard'},
              'lunar_label':lunar.toString(), 'pillars':pillars,
              'previous_jie':{'name':prev_jie.getName(),'standard_time':prev_jie.getSolar().toYmdHms()},
              'next_jie':{'name':next_jie.getName(),'standard_time':next_jie.getSolar().toYmdHms()},
              'near_solar_terms':near,'warnings':warnings}
    if gender is not None:
        yun = chart.getYun(1 if gender == 'male' else 0,2)
        result['luck_cycles'] = {
            'gender_convention':gender,'yun_sect':2,'forward':yun.isForward(),
            'start_after':{'years':yun.getStartYear(),'months':yun.getStartMonth(),'days':yun.getStartDay(),'hours':yun.getStartHour()},
            'start_standard_time':yun.getStartSolar().toYmdHms(),
            'age_convention':'库虚岁口径；不同于精确周岁',
            'cycles':[{'ganzhi':d.getGanZhi(),'start_year':d.getStartYear(),'end_year':d.getEndYear(),
                       'start_nominal_age':d.getStartAge(),'end_nominal_age':d.getEndAge()} for d in yun.getDaYun(9) if d.getIndex()>0]}
    return result


def calculate(data):
    if not isinstance(data,dict):
        raise ValueError('输入须为JSON对象')
    method = data.get('method')
    funcs = {'bazi':bazi,'liuyao':liuyao,'meihua':meihua}
    if not isinstance(method,str) or method not in funcs:
        raise ValueError('method须为bazi、liuyao或meihua')
    return {'schema_version':'1','tool_version':VERSION,'method':method,'data':funcs[method](data)}


def main():
    parser = argparse.ArgumentParser(description='观象知易离线排盘：bazi / liuyao / meihua；读UTF-8 JSON，不联网不存资料。')
    parser.add_argument('--input',required=True,help='UTF-8 JSON输入文件路径')
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding='utf-8-sig'))
        print(json.dumps(calculate(payload),ensure_ascii=False,indent=2))
    except (ValueError,TypeError,KeyError,StopIteration,OSError,ImportError) as error:
        print(json.dumps({'status':'error','message':str(error)},ensure_ascii=False),file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
