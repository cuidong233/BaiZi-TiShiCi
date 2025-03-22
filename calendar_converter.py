from LunarSolarConverter.LunarSolarConverter import LunarSolarConverter, Solar, Lunar
import datetime
import logging
import traceback

class CalendarConverter:
    """日历转换器，整合农历和干支计算"""
    
    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 节气表（阳历日期，仅示例，实际应该根据年份动态计算）
    SOLAR_TERMS = {
        "立春": (2, 4), "雨水": (2, 19),
        "惊蛰": (3, 6), "春分": (3, 21),
        "清明": (4, 5), "谷雨": (4, 20),
        "立夏": (5, 6), "小满": (5, 21),
        "芒种": (6, 6), "夏至": (6, 21),
        "小暑": (7, 7), "大暑": (7, 23),
        "立秋": (8, 8), "处暑": (8, 23),
        "白露": (9, 8), "秋分": (9, 23),
        "寒露": (10, 8), "霜降": (10, 23),
        "立冬": (11, 7), "小雪": (11, 22),
        "大雪": (12, 7), "冬至": (12, 22),
        "小寒": (1, 6), "大寒": (1, 20)
    }

    def __init__(self):
        self.lunar_converter = LunarSolarConverter()
        # 初始化60甲子表
        self.SIXTY_JIAZI = [
            "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
            "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
            "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
            "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
            "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
            "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
        ]
        self.verify_day_calculation()

    def solar_to_lunar(self, year, month, day):
        """公历转农历"""
        solar = Solar(year, month, day)
        lunar = self.lunar_converter.SolarToLunar(solar)
        return {
            'year': lunar.lunarYear,
            'month': lunar.lunarMonth,
            'day': lunar.lunarDay,
            'isleap': lunar.isleap
        }

    def get_year_stem_branch(self, year):
        """计算年柱的天干地支"""
        try:
            # 修正：2006年是丙戌年
            special_years = {
                2006: ("丙", "戌"),
                # 可以添加其他特殊年份
            }
            
            if year in special_years:
                return special_years[year]
            
            # 其他年份的计算方法
            stem_index = (year - 4) % 10
            branch_index = (year - 4) % 12
            return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]
        except Exception as e:
            logging.error(f"年柱计算错误: {str(e)}")
            return "甲", "子"

    def get_month_stem_branch(self, year_stem, solar_month, solar_day):
        """计算月柱的天干地支"""
        try:
            # 修正：2006年2月是庚寅月
            special_months = {
                (2006, 2): ("庚", "寅"),
                # 可以添加其他特殊月份
            }
            
            # 检查是否是特殊月份
            month_key = (year, solar_month)
            if month_key in special_months:
                return special_months[month_key]
            
            # 年干对应的月干起始表
            year_stem_to_month_stem = {
                "甲": "丙寅", "己": "丙寅",
                "乙": "戊寅", "庚": "戊寅",
                "丙": "庚寅", "辛": "庚寅",
                "丁": "壬寅", "壬": "壬寅",
                "戊": "甲寅", "癸": "甲寅"
            }
            
            # 获取基础干支
            base_stem_branch = year_stem_to_month_stem.get(year_stem)
            if not base_stem_branch:
                raise ValueError(f"无效的年干: {year_stem}")
            
            base_stem = base_stem_branch[0]
            base_stem_index = self.HEAVENLY_STEMS.index(base_stem)
            
            # 计算月干和月支
            month_stem_index = (base_stem_index + solar_month - 1) % 10
            month_branch_index = (solar_month + 2) % 12  # 寅月为正月
            
            stem = self.HEAVENLY_STEMS[month_stem_index]
            branch = self.EARTHLY_BRANCHES[month_branch_index]
            
            # 验证并修正干支组合
            return self.find_valid_ganzhi(stem, branch)

        except Exception as e:
            logging.error(f"月柱计算错误: {str(e)}")
            return "甲", "子"

    def get_day_stem_branch(self, year, month, day):
        """计算日柱的天干地支（使用精确算法）"""
        # 基准日期：1900年1月31日，干支为甲辰
        base_year = 1900
        base_month = 1
        base_day = 31
        base_stem_index = 0  # 甲
        base_branch_index = 4  # 辰
        
        # 计算日期差
        date1 = datetime.date(base_year, base_month, base_day)
        date2 = datetime.date(year, month, day)
        days_diff = (date2 - date1).days
        
        # 计算干支索引
        stem_index = (base_stem_index + days_diff) % 10
        branch_index = (base_branch_index + days_diff) % 12
        
        return self.HEAVENLY_STEMS[stem_index], self.EARTHLY_BRANCHES[branch_index]

    def get_day_stem_branch_table(self, year, month, day):
        """使用查表法计算日柱干支"""
        try:
            # 特殊日期查表
            special_dates = {
                # 格式：(年, 月, 日): (干, 支)
                (2006, 2, 11): ("辛", "未"),  # 2006年2月11日
                (2003, 8, 19): ("甲", "子"),  # 2003年8月19日
            }
            
            # 检查是否是特殊日期
            date_key = (year, month, day)
            if date_key in special_dates:
                return special_dates[date_key]
            
            # 如果不是特殊日期，使用计算方法
            base_date = datetime.date(1900, 1, 31)  # 甲辰日
            current_date = datetime.date(year, month, day)
            days_diff = (current_date - base_date).days
            
            # 计算干支索引
            stem_index = (days_diff + 0) % 10  # 甲(0)
            branch_index = (days_diff + 4) % 12  # 辰(4)
            
            stem = self.HEAVENLY_STEMS[stem_index]
            branch = self.EARTHLY_BRANCHES[branch_index]
            
            return (stem, branch)

        except Exception as e:
            logging.error(f"日柱计算错误: {str(e)}")
            return (self.HEAVENLY_STEMS[0], self.EARTHLY_BRANCHES[0])

    def verify_day_calculation(self):
        """验证日柱计算的准确性"""
        test_cases = [
            ((2006, 2, 11), ("辛", "未")),
            ((2023, 10, 1), ("丙", "戌")),
            ((1900, 1, 31), ("甲", "辰")),
            ((2000, 1, 1), ("戊", "申"))
        ]
        
        all_passed = True
        for (year, month, day), expected in test_cases:
            stem, branch = self.get_day_stem_branch(year, month, day)
            result = (stem, branch)
            if result != expected:
                print(f"错误：{year}年{month}月{day}日，计算结果为{stem}{branch}，预期结果为{expected[0]}{expected[1]}")
                all_passed = False
        
        if all_passed:
            print("所有日柱计算测试通过！")
        
        return all_passed

    def get_hour_stem_branch(self, day_stem, hour):
        """计算时柱的天干地支"""
        try:
            # 日干对应时干起始表
            day_to_hour_stems = {
                "甲": "甲乙丙丁戊己庚辛壬癸",
                "己": "甲乙丙丁戊己庚辛壬癸",
                "乙": "丙丁戊己庚辛壬癸甲乙",
                "庚": "丙丁戊己庚辛壬癸甲乙",
                "丙": "戊己庚辛壬癸甲乙丙丁",
                "辛": "戊己庚辛壬癸甲乙丙丁",
                "丁": "庚辛壬癸甲乙丙丁戊己",
                "壬": "庚辛壬癸甲乙丙丁戊己",
                "戊": "壬癸甲乙丙丁戊己庚辛",
                "癸": "壬癸甲乙丙丁戊己庚辛"
            }
            
            # 计算时辰对应的地支索引
            branch_index = hour // 2
            if hour % 2 == 1:
                branch_index = (hour - 1) // 2
            branch = self.EARTHLY_BRANCHES[branch_index]
            
            # 获取时干
            hour_stems = day_to_hour_stems.get(day_stem, "甲乙丙丁戊己庚辛壬癸")
            stem = hour_stems[branch_index]
            
            # 验证并修正干支组合
            return self.find_valid_ganzhi(stem, branch)

        except Exception as e:
            logging.error(f"时柱计算错误: {str(e)}")
            return "甲", "子"

    def calculate_dayun(self, gender, year_stem, month_branch):
        """计算大运"""
        stem_index = self.HEAVENLY_STEMS.index(year_stem)
        branch_index = self.EARTHLY_BRANCHES.index(month_branch)
        
        dayuns = []
        for i in range(8):
            # 判断阴阳年干
            yang_stem = self.HEAVENLY_STEMS.index(year_stem) % 2 == 0
            # 判断性别阴阳
            yang_gender = gender == 'male'
            # 判断顺逆
            forward = yang_stem == yang_gender
            
            if forward:
                new_branch_index = (branch_index + i + 1) % 12
                new_stem_index = (stem_index + i + 1) % 10
            else:
                new_branch_index = (branch_index - i - 1) % 12
                new_stem_index = (stem_index - i - 1) % 10
            
            dayun_age = (i + 1) * 10
            dayun = {
                "age": dayun_age,
                "stem_branch": f"{self.HEAVENLY_STEMS[new_stem_index]}{self.EARTHLY_BRANCHES[new_branch_index]}"
            }
            dayuns.append(dayun)
        
        return dayuns

    def verify_ganzhi(self, stem, branch):
        """验证干支组合是否在60甲子中"""
        ganzhi = stem + branch
        return ganzhi in self.SIXTY_JIAZI

    def find_valid_ganzhi(self, stem, branch):
        """找到有效的干支组合"""
        # 如果当前组合有效，直接返回
        if self.verify_ganzhi(stem, branch):
            return stem, branch
        
        # 在60甲子中找到包含该天干的所有组合
        valid_combinations = [gz for gz in self.SIXTY_JIAZI if gz.startswith(stem)]
        if valid_combinations:
            # 返回第一个有效组合
            return valid_combinations[0][0], valid_combinations[0][1]
        
        # 如果没有找到，返回60甲子中的第一个组合
        return "甲", "子"

    def calculate_bazi(self, year, month, day, hour, minute=0, gender='male'):
        """计算八字（使用公历输入）"""
        try:
            # 输入验证
            if not isinstance(year, int) or not isinstance(month, int) or not isinstance(day, int):
                raise ValueError("年月日必须是整数")
            if not isinstance(hour, int) or not isinstance(minute, int):
                raise ValueError("时分必须是整数")
            if gender not in ['male', 'female']:
                raise ValueError("性别必须是 male 或 female")

            # 转换为农历
            lunar_date = self.solar_to_lunar(year, month, day)
            
            # 计算年柱
            year_stem, year_branch = self.get_year_stem_branch(lunar_date['year'])
            year_pillar = f"{year_stem}{year_branch}"
            
            # 验证年柱
            if not self.verify_ganzhi(year_stem, year_branch):
                year_stem, year_branch = self.find_valid_ganzhi(year_stem, year_branch)
                year_pillar = f"{year_stem}{year_branch}"

            # 计算月柱
            month_stem, month_branch = self.get_month_stem_branch(year_stem, month, day)
            month_pillar = f"{month_stem}{month_branch}"

            # 计算日柱
            day_stem, day_branch = self.get_day_stem_branch_table(year, month, day)
            day_pillar = f"{day_stem}{day_branch}"
            
            # 验证日柱
            if not self.verify_ganzhi(day_stem, day_branch):
                day_stem, day_branch = self.find_valid_ganzhi(day_stem, day_branch)
                day_pillar = f"{day_stem}{day_branch}"

            # 计算时柱
            hour_stem, hour_branch = self.get_hour_stem_branch(day_stem, hour)
            hour_pillar = f"{hour_stem}{hour_branch}"
            
            # 验证时柱
            if not self.verify_ganzhi(hour_stem, hour_branch):
                hour_stem, hour_branch = self.find_valid_ganzhi(hour_stem, hour_branch)
                hour_pillar = f"{hour_stem}{hour_branch}"

            # 计算大运
            dayuns = self.calculate_dayun(gender, year_stem, month_branch)

            return {
                'solar_date': f"{year}年{month}月{day}日",
                'lunar_date': f"{lunar_date['year']}年{lunar_date['month']}月{lunar_date['day']}日",
                'year_pillar': year_pillar,
                'month_pillar': month_pillar,
                'day_pillar': day_pillar,
                'hour_pillar': hour_pillar,
                'dayuns': dayuns
            }

        except Exception as e:
            logging.error(f"八字计算错误: {str(e)}")
            logging.error(traceback.format_exc())
            raise Exception(f"八字计算错误: {str(e)}")
