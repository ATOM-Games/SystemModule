def getVideoBlock():
    return """
		<div class="brd">
            <img id="video_block"/>
            <input type="button" class="b_hed" value="начать мониторинг" id="imgBut_mn" onclick="start_monitor()" />
        </div></td><td><div class="brd">
            <img id="r_video_block"/>
            <input type="button"  class="b_hed" value="трекинг лица" id="imgBut_tr" onclick="tracking_face()" />
        </div>"""