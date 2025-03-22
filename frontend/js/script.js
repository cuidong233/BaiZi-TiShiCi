document.getElementById('baziForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // 获取表单数据
    const name = document.getElementById('name').value;
    const gender = document.querySelector('input[name="gender"]:checked').value;
    const birthDate = document.getElementById('birthDate').value;
    const birthTime = document.getElementById('birthTime').value;
    
    // 解析日期和时间
    const [year, month, day] = birthDate.split('-');
    const [hour, minute] = birthTime.split(':');
    
    // 构建请求数据
    const data = {
        name: name,
        gender: gender,
        year: parseInt(year),
        month: parseInt(month),
        day: parseInt(day),
        hour: parseInt(hour),
        minute: parseInt(minute)
    };
    
    try {
        // 发送请求到后端
        const response = await fetch('https://your-backend-url/calculate_bazi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        // 显示结果
        displayResult(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('计算失败，请稍后重试');
    }
});

function displayResult(result) {
    // 显示结果容器
    document.getElementById('result').style.display = 'block';
    
    // 更新结果内容
    document.getElementById('resultName').textContent = result.name;
    document.getElementById('resultGender').textContent = result.gender === 'male' ? '男' : '女';
    document.getElementById('resultSolar').textContent = result.solar_date;
    document.getElementById('resultLunar').textContent = result.lunar_date;
    
    // 显示八字
    const baziText = `${result.year_pillar}年 ${result.month_pillar}月 ${result.day_pillar}日 ${result.hour_pillar}时`;
    document.getElementById('resultBazi').textContent = baziText;
    
    // 显示大运
    const dayunList = document.getElementById('dayunList');
    dayunList.innerHTML = '';
    result.dayuns.forEach(dayun => {
        const div = document.createElement('div');
        div.className = 'dayun-item';
        div.textContent = `${dayun.age}岁: ${dayun.stem_branch}`;
        dayunList.appendChild(div);
    });
    
    // 更新复制文本
    const copyText = `姓名：${result.name}
性别：${result.gender === 'male' ? '男' : '女'}
阳历：${result.solar_date}
农历：${result.lunar_date}
八字：${baziText}

大运：
${result.dayuns.map(dayun => `${dayun.age}岁: ${dayun.stem_branch}`).join('\n')}`;
    
    document.getElementById('hiddenCopyText').value = copyText;
}

async function copyText() {
    const textArea = document.getElementById('hiddenCopyText');
    try {
        await navigator.clipboard.writeText(textArea.value);
        alert('复制成功！');
    } catch (err) {
        console.error('复制失败:', err);
        alert('复制失败，请手动复制');
    }
} 