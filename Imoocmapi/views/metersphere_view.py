"""
@version: python 3.6.3
@author: xiaomai
@software: PyCharm
@file: metersphere
@Site:
@time: 2024.05.09
"""
import json

from Imoocmapi.utils.run_plan import start_plan


def run_test_plan(request):
    '''
    :param request:
    :return:
    '''
    if request.is_ajax():
        data = {
            "msg": "开始执行计划"
        }
        request_data = json.loads(request.body.decode('utf-8'))
        plan_name = request_data.get('plan_name')

        run_result = start_plan('https://metersphere.im30.net', 'IOkaSAdC2qZA2gOw', 'd9Dw7OIgZCwywgdb', plan_name)
        data['msg'] = run_result
        return data
