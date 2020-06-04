// 신청인원 보고서
// 신청내역 나오는 화면에서 콘솔(F12) 열어서 

var data_my_mil;
var finished1 = false;
var finished2 = false;
function call_data(){
    call_data2();
    jQuery('table').fadeTo('fast',0.5);
    finished1 = false;
    jQuery.ajax({
        method : "POST",
        url : "https://ysweb.yonsei.ac.kr/sugang.Ysv?action=getCurri",
        headers : {"submissionid" : "sbm_getWish"},
        data : JSON.stringify({curriInfo:{code:"getWish",srhKey:"",lang:"ko"}}),
        dataType: 'json',
        contentType: "application/json",
        success : function(data){
            summary_all(data,0);
        },
        complete : function(){
            finished1 = true;
            if(finished1 && finished2)
                        jQuery('table').fadeTo('fast',1);
        }
    });
}
function call_data2(){
    jQuery('table').fadeTo('fast',0.5);
    finished2 = false;
    jQuery.ajax({
        method : "POST",
        url : "https://ysweb.yonsei.ac.kr/sugang.Ysv?action=getCurri",
        headers : {"submissionid" : "sbm_getMileage"},
        data : JSON.stringify({curriInfo:{code:"getMileage",srhKey:"",lang:"ko"}}),
        dataType: 'json',
        contentType: "application/json",
        success : function(data){
            summary_all(data,1);
        },
        complete : function(){
            finished2 = true;
            if(finished1 && finished2)
                        jQuery('table').fadeTo('fast',1);
        }
    });
}
function summary_all(data,num){
    var table_jq = jQuery(jQuery('table tbody')[num]);
    if(num == 0)
        table_jq.empty().append('<tr id="dummy"><td colspan="10" style="height:5px;"></td></tr>');
    else
        table_jq.empty();
    for(var index in data.data){
        var is_applied = (typeof data_my_mil[data.data[index].HAKBBSBB] != 'undefined');
        var rate = (data.data[index].WAITCNT/data.data[index].MAX1).toFixed(2);
        var background_color = 'white';
        var txt_color = 'black';
        if(rate >= 2 ){
            background_color = '#D60036';
            txt_color = 'white';
        }else if(rate >= 1.5){
            background_color = '#FFA2B2';
        }else if(rate >= 1){
            background_color = '#FFD03E';
        }else{
            background_color = '#10cd7d';
        }
        var tr_string = '<tr style="background-color:'+background_color+';color:'+txt_color+';" class="grid_body_row">'+
            '<td class="gridBodyDefault">'+data.data[index].KNA+'</td>'+
            '<td class="gridBodyDefault">'+data.data[index].PROF+'</td>'+
            '<td class="gridBodyDefault">'+data.data[index].TIME+'</td>'+
            '<td class="gridBodyDefault">'+(is_applied ? data_my_mil[data.data[index].HAKBBSBB] : '')+'</td>'+
            '<td class="gridBodyDefault"><strong>'+rate+'</strong></td>'+
            '<td class="gridBodyDefault"><strong>'+data.data[index].WAITCNT+'</strong></td>'+
            '<td class="gridBodyDefault">'+data.data[index].MAX1+'</td>'+
            '<td class="gridBodyDefault">'+data.data[index].FIX_HAKYOUN+'</td>'+
            '<td class="gridBodyDefault">'+data.data[index].MAX_MAJOR+'</td>'+
            '<td class="gridBodyDefault">'+data.data[index].WISHCNT+'</td>'+
            '</tr>';
        table_jq.append(tr_string);
        if(is_applied && num==0){
            jQuery('#dummy').before(tr_string);
        }
    }
    if(num == 1)
        table_jq.append('<tr><td colspan="10" style="text-align:center"><input type="button" value="Reload" onclick="javascript:call_data();" style="padding:10px;"/></td></tr>');
}
var trs = jQuery('#gridMileage_body_table tbody tr:not(.w2grid_hidedRow)');
if(typeof data_my_mil == 'undefined'){
    data_my_mil = [];
    for(var index = 0 ; index < trs.length ; index++){
        var this_tr = jQuery(jQuery('#gridMileage_body_table tbody tr:not(.w2grid_hidedRow)')[index]);
        var id = jQuery(this_tr.find('td')[0]).find('span').clone().children().remove().end().text().trim();
        var mil = jQuery(this_tr.find('td')[13]).find('span').clone().children().remove().end().text().trim();
        data_my_mil[id] = mil;
    }
}
jQuery(document.body).html('').append('<table id="gridWish_body_table" class="gridHeaderTableDefault" style="width: 1201px;margin:0 auto;"></table>')
.append('<table id="gridWish_body_table2" class="gridHeaderTableDefault" style="width: 1201px;margin:0 auto;"></table>');
    jQuery('table').append('<thead id="gridWish_head_table" class="gridHeaderTableDefault"><tr><th>과목명</th><th>교수</th><th>시간</th><th>내 마일리지</th><th>경쟁률</th><th>신청인원</th><th>정원</th><th>정원(학년)</th><th>정원(전공)</th><th>희망인원</th></tr></thead>')
    .append('<tbody id="gridWish_body_tbody"></tbody>');
call_data();
