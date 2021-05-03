




def getAdmin():
    html_str = """<div id="adminPanel">
        <input type="hidden" id="1bf" value="-" />
        <input type="hidden" id="2bf" value="-" />
        <input type="hidden" id="3bf" value="-" />
        <input type="hidden" id="4bf" value="-" />
        <input type="hidden" id="5bf" value="-" />
		
		<table id="s_tbl">
			<tr id="isHK" class="s_h2">
				<td><h2 id="string_out">Сотрудник : <i>(наблюдение не ведется)</i></h2></td>
				<td width="400px"></td>
				<td width="270px"><h2 id="KS">Критическая ситуация : </h2></td><td width="50px"><img id="light_signal" src="static/light_off.png"/></td>
			</tr>
		</table>
		
        <h1 id="name"></h1>
        <h1 id="ishave"></h1>
        <script src="static/jQuery3.js"></script>
        <script type="text/javascript" src="static/ScriptVideo.js"></script>
    </div>
    """
    return html_str