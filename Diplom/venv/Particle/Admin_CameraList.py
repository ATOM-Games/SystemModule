from Scriptses.DataBase import getCameraList


def getListOfCam(db):
    camers = getCameraList(db)
    str_html = """<div class="clist">"""
    if camers==[] :
        str_html += """not camers"""
    else :
        for row in camers:
            if row['cam_is_running'] == 0 :
                str_html +="""
                    <p class="one_cam_List">
                        <input type='button' class="mb" value='(○) """+row["IP_address"]+""" : """+row["PORT"]+"""' />
                        <a class="a" href='/CID_Cam?Edit="""+str(row["ID"])+"""'>&#9998</a>
                        <a class="a" href='/CID_Cam?Delete="""+str(row["ID"])+"""'>&#10006</a>
                    </p>
                """
            else:
                str_html += """
                    <p class="one_cam_List">
                        <input type='button' class="mb" value='(●) """ + row["IP_address"] + """ : """ + row["PORT"] + """' onclick="createSocket('""" + row["IP_address"] + """', '""" + row["PORT"] + """')" title="online"/>
                        <a class="a" href='/CID_Cam?Edit=""" + str(row["ID"]) + """'>&#9998</a>
                        <a class="a" href='/CID_Cam?Delete=""" + str(row["ID"]) + """'>&#10006</a>
                    </p>
                """

    str_html += """<p class="one_cam_List">
						<input type='button' class="mbp" value='новая камера' onclick="window.location.href='/CID_Cam?Create=Создать'"/>
					</p></div>"""
    return str_html