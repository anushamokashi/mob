/*------------------------------------------------------------------------------
*function for Login Generate Page Button in loginindex.html
*----------------------------------------------------------------------------*/


$(document).on('click', '#createLoginpg',function(event){
      debugger;
      projectid = event.currentTarget.dataset['pid'];
      $("#processing-modal").modal('show');
      var message="";
         $.ajax({
         type : 'get',
         url : '/logintemplate/createLoginpg/'+projectid,
         //data : sample,
         //dataType: 'json',            
         success : function (data) {
         	if (data == "success"){
             message = "Definiton For Login Page Created"
             $("#processing-modal").modal('hide');
              $("#createLoginlb").addClass('bg-green-active');
         	}
            if (!$('#dataConfirmModal').length) {
                $('body').append('<div id="dataConfirmModal" class="modal fade" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">Ã—</button><h3 id="dataConfirmLabel">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
            }
            $('#dataConfirmModal').find('.modal-body').text(message);
            $('#dataConfirmModal').modal({
                show: true
            });
            return false;
         },
         error : function (data) {
            debugger;
            console.log(data);
            message = "Failure"
            $("#processing-modal").modal('hide');
             if (!$('#dataConfirmModal').length) {
                $('body').append('<div id="dataConfirmModal" class="modal fade" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">Ã—</button><h3 id="dataConfirmLabel">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
            }
            $('#dataConfirmModal').find('.modal-body').text(message);
            $('#dataConfirmModal').modal({
                show: true
            });
            return false;
         }
      });
   });


/*------------------------------------------------------------------------------
  function for Delete Modal in loginindex.html
*----------------------------------------------------------------------------*/
$(document).ready(function() {
    $('a[data-confirm]').click(function(ev) {
        debugger;
        var href = $(this).attr('href');
        if (!$('#dataConfirmModal').length) {
            $('body').append('<div id="dataConfirmModal" class="modal fade" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="dataConfirmLabel">Please Confirm</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button><a class="btn btn-primary" id="dataConfirmOK">OK</a></div></div></div></div>');
        }
        $('#dataConfirmModal').find('.modal-body').text($(this).attr('data-confirm'));
        $('#dataConfirmOK').attr('href', href);
        $('#dataConfirmModal').modal({
            show: true
        });
        return false;
    });
});



/*------------------------------------------------------------------------------
  Function for Add User modal in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#addUserModal',function(e) {
    debugger;
    var url = '/logintemplate/adduser/';
    var model = null;
    $("#userModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#userModelbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#userModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#userModelbody').modal('hide');
        $(this).data('modal', null);
        $("#userModelbody").html("");
    });
});

/*------------------------------------------------------------------------------
  Function for Add User in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#addUser',function(e) {
    debugger;
    var password = $('#id_password').val()
    var confirmPassword = $("#id_confirm_password").val();
    if (password != confirmPassword) {
        $("#divErrorUser").empty();
        $("#divErrorUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Password doesnot match").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
            $("#divErrorUser").slideUp(500);
        });

        e.preventDefault(); 
    }
    else{
        var formdata = $("#userform").serialize();

        $.ajax({
            type: 'POST',
            url: "/logintemplate/adduser/",
            data: formdata,          
            success: function(data) {
                debugger;
                if (data == "Failure1"){
                    console.log(data)
                    $("#divErrorUser").empty();
                    $("#divErrorUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Email Id already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorUser").slideUp(500);
                    });

                }
                if (data == "Failure2"){
                    debugger;
                    console.log(data)
                    $("#divErrorUser").empty();
                    $("#divErrorUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Please fill all * the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorUser").slideUp(500);
                    });
                }
                else if(data == "Success"){
                    debugger;
                    $("#divResultUser").empty();

                    $("#divResultUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                        $("#divResultUser").slideUp(500);
                    });
                    window.location.reload();
                }
                
            
                
            },
            failure: function(data) {
                debugger;
                console.log(data)
                $(saveclose).click();
                $("#divErrorUser").empty();
                $("#divErrorUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorUser").slideUp(500);
                });
            }
        });
        e.preventDefault(); 
    }

    
    
});


/*------------------------------------------------------------------------------
  Function for Edit User modal in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#userEdit',function(e) {
    debugger;
    var userid = e.currentTarget.attributes['data-userid'].value;
    var url = '/logintemplate/edituser/'+userid;
    var model = null;
    $("#userEditModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#userEditModelbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#userEditModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#userEditModelbody').modal('hide');
        $(this).data('modal', null);
        $("#userEditModelbody").html("");
    });
});


/*------------------------------------------------------------------------------
  Function for Update User in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#updateUser',function(e) {
    debugger;
    var password = $('#id_password').val()
    var confirmPassword = $('#id_confirm_password').val()
    if (password != confirmPassword) {
        $("#divErrorEditUser").empty();
        $("#divErrorEditUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Password doesnot match").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
            $("#divErrorEditUser").slideUp(500);
        });
        e.preventDefault(); 
    }
    else{
        var formdata = $("#usereditform").serialize();
        var userid = e.currentTarget.attributes['data-userid'].value;

        $.ajax({
            type: 'POST',
            url: "/logintemplate/edituser/"+userid,
            data: formdata,          
            success: function(data) {
                debugger;
                if (data == "Failure1"){
                    console.log(data)
                    $("#divErrorEditUser").empty();
                    $("#divErrorEditUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Email Id already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorEditUser").slideUp(500);
                    }); 

                }
                else if (data == "Failure2"){
                    debugger;
                    console.log(data)
                    $("#divErrorEditUser").empty();
                    $("#divErrorEditUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the * fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorEditUser").slideUp(500);
                    });
                }
                else if(data == "Success"){
                    debugger;
                    $("#divResultEditUser").empty();

                    $("#divResultEditUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                        $("#divResultEditUser").slideUp(500);
                    });
                    window.location.reload();
                }
                
               
            
                
            },
            failure: function(data) {
                debugger;
                console.log(data)
                $(saveclose).click();
                $("#divErrorEditUser").empty();
                $("#divErrorEditUser").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEditUser").slideUp(500);
                });
            }
        });
        e.preventDefault();
    }
    
});


/*------------------------------------------------------------------------------
  Function for add new general info in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#addinfo',function(e) {
    var formdata = $("#infoForm").serialize();

    $.ajax({
        type: 'POST',
        url: "/logintemplate/addinfo/",
        data: formdata,          
        success: function(data) {
            debugger;
            if (data == "Failure1"){
                console.log(data)
                $("#divErrorInfo").empty();
                $("#divErrorInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Key already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorInfo").slideUp(500);
                });

            }
            if (data == "Failure2"){
                debugger;
                console.log(data)
                $("#divErrorInfo").empty();
                $("#divErrorInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorInfo").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultInfo").empty();

                $("#divResultInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultInfo").slideUp(500);
                });
            }
            // window.location.reload();
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorInfo").empty();
            $("#divErrorInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorInfo").slideUp(500);
            });
        }
    });

});

/*------------------------------------------------------------------------------
  Function for Edit Info modal in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#editInfoModal',function(e) {
    debugger;
    var infoid = e.currentTarget.attributes['data-infoid'].value;
    var url = '/logintemplate/editinfo/'+infoid;
    var model = null;
    $("#infoEditModal").on("shown.bs.modal",function() { 
        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(url)
                .done(function(data) {
                    $("#infoEditModelbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);                
    }); 

    $('#infoEditModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#infoEditModelbody').modal('hide');
        $(this).data('modal', null);
        $("#infoEditModelbody").html("");
    });
});

/*------------------------------------------------------------------------------
  Function for Update Info in servercofig.html
*----------------------------------------------------------------------------*/
$(document).on('click', '#updateinfo',function(e) {
    debugger;
    var formdata = $("#infoEditForm").serialize();
    var infoid = e.currentTarget.attributes['data-infoid'].value;

    $.ajax({
        type: 'POST',
        url: "/logintemplate/editinfo/"+infoid,
        data: formdata,          
        success: function(data) {
            debugger;
            if (data == "Failure1"){
                console.log(data)
                $("#divErrorEditInfo").empty();
                $("#divErrorEditInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Key already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEditInfo").slideUp(500);
                });

            }
            if (data == "Failure2"){
                debugger;
                console.log(data)
                $("#divErrorEditInfo").empty();
                $("#divErrorEditInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEditInfo").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultEditInfo").empty();

                $("#divResultEditInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultEditInfo").slideUp(500);
                });
            }
            // window.location.reload();
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorEditInfo").empty();
            $("#divErrorEditInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorEditInfo").slideUp(500);
            });
        }
    });
    
});


/*------------------------------------------------------------------------------
  Function update DB Modal
*----------------------------------------------------------------------------*/
function updateDb(event){
//$(document).on('click', '#updateDb',function(e) {
    debugger;
    dbtype = "server"
    $("#processing-modal").modal('show');
    $.ajax({
        type : 'POST',
        url :"/logintemplate/updateuserindb/",
        data : {'dbType':dbtype},
        success : function (data) {
            // alert(data);
            debugger;
            if (data == "SUCCESS"){
                setTimeout(function() {
                    debugger;
                    $("#processing-modal").modal('hide');
                    $('#userUpdateDbModal').find('#modallabel').empty();
                    $('#userUpdateDbModal').find('.modal-body').empty();
                    $('#userUpdateDbModal').find('#modallabel').append("Information");
                    $('#modallabel').css("color","rgb(60, 141, 188)")
                    
                    if (!$('#userUpdateDbModal').length) {
                        $('body').append('<div id="userUpdateDbModal" class="modal" role="dialog" aria-labelledby="modallabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="modallabel" style="color: rgb(60, 141, 188);">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
                    }
                    
                    $('#userUpdateDbModal').find('.modal-body').text("Updated Successfully");
                    $('#userUpdateDbModal').modal({
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
                    $('#userUpdateDbModal').find('#modallabel').empty();
                    $('#userUpdateDbModal').find('.modal-body').empty();
                    $('#userUpdateDbModal').find('#modallabel').append("Error");
                    $('#dataConfirmLabel').css("color", "red");
                    
                    if (!$('#userUpdateDbModal').length) {
                        $('body').append('<div id="userUpdateDbModal" class="modal" role="dialog" aria-labelledby="modallabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="modallabel" style="color: red">Error</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
                    }
                   
                    for(i=0; i<errorArray.length;i++){
                        $('#userUpdateDbModal').find('.modal-body').append(errorArray[i]+'<br>')
                    }
                    
                    $('#userUpdateDbModal').modal({
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






