from ganzhi_calendar_importer import GanzhiCalendarImporter

def update_calendar_data():
    """更新日历数据"""
    try:
        # 假设您的日历数据文件名为 calendar_data.json
        file_path = 'calendar_data.json'
        
        # 导入数据
        GanzhiCalendarImporter.import_from_file(file_path)
        print("日历数据更新成功！")
        
    except Exception as e:
        print(f"更新失败: {str(e)}")

if __name__ == "__main__":
    update_calendar_data() 