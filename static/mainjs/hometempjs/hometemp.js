  /*------------------------------------------------------------------------------
   *function for switching menutype
   *----------------------------------------------------------------------------*/
  $('#id_menutype').focusout(function() {
      debugger;
      var lab = $("#id_menutype").val();
      if (lab == 'grid') {
          $("#divsidemenu").hide();
          $("#divcolumn").show();
          $('#id_sidemenu').val('');
      } else if (lab == 'sidemenu') {
          $("#divsidemenu").show();
          $("#divcolumn").hide();
          $('#id_column').val('');
      } else {
          alert("please select menu type");
      }
  });

  /*------------------------------------------------------------------------------
   *function for Root page selection options
   *----------------------------------------------------------------------------*/
  $('#id_pageoption').focusout(function() {
      debugger;
      var root = $("#id_pageoption").val();
      if (root == 'default') {
          $("#select_root").hide();
          $('#id_pageValue').val('');
      } else {
          $("#select_root").show();
        }
  });
/*------------------------------------------------------------------------------
*function for adding menutype
*----------------------------------------------------------------------------*/

function addmenu() {

    var model = null
    var tablecomp = '/hometemplate/addmenu/';

    $("#menuModal").on("shown.bs.modal", function() {

        setTimeout(function() {
            if (model == null) {    
            model = $.ajax(tablecomp)
                .done(function(data) {
                    $("#mymodelbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);     

      });

    $('#menuModal').on('hidden.bs.modal', function(e) {
        console.log("Modal hidden");
        $('#mymodelbody').modal('hide');
        $(this).data('modal', null);
        $("#mymodelbody").html("");
    });
};

/*------------------------------------------------------------------------------
*function for submit button in pagecomponent.html
*----------------------------------------------------------------------------*/
function home_submit() {
  debugger;
  var formdata = $("#menu_form").serialize();
  $.ajax({
         type: 'POST',
         url: "/hometemplate/pagecomponent/",
         data: formdata,
         success: function(data) {
           $("#menutype_Results").empty();
           $("#menutype_Results").fadeTo(2000, 500).append('<h4><i class="icon fa fa-check"></i> Alert!</h4>Saved Successfully.').addClass("alert alert-success alert-dismissible").slideUp(500, function() {
            $("#menutype_Results").slideUp(300);
          });
         },
         error: function(data) {

             console.log(data)
         }
     });

    
};


/*------------------------------------------------------------------------------
*function for root page tab submit button in pagecomponent.html
*----------------------------------------------------------------------------*/
function root_submit(event) {
  debugger;
  var formdata = $("#root_menu_form").serialize();
  var home = event.currentTarget.attributes['data-homeid'].value
  $.ajax({
         type: 'POST',
         url: "/hometemplate/rootpage/"+home,
         data: formdata,
         success: function(data) {
           $("#root_divResults").empty();
           $("#root_divResults").fadeTo(2000, 500).append('<h4><i class="icon fa fa-check"></i> Alert!</h4>Saved Successfully.').addClass("alert alert-success alert-dismissible").slideUp(500, function() {
            $("#root_divResults").slideUp(300);
          });
         },
         error: function(data) {

           $("#root_divErrorMessages").empty();
           $("#root_divErrorMessages").fadeTo(2000, 500).append('<h4><i class="icon fa fa-warning"></i> Alert!</h4>Saved Failed.').addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
               $("#root_divErrorMessages").slideUp(500);
           });
         }
     });


};

/*------------------------------------------------------------------------------
*function for editing menutype
*----------------------------------------------------------------------------*/
function edit_menu(mevent) {
    debugger;
    
    var model = null;
    id = mevent.currentTarget.attributes['data-transactionid'].value
    tablecomp = '/hometemplate/editmenu/' + id;
    
    $("#editmenuModal").on("show.bs.modal", function() {
        
        setTimeout(function() {
            if (model == null) {
            model = $.ajax(tablecomp)
                .done(function(data) {
                $("#mymenubody").html("");
                $("#mymenubody").html(data);
                var type_view = $("#id_typeofview").val();
                if(type_view == 'transactionview'){
                  $("#review").hide();
                  $("#trview").show();
                }
                else if(type_view == 'reportview')
                {
                  $("#review").show();
                  $("#trview").hide();
                 } 
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });   
      
    $('#editmenuModal').on('hidden.bs.modal', function() {
        
        $("#mymenubody").modal('hide');
        $(this).data('modal', null);
        $("#mymenubody").html("");
    
    });
};


/*------------------------------------------------------------------------------
*function for Generate Page Button
*----------------------------------------------------------------------------*/
$(document).on('change', '#generate_page',function(event){
      debugger;
      menuid = event.currentTarget.dataset['menuid'];
      var pvalue ="";
      var type ="";
      var txn = event.currentTarget.dataset['txn'];
      var rep = event.currentTarget.dataset['rep'];
      var txn_id = event.currentTarget.dataset['txn_id'];
      var rep_id = event.currentTarget.dataset['rep_id'];
      if (txn != ""){
      pvalue  = txn;
      type ="txview";
      }
      else if(rep !=""){
      pvalue = rep;
      type="report";
      }
      value = $(this).prop('checked');
      console.log(value);
      $.ajax({
         type : 'get',
         url : '/hometemplate/generatepage/'+menuid,
         data : {value:value,txn:txn,page:pvalue},

         //data : sample,
         //dataType: 'json',            
         success : function (data) {
         
         },
         error :function (data) {
           setTimeout(function() {
           
               if (!$('#dataConfirmModal').length) {
                $('body').append('<div id="dataConfirmModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true" data-backdrop="static"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h3 id="dataConfirmLabel">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true" onclick="popup_generate(event)" id="popup_generate" data-id="" data-type="">Generate Page</button><button class="btn btn-default" data-dismiss="modal" aria-hidden="true">Close</button></div></div></div></div>');
                $("#popup_generate")[0].dataset['id'] = menuid;
                $("#popup_generate")[0].dataset['type'] = type;
                $("#popup_generate")[0].dataset['txn_id'] = txn_id;
                $("#popup_generate")[0].dataset['rep_id'] = rep_id;
            }
            $('#dataConfirmModal').find('.modal-body').text(data.responseText);
            $('#dataConfirmModal').modal({
                show: true
            });
            return false;
           },100);
         }
      });

   });

function popup_generate(event){
  var type = event.currentTarget.dataset['type'];
  var generate_url ="";
  if(type == 'txview'){
    var id = event.currentTarget.dataset['txn_id'];
    generate_url = '/transactionview/generatepage/'+id ;

  }else if(type == 'report'){
    var id = event.currentTarget.dataset['txn_id'];
  }
    $.ajax({
         type : 'get',
         url : generate_url,

         success : function (data) {
          $('#dataConfirmModal').modal('hide');
          popupmessage(data);
         },
          error: function(data) {
            $('#dataConfirmModal').modal('hide');
            popupmessage(data.responseText);
          }
        });

};

/*------------------------------------------------------------------------------
*function for save button in menuproperty.html
*----------------------------------------------------------------------------*/


 $('#menuproperty').click(function(e){
   debugger;
   var formdata = $("#contform").serialize();
   $.ajax({
               type : 'POST',
               url : "/hometemplate/addmenu/",
               data : formdata,
               //dataType: 'json',                 
               success : function (data) {
                    $('#menuModal').modal('hide');
                    $("#divResults").empty();
   
                     $("#divResults").fadeTo(2000, 500).append('<h4><i class="icon fa fa-check"></i> Alert!</h4>Saved Successfully.').addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                      $("#divResults").slideUp(300);
                      location.reload(400);
                     });

               },
               error : function (data) {
                    $('#menuModal').modal('hide');
                    $("#divErrorMessages").empty();
                    $("#divErrorMessages").fadeTo(2000, 500).append('<h4><i class="icon fa fa-warning"></i> Alert!</h4>Saved Failed.').addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                        $("#divErrorMessages").slideUp(500);
                    });
                           }
                      });
   });

/*------------------------------------------------------------------------------
*function for save button in editmenu.html
*----------------------------------------------------------------------------*/
 $('#editmenuproperty').click(function(e){
       debugger;
       var formdata = $("#contform").serialize();
       var menuid = e.currentTarget.attributes['data-menuid'].value
        $.ajax({
                         type : 'POST',
                         url : "/hometemplate/editmenu/"+menuid,
                         data : formdata,
                         //dataType: 'json',                 
                         success : function (data) {
                          $('#editmenuModal').modal('hide');
                          var Scrollvalue = parseInt(document.documentElement.scrollTop);
                          sessionStorage.setItem("scroll", Scrollvalue);                                
                          $("#divResults").fadeTo(2000, 500).append('<h4><i class="icon fa fa-check"></i> Alert!</h4>Saved Successfully.').addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                            $("#divResults").slideUp(300);                            
                            location.reload(400);
                          });
                              
                         },
                         error : function (data) {
                            $('#editmenuModal').modal('hide');
                            $("#divErrorMessages").empty();
                          $("#divErrorMessages").fadeTo(2000, 500).append('<h4><i class="icon fa fa-warning"></i> Alert!</h4>Saved Failed.').addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                              $("#divErrorMessages").slideUp(500);
                          });
                         }
                    });
             });

/*------------------------------------------------------------------------------
  * function for Popupmessage
  *----------------------------------------------------------------------------*/
    function popupmessage(msg){
    if (!$('#ConfirmModal').length) {
                $('body').append('<div id="ConfirmModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h3 id="ConfirmLabel" style="color: cadetblue;">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
            }
            $('#ConfirmModal').find('.modal-body').text(msg);
            $('#ConfirmModal').modal({
                show: true
            });

   }