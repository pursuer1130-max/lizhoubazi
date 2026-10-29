"""Offline observable checks; run: python -X utf8 tests/test_calculations.py."""
import importlib.util
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('divination',ROOT/'codex-plugin/skills/guanxiang-divination/scripts/divination.py')
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)


def birth(value='2005-12-23T08:37:00',**overrides):
    result = dict(method='bazi',calendar='solar',birth=value,time_precision='minute',birth_city='北京',
                  utc_offset='+08:00',dst_minutes=0,time_basis='civil_standard',sect=2)
    result.update(overrides)
    return result


class CalculationTests(unittest.TestCase):
    def test_upstream_known_four_pillars(self):
        # Source: 6tail/lunar-python test/EightCharTest.py test_gan_zhi.
        p = d.calculate(birth())['data']['pillars']
        self.assertEqual([p[k]['ganzhi'] for k in ('year','month','day','hour')],['乙酉','戊子','辛巳','壬辰'])

    def test_second_known_date(self):
        p = d.calculate(birth('2022-08-28T01:50:00'))['data']['pillars']
        self.assertEqual([p[k]['ganzhi'] for k in ('year','month','day','hour')],['壬寅','戊申','癸丑','癸丑'])

    def test_late_zi_matches_upstream(self):
        p = d.calculate(birth('1988-02-15T23:30:00'))['data']['pillars']
        self.assertEqual([p[k]['ganzhi'] for k in ('year','month','day','hour')],['戊辰','甲寅','庚子','戊子'])

    def test_day_sect_changes_at_late_zi(self):
        a = d.calculate(birth('1988-02-15T23:30:00',sect=1))['data']
        b = d.calculate(birth('1988-02-15T23:30:00',sect=2))['data']
        self.assertNotEqual(a['pillars']['day']['ganzhi'],b['pillars']['day']['ganzhi'])
        self.assertEqual(a['pillars']['hour']['ganzhi'],b['pillars']['hour']['ganzhi'])

    def test_dst_normalizes_once(self):
        a = d.calculate(birth('1990-05-17T11:30:00',dst_minutes=60))['data']
        b = d.calculate(birth('1990-05-17T10:30:00'))['data']
        self.assertEqual(a['pillars'],b['pillars'])
        self.assertEqual(a['normalized_standard_time'],'1990-05-17T10:30:00')

    def test_lichun_transition_is_not_lunar_new_year(self):
        a = d.calculate(birth('2024-02-04T10:00:00'))['data']['pillars']
        b = d.calculate(birth('2024-02-04T20:00:00'))['data']['pillars']
        self.assertEqual(a['year']['ganzhi'],'癸卯')
        self.assertEqual(b['year']['ganzhi'],'甲辰')
        self.assertNotEqual(a['month']['ganzhi'],b['month']['ganzhi'])

    def test_no_gender_does_not_invent_luck_cycles(self):
        self.assertNotIn('luck_cycles',d.calculate(birth())['data'])

    def test_optional_luck_cycles_are_ordered(self):
        cycles = d.calculate(birth(gender_convention='female'))['data']['luck_cycles']['cycles']
        self.assertEqual(len(cycles),8)
        self.assertTrue(all(b['start_year']==a['start_year']+10 for a,b in zip(cycles,cycles[1:])))

    def test_rejects_unavailable_precision_timezone_and_invalid_dates(self):
        cases = [birth(time_precision='unknown'),birth(utc_offset='-05:00'),birth(calendar='lunar'),
                 birth(dst_minutes=None),birth(time_basis='true_solar'),birth('2005-02-30T08:00:00'),
                 birth('1899-01-01T08:00:00'),birth(gender_convention='guess'),birth(sect=True)]
        for case in cases:
            with self.subTest(case=case),self.assertRaises(ValueError):
                d.calculate(case)

    def test_all_static_hexagrams_keep_bits_and_number_unique(self):
        numbers=[]
        for n in range(64):
            bits=[(n>>i)&1 for i in range(6)]
            r=d.calculate({'method':'liuyao','lines':[7 if b else 8 for b in bits]})['data']
            self.assertEqual(r['base'],r['changed'])
            self.assertEqual(r['base']['lines_bottom_to_top'],bits)
            self.assertEqual(r['moving_lines'],[])
            numbers.append(r['base']['number'])
        self.assertEqual(sorted(numbers),list(range(1,65)))

    def test_qian_to_kun_all_moving(self):
        r=d.calculate({'method':'liuyao','lines':[9]*6})['data']
        self.assertEqual((r['base']['number'],r['changed']['number']),(1,2))
        self.assertEqual(r['moving_lines'],[1,2,3,4,5,6])

    def test_ji_ji_and_wei_ji(self):
        self.assertEqual(d.hexagram([1,0,1,0,1,0])['number'],63)
        self.assertEqual(d.hexagram([0,1,0,1,0,1])['number'],64)

    def test_meihua_remainder_zero_and_moving_position(self):
        r=d.calculate({'method':'meihua','numbers':[8,8,6]})['data']
        self.assertEqual(r['base']['number'],2)
        self.assertEqual(r['moving_lines'],[6])
        self.assertEqual(r['changed']['number'],23)
        self.assertEqual(r['body']['trigram'],'坤')

    def test_meihua_known_case(self):
        r=d.calculate({'method':'meihua','numbers':[12,25,9]})['data']
        self.assertEqual(r['base']['number'],34)
        self.assertEqual(r['changed']['number'],54)
        self.assertEqual(r['mutual']['number'],43)
        self.assertEqual(r['body']['trigram'],'震')
        self.assertEqual(r['use']['trigram'],'乾')

    def test_rejects_bad_lines_numbers_and_method(self):
        cases=[{'method':'liuyao','lines':[7]*5}, {'method':'liuyao','lines':[7]*5+[True]},
               {'method':'liuyao','lines':[10]*6},{'method':'meihua','numbers':[0,1,2]},
               {'method':'meihua','numbers':[True,1,2]},{'method':[]},[],{'method':'ziwei'}]
        for case in cases:
            with self.subTest(case=case),self.assertRaises(ValueError):
                d.calculate(case)


if __name__=='__main__':
    unittest.main(verbosity=2)
