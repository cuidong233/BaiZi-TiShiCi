import argparse
from lunar_python import Lunar, Solar

# 天干 & 地支
Gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
Zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

def get_lunar_date(year, month, day):
    """获取农历日期"""
    solar = Solar.fromYmdHms(year, month, day, 0, 0, 0)
    lunar = solar.getLunar()
    return {
        'year': lunar.getYearInChinese(),
        'month': lunar.getMonthInChinese(),
        'day': lunar.getDayInChinese()
    }

def get_xiaoyun_start_age(year_gan, month_gan, day_gan, hour_gan):
    """计算小运起始年龄"""
    # 新派小运从0岁开始
    return 0

def get_dayun(year_gan, month_gan, month_zhi, is_female):
    """计算大运"""
    # 计算大运
    gan_seq = Gan.index(month_gan)
    zhi_seq = Zhi.index(month_zhi)
    
    # 确定大运方向
    year_gan_yinyang = (Gan.index(year_gan)) % 2  # 年干阴阳
    gender_yinyang = 0 if is_female else 1  # 性别阴阳（女为阴0，男为阳1）
    direction = 1 if (year_gan_yinyang == gender_yinyang) else -1  # 阳男阴女顺排，阴男阳女逆排

    dayuns = []
    for i in range(12):
        gan_seq += direction
        zhi_seq += direction
        dayuns.append(Gan[gan_seq % 10] + Zhi[zhi_seq % 12])

    return dayuns

def get_ganzhi(year, month, day, hour, minute):
    """计算八字干支"""
    try:
        # 获取阳历日期
        solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        lunar = solar.getLunar()
        ba = lunar.getEightChar()
        
        # 返回天干地支对象
        class Ganzhi:
            def __init__(self):
                self.year = ba.getYearGan()
                self.month = ba.getMonthGan()
                self.day = ba.getDayGan()
                self.hour = ba.getTimeGan()
        
        class Zhis:
            def __init__(self):
                self.year = ba.getYearZhi()
                self.month = ba.getMonthZhi()
                self.day = ba.getDayZhi()
                self.hour = ba.getTimeZhi()
        
        return Ganzhi(), Zhis()
    except Exception as e:
        print(f"计算干支时出错: {str(e)}")
        return None, None

def get_bazi(year, month, day, hour, minute, gender):
    """计算八字"""
    try:
        # 获取阳历日期
        solar_date = f"{year}年{month}月{day}日"
        
        # 获取农历日期
        lunar_date = get_lunar_date(year, month, day)
        
        # 计算八字
        gans, zhis = get_ganzhi(year, month, day, hour, minute)
        if gans is None or zhis is None:
            return None
        
        # 计算小运起始年龄
        xiaoyun_start_age = get_xiaoyun_start_age(gans.year, gans.month, gans.day, gans.hour)
        
        # 计算大运
        dayuns = get_dayun(gans.year, gans.month, zhis.month, gender == 'female')
        
        # 构建大运列表
        dayun_list = []
        for i, dayun in enumerate(dayuns, 1):
            age = 6 + (i - 1) * 10  # 从6岁开始，每10年一个大运
            dayun_list.append({
                'age': age,
                'stem_branch': dayun
            })
        
        return {
            'name': '',  # 姓名由前端传入
            'gender': gender,
            'solar_date': solar_date,
            'lunar_date': lunar_date,
            'year_pillar': gans.year + zhis.year,
            'month_pillar': gans.month + zhis.month,
            'day_pillar': gans.day + zhis.day,
            'hour_pillar': gans.hour + zhis.hour,
            'xiaoyun_start_age': xiaoyun_start_age,  # 添加小运起始年龄
            'dayuns': dayun_list
        }
    except Exception as e:
        print(f"计算八字时出错: {str(e)}")
        return None

# 移除命令行参数部分，让文件作为模块使用
