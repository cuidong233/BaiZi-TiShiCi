// 性别选择功能
function selectGender(gender, element) {
    // 移除所有性别选项的选中状态
    document.querySelectorAll('.gender-option').forEach(option => {
        option.classList.remove('selected');
    });
    
    // 添加选中状态到当前选项
    element.classList.add('selected');
    
    // 设置radio按钮的值
    document.querySelector(`input[value="${gender}"]`).checked = true;
}

// 生成八字结果函数
async function generateResult() {
    try {
        // 显示加载状态
        const resultContainer = document.getElementById('resultContainer');
        const resultDiv = document.getElementById('result');
        if (resultContainer && resultDiv) {
            resultDiv.innerHTML = '<div class="loading">计算中...</div>';
            resultContainer.style.display = 'block';
            document.getElementById('inputForm').style.display = 'none';
        }

        // 获取输入值
        const name = document.getElementById('name')?.value?.trim();
        const genderElement = document.querySelector('input[name="gender"]:checked');
        const birthDate = document.getElementById('birthDate')?.value;
        const birthTime = document.getElementById('birthTime')?.value;

        // 输入验证
        if (!name) {
            throw new Error('请输入姓名');
        }
        if (!genderElement) {
            throw new Error('请选择性别');
        }
        if (!birthDate) {
            throw new Error('请选择出生日期');
        }
        if (!birthTime) {
            throw new Error('请选择出生时间');
        }

        const gender = genderElement.value;

        // 解析日期和时间
        const [year, month, day] = birthDate.split('-').map(num => parseInt(num, 10));
        const [hour, minute] = birthTime.split(':').map(num => parseInt(num, 10));

        // 准备请求数据
        const requestData = {
            year,
            month,
            day,
            hour,
            minute,
            gender: gender,  // 直接使用 'male' 或 'female'
            name
        };

        // 发送请求
        const API_URL = 'https://baizi-tishilalala.vercel.app/api/calculate_bazi';
        console.log('正在发送请求到:', API_URL);
        console.log('请求数据:', requestData);

        // 发送POST请求
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        // 检查响应状态
        if (!response.ok) {
            const errorData = await response.text();
            console.error('服务器响应错误:', errorData);
            throw new Error(`服务器响应错误: ${response.status}`);
        }

        // 获取响应数据
        const data = await response.json();
        console.log('响应数据:', data);

        // 显示结果
        displayResult(data);

    } catch (error) {
        console.error('计算错误:', error);
        // 显示错误信息
        const resultContainer = document.getElementById('resultContainer');
        const resultDiv = document.getElementById('result');
        if (resultContainer && resultDiv) {
            resultDiv.innerHTML = `
                <div class="error-message">
                    计算失败：${error.message}
                    <br>
                    <small>请检查网络连接或稍后重试</small>
                </div>
                <button onclick="showInputForm()" class="back-button">返回重试</button>
            `;
            resultContainer.style.display = 'block';
            document.getElementById('inputForm').style.display = 'none';
        }
    }
}

function displayResult(data) {
    try {
        // 获取结果容器
        const resultContainer = document.getElementById('resultContainer');
        const resultDiv = document.getElementById('result');
        
        if (!resultContainer || !resultDiv) {
            throw new Error('找不到结果显示区域');
        }

        // 获取性别值
        const genderElement = document.querySelector('input[name="gender"]:checked');
        const gender = genderElement ? genderElement.value : 'male'; // 默认为男性
        const genderText = gender === 'male' ? '男' : '女';

        // 构建AI提示词
        const promptText = `你是一个顶尖的八字及算命大师，熟读穷通宝典、三命通会、滴天髓、渊海子平这些书籍。你熟读千里命稿、协纪辨方书、果老星宗子平真栓、神峰通考，袁天罡称骨，命理奇门等一系列书籍。帮我分析一下这个八字 ${data.year_pillar} ${data.month_pillar} ${data.day_pillar} ${data.hour_pillar} 出生于 ${data.solar_date.split('年')[0]} 大运是 ${data.dayuns.map(dayun => `${dayun.stem_branch}(${dayun.age})`).join(',')} 性别是 ${genderText}，需要严格按照八字命理的理论和步骤进行分析，看看我的八字和大运流年，请测算一下我详细的历史事件用以验证，以及未来规划，请推测一下请推测一下我的外貌(身高体重五官肤色),性格，职业，家乡，目前我的财富水平，婚姻姻缘情况`;

        // 构建结果HTML
        let html = `
            <div class="result-container">
                <h3>AI提示词（通用）</h3>
                <div class="result-item">
                    <textarea class="prompt-text" readonly>${promptText}</textarea>
                </div>
            </div>
        `;

        // 更新结果显示
        resultDiv.innerHTML = html;
        resultContainer.style.display = 'block';
        document.getElementById('inputForm').style.display = 'none';

        // 创建一个隐藏的文本区域用于复制
        const hiddenTextArea = document.createElement('textarea');
        hiddenTextArea.style.display = 'none';
        hiddenTextArea.value = promptText;
        document.body.appendChild(hiddenTextArea);
        hiddenTextArea.id = 'hiddenCopyText';

    } catch (error) {
        console.error('显示结果时出错:', error);
        alert('显示结果时出错: ' + error.message);
    }
}

// 修改复制文本功能
async function copyText() {
    try {
        const hiddenTextArea = document.getElementById('hiddenCopyText');
        if (!hiddenTextArea) {
            throw new Error('找不到复制文本');
        }

        // 使用现代的clipboard API
        await navigator.clipboard.writeText(hiddenTextArea.value);
        alert('复制成功！');
    } catch (error) {
        console.error('复制时出错:', error);
        // 如果clipboard API失败，尝试使用传统方法
        try {
            hiddenTextArea.select();
            document.execCommand('copy');
            alert('复制成功！');
        } catch (fallbackError) {
            console.error('备用复制方法也失败:', fallbackError);
            alert('复制失败，请手动复制文本');
        }
    }
}

// 返回输入表单
function showInputForm() {
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('inputForm').style.display = 'block';
}