 /*------------------------------------------------------------------------------
  *Function for Edit Table property  in tabledetail.html
  *----------------------------------------------------------------------------*/

function edittable(tabid) {
    $("#propertyDivBody").show();
    $("#fieldProp").hide();
    $("#tabProp").addClass("box box-solid boxcolor").show(); {
        var tablecomp = '/transaction/tabledetailedit/'+tabid;
        var modal = $.ajax(tablecomp)
            .done(function(data) {
                $("#tabPropBody").html(data);
            })
            .fail(function() {
                alert("error");
            });
    }

 };

 /*------------------------------------------------------------------------------
  *Function for Edit Field property  in tabledetail.html
  *----------------------------------------------------------------------------*/

 function editField(fieldId) { 
     debugger;
     console.log(fieldId);
     $("#propertyDivBody").show();
     $("#tabProp").hide();
     $("#fieldProp").addClass("box box-solid boxcolor").show(); {

         var tablecomp = '/transaction/tablecomponentedit/'+fieldId;
         var modal = $.ajax(tablecomp)
             .done(function(data) {
                 $("#fieldPropBody").html(data);
             })
             .fail(function() {
                 alert("error");
             });
     }

 };

/*------------------------------------------------------------------------------
* Function for Add Table in tabledetail.html
*----------------------------------------------------------------------------*/
// $(document).on('click', '#addtable',function(e){
// $("#addtable").click(function(e) {
function addtable(e) { 
    debugger;
    var formdata = $("#tableForm").serialize();
   
    $.ajax({
        type: 'POST',
        url: "/transaction/addtable/",
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            debugger;
            if (data == "slug"){
                console.log(data)
                $("#divError").empty();
                $("#divError").fadeTo(2000, 500).append("<h4>Alert!</h4>Create View First!!!.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divError").slideUp(500);
                });
               

            }
            if (data == "Failure1"){
                console.log(data)
                $("#divError").empty();
                $("#divError").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Table already exist in this name.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divError").slideUp(500);
                });
               

            }
            if (data == "Failure2"){
                console.log(data)
                $("#divError").empty();
                $("#divError").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divError").slideUp(500);
                });
               
            }
            else if(data == "Success"){
                debugger;
                $("#divResult").empty();

                $("#divResult").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResult").slideUp(500);
                });
                window.location.reload();

            }
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divError").empty();
            $("#divError").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divError").slideUp(500);
            });
            
        }
    });
    e.preventDefault(); 
};



 /*------------------------------------------------------------------------------
  * Function for updateTable in tabledetail.html
  *----------------------------------------------------------------------------*/

// $(document).on('click', '#updateTable',function(e){
// $("#updateTable").click(function(e) {
function updateTable(tableeditid) { 
    debugger;
    var formdata = $("#tableEditForm").serialize();
    var tabid = tableeditid
    $.ajax({
        type: 'POST',
        url: "/transaction/tabledetailedit/" + tabid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            debugger;
            if (data == "Failure"){
                console.log(data)
                $("#divErrorMessages").empty();
                $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorMessages").slideUp(500);
                });

            }
            if (data == "Failure1"){
                console.log(data)
                $("#divErrorMessages").empty();
                $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Table Name Exist Already.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorMessages").slideUp(500);
                });

            }
            else{
                debugger;
                $('#tableHeader').html("");
                $('#tableHeader').html(data);
                var datatable = $('#tabHeadcol').dataTable({
                    "ordering": false,
                });
                $('#tabHeadcol').DataTable();
                $("#divResults").empty();

                $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResults").slideUp(500);
                });
               

            }
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
   
};


/*----------------------------------------------------------------------------*
   Function for Add Column in tabledetail.html
*----------------------------------------------------------------------------*/
// $(document).on('click', '#addColumn',function(e){
// $("#addColumn").click(function(e) {
function addColumn(tableid) { 
    debugger;
    var formdata = $("#columnAddForm").serialize();
    var tableid = tableid
   
    $.ajax({
        type: 'POST',
        url: "/transaction/tablecomponent/"+tableid,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            debugger;
            if (data == "Failure1"){
                console.log(data)
                $("#divErrorField").empty();
                $("#divErrorField").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Column already exist in this name.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorField").slideUp(500);
                });

            }
            if (data == "Failure2"){
                console.log(data)
                $("#divErrorField").empty();
                $("#divErrorField").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorField").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultField").empty();

                $("#divResultField").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultField").slideUp(500);
                });
                window.location.reload();

            }
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divError").empty();
            $("#divError").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divError").slideUp(500);
            });
        }
    });
    e.preventDefault();
};

/*------------------------------------------------------------------------------
  * Function for updateField in tabledetail.html
  *----------------------------------------------------------------------------*/


// $("#updateField").click(function(e) {
function updateField(tabCompId){
    debugger;
    var formdata = $("#fieldForm").serialize();
    var fieldId = tabCompId
    $.ajax({
        type: 'POST',
        url: "/transaction/tablecomponentedit/"+fieldId,
        data: formdata,
        //dataType: 'json',                 
        success: function(data) {
            debugger;
            if (data == "Failure"){
                console.log(data)
                $("#divErrorMessages").empty();
                $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorMessages").slideUp(500);
                });

            }
            else if (data == "Exist"){
                console.log(data)
                $("#divErrorMessages").empty();
                $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Column name already exist in this Table.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorMessages").slideUp(500);
                });

            }
            else{
                debugger;
                $('#tableHeader').html("");
                $('#tableHeader').html(data);
                var datatable = $('#tabHeadcol').dataTable({
                    "ordering": false,
                });
                $('#tabHeadcol').DataTable();
                $("#divResults").empty();

                $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResults").slideUp(500);
                });
                

            }
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $("#divErrorMessages").empty();
            $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorMessages").slideUp(500);
            });
        }
    });
    
    
};

/*------------------------------------------------------------------------------
  * Function for removing blank option parent field if parent table exist
  *----------------------------------------------------------------------------*/


// $("#addTable").click(function(e) {
//     debugger;
//     var options = document.getElementById("id_parent").options;
//     if (options.length >1){
//         $("#id_parent option[value='']").remove();
//     }
// });

/*------------------------------------------------------------------------------
  * Function for Schema Generation
  *----------------------------------------------------------------------------*/
function generateschema(event){
// $(document).on('click', '#generateschema',function(event){
    debugger;
   
    txnid = event.currentTarget.dataset['txnid'];
    sample = "aaaa" ;
    $("#processing-modal").modal('show');
    $.ajax({
        type : 'POST',
        url :"/transaction/generateSchema/"+txnid,
        data : {'sample':sample},
        success : function (data) {
            debugger;
            if (data == "SUCCESS"){
                setTimeout(function() {
                    debugger;
                    $("#processing-modal").modal('hide');
                    $('#schemaGenModal').find('#dataConfirmLabel').empty();
                    $('#schemaGenModal').find('.modal-body').empty();
                    $('#schemaGenModal').find('#dataConfirmLabel').append("Information");
                    $('#dataConfirmLabel').css("color","rgb(60, 141, 188)")
                    
                    if (!$('#schemaGenModal').length) {
                        $('body').append('<div id="schemaGenModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="dataConfirmLabel" style="color: rgb(60, 141, 188);">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
                    }
                    
                    $('#schemaGenModal').find('.modal-body').text("Schema Generated Succfully");
                    $('#schemaGenModal').modal({
                        show: true
                    });
                    return false;
                },300);

            }
            else{
                errorArray = JSON.parse(data);
                debugger;
                setTimeout(function() {
                    $("#processing-modal").modal('hide');
                    $('#schemaGenModal').find('#dataConfirmLabel').empty();
                    $('#schemaGenModal').find('#dataConfirmLabel').append("Error");
                    $('#dataConfirmLabel').css("color", "red");
                    
                    if (!$('#schemaGenModal').length) {
                        $('body').append('<div id="schemaGenModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="dataConfirmLabel" style="color: red">Error</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
                    }
                    $('#schemaGenModal').find('.modal-body').empty();
                    for(i=0; i<errorArray.length;i++){
                        $('#schemaGenModal').find('.modal-body').append(errorArray[i]+'<br>')
                    }
                    
                    $('#schemaGenModal').modal({
                        show: true
                    });
                    return false;
                },300);

            }
            
           
         },
         failure : function (data) {
            debugger;
            console.log(data)
         }
      });
   };



/*------------------------------------------------------------------------------
* Add row dynamically
*----------------------------------------------------------------------------*/

$(document).on('click', '#addrow',function(event){
    debugger;
    $("#customEnumKeyValue").find("tbody").find('tr:last').prev().after('<tr class="dynamic-form"><td><input id="key" maxlength="100" name="key" type="text"></td><td><input id="value" maxlength="255" name="value" type="text"></td><td><input type="hidden" name="delete" id="delete"><a class="delete-row" href="javascript:void(0)"><button type="button" id="deleteKV" class="btn btn-danger btn-xs"><i class="fa fa-trash" style="color: white;"></i></button></a></td></tr>');
    
});


/*------------------------------------------------------------------------------
* Add row dynamically In Edit Form
*----------------------------------------------------------------------------*/

$(document).on('click', '#addRowEdit',function(event){
    debugger;
    $("#EditEnumKeyValue").find("tbody").find('tr:last').prev().after('<tr class="dynamic-form"><td><input id="key" maxlength="100" name="key" type="text"></td><td><input id="value" maxlength="255" name="value" type="text"></td><td><input type="hidden" name="delete" id="delete"><a class="delete-row" href="javascript:void(0)"><button type="button" id="deleteKV" class="btn btn-danger btn-xs"><i class="fa fa-trash" style="color: white;"></i></button></a></td></tr>');
    
});


/*------------------------------------------------------------------------------
* Add New Enum
*----------------------------------------------------------------------------*/

$(document).on('click', '#addenum',function(event){  
    debugger;
    var keyValueArray = []
    
    $("tr.dynamic-form").each(function(){
        if ($(this).find("#key").val() != "" && $(this).find("#value").val() != ""){
            keyValueArray.push({key:$(this).find("#key").val(),value:$(this).find("#value").val()})
        }
        
    });
    console.log(keyValueArray);
    
    enumData = {
        'title':$("#enum_title").val(),
        'desc' : $("#description").val(),
        'KV'   : JSON.stringify(keyValueArray)

    };
    
    
    $.ajax({
        type: 'POST',
        url: "/transaction/enumlist/",
        data: enumData,            
        success: function(data) {
            debugger;
            if (data == "Exist"){
                debugger;
                console.log(data)
                $("#divErrorEnum").empty();
                $("#divErrorEnum").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Enum Name already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEnum").slideUp(500);
                });

            }
            if (data == "Failure"){
                debugger;
                console.log(data)
                $("#divErrorEnum").empty();
                $("#divErrorEnum").fadeTo(2000, 500).append("<h4>Alert!</h4>Error while saving.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEnum").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultEnum").empty();

                $("#divResultEnum").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultEnum").slideUp(500);
                });
                
                window.location.href = '/transaction/enumlist/';

            }
            
            
        },
        failure : function (data) {
            console.log("FAILURE")
        }
    });
    event.preventDefault();
    
});


/*------------------------------------------------------------------------------
* Delete Temp Key Value 
*----------------------------------------------------------------------------*/
$(document).on('click', '#deleteKV',function(event){  
    debugger;
    $(this).parent().parent().parent().remove()
});



/*------------------------------------------------------------------------------
*Model Function for Enum Edit 
*----------------------------------------------------------------------------*/
$(document).on('click', '#edit_enum',function(e) {
    debugger;
    var  enumId = e.currentTarget.attributes['data-enumid'].value
    var enumedit = '/transaction/enumedit/' + enumId;
    var model = null;
    $("#enumModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(enumedit)
                .done(function(data) {
                    $("#myEnumModelbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#enumModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#myEnumModelbody').modal('hide');
        $(this).data('modal', null);
        $("#myEnumModelbody").html("");
    });
});

/*-----------------------------------------------------------------------------
* Update Enum 
*----------------------------------------------------------------------------*/

$(document).on('click', '#update_enum',function(e) {
    debugger;
    
    var keyValueArray = [];
    var existingkv  = [];
    // var editEnumForm = $("#enumTitleEditForm").serialize();
    var enumId = e.currentTarget.dataset['enumid'];
    document.getElementsByName("enum_title")[1].value
    
    $("tr.dynamic-form").each(function(){
        if ($(this).find("#key").val() != "" && $(this).find("#value").val() != ""){
            keyValueArray.push({id:$(this).find('input[type=hidden]').val(),key:$(this).find("#key").val(),value:$(this).find("#value").val()})
            
            if ($(this).find('input[type=hidden]').val() != ""){
                existingkv.push($(this).find('input[type=hidden]').val());
            }
        }
        
        
    });
    console.log(keyValueArray);
    enumEditData = {
        'title': document.getElementsByName("enum_title")[1].value,
        'desc' : document.getElementsByName("description")[1].value,
        'KV'   : JSON.stringify(keyValueArray),
        'existingkv' : JSON.stringify(existingkv)

    };
    
    $.ajax({
        type: 'POST',
        url: "/transaction/enumedit/"+enumId,
        data: enumEditData,            
        success: function(data) {
             debugger;
            if (data == "Exist"){
                debugger;
                console.log(data)
                $("#divErrorEnumEdit").empty();
                $("#divErrorEnumEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Enum Name already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEnumEdit").slideUp(500);
                });

            }
            if (data == "Failure"){
                debugger;
                console.log(data)
                $("#divErrorEnumEdit").empty();
                $("#divErrorEnumEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Error while saving.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEnumEdit").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultEnumEdit").empty();

                $("#divResultEnumEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultEnumEdit").slideUp(500);
                });
                
                window.location.href = '/transaction/enumlist/';

            }
            
            
        },
        failure : function (data) {
            console.log("FAILURE")
        }
        
    });
    e.preventDefault();
    

});

/*-----------------------------------------------------------------------------
* Restriction For Table Name Input
*----------------------------------------------------------------------------*/
$(document).bind('cut copy paste','#id_tablename',function(e){
   
        e.preventDefault();
    
});

$(document).on('keypress', '#id_tablename',function(e) {

    debugger;
    if (e.keyCode == 32 || e.keyCode > 64 && e.keyCode < 91)
        return false;

});


/*-----------------------------------------------------------------------------
* Restriction For Column Name Input
*----------------------------------------------------------------------------*/
$(document).bind('cut copy paste','#id_columnname',function(e){
   
        e.preventDefault();
    
});

$(document).on('keypress', '#id_columnname',function(e) {

    debugger;
    if (e.keyCode == 32 || e.keyCode > 64 && e.keyCode < 91)
        return false;

});