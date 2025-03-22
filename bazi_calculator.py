from ganzhi_data import GanzhiData

class BaziCalculator:
    # 天干
    HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 地支
    EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    
    # 节气时间（公历日期，仅作为示例，实际应该根据年份动态计算）
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

    # 月干对应表（五虎遁）
    MONTH_STEMS = {
        "甲己": "丙丁戊己庚辛壬癸甲乙",
        "乙庚": "戊己庚辛壬癸甲乙丙丁",
        "丙辛": "庚辛壬癸甲乙丙丁戊己",
        "丁壬": "壬癸甲乙丙丁戊己庚辛",
        "戊癸": "甲乙丙丁戊己庚辛壬癸"
    }

    # 修改时辰对应表，更精确的时间划分
    HOUR_BRANCHES = [
        (23, "子", 1),  # 23:00-00:59
        (1, "丑", 3),   # 01:00-02:59
        (3, "寅", 5),   # 03:00-04:59
        (5, "卯", 7),   # 05:00-06:59
        (7, "辰", 9),   # 07:00-08:59
        (9, "巳", 11),  # 09:00-10:59
        (11, "午", 13), # 11:00-12:59
        (13, "未", 15), # 13:00-14:59
        (15, "申", 17), # 15:00-16:59
        (17, "酉", 19), # 17:00-18:59
        (19, "戌", 21), # 19:00-20:59
        (21, "亥", 23)  # 21:00-22:59
    ]

    # 日干对应时干起始表
    DAY_HOUR_STEMS = {
        "甲": {"start": "甲", "order": 1},
        "己": {"start": "甲", "order": 1},
        "乙": {"start": "丙", "order": 1},
        "庚": {"start": "丙", "order": 1},
        "丙": {"start": "戊", "order": 1},
        "辛": {"start": "戊", "order": 1},
        "丁": {"start": "庚", "order": 1},
        "壬": {"start": "庚", "order": 1},
        "戊": {"start": "壬", "order": 1},
        "癸": {"start": "壬", "order": 1}
    }

    @staticmethod
    def get_year_stem_branch(year):
        """计算年柱的天干地支"""
        stem_index = (year - 4) % 10
        branch_index = (year - 4) % 12
        return BaziCalculator.HEAVENLY_STEMS[stem_index], BaziCalculator.EARTHLY_BRANCHES[branch_index]

    @staticmethod
    def get_month_stem_branch(year_stem, month, day):
        """计算月柱的天干地支（考虑节气）"""
        # 获取年干所在组
        for key in BaziCalculator.MONTH_STEMS.keys():
            if year_stem in key:
                month_stems = BaziCalculator.MONTH_STEMS[key]
                break
        
        # 根据节气调整月份
        solar_month = month
        for term, (term_month, term_day) in BaziCalculator.SOLAR_TERMS.items():
            if month == term_month and day >= term_day:
                solar_month = (term_month % 12) + 1
            elif month == ((term_month + 1) % 12):
                if day < BaziCalculator.SOLAR_TERMS[term][1]:
                    solar_month = term_month
        
        # 获取月干和月支
        month_stem = month_stems[(solar_month - 1) % 10]
        month_branch = BaziCalculator.EARTHLY_BRANCHES[(solar_month + 1) % 12]
        
        return month_stem, month_branch

    @staticmethod
    def get_day_stem_branch(year, month, day):
        """计算日柱的天干地支（使用查表法）"""
        try:
            # 从GanzhiData获取干支索引
            stem_index, branch_index = GanzhiData.get_ganzhi_index(year, month, day)
            return BaziCalculator.HEAVENLY_STEMS[stem_index], BaziCalculator.EARTHLY_BRANCHES[branch_index]
        except Exception as e:
            raise Exception(f"干支查询错误: {str(e)}")

    @staticmethod
    def get_hour_stem_branch(day_stem, hour, minute=0):
        """计算时柱的天干地支（考虑具体时间）"""
        # 处理23:00-23:59的特殊情况
        if hour == 23:
            branch = "子"
            next_day = True
        else:
            # 查找对应时辰
            branch = None
            next_day = False
            decimal_hour = hour + minute/60.0
            
            for start_hour, br, end_hour in BaziCalculator.HOUR_BRANCHES:
                if start_hour <= decimal_hour < end_hour:
                    branch = br
                    break
            
            if not branch:
                branch = "子"  # 默认子时

        # 获取日干的时干起始信息
        day_info = BaziCalculator.DAY_HOUR_STEMS[day_stem]
        start_stem = day_info["start"]
        start_index = BaziCalculator.HEAVENLY_STEMS.index(start_stem)
        
        # 计算时干
        branch_index = BaziCalculator.EARTHLY_BRANCHES.index(branch)
        stem_index = (start_index + branch_index) % 10
        
        # 如果是次日子时，需要调整时干
        if next_day:
            stem_index = (stem_index + 1) % 10
            
        stem = BaziCalculator.HEAVENLY_STEMS[stem_index]
        return stem, branch

    @staticmethod
    def calculate_dayun(gender, year_stem, month_branch):
        """计算大运"""
        stem_index = BaziCalculator.HEAVENLY_STEMS.index(year_stem)
        branch_index = BaziCalculator.EARTHLY_BRANCHES.index(month_branch)
        
        dayuns = []
        for i in range(8):
            # 判断阴阳年干
            yang_stem = BaziCalculator.HEAVENLY_STEMS.index(year_stem) % 2 == 0
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
                "stem_branch": f"{BaziCalculator.HEAVENLY_STEMS[new_stem_index]}{BaziCalculator.EARTHLY_BRANCHES[new_branch_index]}"
            }
            dayuns.append(dayun)
        
        return dayuns

def calculate_bazi(year, month, day, hour, minute=0, gender='male'):
    """计算八字"""
    try:
        calc = BaziCalculator()
        
        # 计算年柱
        year_stem, year_branch = calc.get_year_stem_branch(year)
        year_pillar = f"{year_stem}{year_branch}"
        
        # 计算月柱
        month_stem, month_branch = calc.get_month_stem_branch(year_stem, month, day)
        month_pillar = f"{month_stem}{month_branch}"
        
        # 计算日柱
        day_stem, day_branch = calc.get_day_stem_branch(year, month, day)
        day_pillar = f"{day_stem}{day_branch}"
        
        # 计算时柱
        hour_stem, hour_branch = calc.get_hour_stem_branch(day_stem, hour, minute)
        hour_pillar = f"{hour_stem}{hour_branch}"
        
        # 计算大运
        dayuns = calc.calculate_dayun(gender, year_stem, month_branch)
        
        return {
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar,
            "dayuns": dayuns
        }
        
    except Exception as e:
        raise Exception(f"八字计算错误: {str(e)}") 