$(document).on('click', '#addtablemap',function(e) {
    debugger;
    var formdata = $("#tableMapForm").serialize();

    $.ajax({
        type: 'POST',
        url: "/syncmaster/tablemapsave/",
        data: formdata,          
        success: function(data) {
            debugger;
            if (data == "Failure1"){
                console.log(data)
                $("#divErrorTableInfo").empty();
                $("#divErrorTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Map already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorTableInfo").slideUp(500);
                });

            }
            if (data == "Failure2"){
                debugger;
                console.log(data)
                $("#divErrorTableInfo").empty();
                $("#divErrorTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorTableInfo").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultTableInfo").empty();

                $("#divResultTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultTableInfo").slideUp(500);
                });
                window.location.reload();
            }
            
          
            
        },
        failure: function(data) {
            debugger;
            console.log(data)
            $(saveclose).click();
            $("#divErrorTableInfo").empty();
            $("#divErrorTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorTableInfo").slideUp(500);
            });
        }
    });
    e.preventDefault();
    
});

/*------------------------------------------------------------------------------
*Model Function for Tablemap Edit in syncmaster.html
*----------------------------------------------------------------------------*/
 $(document).on('click', '#edit_button',function(mevent) {

    debugger;
    var model = null;
    tmapid = mevent.currentTarget.attributes['data-tmapid'].value
    viewcompedit = '/syncmaster/tablemapedit/' + tmapid;
    $("#viewModal").on("show.bs.modal", function() {
        setTimeout(function() {
            if (model == null) {
                model = $.ajax(viewcompedit)
                .done(function(data) {
                    $("#viewmodelbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });

    $('#viewModal').on('hidden.bs.modal', function () {
        $("#viewmodelbody").modal('hide');
        $(this).data('modal', null);
        $("#viewmodelbody").html("");
    })
});

  /*------------------------------------------------------------------------------
  * Function for update tablemap in syncmaster.html
  *----------------------------------------------------------------------------*/

function updatetablemap(event) {
    debugger;
    var tmapid = event.currentTarget.dataset['id'];
    var formdata = $("#updatemap").serialize();
    //alert("hi");
    $.ajax({
        type: 'POST',
        url: "/syncmaster/tablemapedit/" + tmapid,
        data: formdata,
        success: function(data) {
            debugger;
            if (data == "Failure1"){
                console.log(data)
                $("#divErrorEditTableInfo").empty();
                $("#divErrorEditTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Map already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEditTableInfo").slideUp(500);
                });

            }
            if (data == "Failure2"){
                debugger;
                console.log(data)
                $("#divErrorEditTableInfo").empty();
                $("#divErrorEditTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed. Please fill all the fields.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#divErrorEditTableInfo").slideUp(500);
                });
            }
            else if(data == "Success"){
                debugger;
                $("#divResultEditTableInfo").empty();

                $("#divResultEditTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#divResultTableInfo").slideUp(500);
                });
                window.location.reload();
            }         
        },
        error: function(data) {

            $("#divErrorEditTableInfo").empty();
            $("#divErrorEditTableInfo").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                $("#divErrorEditTableInfo").slideUp(500);
            });
        }
    });
    e.preventDefault();
 };

 /*------------------------------------------------------------------------------
  *Model Function for configuration button in syncmaster.html
  *----------------------------------------------------------------------------*/
 $(document).on('click', '#conf_button',function(mevent) {

    debugger;
    var model = null;
    tmapid = mevent.currentTarget.attributes['data-tmapid'].value
    viewcompedit = '/syncmaster/columnmap/' + tmapid;
     $("#confModal").on("show.bs.modal", function() {
         
         setTimeout(function() {
         if (model == null) {
          model = $.ajax(viewcompedit)
             .done(function(data) {

                 $("#confmodelbody").html(data);
             })
             .fail(function() {
                 alert("error");
             });
         }
         },500);
     });
 });

/*------------------------------------------------------------------------------
* Function for closing Modal inside modal in synmaster.html
*----------------------------------------------------------------------------*/

 function closemodal(event) {
    debugger;
    parentid = event.currentTarget.offsetParent.offsetParent.id;
    if (parentid == "coulmnmodalbody"){
   $("#column-mapping").modal('hide');
   $('#column-mapping').on('hidden.bs.modal', function () {
             $("#coulmnmodalbody").modal('hide');
             $(this).data('modal', null);
             $("#coulmnmodalbody").html("");
            });
}
   else if(parentid == "editcoulmnmodal"){
    $("#editcolumn-mapping").modal('hide');
   $('#editcolumn-mapping').on('hidden.bs.modal', function () {
             $("#editcoulmnmodal").modal('hide');
             $(this).data('modal', null);
             $("#editcoulmnmodal").html("");
            });

   }
 }

 /*------------------------------------------------------------------------------
* Function for closing Modal inside modal in synmaster.html
*----------------------------------------------------------------------------*/

 function tmapmodalclose(event) {
    debugger;

   $("#confModal").modal('hide');
   $('#confModal').on('hidden.bs.modal', function () {
             $("#confmodelbody").modal('hide');
            });
   location.reload();

 }

 /*------------------------------------------------------------------------------
  *Model Function for Tablemap Edit in syncmaster.html
  *----------------------------------------------------------------------------*/
 $(document).on('click', '#columnmapadd',function(mevent) {

    debugger;
    var model = null;
    tmapid = mevent.currentTarget.attributes['data-id'].value
    viewcompedit = '/syncmaster/columnmapadd/' + tmapid;
     $("#column-mapping").on("show.bs.modal", function() {
         
         setTimeout(function() {
         if (model == null) {
          model = $.ajax(viewcompedit)
             .done(function(data) {
                 $("#coulmnmodalbody").html("");
                 $("#coulmnmodalbody").html(data);
             })
             .fail(function() {
                 alert("error");
             });
         }
         },500);
     });

     $('#column-mapping').on('hidden.bs.modal', function () {
            $("#coulmnmodalbody").modal('hide');
             $(this).data('modal', null);
            $("#coulmnmodalbody").html("");
            })
 });


/*------------------------------------------------------------------------------
  *Model Function for Columnmap Edit in syncmaster.html
  *----------------------------------------------------------------------------*/
 $(document).on('click', '#edit_columnmap',function(mevent) {

    debugger;
    var model = null;
    tmapid = mevent.currentTarget.attributes['data-tmapid'].value
    cmapid = mevent.currentTarget.attributes['data-cmapid'].value
    viewcompedit = '/syncmaster/columnmapedit/'+cmapid+'/'+tmapid;
     $("#editcolumn-mapping").on("show.bs.modal", function() {
         
         setTimeout(function() {
         if (model == null) {
          model = $.ajax(viewcompedit)
             .done(function(data) {
                 $("#editcoulmnmodal").html("");
                 $("#editcoulmnmodal").html(data);
             })
             .fail(function() {
                 alert("error");
             });
         }
         },500);
     });

     $('#editcolumn-mapping').on('hidden.bs.modal', function () {
            $("#editcoulmnmodal").modal('hide');
             $(this).data('modal', null);
            $("#editcoulmnmodal").html("");
            })
 });

/*------------------------------------------------------------------------------
* Function for columnmap save in columnmap.html
*----------------------------------------------------------------------------*/

 function columnmapsave(event) {
    debugger;
    var tmapid = event.currentTarget.dataset['id'];
    var cmapid = event.currentTarget.dataset['cmapid'];
     var formdata = $("#cmapform").serialize();
     var parentid = event.currentTarget.offsetParent.offsetParent.id;
     //alert("hi");
     $.ajax({
         type: 'POST',
         url: "/syncmaster/columnmapsave/"+cmapid+"/"+tmapid,
         data: formdata,
         success: function(data) {
        if (parentid == "coulmnmodalbody"){
            $("#column-mapping").modal('hide');
            $("#column-mapping").data('modal', null);
        }
        else if(parentid == "editcoulmnmodal"){
            $("#editcolumn-mapping").modal('hide');
            $("#editcolumn-mapping").data('modal', null); 
        }
             $('#colmaptb').html("");
             $('#colmaptb').html(data);
             var datatable = $('#colmaptbnew').dataTable({
                 "ordering": false,
             });
             $('#colmaptbnew').DataTable();
            $("#divResultsmodal").empty();

             $("#divResultsmodal").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                 $("#divResultsmodal").slideUp(500);
             });
             //window.location.reload(600);            
         },
         error: function(data) {

             $("#divErrormodal").empty();
             $("#divErrormodal").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                 $("#divErrormodal").slideUp(500);
             });
         }
     });
 };

/*------------------------------------------------------------------------------
* Function for columnmap delete in columnmap.html
*----------------------------------------------------------------------------*/


   $(document).on('click', '#columnmapdelete',function(event) {
    debugger;
    var cmapid = "";
    var tmapid ="";
     cmapid = event.currentTarget.dataset['cmapid'];
     tmapid = event.currentTarget.dataset['tmapid'];
     
     $('#dataConfirmModal1').modal('show');
          $(document).on('click', '#dataConfirm',function(mevent){
            deleteaction(cmapid,tmapid);
         });
         //$('#dataConfirmModal').modal('show');
 });

 function deleteaction(cmid,tmid){
    var ajax = null;
    var deleteurl = ""
    deleteurl = "/syncmaster/columnmapdelete/"+cmid+"/"+tmid;
     if (ajax == null)
     {
       ajax = $.ajax(deleteurl)
             .done(function(data) {
                $('#dataConfirmModal1').modal('hide'); 
                 $('#colmaptb').html("");
                 $('#colmaptb').html(data);
                 var datatable = $('#colmaptbnew').dataTable({
                     "ordering": false,
                 });
                 $('#colmaptbnew').DataTable();
                $("#divResultsmodal").empty();
                $("#divErrormodal").empty();

                 $("#divResultsmodal").fadeTo(2000, 500).append("<h4>Alert!</h4>Deleted Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                 $("#divResultsmodal").slideUp(500);
             });
             })
             .fail(function() {
                 alert("error");
             });
         }
     //        $.ajax({
     //     type: 'POST',
     //     url: "/syncmaster/columnmapdelete/"+cmapid+"/"+tmapid,
     //     success: function(data) {
            
     //         //window.location.reload(600);            
     //     },
     //     error: function(data) {

     //         $("#divErrormodal").empty();
     //         $("#divErrormodal").fadeTo(2000, 500).append("<h4>Alert!</h4>Delete Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
     //             $("#divErrormodal").slideUp(500);
     //         });
     //     }
     // });
 }


/*------------------------------------------------------------------------------
* Function for Update Db in syncmaster.html
*----------------------------------------------------------------------------*/

$(document).on('click', '#syncMaster',function(mevent) {
    debugger;
    dbtype = "server"
    $("#processing-modal").modal('show');
    $.ajax({
        type : 'POST',
        url :"/syncmaster/updatedb/",
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
                    
                    $('#userUpdateDbModal').find('.modal-body').text("Updated Succfully");
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
                    $('#userUpdateDbModal').find('#modallabel').append("Error");
                    $('#dataConfirmLabel').css("color", "red");
                    
                    if (!$('#userUpdateDbModal').length) {
                        $('body').append('<div id="userUpdateDbModal" class="modal" role="dialog" aria-labelledby="modallabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="modallabel" style="color: red">Error</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
                    }
                    $('#userUpdateDbModal').find('.modal-body').empty();
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

  });