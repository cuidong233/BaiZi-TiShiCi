class GanzhiData:
    """干支数据存储类"""
    
    # 2023年干支数据
    # 格式：(年, 月, 日): (天干索引, 地支索引)
    # 天干索引：0-9 对应 ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
    # 地支索引：0-11 对应 ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    GANZHI_DAYS_2023 = {
        # 10月
        (2023, 10, 1): (2, 10),  # 丙戌
        (2023, 10, 2): (3, 11),  # 丁亥
        (2023, 10, 3): (4, 0),   # 戊子
        (2023, 10, 4): (5, 1),   # 己丑
        (2023, 10, 5): (6, 2),   # 庚寅
        (2023, 10, 6): (7, 3),   # 辛卯
        (2023, 10, 7): (8, 4),   # 壬辰
        (2023, 10, 8): (9, 5),   # 癸巳
        (2023, 10, 9): (0, 6),   # 甲午
        (2023, 10, 10): (1, 7),  # 乙未
        # ... 可以继续添加更多日期
    }

    # 2024年干支数据
    GANZHI_DAYS_2024 = {
        (2024, 1, 1): (8, 2),    # 壬寅
        (2024, 1, 2): (9, 3),    # 癸卯
        # ... 可以继续添加更多日期
    }

    @classmethod
    def get_ganzhi_index(cls, year, month, day):
        """获取指定日期的干支索引"""
        # 根据年份选择对应的数据字典
        if year == 2023:
            data_dict = cls.GANZHI_DAYS_2023
        elif year == 2024:
            data_dict = cls.GANZHI_DAYS_2024
        else:
            raise Exception(f"暂不支持 {year} 年的干支数据")

        # 查找日期对应的干支索引
        date_key = (year, month, day)
        if date_key in data_dict:
            return data_dict[date_key]
        else:
            raise Exception(f"未找到 {year}年{month}月{day}日 的干支数据")

    @classmethod
    def add_ganzhi_data(cls, year, month, day, stem_index, branch_index):
        """添加新的干支数据"""
        if year == 2023:
            cls.GANZHI_DAYS_2023[(year, month, day)] = (stem_index, branch_index)
        elif year == 2024:
            cls.GANZHI_DAYS_2024[(year, month, day)] = (stem_index, branch_index)
        else:
            raise Exception(f"暂不支持添加 {year} 年的干支数据")

    @classmethod
    def batch_update(cls, data_dict):
        """
        批量更新干支数据
        
        Args:
            data_dict: {(year, month, day): (stem_index, branch_index)}
        """
        for (year, month, day), (stem_index, branch_index) in data_dict.items():
            cls.add_ganzhi_data(year, month, day, stem_index, branch_index)

    @classmethod
    def add_year_data(cls, year):
        """
        添加新的年份数据存储
        """
        if not hasattr(cls, f'GANZHI_DAYS_{year}'):
            setattr(cls, f'GANZHI_DAYS_{year}', {}) 