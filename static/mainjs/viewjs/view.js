 /*------------------------------------------------------------------------------
  *Model Function for View Edit in transaview.html
  *----------------------------------------------------------------------------*/
 $(document).on('click', '#edit_button',function(mevent) {

    debugger;
    var txviewid = "";
    var viewcompedit = "";
    var model = null;
    txviewid = mevent.currentTarget.attributes['data-transactionid'].value
    viewcompedit = '/transactionview/viewedit/' + txviewid;
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
   Function for add Component in viewcomponent.html
  *----------------------------------------------------------------------------*/
 function addComponent(event) {
     debugger;
     console.log(event);
     var tableid = event.currentTarget.dataset['transactionid'];
     var component = event.currentTarget.dataset['component'];
     var dbtable = event.currentTarget.dataset['dbtable']
     var componentdata = JSON.parse(component);
     var tablecomp="";
     tablecomp = '/transactionview/addcomponent/' + tableid;
     var model= null;
     console.log(componentdata);
     $("#compModal").on("show.bs.modal", function() {
         debugger;
        setTimeout(function() {
         if (model == null) {
         model = $.ajax(tablecomp)
             .done(function(data) {
                 $("#bodyCal").html("");
                 $("#compbody").html(data);
                 $.ajax({
                     type: 'POST',
                     url: '/transactionview/tabledetails/',
                     data: {
                         'Dbtableid': dbtable,
                     },
                     success: function(response) {
                         meta_data = JSON.parse(response);
                         var tabledata = meta_data[0]["field_meta"] 
                         console.log(response);
                         //var data = JSON.stringify(response);
                         //console.log(data);
                         var tbody = '';
                         var newtd = '';
                         //console.log(data);
                         if (component == "[]") {
                             for (var i = 0; i < tabledata.length; i++) {
                                data = JSON.stringify(tabledata[i])
                                 //console.log(tabledata[i]);
                                 tbody += '<tr><td>' + tabledata[i].title + '</td><td>' + tabledata[i].datatype + '</td><td>' + tabledata[i].field_slug + '</td><td><button id=\'' + tabledata[i].id + '\' class="btn btn-primary" value=\'' + data + '\' onclick="savecomponent(this.value,' + tableid + ',this.id)">ADD</button></td></tr>';
                                 $('#bodyCal').html(tbody);
                             }
                         } else {
                             var componentid = [];
                             for (var j = 0; j < componentdata.length; j++) {
                                 componentid.push(componentdata[j].componentrefer_id);
                             }
                             console.log(componentid);
                             for (var i = 0; i < tabledata.length; i++) {
                                 if (componentid.indexOf(tabledata[i].id) === -1) {
                                     var data = JSON.stringify(tabledata[i]);
                                     console.log(componentid.indexOf(tabledata[i].id))
                                     newtd += '<tr><td>' + tabledata[i].title + '</td><td>' + tabledata[i].datatype + '</td><td>' + tabledata[i].field_slug + '</td><td><button id=\'' + tabledata[i].id + '\' class="btn btn-primary" value=\'' + data + '\' onclick="savecomponent(this.value,' + tableid + ',this.id)">ADD</button></td></tr>';
                                     $('#bodyCal').html(newtd);
                                 }
                             }

                             //$('#bodyCal').html(newtd);
                         }

                         console.log(tbody);
                         //$('#bodyCal').html(tbody);
                         $("#modeltab").DataTable();
                     },
                     error: function() {
                         //if there is an error append a 'none available' option

                     }
                 });
             })
             .fail(function() {
                 alert("error");
             });
         }
     },);
             

     });
     $('#compModal').on('hidden.bs.modal', function(e) {
         console.log("Modal hidden");
        $("#compbody").modal('hide');
        $(this).data('modal', null);
        $("#bodyCal").html("");
        location.reload();        
     });

 };

 /*------------------------------------------------------------------------------
  * Function for edit component button in viewcomponent.html
  *----------------------------------------------------------------------------*/

 function editcomponent(compid) {
     debugger;
     console.log(compid);
     $("#divbody").show();
     $("#compprop2").hide();
     $("#containerdiv").removeClass("col-lg-12 col-xs-12")
      $("#containerdiv").addClass("col-lg-8 col-xs-8")
     $("#compprop1").show(); {
         var componid = compid

         var tablecomp = '/transactionview/editcomponent/' + componid;
         var modal = $.ajax(tablecomp)
             .done(function(data) {

                 $("#tablebody1").html(data);
             })
             .fail(function() {
                 alert("error");
             });
     }

 };


 /*------------------------------------------------------------------------------
  *Function for Edit container button in viewcomponent.html
  *----------------------------------------------------------------------------*/

 function editcontainer(contid) {
     debugger;
     console.log(contid);
     $("#divbody").show();
     $("#compprop1").hide();
      $("#containerdiv").removeClass("col-lg-12 col-xs-12")
      $("#containerdiv").addClass("col-lg-8 col-xs-8")
     $("#compprop2").show(); {
         var containid = contid

         var tablecomp = '/transactionview/editcontainer/' + containid;
         var modal = $.ajax(tablecomp)
             .done(function(data) {

                 $("#tablebody").html(data);
             })
             .fail(function() {
                 alert("error");
             });
     }

 };


 /*------------------------------------------------------------------------------
  *Template Function for Delete Componenet in viewcomponent.html
  *----------------------------------------------------------------------------*/

 function deletecomp() {

     console.log();
     $('a[data-confirm]').on('click', function(e) {

         e.preventDefault();
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
 };

 /*------------------------------------------------------------------------------
  * Function for Savecomponent in viewcomponent.html
  *----------------------------------------------------------------------------*/

 function savecomponent(response, compid, id) {
    debugger;
     console.log(response);
     var containid = compid;
     //alert("hi");
     $.ajax({
         type: 'POST',
         url: "/transactionview/savecomponent/" + containid,
         data: {jsonData:response},
         success: function(data) {

             //alert("success");
             $('#viewtable').html("");
             $('#viewtable').html(data);
             var datatable = $('#tabcol').dataTable({
                stateSave: true,
                "ordering": false

             });
             $('#tabcol').DataTable();
             $('#' + id).addClass('btn btn btn-success')
             $('#' + id).text('ADDED');
             $('#' + id)[0].disabled = true;

         },
         error: function(data) {

             console.log(data)
         }
     });
 };


 /*------------------------------------------------------------------------------
  * Function for updateContainer in contproperty.html
  *----------------------------------------------------------------------------*/
 
 function updatecontainer(event){
     debugger;
     var formdata = $("#contform").serialize();
     var containerid = event.currentTarget.attributes['data-container'].value
     $.ajax({
         type: 'POST',
         url: "/transactionview/editcontainer/" + containerid,
         data: formdata,
         //dataType: 'json',                 
         success: function(data) {

             ///alert("success");
             $('#viewtable').html("");
             $('#viewtable').html(data);
             var datatable = $('#tabcol').dataTable({
                 "ordering": false,
                  stateSave: true
             });
             $('#tabcol').DataTable();
             
             $("#divResults").empty();

             $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                 $("#divResults").slideUp(500);
             });
             $("#createIoniclb").removeClass('bg-green-active');
             $("#createIoniclb").addClass('bg-blue');
         },
         error: function(data) {
             console.log(data)
              result = JSON.parse(data.responseText);
             listid = ['title','caption','containertype','inputtype','parent','dbtable','displayorder']
              var errmsg ="";
             for (var i=0;i<listid.length;i++){
                var name = listid[i];

                try{
                    errmsg += result[name][0]; 
                }
                catch(err) {
                    console.log(err);
                } }
                popupmessage("Errors:"+errmsg);
             $("#divErrorMessages").empty();
             $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                 $("#divErrorMessages").slideUp(500);
             });
         }
     });
 };



 /*------------------------------------------------------------------------------
  * Function for updateContainer in comproperty.html
  *----------------------------------------------------------------------------*/
 
 function updatecomponent(event){

     var formdata = $("#comptform").serialize();
     var containerid = event.currentTarget.attributes['data-container'].value
     $.ajax({
         type: 'POST',
         url: "/transactionview/editcomponent/" + containerid,
         data: formdata,
         //dataType: 'json',                 
         success: function(data) {
             debugger;

             ///alert("success");
             $('#viewtable').html("");
             $('#viewtable').html(data);
             var datatable = $('#tabcol').dataTable({
                 "ordering": false,
                  stateSave: true
             });
             $('#tabcol').DataTable();
             $("#createIoniclb").removeClass('bg-green-active');
             $("#createIoniclb").addClass('bg-blue');
             /* clear the error message first */
             $("#divResults").empty();

             $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                 $("#divResults").slideUp(500);
             });
         },
         error: function(data) {
            debugger;
            var result;
            try{
                result = JSON.parse(data.responseText);
            }
            catch(err) {
                result = data.responseText;
            }
           
            var errmsg ="";
            try{
                if(result['title']){
                    errmsg += result['title'][0];
                }
                if(result['displayorder']) {
                   errmsg += result['displayorder'][0];
                }
                else{
                    errmsg = result;
                }
            }
            catch(err) {
                errmsg = err;
            }
             popupmessage("Errors:"+errmsg);
             $("#divErrorMessages").empty();
             $("#divErrorMessages").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                 $("#divErrorMessages").slideUp(500);
             });
         }
     });
 };


 /*------------------------------------------------------------------------------
  * Postfix Conversion for Container Expression
  *----------------------------------------------------------------------------*/

     $('.expression').blur(function(){
      //debugger;
        //alert("This input field has lost its focus.");
        var postfix ;
        var expression  = $("#expression").val();
        if (expression){
        postfix = Tokanize(expression);
        $("#postexp").val( postfix[1]);
        console.log($("#postexp").val());
      }
    });

 /*------------------------------------------------------------------------------
  * click for Generate Page
  *----------------------------------------------------------------------------*/

    function generate_page(event){
      debugger;
      txviewid = event.currentTarget.dataset['txviewid'];
      from = event.currentTarget.dataset['from'];
      $("#processing-modal").modal('show');
      $.ajax({
         type : 'get',
         url : '/transactionview/generatepage/'+txviewid,

         //data : sample,
         //dataType: 'json',            
         success : function (data) {
          setTimeout(function() {
            if(from == "tview"){
           $("#processing-modal").modal('hide');
           $('#generate_page').removeClass('btn btn-warning btn-xs btn-primary').addClass('btn bg-navy btn-xs');
           }else if(from == "view"){
             $("#processing-modal").modal('hide');
               $("#createIoniclb").addClass('bg-green-active');
           }
           popupmessage("Page Generated Successfully")
           },500);
         },         
         error: function(data) {
           setTimeout(function() {
            if(from == "tview"){
           $("#processing-modal").modal('hide');
           $('#generate_page').removeClass('btn btn-warning btn-xs btn-primary').addClass('btn bg-navy btn-xs');
           }else if(from == "view"){
             $("#processing-modal").modal('hide');
               $("#createIoniclb").addClass('bg-green-active');
           }
           popupmessage(data.responseText)
           },500);
         }
      });

   };

/*------------------------------------------------------------------------------
  * function for add container in viewcomponent html
  *----------------------------------------------------------------------------*/
   
    function container_add(event){
        var formdata = $("#cont_add").serialize();
        debugger;
        viewid = event.currentTarget.dataset['viewid'];
        console.log(formdata);
         $.ajax({
         type: 'POST',
         url: "/transactionview/viewcomponent/"+viewid,
         data: formdata,
         //dataType: 'json',                 
         success: function(data) {

             ///alert("success");
             $("#cont_add")[0].reset();
             $("#CompModal").modal('hide');
             $('#viewtable').html("");
             $('#viewtable').html(data);
             var datatable = $('#tabcol').dataTable({
                 "ordering": false,
                  stateSave: true
             });
             $('#tabcol').DataTable();
             /* clear the error message first */
             $("#divResults").empty();

             $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
             $("#divResults").slideUp(500);
             });
         },
         error: function(data) {
             console.log(data)
             console.log(JSON.parse(data.responseText));
             result = JSON.parse(data.responseText);
             listid = ['','title','caption','containertype','inputtype','parent','dbtable','displayorder']
             var element = document.getElementById('cont_add').querySelectorAll('*[name]');
             for (var i=1;i<element.length;i++){
                let id = element[i].id;
                let name = listid[i];
                try{
                $("#"+id+"er").empty()   
                $("#"+id+"er").fadeTo(2000, 1000).append('<p style="color:red">'+result[name][0]+'</p>').slideUp(1000, function() {
                 $("#"+id+"er").slideUp(1000);
                     });
                }
                catch(err) {
                    console.log(err);
                } 
             }
             $("#divResults").empty();     
             $("#divResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Failed.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
               $("#divResults").slideUp(500);
             });
         }
     });
    };

/*------------------------------------------------------------------------------
  * function for Popupmessage
  *----------------------------------------------------------------------------*/
    function popupmessage(msg){
    if (!$('#ConfirmModal').length) {
                $('body').append('<div id="ConfirmModal" class="modal" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="ConfirmLabel" style="color: cadetblue;">Information</h3></div><div class="modal-body"></div><div class="modal-footer"><button class="btn btn-primary" data-dismiss="modal" aria-hidden="true">OK</button></div></div></div></div>');
            }
            $('#ConfirmModal').find('.modal-body').text(msg);
            $('#ConfirmModal').modal({
                show: true
            });

   }

/*------------------------------------------------------------------------------
  * function for remove properties box in contproperty.html
  *----------------------------------------------------------------------------*/  

  function remove() {
      debugger;
      $("#compprop1").hide();
      $("#compprop2").hide();
      $("#containerdiv").removeClass("col-lg-8 col-xs-8")  
      $("#containerdiv").addClass("col-lg-12 col-xs-12")
   } 

/*------------------------------------------------------------------------------
  * function for eupdate add button in viewcomponent.html
  *----------------------------------------------------------------------------*/  

  function eupdateAdd(event) {
      debugger;
      console.log(event);
      var viewid ="";
      var eupdateAdd = "";
      viewid = event.currentTarget.dataset['viewid'];
      var model = null;
      eupdateAdd = '/transactionview/eupdateAdd/' + viewid;
     $("#EupdateModal").on("show.bs.modal", function() {
         
         setTimeout(function() {
         if (model == null) {
          model = $.ajax(eupdateAdd)
             .done(function(data) {

                 $("#eupdateaddbody").html(data);
             })
             .fail(function() {
                 alert("error");
             });
         }
         },500);
     });

     $('#EupdateModal').on('hidden.bs.modal', function () {
            $("#eupdateaddbody").modal('hide');
             $(this).data('modal', null);
            $("#eupdateaddbody").html("");
            });
   };    


/*------------------------------------------------------------------------------
  * function for eupdate Edit button in viewcomponent.html
  *----------------------------------------------------------------------------*/  

  function eupdateEdit(event) {
      debugger;
      console.log(event);
      var viewid ="";
      var eupdateAdd = "";
      eupdateid = event.currentTarget.dataset['eupdateid'];
      var model = null;
      eupdateEdit = '/transactionview/eupdateEdit/' + eupdateid;
     $("#eupdateEditModal").on("show.bs.modal", function() {
         
         setTimeout(function() {
         if (model == null) {
          model = $.ajax(eupdateEdit)
             .done(function(data) {

                 $("#eupdateeditbody").html(data);
             })
             .fail(function() {
                 alert("error");
             });
         }
         },500);
     });

     $('#eupdateEditModal').on('hidden.bs.modal', function () {
            $("#eupdateeditbody").modal('hide');
             $(this).data('modal', null);
            $("#eupdateeditbody").html("");
            });
   }; 


 /*------------------------------------------------------------------------------
  * function of focusout for element targettransactionview in eupdatemodal.html
  *----------------------------------------------------------------------------*/  

  $( "#id_updatetype" ).focusout(function(event) {
   console.log(event);
   var updatetype = "";
   updatetype = event.currentTarget.value;
    $.ajax({
         type: 'POST',
         url: "/transactionview/eupdatetype/",
         data: {'type' :updatetype},
         //dataType: 'json',                 
         success: function(data) {
            var reqdata = JSON.parse(data);
            $('#targettxview').empty();
            $('#targettxview').append(new Option('--------', ''));
            for (var i=0;i<reqdata.length;i++){
                $('#targettxview').append(new Option(reqdata[i].fields['title'], reqdata[i].pk));
            }
         },
         error: function(data) {
            console.log('error');
            $('#targettxview').empty();
            $('#targettxview').append(new Option('--------', ''));
         }
     });
  });
  
  /*------------------------------------------------------------------------------
  * function of focusout for element target ui field in eupdatemodal.html
  *----------------------------------------------------------------------------*/  

  $( "#targettxview" ).focusout(function(event) {
    debugger;
   console.log(event);
   var updatetype = "";
   targettx = $( "#targettxview" ).val();
   if (targettx){
    $.ajax({
         type: 'POST',
         url: "/transactionview/eupdate_trfields/",
         data: {'tx' :targettx},
         //dataType: 'json',                 
         success: function(data) {
            var reqdata = JSON.parse(data);
            $('#target_ui_field').empty();
            $('#target_ui_field').append(new Option('--------', ''));
            for (var i=0;i<reqdata.length;i++){
                json = JSON.parse(reqdata[0]['fields']['componentrefer_dt']);
                var tbname = json.txtabledetailid;
                $('#target_ui_field').append(new Option('{'+tbname+'}-'+reqdata[i].fields['title'], reqdata[i].pk));
            }
         },
         error: function(data) {
            console.log('error');
            $('#target_ui_field').empty();
            $('#target_ui_field').append(new Option('--------', ''));
         }
     });
}else{
    $('#target_ui_field').empty();
    $('#target_ui_field').append(new Option('--------', ''));
}
  });
  

   /*------------------------------------------------------------------------------
  * function save button in eupdatemodal.html
  *----------------------------------------------------------------------------*/   
  function eupdatesave(event){
    debugger;
    var formdata = $("#eupdatemodalform_add").serialize();
    console.log(formdata);
    var id = event.currentTarget.dataset['id'];
    var url =""
    var md =""
    var process = event.currentTarget.dataset['process'];
    var targetfield = $('#target_ui_field').val();
    var targettx = $('#targettxview').val();
    if(targetfield == null || targettx == null || targetfield == '' || targettx==''){
     listid = ['','targettxview','target_ui_field'];
     for (var i=1;i<listid.length;i++){
        if ($('#'+listid[i]).val() == null || $('#'+listid[i]).val() == ''){
          $("#"+listid[i]+"er").empty();   
          $("#"+listid[i]+"er").fadeTo(2000, 1000).append('<p style="color:red">This Field is Required.</p>').slideUp(1000, function() {
          $("#"+listid[i]+"er").slideUp(1000);
                     });
        }
     }

    }
    else
    {
    $('#eupdatesavebt').removeClass('btn btn-success');
    $('#eupdatesavebt').addClass('btn btn-success disabled');
    if (process == 'add'){
     url = "/transactionview/eupdateSave/" + id;
     md = "EupdateModal";
    }
    else if(process == 'edit'){
        url ="/transactionview/eupdateEdit/" + id;
        md = "eupdateEditModal";
    }
     $.ajax({
         type: 'POST',
         url: url,
         data: formdata,
         //dataType: 'json',                 
         success: function(data) {
            $('#eupdatetbbody').html("");
            $('#eupdatetbbody').html(data);
            $("#saveresult").fadeTo(1000, 500).append('<p style="color:green">Saved Successfully</p>').slideUp(1000, function() {
                 // $("#"+id+"er").slideUp(1000);
                  $("#"+md).modal('hide');
                     });
                
         },
         error: function(data) {
            $('#eupdatesavebt').removeClass('btn btn-success disabled');
            $('#eupdatesavebt').addClass('btn btn-success ');
            result = JSON.parse(data.responseText);
             listid = ['title','actiontype','filter_clause','source_ui_field','target_ui_field','ui_control_field','updatetype']
             for (var i=0;i<listid.length;i++){
                let id = listid[i];
                try{
                $("#"+id+"er").empty()   
                $("#"+id+"er").fadeTo(2000, 1000).append('<p style="color:red">'+result[id][0]+'</p>').slideUp(1000, function() {
                 $("#"+id+"er").slideUp(1000);
                     });
                }
                catch(err) {
                    console.log(err);
                } 
         }
     }
     });
 }
}

/*------------------------------------------------------------------------------
 * function delete button in eupdate 
 *----------------------------------------------------------------------------*/   
   function  eupdatedelete(event) {
    debugger;
    var eupdateid = "";
     eupdateid = event.currentTarget.dataset['eupdateid'];
     
     if (!$('#dataConfirmModal1').length) {
             $('body').append('<div id="dataConfirmModal1" class="modal fade" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="dataConfirmLabel">Please Confirm</h3></div><div class="modal-body"><p>Are you sure you want to delete?</p></div><div class="modal-footer"><button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button><a class="btn btn-primary" data-id="" onclick="deleteaction(event)" id="dataConfirm">OK</a></div></div></div></div>');
         }
         $('#dataConfirmModal1').modal({
             show: true
         });
         document.getElementById('dataConfirm').dataset.id = eupdateid;
         //$('#dataConfirmModal').modal('show');
 };

 function deleteaction(event){
   var id ="";
   id = event.currentTarget.dataset['id'];
    var ajax = null;
    var deleteurl = ""
    deleteurl = "/transactionview/eupdateDelete/"+id;
     if (ajax == null)
     {
       ajax = $.ajax(deleteurl)
             .done(function(data) {
                $('#dataConfirmModal1').modal('hide'); 
                 $('#eupdatetbbody').html("");
                 $('#eupdatetbbody').html(data);
                 $("#eupdateResults").empty();
                 $("#divErrormodal").empty();

                 $("#eupdateResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Deleted Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                 $("#eupdateResults").slideUp(500);
                 return false;
             });
             })
             .fail(function() {
                 alert("error");
                 return false;
             });
         }

 }

 /*----------------------------------------------------------------------------
* function for sql Modal SHOW and HIDDEN
*----------------------------------------------------------------------------*/

function sqlModalFun(event){
   
    sqlString = event.currentTarget.value
    if (sqlString != ""){
        sqlObj = JSON.parse(sqlString);
    }
    

    var sqlmodal = "";
    var model = null;
    
    sqlmodal = '/transactionview/componentSQLModal/';
    $("#sqlModal").on("show.bs.modal", function() {
        debugger;
        setTimeout(function() {
            if (model == null) {
                model = $.ajax(sqlmodal)
                .done(function(data) {
                     $("#sqlModalBody").html(data);
                    if (sqlString != ""){
                        $("#sqlDbType").val(sqlObj ["sqlDbType"]);
                        $("#sqlTextArea").val(sqlObj ["Sql"]);
                        $("#sql_key").val(sqlObj ["key"]);
                        $("#sql_value").val(sqlObj ["value"]);
                    }
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });

    $('#sqlModal').on('hidden.bs.modal', function () {
        debugger;
        $("#sqlModalBody").modal('hide');
        $(this).data('modal', null);
        $("#sqlModalBody").html("");
    })
};

/*----------------------------------------------------------------------------
* function for force Lower and not space in key and value input field
*----------------------------------------------------------------------------*/

// $(document).on('keypress', '#sql_key',function(e) {

//     debugger;
//     if (e.keyCode == 32)
//         return false;

// });
// $(document).bind('cut copy paste','#sql_key',function(e){
   
//     e.preventDefault();

// });

// $(document).on('keypress', '#sql_value',function(e) {

//     debugger;
//     if (e.keyCode == 32)
//         return false;

// });
// $(document).bind('cut copy paste','#sql_value',function(e){
   
//     e.preventDefault();

// });


/*----------------------------------------------------------------------------
* function for save sql Modal
*----------------------------------------------------------------------------*/
function saveSQL(e){
    debugger;
    var sqlText = $('textarea#sqlTextArea').val();   // $('#sqlTextArea')[0].value
    var sqlDbType = $('#sqlDbType').find(":selected").val();  //$('#sqlDbType')[0].value
    var key = $('#sql_key').val();
    var value = $('#sql_value').val();
    if(sqlText == "" || sqlDbType == "" || key == "" || value == ""){
        $("#sqlError").empty();
        $("#sqlError").fadeTo(2000, 500).append('<h4><i class="icon fa fa-warning"></i> Alert!</h4>Please Fill All Fields.').addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
            $("#sqlError").slideUp(500);
        });
    }
    else{
        $("#sqlResult").empty();

        $("#sqlResult").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
            $("#sqlResult").slideUp(500);
        });
        setTimeout(function() {
            $('#sqlCloseModal').click();
        },3000);
        
        var sqlObj = {}
        sqlObj ["sqlDbType"] = sqlDbType;
        sqlObj ["Sql"] = sqlText;
        sqlObj ["key"] = key;
        sqlObj ["value"] = value;
        $("#sql").val(JSON.stringify(sqlObj));
        console.log(sqlObj);

    }
    e.preventDefault();
};
/*----------------------------------------------------------------------------
* function for delete sql Modal
*----------------------------------------------------------------------------*/
function deleteSQL(e){
    debugger;
    $('#sqlTextArea')[0].value = "";
    $('#sqlDbType')[0].value = ""
    $('#sql_key')[0].value = ""
    $('#sql_value')[0].value = ""
    $('#sql')[0].value = ""
    
    $("#sqlResult").empty();

    $("#sqlResult").fadeTo(2000, 500).append("<h4>Alert!</h4>Deleted Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
        $("#sqlResult").slideUp(500);
    });

    setTimeout(function() {
        $('#sqlCloseModal').click();
    },3000);
       
    
};

/*----------------------------------------------------------------------------
* function for save SQL in SERVER
*----------------------------------------------------------------------------*/
function saveSqlInServerDb(e){
    debugger;
    viewid = event.currentTarget.dataset['viewid'];
    sample = "aaaa" ;
    $("#processing-modal").modal('show');
    $.ajax({
        type : 'POST',
        url :"/transactionview/updateSqlInDb/"+viewid,
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
                    
                    $('#schemaGenModal').find('.modal-body').text("SQL Updated");
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
* function for epost popup add modal in viewcomponent.html
*----------------------------------------------------------------------------*/  

function epostAddModal(event) {
    debugger;
    console.log(event);
    var viewid ="";
    var eupdateAdd = "";
    viewid = event.currentTarget.dataset['viewid'];
    var model = null;
    eupdateAdd = '/transactionview/epostadd/' + viewid;
     $("#EpostModal").on("show.bs.modal", function() {
        setTimeout(function() {
            if (model == null) {
                model = $.ajax(eupdateAdd)
                .done(function(data) {
                    $("#epostaddbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });
    $('#EpostModal').on('hidden.bs.modal', function () {
        $("#epostaddbody").modal('hide');
            $(this).data('modal', null);
        $("#epostaddbody").html("");
    });
};



/*------------------------------------------------------------------------------
* Function For Epost Save in viewcomponent.html
*----------------------------------------------------------------------------*/


function epostSave(event){
    var isError = epostFieldValCheck(); 
    if (isError == false){
        debugger;
        var viewid = event.currentTarget.dataset['viewid'];
        var url ="";
        url = "/transactionview/epostSave/"+viewid;    
        var formdata = $("#epostadd").serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: formdata,
            //dataType: 'json',                 
            success: function(data){
                debugger;
                $('#eposttbbody').html("");
                $('#eposttbbody').html(data);
                $("#saveresult").empty();
                $("#saveresult").fadeTo(1000, 500).append('<p style="color:green">Saved Successfully</p>').slideUp(1000, function() {
                    // $("#"+id+"er").slideUp(1000);
                    $("#EpostModal").modal('hide');
                });               
            },
            error: function(data) {
                debugger;
                console.log(data);
                $("#MapError").empty();
                $("#MapError").fadeTo(2000, 500).append("<h4>Alert!</h4>Form Error. Please Check TARGET ROW and ORDER BY. ").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#MapError").slideUp(2000);
                });
                
            }
        });
        console.log(formdata);
    }

};

/*------------------------------------------------------------------------------
* Function For Epost Delete in viewcomponent.html
*----------------------------------------------------------------------------*/


function epostdelete(event){
    debugger;
    var epostid = "";
     epostid = event.currentTarget.dataset['epostid'];
     
     if (!$('#dataConfirmModal_Epost').length) {
             $('body').append('<div id="dataConfirmModal_Epost" class="modal fade" role="dialog" aria-labelledby="dataConfirmLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button><h3 id="dataConfirmLabel">Please Confirm</h3></div><div class="modal-body"><p>Are you sure you want to delete?</p></div><div class="modal-footer"><button class="btn" data-dismiss="modal" aria-hidden="true">Cancel</button><a class="btn btn-primary" data-id="" onclick="deletepost(event)" id="dataConfirm">OK</a></div></div></div></div>');
         }
         $('#dataConfirmModal_Epost').modal({
             show: true
         });
         document.getElementById('dataConfirm').dataset.id = epostid;
         //$('#dataConfirmModal').modal('show');
 };

 function deletepost(event){
     debugger;
   var id ="";
   id = event.currentTarget.dataset['id'];
    var ajax = null;
    var deleteurl = ""
    deleteurl = "/transactionview/epostDelete/"+id;
     if (ajax == null)
     {
       ajax = $.ajax(deleteurl)
             .done(function(data) {
                 debugger;
                $('#dataConfirmModal_Epost').modal('hide'); 
                 $('#eposttbbody').html("");
                 $('#eposttbbody').html(data);
                 $("#epostResults").empty();
                 $("#epostError").empty();

                 $("#epostResults").fadeTo(2000, 500).append("<h4>Alert!</h4>Deleted Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                 $("#epostResults").slideUp(500);
                 return false;
             });
             })
             .fail(function() {
                 alert("error");
                 return false;
             });
         }
 }

/*------------------------------------------------------------------------------
* Function For Epost Edit in viewcomponent.html
*----------------------------------------------------------------------------*/


function epostEdit(event){
    debugger;
    console.log(event);
    var epostid ="";
    var epostEdit = "";
    var viewid ="";
    epostid = event.currentTarget.dataset['epostid'];
    viewid =  event.currentTarget.dataset['viewid'];
    var model = null;
    epostEdit = '/transactionview/epostEdit/' + epostid+'/'+viewid;
    $("#EpostEditModal").on("show.bs.modal", function() {
        setTimeout(function() {
            if (model == null) {
                model = $.ajax(epostEdit)
                .done(function(data) {
                    debugger;
                    $("#epostEditbody").html("");
                    $("#epostEditbody").html(data);
                    $('#epostadd')[0].dataset['epostid'] = epostid;
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });
    

    $('#EpostEditModal').on('hidden.bs.modal', function () {
        $("#epostEditbody").modal('hide');
        $(this).data('modal', null);
        $("#epostEditbody").html("");
    });
}; 

/*------------------------------------------------------------------------------
* Function For Epost Update in viewcomponent.html
*----------------------------------------------------------------------------*/


function epostUpdate(event){
    var isError = epostFieldValCheck(); 
    if (isError == false){
        debugger;
        var viewid = event.currentTarget.dataset['viewid'];
        var epostid = $('#epostadd')[0].dataset['epostid'];
        var url ="";
        url = "/transactionview/epostUpdate/"+epostid+"/"+viewid;    
        var formdata = $("#epostadd").serialize();
        $.ajax({
            type: 'POST',
            url: url,
            data: formdata,
            //dataType: 'json',                 
            success: function(data) { 
                debugger;
            $('#eposttbbody').html("");
            $('#eposttbbody').html(data);
            $("#updateresult").empty();
            $("#updateresult").fadeTo(1000, 500).append('<p style="color:green">Saved Successfully</p>').slideUp(1000, function() {
            // $("#"+id+"er").slideUp(1000);
            $("#EpostEditModal").modal('hide');
                });               
            },
            error: function(data) {
                debugger;
                console.log(data);
                $("#MapError").empty();
                $("#MapError").fadeTo(2000, 500).append("<h4>Alert!</h4>Form Error. Please Check TARGET ROW and ORDER BY. ").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#MapError").slideUp(2000);
                });
            }
        });
        console.log(formdata);
    }
};


/*------------------------------------------------------------------------------
* Function For Epost Update in viewcomponent.html
*----------------------------------------------------------------------------*/


$("#id_target_tx_view").change(function() {
    debugger;
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
    try{
    var addrow = $(".add-row");
    addrow[0].onclick = function click(){
        debugger;
            
        var target_txview = $("#id_target_tx_view").val();
        if (target_txview){
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
                    var target_Selectfield =  $("#epostadd").find('#id_form-'+(total_form_set-1)+'-target_ui_field');
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
}
catch(err){
    
}
});


function epostFieldValCheck(){
    debugger;
    var isError = false;
    var rows =  $(".dynamic-form");
    for (i=0;i<rows.length;i++){
        singleRow = rows[i];
        srcField = singleRow.children[0].children
        srcFieldVal = srcField[0].value
        targetField = singleRow.children[1].children
        targetFieldVal = targetField[0].value
        targetFieldConstant = singleRow.children[2].children
        targetFieldConstantVal = targetFieldConstant[0].value
        if(targetFieldVal){
            if (srcFieldVal == "" && targetFieldConstantVal ==""){
                rows[i].style = "background : khaki";
                isError = true;
            }
            else if (srcFieldVal && targetFieldConstantVal ){
                rows[i].style = "background : khaki";
                isError = true;
            }


        }
            
    }
    if (isError == true){
        $("#MapError").empty();
        $("#MapError").fadeTo(2000, 500).append("<h4>Alert!</h4>Please select anyone field \"SOURCE FIELD\" or \"TARGET FIELD CONSTANT VALUE\".").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
            //tabTr.style = "background : #f9f9f9"; 
            $("#MapError").slideUp(2000);
        });
    }

    return isError;
}




/*------------------------------------------------------------------------------
  * function for firesql add button in viewcomponent.html
  *----------------------------------------------------------------------------*/  

 function firesqlAddModal(event) {
    debugger;
    console.log(event);
    var viewid ="";
    var firesqlAdd = "";
    viewid = event.currentTarget.dataset['viewid'];
    viewid = event.currentTarget.dataset['viewid'];
    var model = null;
    firesqlAdd = '/transactionview/firesqladdmodal/' + viewid;
    $("#FireSQLModal").on("show.bs.modal", function() {
       
        setTimeout(function() {
            if (model == null) {
                model = $.ajax(firesqlAdd)
                .done(function(data) {

                    $("#FireSQLModalbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });

   $('#FireSQLModal').on('hidden.bs.modal', function () {
          $("#FireSQLModalbody").modal('hide');
           $(this).data('modal', null);
          $("#FireSQLModalbody").html("");
          });
};   

/*------------------------------------------------------------------------------
  * function for firesql save new in viewcomponent.html
  *----------------------------------------------------------------------------*/  

 function firesqlSave(event){
  
    debugger;
    var viewid = event.currentTarget.dataset['viewid'];
    var url ="";
    url = "/transactionview/firesqladdmodal/"+viewid;    
    var formdata = $("#firesqlAddForm").serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: formdata,
        //dataType: 'json',                 
        success:function(res){
            debugger
            console.log(res);
            if (res == "Failure1"){
                console.log(res)
                $("#firesqladderror").empty();
                $("#firesqladderror").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed! Title already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#firesqladderror").slideUp(500);
                });

            }

            else if (res == "Failure2"){
                console.log(res)
                $("#firesqladderror").empty();
                $("#firesqladderror").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Please fill all fields").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#firesqladderror").slideUp(500);
                });

            }
    
            else if(res == "Success"){
                debugger;
                $("#firesqladdresult").empty();

                $("#firesqladdresult").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#firesqladdresult").slideUp(500);
                });
                window.location.reload();
            }
           
        },
        error: function(data) {
            debugger
            console.log(data);
            $("#firesqladderror").empty();
                $("#firesqladderror").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed!").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#firesqladderror").slideUp(500);
            });
        }
    });
    event.preventDefault();
};

/*------------------------------------------------------------------------------
* function for firesql update modal in viewcomponent.html
*----------------------------------------------------------------------------*/
function FiewSqlEdit(event){

  
    debugger;
    console.log(event);
    var viewid ="";
    var firesqlid = "";
    var firesqledit = "";
    viewid = event.currentTarget.dataset['viewid'];
    firesqlid = event.currentTarget.dataset['firesqlid'];
    var model = null;
    firesqledit = '/transactionview/firesqledit/' + viewid+'/'+firesqlid;
    $("#FireSqlEditModal").on("show.bs.modal", function() {
        
        setTimeout(function() {
            if (model == null) {
                model = $.ajax(firesqledit)
                .done(function(data) {

                    $("#FireSqlEditModalbody").html(data);
                })
                .fail(function() {
                    alert("error");
                });
            }
        },500);
    });

    $('#FireSqlEditModal').on('hidden.bs.modal', function () {
            $("#FireSqlEditModalbody").modal('hide');
            $(this).data('modal', null);
            $("#FireSqlEditModalbody").html("");
            });


};

/*------------------------------------------------------------------------------
  * function for firesql update in viewcomponent.html
  *----------------------------------------------------------------------------*/  

function firesqlUpdate(event){
  
    debugger;
    var viewid = event.currentTarget.dataset['viewid'];
    var firesqlid = event.currentTarget.dataset['firesqlid'];
    var url ="";
    url = "/transactionview/firesqledit/"+viewid+'/'+firesqlid;    
    var formdata = $("#firesqlEditForm").serialize();
    $.ajax({
        type: 'POST',
        url: url,
        data: formdata,
        //dataType: 'json',                 
        success:function(res){
            debugger
            console.log(res);
            if (res == "Failure1"){
                console.log(res)
                $("#firesqlediterror").empty();
                $("#firesqlediterror").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed! Title already exist.").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#firesqlediterror").slideUp(500);
                });

            }

            else if (res == "Failure2"){
                console.log(res)
                $("#firesqlediterror").empty();
                $("#firesqlediterror").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed. Please fill all fields").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#firesqlediterror").slideUp(500);
                });

            }
    
            else if(res == "Success"){
                debugger;
                $("#firesqleditresult").empty();

                $("#firesqleditresult").fadeTo(2000, 500).append("<h4>Alert!</h4>Saved Successfully.").addClass("alert alert-success alert-dismissible").slideUp(500, function() {
                    $("#firesqleditresult").slideUp(500);
                });
                window.location.reload();
            }
           
        },
        error: function(data) {
            debugger
            console.log(data);
            $("#firesqlediterror").empty();
                $("#firesqlediterror").fadeTo(2000, 500).append("<h4>Alert!</h4>Save Failed!").addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
                    $("#firesqlediterror").slideUp(500);
            });
        }
    });
    event.preventDefault();
};


/*------------------------------------------------------------------------------
*function for submit button in cssutilites.html
*----------------------------------------------------------------------------*/
function csstxn_submit(event) {
  debugger;
  var viewid = event.currentTarget.dataset['viewid'];
  var formdata = $("#csstxn_form").serialize();
  $.ajax({
         type: 'POST',
         url: "/transactionview/txncss/"+viewid,
         data: formdata,
         success: function(data) {
           $("#css_divResults").empty();
           $("#css_divResults").fadeTo(2000, 500).append('<h4><i class="icon fa fa-check"></i> Alert!</h4>Saved Successfully.').addClass("alert alert-success alert-dismissible").slideUp(500, function() {
            $("#css_divResults").slideUp(300);
          });
         },
         error: function(data) {
           console.log(data)
           $("#root_divErrorMessages").empty();
           $("#root_divErrorMessages").fadeTo(2000, 500).append('<h4><i class="icon fa fa-warning"></i> Alert!</h4>Saved Failed.').addClass("alert alert-danger alert-dismissible").slideUp(500, function() {
               $("#root_divErrorMessages").slideUp(500);
           });
         }
     });


};






