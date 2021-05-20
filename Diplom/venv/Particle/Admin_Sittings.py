def getSittings():
    str_html = """<div class="clist" id="Sittings" style="display:none">"""
    str_html += """<h3 style="text-align:center">Настройки анализа</h3>
		<p><input id="ch1" type="checkbox"/> Отслеживать присутствие на рабочем месте</p>
		<p><input id="ch2" type="checkbox" checked/> Отслеживать состояние здоровья</p>
		<p><input id="ch3" type="number" min='3' max='30' value="3"/> Длинна временного ряда</p>"""

    str_html += """<p class="one_cam_List">
						<input type='button' class="mbp" value='Принять' onclick="SaveSittings()"/>
					</p></s>"""
    return str_html