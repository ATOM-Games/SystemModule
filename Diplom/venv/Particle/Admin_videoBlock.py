def getVideoBlock():
    return """
		<div class="vidBlock2"></div>
		<div class="brd">
            <img id="video_block" class="vidBlock"/>
            <input type="button" class="b_hed" value="начать мониторинг" id="imgBut_mn" onclick="start_monitor()" />
        </div>
		<div class="vidBlock2"></div>"""
		
		
		#<div class="brd">
        #    <div class="vidBlock">
		#		<h3 style="text-align:center">Настройки анализа</h3>
		#		<p><input id="ch1" type="checkbox" value="Ага"/> Отслеживать присутствие на рабочем месте</p>
		#		<p><input id="ch2" type="checkbox" value="Ага" checked/> Отслеживать состояние здоровья</p>
		#		<p><input id="ch3" type="number" min='3' max='30' value="3"/> Длинна временного ряда</p>
		#	</div>
        #    <input type="button" class="b_hed" value="трекинг лица" id="imgBut_tr" onclick="tracking_face()" />
        #</div>