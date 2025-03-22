from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import traceback
from bazi import get_bazi, get_dayun, get_lunar_date

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """返回主页"""
    return render_template('index.html')

@app.route('/calculate_bazi', methods=['POST'])
def calculate_bazi():
    """计算八字接口"""
    try:
        # 获取请求数据
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['year', 'month', 'day', 'hour', 'minute', 'gender', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 转换数据类型
        try:
            year = int(data['year'])
            month = int(data['month'])
            day = int(data['day'])
            hour = int(data['hour'])
            minute = int(data['minute'])
            gender = data['gender']
            name = data['name']
        except ValueError:
            return jsonify({'error': '日期时间格式不正确'}), 400
        
        # 验证数值范围
        if not (1900 <= year <= 2100):
            return jsonify({'error': '年份必须在1900-2100之间'}), 400
        if not (1 <= month <= 12):
            return jsonify({'error': '月份必须在1-12之间'}), 400
        if not (1 <= day <= 31):  # 这里可以添加更严格的日期验证
            return jsonify({'error': '日期必须在1-31之间'}), 400
        if not (0 <= hour <= 23):
            return jsonify({'error': '小时必须在0-23之间'}), 400
        if not (0 <= minute <= 59):
            return jsonify({'error': '分钟必须在0-59之间'}), 400
        if gender not in ['male', 'female']:
            return jsonify({'error': '性别必须是male或female'}), 400
        
        # 计算八字
        result = get_bazi(year, month, day, hour, minute, gender)
        if result is None:
            return jsonify({'error': '计算失败'}), 500
            
        # 添加姓名
        result['name'] = name
        
        return jsonify(result)
        
    except Exception as e:
        print(f"计算八字时出错: {str(e)}")
        return jsonify({'error': '服务器内部错误'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # 设置调试模式
    app.config['DEBUG'] = True
    
    # 启动服务器
    app.run(host='0.0.0.0', port=5000)