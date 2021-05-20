from Scriptses.DataBase import getListenerList


def getListOfList(db):
    camers = getListenerList(db)
    str_html = """<div class="clist" id="List_Listeners" style="display:none">"""
    if camers==[] :
        str_html += """Нет слушателей"""
    else :
        for row in camers:
            str_html += """
                <p class="one_cam_List">
                    <input type='button' class="mb" value='""" + row["IP_address"] + """ : """ + row["Port"].__str__() + """' onclick="dontClick('""" + row["IP_address"] + """', '""" + row["Port"].__str__() + """')"/>
                    <a class="a" href='/CID_List?Edit=""" + str(row["ID"]) + """'>&#9998</a>
                    <a class="a" href='/CID_List?Delete=""" + str(row["ID"]) + """'>&#10006</a>
                </p>
            """

    str_html += """<p class="one_cam_List">
						<input type='button' class="mbp" value='новый слушатель' onclick="window.location.href='/CID_List?Create=Создать'"/>
					</p></div>"""
    return str_html