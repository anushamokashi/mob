/*------------------------------------------------------------------------------
  Function for Add Role modal in roleindex.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#addRoleModal',function(e) {
    debugger;
    var url = '/rolesetup/rolesave/';
    var model = null;
    $("#roleModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#roleModalBody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#roleModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#roleModalBody').modal('hide');
        $(this).data('modal', null);
        $("#roleModalBody").html("");
    });
});

/*-----------------------------------------------------------------------------
  Function for Add Role in roleindex.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#addRole',function(e) {
    debugger;
   
  
    var formdata = $("#roleform").serialize();

    $.ajax({
        type: 'POST',
        url: "/rolesetup/rolesave/",
        data: formdata,          
        success: function(data) {
            debugger;
            if (data == "Failure"){
                console.log(data)
                $("#divErrorRole").empty();
                $("#divErrorRole").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Role already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorRole").slideUp(500);
                });

            }
 
            else if(data == "Success"){
                debugger;
                $("#divResultRole").empty();

                $("#divResultRole").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultRole").slideUp(500);
                });
                window.location.reload();
            }
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorRole").empty();
            $("#divErrorRole").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorRole").slideUp(500);
            });
        }
    });
    e.preventDefault(); 
    
});


/*------------------------------------------------------------------------------
  Function for Edit Role modal in roleindex.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#role_Edit_button',function(e) {
    debugger;
    var roleid = e.currentTarget.attributes['data-roleid'].value;
    var url = '/rolesetup/roleedit/'+roleid;
    var model = null;
    $("#roleEditModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#roleEditModalBody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#roleEditModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#roleEditModalBody').modal('hide');
        $(this).data('modal', null);
        $("#roleEditModalBody").html("");
    });
});


/*-----------------------------------------------------------------------------
  Function for Edit Role in roleindex.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#EditRole',function(e) {
    debugger;
   
    var roleid = e.currentTarget.attributes['data-roleid'].value;
    var formdata = $("#roleeditform").serialize();

    $.ajax({
        type: 'POST',
        url: "/rolesetup/roleedit/"+roleid,
        data: formdata,          
        success: function(data) {
            debugger;
            if (data == "Failure"){
                console.log(data)
                $("#divErrorRoleEdit").empty();
                $("#divErrorRoleEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Role already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorRoleEdit").slideUp(500);
                });

            }
 
            else if(data == "Success"){
                debugger;
                $("#divResultRoleEdit").empty();

                $("#divResultRoleEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultRoleEdit").slideUp(500);
                });
                window.location.reload();
            }
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorRoleEdit").empty();
            $("#divErrorRoleEdit").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorRoleEdit").slideUp(500);
            });
        }
    });
    e.preventDefault(); 
    
});

/*------------------------------------------------------------------------------
  Function for Assign View modal in roleindex.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#role_conf_button',function(e) {
    debugger;
    var roleid = e.currentTarget.attributes['data-roleid'].value;
    var url = '/rolesetup/assignview/'+roleid;
    var model = null;
    $("#roleConfModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#roleConfModalBody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#roleConfModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#roleConfModalBody').modal('hide');
        $(this).data('modal', null);
        $("#roleConfModalBody").html("");
    });
});

/*-----------------------------------------------------------------------------
  Function for Edit Role in roleindex.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#saveViewSetup',function(e) {
    debugger;
   
   
    // var txViewSelectedValues = $("#txview").val();
    // var reportViewSelectedValues = $("#reportview").val();
    // var dataJson = {
    //     'txview' : txViewSelectedValues,
    //     'reportview' : reportViewSelectedValues,
    // }
    var roleid = $("#role").val();
    

    var formdata = $("#ViewForRoleForm").serialize();

    $.ajax({
        type: 'POST',
        url: "/rolesetup/assignview/"+roleid,
        data: formdata,          
        success: function(data) {
            debugger;
            if (data == "Failure"){
                console.log(data)
                $("#divErrorRoleConf").empty();
                $("#divErrorRoleConf").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Role already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorRoleConf").slideUp(500);
                });

            }
 
            else if(data == "Success"){
                debugger;
                $("#divResultRoleConf").empty();

                $("#divResultRoleConf").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultRoleConf").slideUp(500);
                });
                window.location.reload();
            }
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorRoleConf").empty();
            $("#divErrorRoleConf").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorRoleConf").slideUp(500);
            });
        }
    });
    e.preventDefault(); 
    
});





