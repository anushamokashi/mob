$("#id_txview").change(function() {
    debugger;
    var txviewid = $(this).val();
    var idArray = ['id_event_title','id_event_desc','id_event_location','id_event_start_day','id_event_start_time','id_event_end_day','id_event_end_time']
    if(txviewid == ""){
        for(let i=0;i<idArray.length;i++){
            var field = document.getElementById(idArray[i]);
            field.options.length = 0;
        }

    }
    else{
        var url = "/eventconfiguration/getcomponents/"+txviewid;
        $.ajax({
            type: 'GET',
            url: url,
            //dataType: 'json',
            success: function(data) { 
                debugger;
                console.log(data);
                var components = $.parseJSON(data);

                for(let i=0;i<idArray.length;i++){
                    var field = document.getElementById(idArray[i]);
                    field.options.length = 0;
                    var option = document.createElement("option");
                    option.text = "----------";
                    option.value = "";
                    field.appendChild(option);
                    for(var k=0;k<components.length;k++){
                        var option = document.createElement("option");
                        option.text = components[k]['title'];
                        option.value = components[k]['id'];
                        field.appendChild(option);
                    }
                }
            },
            error: function(data) {
                console.log(data);
            }
        });
    }
       
        

});

function saveEvent(event){
    debugger;
    var formdata = $("#eventForm").serialize();
    $.ajax({
        type : 'POST',
        url : "/eventconfiguration/addEvent/",
        data : formdata,
        //dataType: 'json',                 
        success : function (data) {
            if(data == "success"){
                $("#divResultEvent").empty();

                $("#divResultEvent").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultEvent").slideUp(500);
                });
                window.location.reload();
            }
            else if(data == "error"){
                $("#divErrorEvent").empty();
                $("#divErrorEvent").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEvent").slideUp(500);
                });
            }

        },
        error : function (data) {
            $("#divErrorEvent").empty();
            $("#divErrorEvent").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorEvent").slideUp(500);
            });
        }
    });
    // event.preventDefault();
}



