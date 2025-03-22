from flask import Flask, request, jsonify
from flask_cors import CORS
from bazi import get_bazi

app = Flask(__name__)
CORS(app)

@app.route('/api/calculate_bazi', methods=['POST'])
@app.route('/calculate_bazi', methods=['POST'])  # 添加一个不带api前缀的路由
def calculate_bazi():
    try:
        # 获取请求数据
        data = request.get_json()
        print("收到请求数据:", data)  # 调试日志
        
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
        if not (1 <= day <= 31):
            return jsonify({'error': '日期必须在1-31之间'}), 400
        if not (0 <= hour <= 23):
            return jsonify({'error': '小时必须在0-23之间'}), 400
        if not (0 <= minute <= 59):
            return jsonify({'error': '分钟必须在0-59之间'}), 400
        if gender not in ['male', 'female']:
            return jsonify({'error': '性别必须是male或female'}), 400
        
        # 计算八字
        result = get_bazi(year, month, day, hour, minute, gender)
        print("计算结果:", result)  # 调试日志
        
        if result is None:
            return jsonify({'error': '计算失败'}), 500
            
        # 添加姓名
        result['name'] = name
        
        return jsonify(result)
        
    except Exception as e:
        print(f"计算八字时出错: {str(e)}")  # 调试日志
        return jsonify({'error': '服务器内部错误'}), 500

@app.route('/')
def index():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True) 