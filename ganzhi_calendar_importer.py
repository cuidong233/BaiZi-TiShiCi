import json
import os

class GanzhiCalendarImporter:
    """干支日历数据导入工具"""
    
    @staticmethod
    def import_calendar_data(calendar_data):
        """
        导入日历数据到GanzhiData格式
        
        Args:
            calendar_data: 外部日历数据
        Returns:
            dict: 转换后的干支数据字典
        """
        converted_data = {}
        
        try:
            # 根据数据格式进行相应的转换
            for date_info in calendar_data:
                # 假设外部数据格式为：
                # {"date": "2023-10-01", "ganzhi": "丙戌"}
                year = int(date_info['date'].split('-')[0])
                month = int(date_info['date'].split('-')[1])
                day = int(date_info['date'].split('-')[2])
                
                # 获取天干地支索引
                gan = date_info['ganzhi'][0]  # 取第一个字（天干）
                zhi = date_info['ganzhi'][1]  # 取第二个字（地支）
                
                # 转换成索引
                gan_index = "甲乙丙丁戊己庚辛壬癸".index(gan)
                zhi_index = "子丑寅卯辰巳午未申酉戌亥".index(zhi)
                
                # 存储转换后的数据
                converted_data[(year, month, day)] = (gan_index, zhi_index)
                
        except Exception as e:
            raise Exception(f"数据转换错误: {str(e)}")
            
        return converted_data

    @staticmethod
    def update_ganzhi_data(converted_data):
        """
        更新GanzhiData类中的数据
        """
        from ganzhi_data import GanzhiData
        
        for (year, month, day), (stem_index, branch_index) in converted_data.items():
            try:
                GanzhiData.add_ganzhi_data(year, month, day, stem_index, branch_index)
            except Exception as e:
                print(f"添加数据失败 {year}-{month}-{day}: {str(e)}")

    @staticmethod
    def load_calendar_file(file_path):
        """
        从文件加载日历数据
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                calendar_data = json.load(f)
            return calendar_data
        except Exception as e:
            raise Exception(f"文件读取错误: {str(e)}")

    @staticmethod
    def import_from_file(file_path):
        """
        从文件导入并更新干支数据
        """
        # 加载文件
        calendar_data = GanzhiCalendarImporter.load_calendar_file(file_path)
        
        # 转换数据
        converted_data = GanzhiCalendarImporter.import_calendar_data(calendar_data)
        
        # 更新GanzhiData
        GanzhiCalendarImporter.update_ganzhi_data(converted_data) 