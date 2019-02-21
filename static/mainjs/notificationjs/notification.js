/*------------------------------------------------------------------------------
* function for notification Edit Modal 
*----------------------------------------------------------------------------*/  

function notificationEdit(event) {
    debugger;
    console.log(event);
    notificationid = event.currentTarget.dataset['notificationid'];
    var model = null;
    notificationedit = '/notification/notificationEdit/' + notificationid;
   $("#notificationEditModal").on("show.bs.modal", function() {
       
       setTimeout(function() {
       if (model == null) {
        model = $.ajax(notificationedit)
           .done(function(data) {

               $("#notificationEditModalBody").html(data);
           })
           .fail(function() {
               alert("error");
           });
       }
       },500);
   });

   $('#notificationEditModal').on('hidden.bs.modal', function () {
          $("#notificationEditModalBody").modal('hide');
           $(this).data('modal', null);
          $("#notificationEditModalBody").html("");
          });
 }; 

/*------------------------------------------------------------------------------
* function for notification Update
*----------------------------------------------------------------------------*/  

function notificationUpdate(event) {
    debugger;
    console.log(event);
    notificationid = event.currentTarget.dataset['notificationid'];
    var formdata = $("#notificationEditForm").serialize();
    
        $.ajax({
            type: 'POST',
            url: "/notification/notificationEdit/"+notificationid,
            data: formdata,          
            success: function(data) {
                debugger;
                if (data == "Error1"){
                    console.log(data)
                    $("#divErrorNotitifcationEdit").empty();
                    $("#divErrorNotitifcationEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Notification Name already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorNotitifcationEdit").slideUp(500);
                    });
    
                }

                else if (data == "Error2"){
                    console.log(data)
                    $("#divErrorNotitifcationEdit").empty();
                    $("#divErrorNotitifcationEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorNotitifcationEdit").slideUp(500);
                    });
    
                }
     
                else if(data == "Success"){
                    debugger;
                    $("#divResultNotitifcationEdit").empty();
    
                    $("#divResultNotitifcationEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                        $("#divResultNotitifcationEdit").slideUp(500);
                    });
                    window.location.reload();
                }
                
            },
            failure: function(data) {
                debugger;
                console.log(data)
                $(saveclose).click();
                $("#divErrorNotitifcationEdit").empty();
                $("#divErrorNotitifcationEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorNotitifcationEdit").slideUp(500);
                });
            }
        });
        event.preventDefault(); 
        
   
};


/*------------------------------------------------------------------------------
* Function For Stage Add Modal 
*----------------------------------------------------------------------------*/
 
function stageAddModal(event) {

    debugger;
    console.log(event);
    notificationid = event.currentTarget.dataset['notificationid'];
    var model = null;
    modalURL = '/notification/addstage/' + notificationid;
   $("#stageAddModal").on("show.bs.modal", function() {
       
       setTimeout(function() {
       if (model == null) {
        model = $.ajax(modalURL)
           .done(function(data) {

               $("#stageAddModalBody").html(data);
           })
           .fail(function() {
               alert("error");
           });
       }
       },500);
   });

   $('#stageAddModal').on('hidden.bs.modal', function () {
          $("#stageAddModalBody").modal('hide');
           $(this).data('modal', null);
          $("#stageAddModalBody").html("");
          });

};

/*------------------------------------------------------------------------------
* Function For Stage Save 
*----------------------------------------------------------------------------*/


function stageSave(event){
    debugger;
    var notificationid = event.currentTarget.dataset['notificationid'];
    var url ="";
    url = "/notification/savestage/" + notificationid;    
    var formdata = $("#stageadd").serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: formdata,
        //dataType: 'json',                 
        success: function(data){
            debugger;
            if (data == "Stage"){
                console.log(data)
                $("#StageError").empty();
                $("#StageError").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. STAGE NAME already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#StageError").slideUp(500);
                });

            }
            else if (data == "Button1"){
                console.log(data)
                $("#StageError").empty();
                $("#StageError").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.BUTTON NAME already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#StageError").slideUp(500);
                });

            }

            else if (data == "Button2"){
                console.log(data)
                $("#StageError").empty();
                $("#StageError").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.Give Button Name.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#StageError").slideUp(500);
                });

            }
 
            else if(data == "Success"){
                debugger;
                $("#StageResult").empty();

                $("#StageResult").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#StageResult").slideUp(500);
                });
                window.location.reload();
            }
                        
        },
        error: function(data) {
            debugger;
            console.log(data);
            $("#MapError").empty();
            $("#MapError").fadeTo(2000, 500).append("<h4>Alert!</h4>Form Error. ").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#MapError").slideUp(2000);
            });
            
        }
    });
    console.log(formdata);
   

};


/*------------------------------------------------------------------------------
* Function For Stage Edit Modal 
*----------------------------------------------------------------------------*/
 
function stageEditModal(event) {

    debugger;
    console.log(event);
    notificationstageid = event.currentTarget.dataset['notificationstageid'];
    var model = null;
    modalURL = '/notification/updatestage/' + notificationstageid;
   $("#stageEditModal").on("show.bs.modal", function() {
       
       setTimeout(function() {
       if (model == null) {
        model = $.ajax(modalURL)
           .done(function(data) {

               $("#stageEditModalBody").html(data);
           })
           .fail(function() {
               alert("error");
           });
       }
       },500);
   });

   $('#stageEditModal').on('hidden.bs.modal', function () {
          $("#stageEditModalBody").modal('hide');
           $(this).data('modal', null);
          $("#stageEditModalBody").html("");
          });

};

/*------------------------------------------------------------------------------
* Function For Stage Update
*----------------------------------------------------------------------------*/


function stageUpdate(event){
    debugger;
    var notificationstageid = document.getElementById("notificationstageid").value;
    var url ="";
    url = "/notification/updatestage/" + notificationstageid;
    var formdata = $("#stageadd").serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: formdata,
        //dataType: 'json',                 
        success: function(data){
            debugger;
            if (data == "Stage"){
                console.log(data)
                $("#StageEditError").empty();
                $("#StageEditError").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. STAGE NAME already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#StageEditError").slideUp(500);
                });

            }
            else if (data == "Button1"){
                console.log(data)
                $("#StageEditError").empty();
                $("#StageEditError").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.BUTTON NAME already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#StageEditError").slideUp(500);
                });

            }

            else if (data == "Button2"){
                console.log(data)
                $("#StageEditError").empty();
                $("#StageEditError").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed.Give Button Name.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#StageEditError").slideUp(500);
                });

            }
 
            else if(data == "Success"){
                debugger;
                $("#StageEditResult").empty();

                $("#StageEditResult").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#StageEditResult").slideUp(500);
                });
                window.location.reload();
            }
                        
        },
        error: function(data) {
            debugger;
            console.log(data);
            $("#StageEditError").empty();
            $("#StageEditError").fadeTo(2000, 500).append("<h4>Alert!</h4>Form Error. ").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#StageEditError").slideUp(2000);
            });
            
        }
    });
    console.log(formdata);
   

};


/*----------------------------------------------------------------------------
* Function For Onchange of Status Process Type
*----------------------------------------------------------------------------*/


$("#id_status_process_type").change(function() {

    debugger;
    var processType = $(this).val();
    var notificationId = document.getElementById("notification").value
    var url = "/notification/processType/";
    $.ajax({
        type: 'GET',
        url: url,
        //dataType: 'json',
        data : {
            'ProcessType':processType,
            'notificationId' : notificationId,
        },
        success: function(data) { 
            debugger;
            if(data=="None"){
                var select = document.getElementById("id_status_process");
                select.options.length = 0;

            }
            else{
                console.log(data);
                var components = $.parseJSON(data);
                var select = document.getElementById("id_status_process"); 
                select.options.length = 0;
                var option = document.createElement("option");
                option.text = "----------";
                option.value = "";
                option.dataset['type'] = "";
                select.appendChild(option);
                
                if(components.type == "Message"){
                    var choicesArray = [];
                    // var txArray = JSON.parse(components.txview);
                    // var reportArray = JSON.parse(components.report);
                    // var buttonArray = JSON.parse(components.buttons);
                    choicesArray = JSON.parse(components.txview).concat(JSON.parse(components.report)).concat(JSON.parse(components.buttons))

                    for(var k=0;k<choicesArray.length;k++){
                        var option = document.createElement("option");
                        option.text = choicesArray[k]['title'];
                        option.value = choicesArray[k]['value'];
                        option.dataset['type'] = choicesArray[k]['type'];
                        select.appendChild(option);
                    }

                }
                
                else{
                    for(var k=0;k<components.length;k++){
                        //traget_Field.append("<option value=" + components[k]['id'] + ">" + components[k]['identifiers'] + "</option>");
                        var option = document.createElement("option");
                        option.text = components[k]['title'];
                        option.value = components[k]['value'];
                        option.dataset['type'] = components[k]['type'];
                        select.appendChild(option);
                    }

                }

            }
            
        },
        error: function(data) {

        }
    });


});


/*----------------------------------------------------------------------------
* Function For Onchange of Status Process
*----------------------------------------------------------------------------*/

$("#id_status_process").change(function() {
    debugger;
    var txviewid = $(this).val();
    var txviewArray = txviewid.split('-')
    //var ele = document.getElementsByName("status_process");
    // var type = ele[0].selectedOptions[0].dataset.type
    var type = txviewArray[1];
    document.getElementById("choosed_status_process").value =  txviewArray[1];
   
    if(type == "Transaction" ){

        var url = "/notification/gettxviewfield/"+txviewArray[0];
        $.ajax({
            type: 'GET',
            url: url,
            //dataType: 'json',
            success: function(data) { 
                debugger;
                console.log(data);
                var components = $.parseJSON(data);
    
                var FromDateselect = document.getElementById("id_from_date");
                FromDateselect.options.length = 0;
                var option = document.createElement("option");
                option.text = "----------";
                option.value = "";
                FromDateselect.appendChild(option);
                for(var k=0;k<components.length;k++){
                    //traget_Field.append("<option value=" + components[k]['id'] + ">" + components[k]['identifiers'] + "</option>");
                    var option = document.createElement("option");
                    option.text = components[k]['identifiers'];
                    option.value = components[k]['id'];
                    FromDateselect.appendChild(option);
                }

                var ToDateselect = document.getElementById("id_to_date");
                ToDateselect.options.length = 0;
                var option = document.createElement("option");
                option.text = "----------";
                option.value = "";
                ToDateselect.appendChild(option);
                for(var k=0;k<components.length;k++){
                    //traget_Field.append("<option value=" + components[k]['id'] + ">" + components[k]['identifiers'] + "</option>");
                    var option = document.createElement("option");
                    option.text = components[k]['identifiers'];
                    option.value = components[k]['id'];
                    ToDateselect.appendChild(option);
                }

                var ToDateselect = document.getElementById("id_pricelist_field");
                ToDateselect.options.length = 0;
                var option = document.createElement("option");
                option.text = "----------";
                option.value = "";
                ToDateselect.appendChild(option);
                for(var k=0;k<components.length;k++){
                    //traget_Field.append("<option value=" + components[k]['id'] + ">" + components[k]['identifiers'] + "</option>");
                    var option = document.createElement("option");
                    option.text = components[k]['identifiers'];
                    option.value = components[k]['id'];
                    ToDateselect.appendChild(option);
                }
                var ToDateselect = document.getElementById("id_user_field");
                ToDateselect.options.length = 0;
                var option = document.createElement("option");
                option.text = "----------";
                option.value = "";
                ToDateselect.appendChild(option);
                for(var k=0;k<components.length;k++){
                    //traget_Field.append("<option value=" + components[k]['id'] + ">" + components[k]['identifiers'] + "</option>");
                    var option = document.createElement("option");
                    option.text = components[k]['identifiers'];
                    option.value = components[k]['id'];
                    ToDateselect.appendChild(option);
                }
                
            },
            error: function(data) {

            }
        });

    }
    else{

        var FromDateselect = document.getElementById("id_from_date");
        FromDateselect.options.length = 0;
        var ToDateselect = document.getElementById("id_to_date");
        ToDateselect.options.length = 0;
        var ToDateselect = document.getElementById("id_pricelist_field");
        ToDateselect.options.length = 0;
        var ToDateselect = document.getElementById("id_user_field");
        ToDateselect.options.length = 0;

    }
    

});


/*------------------------------------------------------------------------------
* Function For Stage Update
*----------------------------------------------------------------------------*/


function generate_json(event){
    debugger;
   
    $.ajax({
        type : 'get',
        url : '/notification/generateprocess/',      
        success : function (data) {
            popupmessage("JSON Generated Successfully");
            setTimeout(function() {
                window.location.reload();
            },2000);
        },         
        error: function(data) {
            setTimeout(function() {
                popupmessage(data.responseText)

            },500);
        }
    });
    event.preventDefault();

}


/*-----------------------------------------------------------------------------
* Restriction For Notification Name Input
*----------------------------------------------------------------------------*/
// $(document).bind('cut copy paste','#title',function(e){
   
//     e.preventDefault();

// });

// $(document).on('keypress', '#title',function(e) {

// debugger;
// if (e.keyCode == 32 || e.keyCode > 64 && e.keyCode < 91)
//     return false;

// });
/*-----------------------------------------------------------------------------
* Restriction For Stage Name Input
*----------------------------------------------------------------------------*/
// $(document).bind('cut copy paste','#stage_name',function(e){
   
//     e.preventDefault();

// });

// $(document).on('keypress', '#stage_name',function(e) {

// debugger;
// if (e.keyCode == 32 || e.keyCode > 64 && e.keyCode < 91)
//     return false;

// });

/*-----------------------------------------------------------------------------
* Restriction For Action Event Input
*----------------------------------------------------------------------------*/
// $(document).bind('cut copy paste','#action_event',function(e){
   
//     e.preventDefault();

// });

// $(document).on('keypress', '#action_event',function(e) {

// debugger;
// if (e.keyCode == 32 || e.keyCode > 64 && e.keyCode < 91)
//     return false;

// });







