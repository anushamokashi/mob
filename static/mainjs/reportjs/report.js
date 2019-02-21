
/*------------------------------------------------------------------------------
* Function For Epost Update in viewcomponent.html
*----------------------------------------------------------------------------*/
$("#id_epost_target").change(function() {
    var target_txview = $(this).val();
    var url = "/transactionview/eposttarget/"+target_txview;
    $.ajax({
        type: 'GET',
        url: url,
        //dataType: 'json',
        success: function(data) { 
            debugger;
            console.log(data);
            var components = $.parseJSON(data);
            var total_form_set = $("#id_form-TOTAL_FORMS").val();
            for(var index=0;index<total_form_set;index++){
                var target_Selectfield = 'id_form-'+index+'-target_ui_field';
                var traget_Field = $(target_Selectfield);
                var select = document.getElementById(target_Selectfield);
                select.options.length = 0;
                for(var k=0;k<components.length;k++){
                    //traget_Field.append("<option value=" + components[k]['id'] + ">" + components[k]['identifiers'] + "</option>");
                    var option = document.createElement("option");
                    var componentJson = JSON.parse(components[k]['componentrefer_dt']);
                    option.text = components[k]['identifiers'];
                    option.value = components[k]['id'];
                    option.dataset['widget'] = componentJson.component_type
                    select.appendChild(option);
                }
            }
        },
        error: function(data) {

        }
    });
});

/*------------------------------------------------------------------------------
* Function For Epost Update in viewcomponent.html
*----------------------------------------------------------------------------*/

$(document).ready(function(){
    var addrow = $(".add-row");
    addrow[0].onclick = function click(){
        var target_txview = $("#id_epost_target").val();
        if (target_txview){
            var url = "/transactionview/eposttarget/"+target_txview;
            $.ajax({
                type: 'GET',
                url: url,
                //dataType: 'json',
                success: function(data) { 
                    var components = $.parseJSON(data);
                    var total_form_set = $("#id_form-TOTAL_FORMS").val();                 
                    var target_Selectfield =  $("#submitform").find('#id_form-'+(total_form_set-1)+'-target_ui_field');
                    if(target_Selectfield.length>0){
                        target_Selectfield[0].options.length = 0;
                        for(var k=0;k<components.length;k++){
                            var option = document.createElement("option");
                            var componentJson = JSON.parse(components[k]['componentrefer_dt']);
                            option.text = components[k]['identifiers'];
                            option.value = components[k]['id'];
                            option.dataset['widget'] = componentJson.component_type;
                            target_Selectfield[0].appendChild(option);
                        }

                    }
                    
                  
                },
                error: function(data) {

                }
            });
        }
    }
});
